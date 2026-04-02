#!/usr/bin/env python3
"""
初始化共享记忆系统
创建必要的目录结构和配置文件
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

# 共享记忆系统根目录
SHARED_MEMORY_ROOT = Path.home() / ".openclaw" / "shared_memory"

def create_directory_structure():
    """创建目录结构"""
    directories = [
        SHARED_MEMORY_ROOT,
        SHARED_MEMORY_ROOT / "tags",
        SHARED_MEMORY_ROOT / "data",
        SHARED_MEMORY_ROOT / "data" / "public",
        SHARED_MEMORY_ROOT / "data" / "confidential",
        SHARED_MEMORY_ROOT / "data" / "financial",
        SHARED_MEMORY_ROOT / "data" / "technical",
        SHARED_MEMORY_ROOT / "encrypted",
        SHARED_MEMORY_ROOT / "access_log",
        SHARED_MEMORY_ROOT / "backups"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {directory}")

def create_memory_index():
    """创建记忆索引文件"""
    index_file = SHARED_MEMORY_ROOT / "memory_central.md"
    
    if not index_file.exists():
        content = f"""# 中央记忆索引

## 概述
这是所有代理共享的中央记忆库索引。每个记忆条目包含：
- 唯一ID
- 内容摘要
- 存储路径
- 权限标签
- 创建信息
- 过期时间

## 系统信息
- 初始化时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 架构版本: 1.0.0
- 权限模型: 基于标签的访问控制 (TBAC)
- 加密支持: 是

## 记忆条目索引

### 系统初始化
- id: system_init_001
- content: 共享记忆系统已初始化
- path: data/public/system_init.md
- tags: ["public", "system"]
- created: {datetime.now().strftime('%Y-%m-%d')}
- creator: system
- expires: "永久"
- required_role: "all"
- encrypted: false

## 添加新记忆
使用 `add_memory.py` 脚本添加新记忆：

```bash
python3 scripts/add_memory.py \\
  --content "你的记忆内容" \\
  --tags "tag1,tag2" \\
  --creator "agent_name"
```

## 权限说明
- **public**: 所有代理可读
- **confidential**: 需要特定权限
- **financial**: 财务相关代理可读
- **technical**: 技术相关代理可读
- **system**: 系统配置相关
- **user_private**: 用户隐私数据（加密存储）

## 标签管理
每个代理在 `tags/` 目录下有权限配置文件，定义：
- allowed_tags: 允许读取的标签
- denied_tags: 禁止读取的标签
- role: 代理角色
- access_level: 读写权限
"""
        
        index_file.write_text(content)
        print(f"✓ 创建记忆索引: {index_file}")
    else:
        print(f"✓ 记忆索引已存在: {index_file}")

def create_system_init_memory():
    """创建系统初始化记忆"""
    memory_file = SHARED_MEMORY_ROOT / "data" / "public" / "system_init.md"
    
    if not memory_file.exists():
        content = f"""---
permissions:
  read_tags: ["public", "system"]
  write_tags: ["admin", "system_bot"]
  required_role: "all"
created_by: system
created_at: {datetime.now().strftime('%Y-%m-%d')}
encrypted: false
expires: "永久"
---
# 系统初始化记忆

共享记忆系统已成功初始化！

## 系统信息
- 初始化时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 架构版本: 1.0.0
- 权限模型: 基于标签的访问控制

## 使用指南
1. 每个代理需要创建权限配置文件
2. 添加记忆时指定权限标签
3. 代理只能读取 allowed_tags 匹配的记忆
4. 敏感数据建议加密存储

## 默认标签
- **public**: 公开信息，所有代理可读
- **system**: 系统配置，技术代理可读
- **technical**: 技术文档，技术团队可读
- **financial**: 财务数据，财务代理可读
- **confidential**: 机密信息，需要特殊授权
- **user_private**: 用户隐私，加密+严格授权

## 快速开始
```bash
# 1. 创建代理权限
python3 scripts/create_agent_permissions.py --agent alpha

# 2. 添加测试记忆
python3 scripts/add_memory.py --content "测试记忆" --tags public

# 3. 代理获取记忆
python3 scripts/get_agent_memory.py --agent alpha
```
"""
        
        memory_file.write_text(content)
        print(f"✓ 创建系统记忆: {memory_file}")
    else:
        print(f"✓ 系统记忆已存在: {memory_file}")

def create_default_permissions():
    """创建默认权限模板"""
    tags_dir = SHARED_MEMORY_ROOT / "tags"
    
    # 创建默认代理权限模板
    template_file = tags_dir / "TEMPLATE.md"
    
    if not template_file.exists():
        template_content = """# 代理权限模板

复制此文件并重命名为 `agent_<name>.md`，然后修改配置。

## 配置格式
```yaml
agent: "agent_name"                # 代理名称
allowed_tags:                      # 允许读取的标签列表
  - "public"
  - "technical"
  - "system"
denied_tags:                       # 禁止读取的标签列表
  - "financial"
  - "user_private"
  - "confidential"
role: "technical_analyst"          # 代理角色
access_level: "read_only"          # 访问级别：read_only / read_write
created: "2024-04-02"              # 创建时间
expires: "2024-12-31"              # 权限过期时间
description: "技术分析代理"         # 代理描述
```

## 角色定义
- **admin**: 系统管理员，所有权限
- **technical_analyst**: 技术分析师，可读技术相关记忆
- **financial_analyst**: 财务分析师，可读财务相关记忆
- **data_scientist**: 数据科学家，可读数据相关记忆
- **project_manager**: 项目经理，可读项目相关记忆
- **guest**: 访客，仅可读公开记忆

