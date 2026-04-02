#!/usr/bin/env python3
"""
创建代理权限配置文件
"""

import argparse
import yaml
from pathlib import Path
from datetime import datetime

SHARED_MEMORY_ROOT = Path.home() / ".openclaw" / "shared_memory"

# 角色权限映射
ROLE_PERMISSIONS = {
    "admin": {
        "allowed_tags": ["*"],
        "denied_tags": [],
        "access_level": "read_write"
    },
    "technical_analyst": {
        "allowed_tags": ["public", "technical", "system"],
        "denied_tags": ["financial", "user_private"],
        "access_level": "read_only"
    },
    "financial_analyst": {
        "allowed_tags": ["public", "financial", "system"],
        "denied_tags": ["technical", "user_private"],
        "access_level": "read_only"
    },
    "data_scientist": {
        "allowed_tags": ["public", "technical", "system"],
        "denied_tags": ["financial", "confidential"],
        "access_level": "read_only"
    },
    "project_manager": {
        "allowed_tags": ["public", "system", "confidential"],
        "denied_tags": ["financial", "user_private"],
        "access_level": "read_write"
    },
    "guest": {
        "allowed_tags": ["public"],
        "denied_tags": ["*"],
        "access_level": "read_only"
    }
}

def create_agent_permissions(agent_name, role="technical_analyst", expires="2024-12-31"):
    """创建代理权限配置文件"""
    
    # 检查角色是否有效
    if role not in ROLE_PERMISSIONS:
        print(f"❌ 错误：无效的角色 '{role}'")
        print(f"可用角色: {', '.join(ROLE_PERMISSIONS.keys())}")
        return False
    
    # 检查共享记忆系统是否已初始化
    if not SHARED_MEMORY_ROOT.exists():
        print("❌ 错误：共享记忆系统未初始化")
        print("请先运行: python3 init_system.py")
        return False
    
    # 创建权限文件路径
    tags_dir = SHARED_MEMORY_ROOT / "tags"
    permission_file = tags_dir / f"agent_{agent_name}.md"
    
    if permission_file.exists():
        print(f"⚠️ 警告：权限文件已存在: {permission_file}")
        overwrite = input("是否覆盖？(y/N): ").strip().lower()
        if overwrite != 'y':
            print("取消创建权限文件")
            return False
    
    # 获取角色权限配置
    role_config = ROLE_PERMISSIONS[role]
    
    # 创建权限配置
    permission_config = {
        "agent": agent_name,
        "role": role,
        "allowed_tags": role_config["allowed_tags"],
        "denied_tags": role_config["denied_tags"],
        "access_level": role_config["access_level"],
        "created": datetime.now().strftime("%Y-%m-%d"),
        "expires": expires,
        "description": f"{role} 代理"
    }
    
    # 写入文件
    try:
        with open(permission_file, 'w', encoding='utf-8') as f:
            yaml.dump(permission_config, f, allow_unicode=True)
        
        print(f"✓ 创建权限配置文件: {permission_file}")
        print(f"📋 配置详情:")
        print(f"  代理: {agent_name}")
        print(f"  角色: {role}")
        print(f"  允许标签: {role_config['allowed_tags']}")
        print(f"  禁止标签: {role_config['denied_tags']}")
        print(f"  访问级别: {role_config['access_level']}")
        print(f"  过期时间: {expires}")
        
        # 记录到审计日志
        log_access("system", "create_permission", f"agent_{agent_name}", "success")
        
        return True
        
    except Exception as e:
        print(f"❌ 创建权限文件失败: {e}")
        log_access("system", "create_permission", f"agent_{agent_name}", "error", str(e))
        return False

def log_access(agent, operation, memory_id, result, notes=""):
    """记录访问日志"""
    log_file = SHARED_MEMORY_ROOT / "access_log" / "audit_log.md"
    
    if log_file.exists():
        with open(log_file, 'a', encoding='utf-8') as f:
            log_entry = f"""
### {datetime.now().strftime('%Y-%m-%d')} 权限创建
- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 代理: {agent}
- 操作: {operation}
- 记忆ID: {memory_id}
- 结果: {result}
- 备注: {notes}
---
"""
            f.write(log_entry)

def list_available_roles():
    """列出所有可用角色"""
    print("🎭 可用角色:")
    print("-" * 40)
    for role, config in ROLE_PERMISSIONS.items():
        print(f"  {role}:")
        print(f"    允许标签: {config['allowed_tags']}")
        print(f"    禁止标签: {config['denied_tags']}")
        print(f"    访问级别: {config['access_level']}")
        print()

def main():
    parser = argparse.ArgumentParser(description="创建代理权限配置文件")
    parser.add_argument("--agent", required=True, help="代理名称")
    parser.add_argument("--role", default="technical_analyst", 
                       choices=list(ROLE_PERMISSIONS.keys()),
                       help="代理角色")
    parser.add_argument("--expires", default="2024-12-31", 
                       help="权限过期时间 (YYYY-MM-DD)")
    parser.add_argument("--list-roles", action="store_true",
                       help="列出所有可用角色")
    
    args = parser.parse_args()
    
    if args.list_roles:
        list_available_roles()
        return
    
    print(f"🚀 为代理 '{args.agent}' 创建权限配置文件...")
    print(f"   角色: {args.role}")
    print(f"   过期: {args.expires}")
    print("-" * 50)
    
    success = create_agent_permissions(args.agent, args.role, args.expires)
    
    if success:
        print("-" * 50)
        print("🎉 权限创建完成！")
        print()
        print("💡 下一步:")
        print(f"  1. 验证权限: cat {SHARED_MEMORY_ROOT}/tags/agent_{args.agent}.md")
        print(f"  2. 测试读取: python3 get_agent_memory.py --agent {args.agent}")
        print(f"  3. 查看所有权限: ls {SHARED_MEMORY_ROOT}/tags/")
    else:
        print("❌ 权限创建失败")

if __name__ == "__main__":
    main()