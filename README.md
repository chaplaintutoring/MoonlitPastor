# 🧠🤝 OpenClaw Shared Memory System

**让多个AI代理共享记忆池，但只能读取授权给自己的部分内容**

[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.com)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 核心价值

> **"你的公司各部门共享知识库，但财务部不该看研发代码，HR部不该看销售客户名单"**

这个技能让 OpenClaw 的多个AI代理实现类似功能：
- **所有代理共享同一个记忆库**，避免重复工作
- **每个代理只能读取授权内容**，权限隔离
- **审计追踪**，谁什么时候看了什么，都有记录
- **加密存储**，敏感数据自动加密

## 🚀 快速开始

### 1. 安装
```bash
# 克隆仓库
git clone https://github.com/yourusername/openclaw-shared-memory.git
cd openclaw-shared-memory

# 移动到OpenClaw技能目录
mkdir -p ~/.openclaw/skills/
cp -r . ~/.openclaw/skills/shared-memory-system

# 初始化系统
cd ~/.openclaw/skills/shared-memory-system
python3 scripts/init_system.py
```

### 2. 30秒测试
```bash
# 创建技术分析代理
python3 scripts/create_agent_permissions.py --agent alpha --role technical_analyst

# 添加测试记忆
python3 scripts/add_memory.py --content "团队章程" --tags public
python3 scripts/add_memory.py --content "API文档" --tags technical
python3 scripts/add_memory.py --content "财务报告" --tags financial,confidential

# 代理读取记忆（只能看到前2条）
python3 scripts/get_agent_memory.py --agent alpha
```

## 📊 系统架构

```
~/.openclaw/shared_memory/
├── memory_central.md          # 中央记忆索引
├── tags/                      # 代理权限配置文件
│   ├── admin.md              # 管理员权限
│   ├── agent_alpha.md        # Alpha代理权限
│   ├── agent_beta.md         # Beta代理权限
│   └── TEMPLATE.md           # 权限模板
├── data/                      # 记忆数据存储
│   ├── public/               # 公开记忆（所有代理可读）
│   ├── confidential/         # 机密记忆（需要授权）
│   ├── financial/            # 财务记忆（财务代理可读）
│   └── technical/            # 技术记忆（技术代理可读）
├── encrypted/                 # 加密记忆存储
├── access_log/               # 访问审计日志
└── backups/                  # 系统备份
```

## 🔐 权限模型

### 基于标签的访问控制 (TBAC)
- 每个记忆条目有**标签**（如：`public`, `technical`, `financial`, `confidential`）
- 每个代理有**权限配置**（允许哪些标签，禁止哪些标签）
- 代理只能读取**有权限的标签**的记忆

### 预设角色
| 角色 | 允许标签 | 禁止标签 | 访问级别 | 适用场景 |
|------|----------|----------|----------|----------|
| **admin** | 所有 | 无 | 读写 | 系统管理员 |
| **technical_analyst** | public, technical, system | financial, user_private | 只读 | 技术分析代理 |
| **financial_analyst** | public, financial, system | technical, user_private | 只读 | 财务分析代理 |
| **data_scientist** | public, technical, system | financial, confidential | 只读 | 数据科学家 |
| **project_manager** | public, system, confidential | financial, user_private | 读写 | 项目经理 |
| **guest** | public | 所有 | 只读 | 访客代理 |

## 🛠️ 核心脚本

### 初始化与管理
```bash
# 初始化系统
python3 scripts/init_system.py

# 检查系统状态
python3 scripts/check_system.py

# 系统演示（完整功能展示）
python3 scripts/demo_test.py
```

### 代理权限管理
```bash
# 创建代理权限
python3 scripts/create_agent_permissions.py --agent alpha --role technical_analyst

# 查看可用角色
python3 scripts/create_agent_permissions.py --list-roles

# 查看代理权限
python3 scripts/get_agent_memory.py --agent alpha --list-permissions
```

### 记忆操作
```bash
# 添加记忆
python3 scripts/add_memory.py --content "内容" --tags "tag1,tag2"

# 添加加密记忆（敏感数据）
python3 scripts/add_memory.py --content "敏感数据" --tags user_private --encrypt

# 代理读取记忆
python3 scripts/get_agent_memory.py --agent alpha

# 查看详细内容
python3 scripts/get_agent_memory.py --agent alpha --details
```

