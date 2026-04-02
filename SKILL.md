---
name: shared-memory-system
description: 多代理共享记忆系统，支持基于标签的权限控制、审计日志和加密存储。让所有代理共享记忆池，但只能读取授权内容。
metadata:
  openclaw:
    emoji: "🧠🤝"
    requires:
      bins: ["python3"]
    install:
      - id: "init"
        kind: "script"
        script: "python3 scripts/init_system.py"
        label: "初始化共享记忆系统"
---

# 🧠🤝 共享记忆系统技能

## 概述
让**多个代理共享同一个记忆池**，但每个代理**只能读取授权给自己的部分**。

### 核心价值
- **知识共享**：避免重复工作，代理可以基于其他代理的经验
- **权限隔离**：财务代理看不到技术文档，技术代理看不到用户隐私
- **审计追踪**：所有记忆访问都有日志，可追溯谁看了什么
- **加密安全**：敏感数据自动加密存储

## 系统架构

```
~/.openclaw/shared_memory/
├── memory_central.md          # 中央记忆索引
├── tags/                      # 代理权限配置文件
│   ├── admin.md              # 管理员权限
│   ├── agent_alpha.md        # Alpha代理权限
│   ├── agent_beta.md         # Beta代理权限
│   └── TEMPLATE.md           # 权限模板
├── data/                      # 记忆数据
│   ├── public/               # 公开记忆
│   ├── confidential/         # 机密记忆
│   ├── financial/            # 财务记忆
│   └── technical/            # 技术记忆
├── encrypted/                 # 加密记忆存储
├── access_log/               # 访问审计日志
└── backups/                  # 系统备份
```

## 权限模型

### 1. 基于标签的访问控制 (TBAC)
每个记忆条目有标签，每个代理有权限配置：
- **allowed_tags**: 允许读取的标签
- **denied_tags**: 禁止读取的标签

### 2. 代理角色
- **admin**: 管理员（所有权限）
- **technical_analyst**: 技术分析师
- **financial_analyst**: 财务分析师  
- **data_scientist**: 数据科学家
- **project_manager**: 项目经理
- **guest**: 访客（仅公开记忆）

### 3. 访问级别
- **read_only**: 只读
- **read_write**: 读写
- **admin**: 管理员权限

## 使用场景

### 场景1：新代理加入
新代理 `gamma` 加入团队，需要技术文档和项目文档权限：
```bash
# 创建权限配置
python3 scripts/create_agent_permissions.py --agent gamma --role technical_analyst

# 代理读取记忆
python3 scripts/get_agent_memory.py --agent gamma
```

### 场景2：添加机密记忆
添加财务报告，只有财务代理可读：
```bash
python3 scripts/add_memory.py \
  --content "Q1财务报告" \
  --tags "financial,confidential" \
  --encrypt true
```

### 场景3：审计检查
检查谁访问了机密文件：
```bash
python3 scripts/audit_report.py --memory-id finance_report_001
```

## 激活时机

激活本技能当用户：
- 需要多个代理共享记忆
- 要求权限隔离（A代理不能看B代理的记忆）
- 需要审计追踪记忆访问
- 有敏感数据需要加密存储
- 建立多代理协作团队

## 快速开始

### 1. 初始化系统
```bash
python3 scripts/init_system.py
```

### 2. 创建代理权限
```bash
python3 scripts/create_agent_permissions.py --agent alpha --role technical_analyst
python3 scripts/create_agent_permissions.py --agent beta --role financial_analyst
```

### 3. 添加测试记忆
```bash
# 公开记忆
python3 scripts/add_memory.py --content "团队章程" --tags public

# 技术记忆
python3 scripts/add_memory.py --content "API文档" --tags technical

# 财务记忆
python3 scripts/add_memory.py --content "预算报告" --tags financial,confidential --encrypt true
```

### 4. 代理读取记忆
```bash
# Alpha代理（技术角色）
python3 scripts/get_agent_memory.py --agent alpha
# 结果：能看到公开和技术记忆，看不到财务记忆

# Beta代理（财务角色）
python3 scripts/get_agent_memory.py --agent beta
# 结果：能看到公开和财务记忆，看不到技术记忆
```

## API 参考

### 核心脚本
- `init_system.py` - 初始化共享记忆系统
- `create_agent_permissions.py` - 创建代理权限配置
- `add_memory.py` - 添加新记忆条目
- `get_agent_memory.py` - 代理读取授权记忆
- `update_memory.py` - 更新记忆条目
- `delete_memory.py` - 删除记忆条目
- `audit_report.py` - 生成审计报告
- `encrypt_memory.py` - 加密记忆内容
- `backup_system.py` - 系统备份

### 配置文件
- `tags/TEMPLATE.md` - 权限配置模板
- `tags/agent_*.md` - 各代理权限配置
- `memory_central.md` - 中央记忆索引
- `access_log/audit_log.md` - 审计日志

## 安全最佳实践

1. **最小权限原则**：只给代理必要的权限
2. **定期审计**：每周检查访问日志
3. **加密敏感数据**：财务/用户数据必须加密
4. **权限定期更新**：每季度审查代理权限
5. **备份策略**：每日自动备份

## 故障排除

### 常见问题
1. **代理看不到记忆** → 检查权限配置文件
2. **记忆添加失败** → 检查标签格式
3. **加密记忆无法读取** → 确认代理有解密权限
4. **审计日志不完整** → 检查文件权限

### 调试命令
```bash
# 检查系统状态
python3 scripts/check_system.py

# 验证权限配置
python3 scripts/validate_permissions.py --agent alpha

# 修复文件权限
python3 scripts/fix_permissions.py
```

## 扩展功能

### 计划中的功能
- Web管理界面
- 实时权限变更
- 记忆版本控制
- 自动记忆分类
- 智能权限推荐

## 贡献

欢迎提交 Issue 和 Pull Request！

---
**一句话总结**：让多个AI代理像公司不同部门一样，共享知识库但权限隔离。🦊