## 标签说明
每个记忆条目可以有一个或多个标签，代理只能读取：
1. 包含在 allowed_tags 中的标签
2. 且不包含在 denied_tags 中的标签

## 示例配置
```yaml
agent: "alpha"
allowed_tags: ["public", "technical", "system"]
denied_tags: ["financial", "user_private"]
role: "technical_analyst"
access_level: "read_only"
created: "2024-04-02"
expires: "2024-12-31"
description: "技术分析代理，负责系统监控和数据分析"
```
"""
        template_file.write_text(template_content)
        print(f"✓ 创建权限模板: {template_file}")
    else:
        print(f"✓ 权限模板已存在: {template_file}")
    
    # 创建系统管理员权限
    admin_file = tags_dir / "admin.md"
    
    if not admin_file.exists():
        admin_config = {
            "agent": "admin",
            "allowed_tags": ["*"],  # 所有标签
            "denied_tags": [],
            "role": "admin",
            "access_level": "read_write",
            "created": datetime.now().strftime("%Y-%m-%d"),
            "expires": "永久",
            "description": "系统管理员"
        }
        
        admin_file.write_text(yaml.dump(admin_config, allow_unicode=True))
        print(f"✓ 创建管理员权限: {admin_file}")
    else:
        print(f"✓ 管理员权限已存在: {admin_file}")

def create_audit_log():
    """创建审计日志"""
    log_file = SHARED_MEMORY_ROOT / "access_log" / "audit_log.md"
    
    if not log_file.exists():
        content = f"""# 记忆访问审计日志

## 格式说明
- **时间**: 访问时间 (YYYY-MM-DD HH:MM:SS)
- **代理**: 发起访问的代理
- **操作**: read / write / delete / update
- **记忆ID**: 访问的记忆条目ID
- **结果**: success / denied / error
- **备注**: 额外信息

## 日志条目

### {datetime.now().strftime('%Y-%m-%d')} 系统初始化
- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- 代理: system
- 操作: write
- 记忆ID: system_init_001
- 结果: success
- 备注: 系统初始化记忆创建

---
"""
        
        log_file.write_text(content)
        print(f"✓ 创建审计日志: {log_file}")
    else:
        print(f"✓ 审计日志已存在: {log_file}")

def create_readme():
    """创建README文件"""
    readme_file = SHARED_MEMORY_ROOT / "README.md"
    
    if not readme_file.exists():
        content = f"""# 共享记忆系统

## 🚀 快速开始

### 1. 初始化系统
```bash
python3 {sys.argv[0]}
```

### 2. 创建代理权限
```bash
python3 scripts/create_agent_permissions.py --agent alpha --role technical_analyst
```

### 3. 添加记忆
```bash
python3 scripts/add_memory.py --content "团队章程" --tags public
```

### 4. 读取记忆
```bash
python3 scripts/get_agent_memory.py --agent alpha
```

## 📁 目录结构
```
~/.openclaw/shared_memory/
├── memory_central.md          # 中央记忆索引
├── tags/                      # 代理权限配置
├── data/                      # 记忆存储
├── encrypted/                 # 加密记忆
├── access_log/               # 审计日志
└── backups/                  # 系统备份
```

## 🔐 权限模型
- **基于标签**：每个记忆有标签，每个代理有权限标签
- **角色系统**：不同角色不同权限
- **审计追踪**：所有访问都有记录
- **加密存储**：敏感数据加密

## 📞 支持
如有问题，请检查：
1. 权限配置文件是否正确
2. 记忆标签是否匹配
3. 审计日志中的错误信息

---
**初始化时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_file.write_text(content)
        print(f"✓ 创建README: {readme_file}")
    else:
        print(f"✓ README已存在: {readme_file}")

def main():
    """主函数"""
    print("🚀 开始初始化共享记忆系统...")
    print("=" * 50)
    
    # 创建目录结构
    create_directory_structure()
    print("-" * 30)
    
    # 创建记忆索引
    create_memory_index()
    print("-" * 30)
    
    # 创建系统记忆
    create_system_init_memory()
    print("-" * 30)
    
    # 创建权限配置
    create_default_permissions()
    print("-" * 30)
    
    # 创建审计日志
    create_audit_log()
    print("-" * 30)
    
    # 创建README
    create_readme()
    print("-" * 30)
    
    print("=" * 50)
    print("🎉 共享记忆系统初始化完成！")
    print()
    print("📋 下一步操作：")
    print("1. 为你的代理创建权限配置文件")
    print("2. 添加测试记忆")
    print("3. 让代理读取记忆进行测试")
    print()
    print("💡 参考命令：")
    print("  python3 scripts/create_agent_permissions.py --agent alpha")
    print("  python3 scripts/add_memory.py --content '测试' --tags public")
    print("  python3 scripts/get_agent_memory.py --agent alpha")
    print()
    print("📊 系统信息：")
    print(f"  根目录: {SHARED_MEMORY_ROOT}")
    print(f"  记忆索引: {SHARED_MEMORY_ROOT / 'memory_central.md'}")
    print(f"  权限配置: {SHARED_MEMORY_ROOT / 'tags/'}")
    print(f"  审计日志: {SHARED_MEMORY_ROOT / 'access_log/audit_log.md'}")

if __name__ == "__main__":
    main()