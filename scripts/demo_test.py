#!/usr/bin/env python3
"""
演示测试脚本
展示共享记忆系统的完整功能
"""

import subprocess
import time
import sys
from pathlib import Path

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"💻 命令: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 执行成功")
            if result.stdout.strip():
                print(f"\n📋 输出:\n{result.stdout}")
        else:
            print(f"❌ 执行失败 (code: {result.returncode})")
            if result.stderr.strip():
                print(f"\n📛 错误:\n{result.stderr}")
        
        return result.returncode == 0
    
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return False

def demo_initialization():
    """演示系统初始化"""
    print("🎬 开始演示：共享记忆系统")
    print("="*60)
    
    # 1. 初始化系统
    success = run_command(
        "python3 scripts/init_system.py",
        "1. 初始化共享记忆系统"
    )
    
    if not success:
        print("❌ 初始化失败，退出演示")
        return False
    
    # 2. 检查系统状态
    run_command(
        "python3 scripts/check_system.py",
        "2. 检查系统状态"
    )
    
    return True

def demo_agent_setup():
    """演示代理设置"""
    print("\n" + "="*60)
    print("👥 演示：代理权限设置")
    print("="*60)
    
    # 1. 查看可用角色
    run_command(
        "python3 scripts/create_agent_permissions.py --list-roles",
        "1. 查看可用角色"
    )
    
    # 2. 创建3个代理
    agents = [
        ("alpha", "technical_analyst", "技术分析代理"),
        ("beta", "financial_analyst", "财务分析代理"),
        ("gamma", "project_manager", "项目经理代理")
    ]
    
    for agent_name, role, description in agents:
        run_command(
            f"python3 scripts/create_agent_permissions.py --agent {agent_name} --role {role}",
            f"2. 创建{description} ({agent_name})"
        )
    
    # 3. 查看创建的权限文件
    run_command(
        "ls -la ~/.openclaw/shared_memory/tags/",
        "3. 查看权限文件"
    )
    
    return True

def demo_memory_operations():
    """演示记忆操作"""
    print("\n" + "="*60)
    print("📝 演示：记忆操作")
    print("="*60)
    
    # 测试记忆数据
    test_memories = [
        {
            "content": "团队章程：每周一9:00站会，代码review在每周三14:00",
            "tags": "public",
            "creator": "admin",
            "description": "公开记忆（所有代理可读）"
        },
        {
            "content": "API文档：访问地址 https://api.example.com/v1，认证使用Bearer Token，有效期24小时",
            "tags": "technical",
            "creator": "alpha",
            "description": "技术文档（技术代理可读）"
        },
        {
            "content": "Q1财务报告：总收入120万元，总支出80万元，净利润40万元，同比增长15%",
            "tags": "financial,confidential",
            "creator": "beta",
            "description": "财务报告（财务代理可读，机密）"
        },
        {
            "content": "项目roadmap：Q2上线v2.0版本，Q3扩展海外市场，Q4推出移动端应用",
            "tags": "confidential",
            "creator": "gamma",
            "description": "项目计划（项目经理可读，机密）"
        },
        {
            "content": "用户隐私数据：张三，13800138000，zhangsan@example.com，北京市朝阳区",
            "tags": "user_private",
            "creator": "admin",
            "description": "用户隐私（仅管理员可读，加密）",
            "encrypt": True
        }
    ]
    
    # 1. 添加测试记忆
    for i, memory in enumerate(test_memories, 1):
        cmd = f"python3 scripts/add_memory.py --content \"{memory['content']}\" --tags \"{memory['tags']}\" --creator \"{memory['creator']}\""
        
        if memory.get('encrypt'):
            cmd += " --encrypt"
        
        run_command(
            cmd,
            f"{i}. 添加{memory['description']}"
        )
    
    # 2. 查看记忆索引
    run_command(
        "cat ~/.openclaw/shared_memory/memory_central.md | grep -A2 \"id:\"",
        "6. 查看记忆索引摘要"
    )
    
    return True

def demo_agent_access():
    """演示代理访问"""
    print("\n" + "="*60)
    print("🔍 演示：代理访问控制")
    print("="*60)
    
    agents = ["alpha", "beta", "gamma", "admin"]
    
    for agent in agents:
        run_command(
            f"python3 scripts/get_agent_memory.py --agent {agent} --limit 3",
            f"代理 '{agent}' 读取记忆（显示前3个）"
        )
    
    # 演示详细内容查看
    run_command(
        "python3 scripts/get_agent_memory.py --agent alpha --details --limit 1",
        "Alpha代理查看详细记忆内容"
    )
    
    return True

def demo_audit_and_monitoring():
    """演示审计和监控"""
    print("\n" + "="*60)
    print("📊 演示：审计和监控")
    print("="*60)
    
    # 1. 生成审计报告
    run_command(
        "python3 scripts/audit_report.py --days 1",
        "1. 生成今日审计报告"
    )
    
    # 2. 代理专属报告
    run_command(
        "python3 scripts/audit_report.py --agent alpha --days 1",
        "2. Alpha代理专属报告"
    )
    
    # 3. 查看审计日志
    run_command(
        "tail -20 ~/.openclaw/shared_memory/access_log/audit_log.md",
        "3. 查看最近审计日志"
    )
    
    return True

