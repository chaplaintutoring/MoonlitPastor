#!/usr/bin/env python3
"""
检查共享记忆系统状态
"""

import yaml
from pathlib import Path
from datetime import datetime

SHARED_MEMORY_ROOT = Path.home() / ".openclaw" / "shared_memory"

def check_directory_structure():
    """检查目录结构"""
    print("📁 检查目录结构...")
    
    required_dirs = [
        SHARED_MEMORY_ROOT,
        SHARED_MEMORY_ROOT / "tags",
        SHARED_MEMORY_ROOT / "data",
        SHARED_MEMORY_ROOT / "data" / "public",
        SHARED_MEMORY_ROOT / "data" / "confidential",
        SHARED_MEMORY_ROOT / "data" / "financial",
        SHARED_MEMORY_ROOT / "data" / "technical",
        SHARED_MEMORY_ROOT / "access_log",
        SHARED_MEMORY_ROOT / "backups"
    ]
    
    all_ok = True
    for directory in required_dirs:
        if directory.exists():
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ {directory} (缺失)")
            all_ok = False
    
    return all_ok

def check_required_files():
    """检查必需文件"""
    print("\n📄 检查必需文件...")
    
    required_files = [
        SHARED_MEMORY_ROOT / "memory_central.md",
        SHARED_MEMORY_ROOT / "tags" / "TEMPLATE.md",
        SHARED_MEMORY_ROOT / "tags" / "admin.md",
        SHARED_MEMORY_ROOT / "access_log" / "audit_log.md",
        SHARED_MEMORY_ROOT / "data" / "public" / "system_init.md"
    ]
    
    all_ok = True
    for file_path in required_files:
        if file_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (缺失)")
            all_ok = False
    
    return all_ok

def check_permission_files():
    """检查权限文件"""
    print("\n🔐 检查权限文件...")
    
    tags_dir = SHARED_MEMORY_ROOT / "tags"
    
    if not tags_dir.exists():
        print("  ❌ tags目录不存在")
        return False
    
    permission_files = list(tags_dir.glob("agent_*.md"))
    
    if not permission_files:
        print("  ⚠️  没有代理权限文件")
        return True  # 这不是错误，只是警告
    
    print(f"  📋 找到 {len(permission_files)} 个代理权限文件:")
    
    all_valid = True
    for perm_file in permission_files:
        try:
            with open(perm_file, 'r', encoding='utf-8') as f:
                permissions = yaml.safe_load(f)
            
            # 检查必需字段
            required_fields = ["agent", "allowed_tags", "denied_tags", "role"]
            missing_fields = [field for field in required_fields if field not in permissions]
            
            if missing_fields:
                print(f"  ❌ {perm_file.name}: 缺少字段 {missing_fields}")
                all_valid = False
            else:
                print(f"  ✅ {perm_file.name}: {permissions['agent']} ({permissions['role']})")
        
        except Exception as e:
            print(f"  ❌ {perm_file.name}: 解析失败 - {e}")
            all_valid = False
    
    return all_valid

def check_memory_index():
    """检查记忆索引"""
    print("\n📚 检查记忆索引...")
    
    index_file = SHARED_MEMORY_ROOT / "memory_central.md"
    
    if not index_file.exists():
        print("  ❌ 记忆索引文件不存在")
        return False
    
    try:
        content = index_file.read_text(encoding='utf-8')
        
        # 简单检查
        if "## 记忆条目索引" in content:
            # 统计记忆条目
            entries = content.count("- id:")
            print(f"  ✅ 记忆索引有效，包含 {entries} 个记忆条目")
            return True
        else:
            print("  ❌ 记忆索引格式不正确")
            return False
    
    except Exception as e:
        print(f"  ❌ 读取记忆索引失败: {e}")
        return False

def check_audit_log():
    """检查审计日志"""
    print("\n📝 检查审计日志...")
    
    log_file = SHARED_MEMORY_ROOT / "access_log" / "audit_log.md"
    
    if not log_file.exists():
        print("  ❌ 审计日志文件不存在")
        return False
    
    try:
        content = log_file.read_text(encoding='utf-8')
        
        # 统计日志条目
        entries = content.count("- 时间:")
        print(f"  ✅ 审计日志有效，包含 {entries} 条记录")
        return True
    
    except Exception as e:
        print(f"  ❌ 读取审计日志失败: {e}")
        return False