### 审计与监控
```bash
# 生成系统审计报告
python3 scripts/audit_report.py --days 7

# 生成代理专属报告
python3 scripts/audit_report.py --agent alpha --days 30

# 导出报告
python3 scripts/audit_report.py --days 7 --output weekly_report.md
```

## 📋 使用示例

### 场景1：新代理入职
```bash
# 1. 创建权限
python3 scripts/create_agent_permissions.py --agent delta --role data_scientist

# 2. 代理读取现有记忆
python3 scripts/get_agent_memory.py --agent delta

# 3. 代理添加新记忆
python3 scripts/add_memory.py --content "数据分析报告" --tags technical --creator delta
```

### 场景2：权限升级
```bash
# 1. 备份原权限
cp ~/.openclaw/shared_memory/tags/agent_alpha.md ~/.openclaw/shared_memory/tags/agent_alpha.bak.md

# 2. 编辑权限文件添加confidential标签
vim ~/.openclaw/shared_memory/tags/agent_alpha.md

# 3. 测试新权限
python3 scripts/get_agent_memory.py --agent alpha
```

### 场景3：敏感数据保护
```bash
# 添加加密敏感数据
python3 scripts/add_memory.py \
  --content "客户隐私数据" \
  --tags user_private \
  --creator admin \
  --encrypt

# 测试访问
python3 scripts/get_agent_memory.py --agent alpha  # 看不到
python3 scripts/get_agent_memory.py --agent admin  # 能看到
```

## 🎯 集成到你的代理

### 代理启动脚本示例
```bash
#!/bin/bash
# agent_startup.sh

AGENT_NAME="alpha"

# 加载共享记忆
echo "🔍 加载共享记忆..."
python3 ~/.openclaw/skills/shared-memory-system/scripts/get_agent_memory.py --agent $AGENT_NAME --limit 5

# 代理开始工作
echo "🚀 代理 $AGENT_NAME 已加载共享记忆，开始执行任务..."
```

### 定期审计（cron任务）
```bash
# 每周一9点生成审计报告
0 9 * * 1 python3 ~/.openclaw/skills/shared-memory-system/scripts/audit_report.py --days 7 --output /tmp/memory_audit_weekly.md

# 每日凌晨2点备份系统
0 2 * * * python3 ~/.openclaw/skills/shared-memory-system/scripts/backup_system.py
```

## 🔧 故障排除

### 常见问题
1. **代理看不到记忆**
   ```bash
   # 检查权限配置
   cat ~/.openclaw/shared_memory/tags/agent_<name>.md
   
   # 检查记忆标签
   cat ~/.openclaw/shared_memory/memory_central.md | grep -A5 "id:"
   ```

2. **添加记忆失败**
   ```bash
   # 检查系统状态
   python3 scripts/check_system.py
   
   # 检查文件权限
   ls -la ~/.openclaw/shared_memory/
   ```

3. **审计日志不完整**
   ```bash
   # 检查日志文件
   cat ~/.openclaw/shared_memory/access_log/audit_log.md
   
   # 修复权限
   chmod 644 ~/.openclaw/shared_memory/access_log/audit_log.md
   ```

### 修复命令
```bash
# 重新初始化（不删除数据）
python3 scripts/init_system.py

# 修复文件权限
find ~/.openclaw/shared_memory -type f -name "*.md" -exec chmod 644 {} \;
find ~/.openclaw/shared_memory -type d -exec chmod 755 {} \;

# 清理旧备份
find ~/.openclaw/shared_memory/backups -type f -mtime +30 -delete
```

## 📈 路线图

### 已实现
- ✅ 基于标签的权限控制
- ✅ 中央记忆索引
- ✅ 审计日志系统
- ✅ 加密存储支持
- ✅ 完整命令行工具
- ✅ 系统状态检查

### 计划中
- 🔄 Web管理界面
- 🔄 实时权限变更
- 🔄 记忆版本控制
- 🔄 自动记忆分类
- 🔄 智能权限推荐

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🦊 关于作者

这是为 OpenClaw 社区开发的开源技能，旨在解决多代理协作中的记忆共享和权限隔离问题。

**一句话总结**：让多个AI代理像公司不同部门一样，共享知识库但权限隔离。

---
**GitHub**: https://github.com/yourusername/openclaw-shared-memory  
**OpenClaw社区**: https://discord.com/invite/clawd  
**技能市场**: https://clawhub.com