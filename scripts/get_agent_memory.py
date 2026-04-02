#!/usr/bin/env python3
"""
代理读取授权记忆
"""

import argparse
import yaml
import re
from pathlib import Path
from datetime import datetime

SHARED_MEMORY_ROOT = Path.home() / ".openclaw" / "shared_memory"

def load_agent_permissions(agent_name):
    """加载代理权限配置"""
    permission_file = SHARED_MEMORY_ROOT / "tags" / f"agent_{agent_name}.md"
    
    if not permission_file.exists():
        print(f"❌ 错误：代理 '{agent_name}' 的权限文件不存在")
        print(f"请先创建权限: python3 create_agent_permissions.py --agent {agent_name}")
        return None
    
    try:
        with open(permission_file, 'r', encoding='utf-8') as f:
            permissions = yaml.safe_load(f)
        
        # 验证权限配置
        required_fields = ["agent", "allowed_tags", "denied_tags", "role"]
        for field in required_fields:
            if field not in permissions:
                print(f"❌ 错误：权限文件缺少字段 '{field}'")
                return None
        
        return permissions
    
    except Exception as e:
        print(f"❌ 加载权限文件失败: {e}")
        return None

def parse_memory_index():
    """解析记忆索引文件"""
    index_file = SHARED_MEMORY_ROOT / "memory_central.md"
    
    if not index_file.exists():
        print("❌ 错误：记忆索引文件不存在")
        return []
    
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析记忆条目
        memory_entries = []
        current_entry = {}
        
        lines = content.split('\n')
        in_entry = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("### ") and "id:" in line:
                # 新条目开始
                if current_entry:
                    memory_entries.append(current_entry)
                current_entry = {"raw_line": line}
                in_entry = True
            
            elif in_entry and line.startswith("- "):
                # 解析键值对
                if ": " in line:
                    key, value = line[2:].split(": ", 1)
                    
                    # 解析标签
                    if key == "tags":
                        # 移除方括号和引号
                        value = value.strip("[]")
                        tags = [tag.strip().strip("'\"") for tag in value.split(",") if tag.strip()]
                        current_entry["tags"] = tags
                    elif key == "encrypted":
                        current_entry[key] = value.lower() == "true"
                    else:
                        current_entry[key] = value
            
            elif in_entry and line == "":
                # 空行，继续下一个
                pass
        
        # 添加最后一个条目
        if current_entry:
            memory_entries.append(current_entry)
        
        return memory_entries
    
    except Exception as e:
        print(f"❌ 解析记忆索引失败: {e}")
        return []

def can_access_memory(memory_tags, permissions):
    """检查代理是否可以访问该记忆"""
    allowed_tags = permissions.get("allowed_tags", [])
    denied_tags = permissions.get("denied_tags", [])
    
    # 如果允许所有标签
    if "*" in allowed_tags:
        return True
    
    # 检查是否有禁止的标签
    for tag in memory_tags:
        if tag in denied_tags:
            return False
    
    # 检查是否有允许的标签
    for tag in memory_tags:
        if tag in allowed_tags:
            return True
    
    return False

def read_memory_content(memory_path):
    """读取记忆内容"""
    try:
        # 解析存储路径
        if "/" in memory_path:
            path_parts = memory_path.split("/")
            if len(path_parts) == 2:
                category, filename = path_parts
                memory_file = SHARED_MEMORY_ROOT / "data" / category / filename
            else:
                memory_file = SHARED_MEMORY_ROOT / "data" / "public" / memory_path
        else:
            memory_file = SHARED_MEMORY_ROOT / "data" / "public" / memory_path
        
        if not memory_file.exists():
            # 尝试其他路径
            for category in ["public", "confidential", "financial", "technical"]:
                test_file = SHARED_MEMORY_ROOT / "data" / category / memory_path
                if test_file.exists():
                    memory_file = test_file
                    break
        
        if not memory_file.exists():
            return f"❌ 记忆文件不存在: {memory_path}"
        
        content = memory_file.read_text(encoding='utf-8')
        
        # 提取YAML头和实际内容
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_header = parts[1]
                actual_content = parts[2].strip()
                
                try:
                    metadata = yaml.safe_load(yaml_header)
                    # 返回格式化内容
                    return f"""
{'='*60}
📝 记忆: {metadata.get('id', '未知')}
🏷️  标签: {', '.join(metadata.get('tags', []))}
👤 创建者: {metadata.get('created_by', '未知')}
📅 创建时间: {metadata.get('created_at', '未知')}
🔐 加密: {'是' if metadata.get('encrypted', False) else '否'}
{'='*60}

{actual_content}

{'='*60}
"""
                except:
                    return content
        return content
    
    except Exception as e:
        return f"❌ 读取记忆失败: {e}"

