# 🚀 快速开始指南

## 1. 初始化系统

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/shared-memory-system

# 初始化系统
python3 scripts/init_system.py
```

输出：
```
🚀 开始初始化共享记忆系统...
==================================================
✓ 创建目录: /root/.openclaw/shared_memory
✓ 创建目录: /root/.openclaw/shared_memory/tags
✓ 创建目录: /root/.openclaw/shared_memory/data
✓ 创建目录: /root/.openclaw/shared_memory/data/public
✓ 创建目录: /root/.openclaw/shared_memory/data/confidential
✓ 创建目录: /root/.openclaw/shared_memory/data/financial
✓ 创建目录: /root/.openclaw/shared_memory/data/technical
✓ 创建目录: /root/.openclaw/shared_memory/encrypted
✓ 创建目录: /root/.openclaw/shared_memory/access_log
✓ 创建目录: /root/.openclaw/shared_memory/backups
--------------------------------------------------
✓ 创建记忆索引: /root/.openclaw/shared_memory/memory_central.md
--------------------------------------------------
✓ 创建系统记忆: /root/.openclaw/shared_memory/data/public/system_init.md
--------------------------------------------------
✓ 创建权限模板: /root/.openclaw/shared_memory/tags/TEMPLATE.md
✓ 创建管理员权限: /root/.openclaw/shared_memory/tags/admin.md
--------------------------------------------------
✓ 创建审计日志: /root/.openclaw/shared_memory/access_log/audit_log.md
--------------------------------------------------
✓ 创建README: /root/.openclaw/shared_memory/README.md
--------------------------------------------------
==================================================
🎉 共享记忆系统初始化完成！

📋 下一步操作：
1. 为你的代理创建权限配置文件
2. 添加测试记忆
3. 让代理读取记忆进行测试

💡 参考命令：
  python3 scripts/create_agent_permissions.py --agent alpha
  python3 scripts/add_memory.py --content '测试' --tags public
  python3 scripts/get_agent_memory.py --agent alpha
```

## 2. 创建代理权限

### 查看可用角色
```bash
python3 scripts/create_agent_permissions.py --list-roles
```

输出：
```
🎭 可用角色:
----------------------------------------
  admin:
    允许标签: ['*']
    禁止标签: []
    访问级别: read_write

  technical_analyst:
    允许标签: ['public', 'technical', 'system']
    禁止标签: ['financial', 'user_private']
    访问级别: read_only

  financial_analyst:
    允许标签: ['public', 'financial', 'system']
    禁止标签: ['technical', 'user_private']
    访问级别: read_only

  data_scientist:
    允许标签: ['public', 'technical', 'system']
    禁止标签: ['financial', 'confidential']
    访问级别: read_only

  project_manager:
    允许标签: ['public', 'system', 'confidential']
    禁止标签: ['financial', 'user_private']
    访问级别: read_write

  guest:
    允许标签: ['public']
    禁止标签: ['*']
    访问级别: read_only
```

### 创建代理权限
```bash
# 创建技术分析代理
python3 scripts/create_agent_permissions.py --agent alpha --role technical_analyst

# 创建财务分析代理
python3 scripts/create_agent_permissions.py --agent beta --role financial_analyst

# 创建项目经理代理
python3 scripts/create_agent_permissions.py --agent gamma --role project_manager
```

## 3. 添加测试记忆

### 公开记忆（所有代理可读）
```bash
python3 scripts/add_memory.py \
  --content "团队章程：每周一9点站会，代码review在每周三" \
  --tags "public" \
  --creator "admin"
```

### 技术文档（技术代理可读）
```bash
python3 scripts/add_memory.py \
  --content "API文档：访问地址 https://api.example.com，认证使用Bearer Token" \
  --tags "technical" \
  --creator "alpha"
```

### 财务报告（财务代理可读）
```bash
python3 scripts/add_memory.py \
  --content "Q1财务报告：收入120万，支出80万，净利润40万" \
  --tags "financial,confidential" \
  --creator "beta" \
  --encrypt
```

### 项目计划（项目经理可读）
```bash
python3 scripts/add_memory.py \
  --content "项目roadmap：Q2上线v2.0，Q3扩展海外市场" \
  --tags "confidential" \
  --creator "gamma"
```

## 4. 代理读取记忆

### Alpha代理（技术角色）
```bash
python3 scripts/get_agent_memory.py --agent alpha
```

输出：
```
🔍 代理读取记忆...
============================================================
👤 代理: alpha
🎭 角色: technical_analyst
✅ 允许标签: ['public', 'technical', 'system']
❌ 禁止标签: ['financial', 'user_private']
------------------------------------------------------------
📊 统计: 2/4 个记忆可访问
------------------------------------------------------------
📄 1. memory_xxxxxx
   🏷️  public
   👤 admin | 📅 2024-04-02
   📝 团队章程：每周一9点站会，代码review在每周三...

📄 2. memory_yyyyyy
   🏷️  technical
   👤 alpha | 📅 2024-04-02
   📝 API文档：访问地址 https://api.example.com，认证使用Bearer Token...
============================================================
🎉 代理 'alpha' 可访问 2 个记忆
```

### Beta代理（财务角色）
```bash
python3 scripts/get_agent_memory.py --agent beta
```

输出：
```
🔍 代理读取记忆...
============================================================
👤 代理: beta
🎭 角色: financial_analyst
✅ 允许标签: ['public', 'financial', 'system']
❌ 禁止标签: ['technical', 'user_private']
------------------------------------------------------------
📊 统计: 2/4 个记忆可访问
------------------------------------------------------------
📄 1. memory_xxxxxx
   🏷️  public
   👤 admin | 📅 2024-04-02
   📝 团队章程：每周一9点站会，代码review在每周三...