def demo_system_maintenance():
    """演示系统维护"""
    print("\n" + "="*60)
    print("🔧 演示：系统维护")
    print("="*60)
    
    # 1. 系统状态检查
    run_command(
        "python3 scripts/check_system.py",
        "1. 系统状态检查"
    )
    
    # 2. 查看系统信息
    run_command(
        "du -sh ~/.openclaw/shared_memory/",
        "2. 查看存储使用情况"
    )
    
    run_command(
        "find ~/.openclaw/shared_memory -type f -name \"*.md\" | wc -l",
        "3. 统计文件数量"
    )
    
    return True

def demo_real_world_scenarios():
    """演示真实世界场景"""
    print("\n" + "="*60)
    print("🌍 演示：真实世界场景")
    print("="*60)
    
    scenarios = [
        {
            "title": "场景1：新代理入职",
            "steps": [
                "python3 scripts/create_agent_permissions.py --agent delta --role data_scientist",
                "python3 scripts/get_agent_memory.py --agent delta",
                "python3 scripts/add_memory.py --content \"数据分析：用户留存率提升20%\" --tags technical --creator delta"
            ]
        },
        {
            "title": "场景2：权限升级",
            "steps": [
                "# 备份原权限",
                "cp ~/.openclaw/shared_memory/tags/agent_alpha.md ~/.openclaw/shared_memory/tags/agent_alpha_backup.md",
                "# 编辑权限文件添加confidential标签",
                "# 然后测试新权限",
                "python3 scripts/get_agent_memory.py --agent alpha"
            ]
        },
        {
            "title": "场景3：敏感数据保护",
            "steps": [
                "# 添加加密敏感数据",
                "python3 scripts/add_memory.py --content \"客户名单：A公司李总，B公司王经理\" --tags user_private --creator admin --encrypt",
                "# 测试不同代理访问",
                "python3 scripts/get_agent_memory.py --agent alpha | grep -i 客户",
                "python3 scripts/get_agent_memory.py --agent admin | grep -i 客户"
            ]
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n📋 {i}. {scenario['title']}")
        print("-"*40)
        for step in scenario['steps']:
            if step.startswith("#"):
                print(f"   💡 {step[1:].strip()}")
            else:
                print(f"   💻 {step}")
    
    return True

def summary_and_next_steps():
    """总结和下一步"""
    print("\n" + "="*60)
    print("🎯 演示总结和下一步")
    print("="*60)
    
    print("✅ 已完成演示:")
    print("  1. 🏗️  系统初始化")
    print("  2. 👥 代理权限设置")
    print("  3. 📝 记忆添加操作")
    print("  4. 🔍 代理访问控制")
    print("  5. 📊 审计监控")
    print("  6. 🔧 系统维护")
    print("  7. 🌍 真实场景")
    
    print("\n💡 核心价值:")
    print("  • 多代理共享记忆池")
    print("  • 基于标签的权限控制")
    print("  • 完整的审计追踪")
    print("  • 敏感数据加密保护")
    
    print("\n🚀 下一步行动:")
    print("  1. 集成到你的代理系统")
    print("  2. 根据业务需求自定义标签")
    print("  3. 设置定期审计任务")
    print("  4. 扩展更多角色和权限")
    
    print("\n📁 系统位置:")
    print(f"  根目录: ~/.openclaw/shared_memory/")
    print(f"  技能目录: ~/.openclaw/workspace/skills/shared-memory-system/")
    
    print("\n📞 支持:")
    print("  • 查看快速指南: cat references/quick-start.md")
    print("  • 检查系统: python3 scripts/check_system.py")
    print("  • 生成报告: python3 scripts/audit_report.py")
    
    print("\n" + "="*60)
    print("🎉 演示完成！你的多代理共享记忆系统已就绪。")
    print("="*60)

def main():
    """主演示函数"""
    
    print("""
    🧠🤝 共享记忆系统演示
    ====================================
    功能：让多个代理共享记忆，但只能读取授权内容
    ====================================
    """)
    
    # 确认是否继续
    response = input("开始演示？(y/N): ").strip().lower()
    if response != 'y':
        print("演示取消")
        return
    
    # 执行演示步骤
    steps = [
        ("系统初始化", demo_initialization),
        ("代理设置", demo_agent_setup),
        ("记忆操作", demo_memory_operations),
        ("代理访问", demo_agent_access),
        ("审计监控", demo_audit_and_monitoring),
        ("系统维护", demo_system_maintenance),
        ("真实场景", demo_real_world_scenarios)
    ]
    
    all_success = True
    for step_name, step_func in steps:
        try:
            if not step_func():
                print(f"⚠️  {step_name} 步骤存在问题")
                all_success = False
        except Exception as e:
            print(f"❌ {step_name} 步骤异常: {e}")
            all_success = False
        
        # 暂停一下，让用户看清楚
        if step_name != "真实场景":
            input("\n↵ 按回车继续...")
    
    # 总结
    summary_and_next_steps()
    
    if all_success:
        print("\n✅ 所有演示步骤成功完成！")
    else:
        print("\n⚠️  部分演示步骤存在问题，请检查日志。")

if __name__ == "__main__":
    main()