def get_agent_memory(agent_name, show_details=False, limit=None):
    """获取代理可访问的记忆"""
    
    # 检查系统是否已初始化
    if not SHARED_MEMORY_ROOT.exists():
        print("❌ 错误：共享记忆系统未初始化")
        print("请先运行: python3 init_system.py")
        return []
    
    # 加载代理权限
    permissions = load_agent_permissions(agent_name)
    if not permissions:
        return []
    
    print(f"👤 代理: {agent_name}")
    print(f"🎭 角色: {permissions.get('role', '未知')}")
    print(f"✅ 允许标签: {permissions.get('allowed_tags', [])}")
    print(f"❌ 禁止标签: {permissions.get('denied_tags', [])}")
    print("-" * 60)
    
    # 解析记忆索引
    memory_entries = parse_memory_index()
    
    if not memory_entries:
        print("📭 记忆库为空")
        return []
    
    # 过滤代理可访问的记忆
    accessible_memories = []
    for entry in memory_entries:
        if can_access_memory(entry.get("tags", []), permissions):
            accessible_memories.append(entry)
    
    print(f"📊 统计: {len(accessible_memories)}/{len(memory_entries)} 个记忆可访问")
    print("-" * 60)
    
    # 显示记忆列表
    for i, memory in enumerate(accessible_memories):
        if limit and i >= limit:
            print(f"... 还有 {len(accessible_memories) - limit} 个记忆")
            break
        
        memory_id = memory.get("id", f"未知_{i}")
        preview = memory.get("content", "无预览")
        tags = memory.get("tags", [])
        creator = memory.get("creator", "未知")
        created = memory.get("created", "未知")
        
        print(f"📄 {i+1}. {memory_id}")
        print(f"   🏷️  {', '.join(tags)}")
        print(f"   👤 {creator} | 📅 {created}")
        print(f"   📝 {preview[:80]}...")
        
        if show_details:
            content = read_memory_content(memory.get("path", ""))
            print(content)
            print()
        else:
            print()
    
    # 记录访问日志
    log_access(agent_name, "read_memory", f"batch_{len(accessible_memories)}", "success")
    
    return accessible_memories

def log_access(agent, operation, memory_id, result, notes=""):
    """记录访问日志"""
    log_file = SHARED_MEMORY_ROOT / "access_log" / "audit_log.md"
    
    if log_file.exists():
        with open(log_file, 'a', encoding='utf-8') as f:
            log_entry = f"""
### {datetime.now().strftime('%Y-%m-%d')} 记忆访问
- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 代理: {agent}
- 操作: {operation}
- 记忆ID: {memory_id}
- 结果: {result}
- 备注: {notes}
---
"""
            f.write(log_entry)

def main():
    parser = argparse.ArgumentParser(description="代理读取授权记忆")
    parser.add_argument("--agent", required=True, help="代理名称")
    parser.add_argument("--details", action="store_true", help="显示详细内容")
    parser.add_argument("--limit", type=int, help="限制显示数量")
    parser.add_argument("--list-permissions", action="store_true", help="仅列出权限配置")
    
    args = parser.parse_args()
    
    if args.list_permissions:
        permissions = load_agent_permissions(args.agent)
        if permissions:
            print("🔐 权限配置详情:")
            print(yaml.dump(permissions, allow_unicode=True))
        return
    
    print("🔍 代理读取记忆...")
    print("=" * 60)
    
    memories = get_agent_memory(args.agent, args.details, args.limit)
    
    if memories:
        print("=" * 60)
        print(f"🎉 代理 '{args.agent}' 可访问 {len(memories)} 个记忆")
        print()
        print("💡 其他命令:")
        print(f"  查看详细: python3 {__file__} --agent {args.agent} --details")
        print(f"  查看权限: python3 {__file__} --agent {args.agent} --list-permissions")
        print(f"  添加记忆: python3 add_memory.py --content '新记忆' --tags public")
    else:
        print("📭 没有可访问的记忆")

if __name__ == "__main__":
    main()