📄 2. memory_zzzzzz
   🏷️  financial, confidential
   👤 beta | 📅 2024-04-02
   📝 Q1财务报告：收入120万，支出80万，净利润40万...
============================================================
🎉 代理 'beta' 可访问 2 个记忆
```

### Gamma代理（项目经理）
```bash
python3 scripts/get_agent_memory.py --agent gamma
```

输出：
```
🔍 代理读取记忆...
============================================================
👤 代理: gamma
🎭 角色: project_manager
✅ 允许标签: ['public', 'system', 'confidential']
❌ 禁止标签: ['financial', 'user_private']
------------------------------------------------------------
📊 统计: 3/4 个记忆可访问
------------------------------------------------------------
📄 1. memory_xxxxxx
   🏷️  public
   👤 admin | 📅 2024-04-02
   📝 团队章程：每周一9点站会，代码review在每周三...

📄 2. memory_yyyyyy
   🏷️  technical
   👤 alpha | 📅 2024-04-02
   📝 API文档：访问地址 https://api.example.com，认证使用Bearer Token...

📄 3. memory_wwwwww
   🏷️  confidential
   👤 gamma | 📅 2024-04-02
   📝 项目roadmap：Q2上线v2.0，Q3扩展海外市场...
============================================================
🎉 代理 'gamma' 可访问 3 个记忆
```

## 5. 查看详细内容

```bash
# 查看记忆详细内容
python3 scripts/get_agent_memory.py --agent alpha --details

# 查看权限配置
python3 scripts/get_agent_memory.py --agent alpha --list-permissions
```

## 6. 生成审计报告

### 系统摘要报告
```bash
python3 scripts/audit_report.py --days 7
```

### 代理专属报告
```bash
python3 scripts/audit_report.py --agent alpha --days 30
```

### 导出报告
```bash
python3 scripts/audit_report.py --days 7 --output weekly_report.md
```

## 7. 系统维护

### 检查系统状态
```bash
python3 scripts/check_system.py
```

### 查看系统信息
```bash
# 查看目录结构
ls -la ~/.openclaw/shared_memory/

# 查看记忆索引
cat ~/.openclaw/shared_memory/memory_central.md

# 查看审计日志
cat ~/.openclaw/shared_memory/access_log/audit_log.md
```

## 8. 实际使用场景

### 场景1：新代理加入
```bash
# 1. 创建权限
python3 scripts/create_agent_permissions.py --agent delta --role data_scientist

# 2. 代理读取现有记忆
python3 scripts/get_agent_memory.py --agent delta

# 3. 代理添加新记忆
python3 scripts/add_memory.py \
  --content "数据分析报告：用户活跃度提升15%" \
  --tags "technical" \
  --creator "delta"
```

### 场景2：权限调整
```bash
# 1. 备份原权限
cp ~/.openclaw/shared_memory/tags/agent_alpha.md ~/.openclaw/shared_memory/tags/agent_alpha.bak.md

# 2. 编辑权限文件
vim ~/.openclaw/shared_memory/tags/agent_alpha.md
# 修改 allowed_tags 添加 "confidential"

# 3. 验证权限
python3 scripts/get_agent_memory.py --agent alpha
```

### 场景3：敏感数据保护
```bash
# 添加加密记忆
python3 scripts/add_memory.py \
  --content "用户隐私数据：张三，13800138000，北京市朝阳区" \
  --tags "user_private" \
  --creator "admin" \
  --encrypt

# 该记忆只有admin可读
python3 scripts/get_agent_memory.py --agent alpha  # 看不到
python3 scripts/get_agent_memory.py --agent admin  # 能看到
```

## 9. 故障排除

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
   
   # 检查文件权限
   chmod 644 ~/.openclaw/shared_memory/access_log/audit_log.md
   ```

### 修复命令
```bash
# 重新初始化（不删除数据）
python3 scripts/init_system.py

# 修复文件权限
find ~/.openclaw/shared_memory -type f -name "*.md" -exec chmod 644 {} \;
find ~/.openclaw/shared_memory -type d -exec chmod 755 {} \;

# 清理旧文件
find ~/.openclaw/shared_memory/backups -type f -mtime +30 -delete
```

## 10. 进阶使用

### 集成到代理启动脚本
```bash
#!/bin/bash
# agent_startup.sh

# 加载代理权限
AGENT_NAME="alpha"
python3 ~/.openclaw/workspace/skills/shared-memory-system/scripts/get_agent_memory.py --agent $AGENT_NAME --limit 5

# 代理开始工作
echo "代理 $AGENT_NAME 已加载共享记忆，开始执行任务..."
```

### 定期审计任务
```bash
# 添加到cron
0 9 * * 1 python3 ~/.openclaw/workspace/skills/shared-memory-system/scripts/audit_report.py --days 7 --output /tmp/memory_audit_weekly.md
```

### 自动备份
```bash
# 每日备份脚本
0 2 * * * python3 ~/.openclaw/workspace/skills/shared-memory-system/scripts/backup_system.py
```

---

## 🎯 下一步

1. **测试系统**：按照上述步骤完整测试
2. **集成代理**：将记忆读取集成到你的代理启动流程
3. **扩展功能**：根据需求添加自定义标签和角色
4. **监控优化**：定期检查审计报告，优化权限配置

有问题随时问我！🦊