def check_file_permissions():
    """检查文件权限"""
    print("\n🔒 检查文件权限...")
    
    import os
    import stat
    
    # 检查关键文件权限
    sensitive_files = [
        SHARED_MEMORY_ROOT / "tags" / "admin.md",
        SHARED_MEMORY_ROOT / "encrypted" if (SHARED_MEMORY_ROOT / "encrypted").exists() else None
    ]
    
    all_ok = True
    for file_path in sensitive_files:
        if file_path and file_path.exists():
            try:
                st_mode = os.stat(file_path).st_mode
                # 检查是否过于开放（group或others有写权限）
                if st_mode & (stat.S_IWGRP | stat.S_IWOTH):
                    print(f"  ⚠️  {file_path}: 权限过于开放 (建议0600)")
                    all_ok = False
                else:
                    print(f"  ✅ {file_path}: 权限正常")
            except Exception as e:
                print(f"  ❌ {file_path}: 检查权限失败 - {e}")
                all_ok = False
    
    return all_ok

def check_storage_usage():
    """检查存储使用情况"""
    print("\n💾 检查存储使用情况...")
    
    import shutil
    
    try:
        total_size = 0
        file_count = 0
        
        for file_path in SHARED_MEMORY_ROOT.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
                file_count += 1
        
        # 转换为易读格式
        size_kb = total_size / 1024
        size_mb = size_kb / 1024
        
        if size_mb > 1:
            size_str = f"{size_mb:.1f} MB"
        else:
            size_str = f"{size_kb:.1f} KB"
        
        print(f"  📊 总文件数: {file_count}")
        print(f"  📊 总大小: {size_str}")
        
        if total_size > 100 * 1024 * 1024:  # 超过100MB
            print(f"  ⚠️  存储使用较大，建议清理或备份")
            return False
        
        return True
    
    except Exception as e:
        print(f"  ❌ 检查存储使用失败: {e}")
        return False

def generate_summary(all_checks):
    """生成检查摘要"""
    print("\n" + "="*60)
    print("📋 系统检查摘要")
    print("="*60)
    
    total_checks = len(all_checks)
    passed_checks = sum(1 for _, passed in all_checks if passed)
    failed_checks = total_checks - passed_checks
    
    # 显示检查结果
    for check_name, passed in all_checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}")
    
    print("-"*60)
    print(f"📊 总体: {passed_checks}/{total_checks} 项检查通过")
    
    if failed_checks == 0:
        print("🎉 所有检查通过！系统运行正常。")
        return True
    else:
        print("⚠️  存在一些问题，请根据上述检查结果进行修复。")
        print("\n💡 修复建议:")
        print("  1. 运行初始化脚本: python3 init_system.py")
        print("  2. 检查文件权限: chmod 600 ~/.openclaw/shared_memory/tags/*.md")
        print("  3. 重新创建缺失文件")
        return False

def main():
    print("🔍 开始检查共享记忆系统...")
    print("="*60)
    
    # 检查系统是否已初始化
    if not SHARED_MEMORY_ROOT.exists():
        print("❌ 共享记忆系统未初始化")
        print("💡 请先运行: python3 init_system.py")
        return
    
    # 执行各项检查
    all_checks = []
    
    # 1. 目录结构
    dir_ok = check_directory_structure()
    all_checks.append(("目录结构", dir_ok))
    
    # 2. 必需文件
    files_ok = check_required_files()
    all_checks.append(("必需文件", files_ok))
    
    # 3. 权限文件
    perm_ok = check_permission_files()
    all_checks.append(("权限文件", perm_ok))
    
    # 4. 记忆索引
    index_ok = check_memory_index()
    all_checks.append(("记忆索引", index_ok))
    
    # 5. 审计日志
    log_ok = check_audit_log()
    all_checks.append(("审计日志", log_ok))
    
    # 6. 文件权限
    file_perm_ok = check_file_permissions()
    all_checks.append(("文件权限", file_perm_ok))
    
    # 7. 存储使用
    storage_ok = check_storage_usage()
    all_checks.append(("存储使用", storage_ok))
    
    # 生成摘要
    system_ok = generate_summary(all_checks)
    
    print("\n" + "="*60)
    print("💡 其他维护命令:")
    print("  审计报告: python3 audit_report.py --days 7")
    print("  备份系统: python3 backup_system.py")
    print("  修复权限: python3 fix_permissions.py")
    print("  清理旧文件: python3 cleanup_old_files.py")
    print("="*60)

if __name__ == "__main__":
    main()