#!/usr/bin/env python3
"""
添加新记忆到共享记忆系统
"""

import argparse
import yaml
import uuid
from pathlib import Path
from datetime import datetime
import hashlib

SHARED_MEMORY_ROOT = Path.home() / ".openclaw" / "shared_memory"

def generate_memory_id():
    """生成唯一记忆ID"""
    return f"memory_{uuid.uuid4().hex[:8]}"

def parse_tags(tag_string):
    """解析标签字符串"""
    if not tag_string:
        return ["public"]
    return [tag.strip() for tag in tag_string.split(",")]

def create_memory_content(content, tags, creator, encrypt=False):
    """创建记忆内容"""
    memory_id = generate_memory_id()
    created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 基础YAML头
    yaml_header = {
        "id": memory_id,
        "permissions": {
            "read_tags": tags,
            "write_tags": ["admin", creator] if creator != "system" else ["admin", "system"],
            "required_role": "all" if "public" in tags else "specific"
        },
        "created_by": creator,
        "created_at": created_time,
        "encrypted": encrypt,
        "expires": "永久",
        "tags": tags
    }
    
    # 构建完整内容
    yaml_str = yaml.dump(yaml_header, allow_unicode=True)
    
    full_content = f"""---
{yaml_str}---
# {memory_id}

{content}

## 元数据
- ID: {memory_id}
- 创建者: {creator}
- 创建时间: {created_time}
- 标签: {', '.join(tags)}
- 加密: {'是' if encrypt else '否'}
- 过期: 永久
"""
    
    return memory_id, full_content

def save_memory(memory_id, content, tags, creator):
    """保存记忆到文件系统"""
    
    # 确定存储路径
    if "financial" in tags or "user_private" in tags:
        # 财务或用户隐私数据
        storage_dir = SHARED_MEMORY_ROOT / "data" / "confidential"
    elif "technical" in tags:
        # 技术文档
        storage_dir = SHARED_MEMORY_ROOT / "data" / "technical"
    else:
        # 公开数据
        storage_dir = SHARED_MEMORY_ROOT / "data" / "public"
    
    # 确保目录存在
    storage_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存文件
    memory_file = storage_dir / f"{memory_id}.md"
    memory_file.write_text(content, encoding='utf-8')
    
    return storage_dir, memory_file

def update_memory_index(memory_id, content_preview, tags, storage_path, creator):
    """更新中央记忆索引"""
    index_file = SHARED_MEMORY_ROOT / "memory_central.md"
    
    if not index_file.exists():
        print("❌ 错误：记忆索引文件不存在")
        return False
    
    # 读取现有索引
    with open(index_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 找到插入位置（在"## 记忆条目索引"之后）
    insert_index = -1
    for i, line in enumerate(lines):
        if "## 记忆条目索引" in line:
            insert_index = i + 1
            break
    
    if insert_index == -1:
        # 如果没有找到，添加到文件末尾
        insert_index = len(lines)
    
    # 创建新条目
    preview = content_preview[:100] + "..." if len(content_preview) > 100 else content_preview
    
    new_entry = f"""
### {datetime.now().strftime('%Y-%m-%d')} {creator}
- id: {memory_id}
- content: {preview}
- path: {storage_path}
- tags: {tags}
- created: {datetime.now().strftime('%Y-%m-%d')}
- creator: {creator}
- expires: "永久"
- encrypted: false
"""
    
    # 插入新条目
    lines.insert(insert_index, new_entry)
    
    # 写回文件
    with open(index_file, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return True

def log_access(agent, operation, memory_id, result, notes=""):
    """记录访问日志"""
    log_file = SHARED_MEMORY_ROOT / "access_log" / "audit_log.md"
    
    if log_file.exists():
        with open(log_file, 'a', encoding='utf-8') as f:
            log_entry = f"""
### {datetime.now().strftime('%Y-%m-%d')} 记忆添加
- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 代理: {agent}
- 操作: {operation}
- 记忆ID: {memory_id}
- 结果: {result}
- 备注: {notes}
---
"""
            f.write(log_entry)

def add_memory(content, tags, creator="user", encrypt=False):
    """添加新记忆"""
    
    # 检查系统是否已初始化
    if not SHARED_MEMORY_ROOT.exists():
        print("❌ 错误：共享记忆系统未初始化")
        print("请先运行: python3 init_system.py")
        return False
    
    # 解析标签
    tag_list = parse_tags(tags)
    
    # 创建记忆内容
    memory_id, memory_content = create_memory_content(content, tag_list, creator, encrypt)
    
    # 保存记忆文件
    storage_dir, memory_file = save_memory(memory_id, memory_content, tag_list, creator)
    
    # 更新索引
    success = update_memory_index(
        memory_id, 
        content, 
        tag_list, 
        f"{storage_dir.name}/{memory_file.name}", 
        creator
    )
    
    if success:
        print(f"✓ 记忆添加成功！")
        print(f"📋 记忆详情:")
        print(f"  ID: {memory_id}")
        print(f"  存储位置: {memory_file}")
        print(f"  标签: {', '.join(tag_list)}")
        print(f"  创建者: {creator}")
        print(f"  预览: {content[:50]}...")
        
        # 记录到审计日志
        log_access(creator, "add_memory", memory_id, "success")
        
        return True
    else:
        print("❌ 记忆添加失败")
        log_access(creator, "add_memory", memory_id, "error", "更新索引失败")
        return False

def main():
    parser = argparse.ArgumentParser(description="添加新记忆到共享记忆系统")
    parser.add_argument("--content", required=True, help="记忆内容")
    parser.add_argument("--tags", default="public", help="记忆标签（逗号分隔）")
    parser.add_argument("--creator", default="user", help="创建者")
    parser.add_argument("--encrypt", action="store_true", help="是否加密存储")
    
    args = parser.parse_args()
    
    print("📝 添加新记忆...")
    print(f"   创建者: {args.creator}")
    print(f"   标签: {args.tags}")
    print(f"   加密: {'是' if args.encrypt else '否'}")
    print("-" * 50)
    
    success = add_memory(args.content, args.tags, args.creator, args.encrypt)
    
    if success:
        print("-" * 50)
        print("🎉 记忆添加完成！")
        print()
        print("💡 下一步:")
        print("  1. 查看记忆索引: cat ~/.openclaw/shared_memory/memory_central.md")
        print("  2. 测试代理读取: python3 get_agent_memory.py --agent <agent_name>")
        print("  3. 查看审计日志: cat ~/.openclaw/shared_memory/access_log/audit_log.md")
    else:
        print("❌ 记忆添加失败")

if __name__ == "__main__":
    main()