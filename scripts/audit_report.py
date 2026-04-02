#!/usr/bin/env python3
"""
生成审计报告
分析记忆访问日志
"""

import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter, defaultdict

SHARED_MEMORY_ROOT = Path.home() / ".openclaw" / "shared_memory"

def parse_audit_log():
    """解析审计日志"""
    log_file = SHARED_MEMORY_ROOT / "access_log" / "audit_log.md"
    
    if not log_file.exists():
        print("❌ 错误：审计日志文件不存在")
        return []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析日志条目
        log_entries = []
        current_entry = {}
        
        lines = content.split('\n')
        in_entry = False
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("### ") and "时间:" in line:
                # 新条目开始
                if current_entry:
                    log_entries.append(current_entry)
                current_entry = {}
                in_entry = True
            
            elif in_entry and line.startswith("- "):
                # 解析键值对
                if ": " in line:
                    key, value = line[2:].split(": ", 1)
                    current_entry[key] = value
            
            elif in_entry and line == "---":
                # 条目结束
                if current_entry:
                    log_entries.append(current_entry)
                current_entry = {}
                in_entry = False
        
        # 添加最后一个条目
        if current_entry:
            log_entries.append(current_entry)
        
        return log_entries
    
    except Exception as e:
        print(f"❌ 解析审计日志失败: {e}")
        return []

def filter_entries_by_time(entries, days=7):
    """按时间过滤条目"""
    if not entries:
        return []
    
    cutoff_date = datetime.now() - timedelta(days=days)
    
    filtered = []
    for entry in entries:
        time_str = entry.get("时间", "")
        try:
            entry_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            if entry_time >= cutoff_date:
                filtered.append(entry)
        except:
            # 如果解析失败，包含该条目
            filtered.append(entry)
    
    return filtered

def generate_summary_report(entries, days=7):
    """生成摘要报告"""
    if not entries:
        return "📭 指定时间段内无访问记录"
    
    total_entries = len(entries)
    
    # 统计操作类型
    operations = Counter([e.get("操作", "未知") for e in entries])
    
    # 统计代理访问
    agents = Counter([e.get("代理", "未知") for e in entries])
    
    # 统计结果
    results = Counter([e.get("结果", "未知") for e in entries])
    
    # 按日期统计
    dates = Counter()
    for entry in entries:
        time_str = entry.get("时间", "")
        if time_str:
            date_str = time_str.split(" ")[0]
            dates[date_str] += 1
    
    # 构建报告
    report = f"""
{'='*80}
📊 共享记忆系统审计报告
{'='*80}

📅 报告周期: 最近 {days} 天
📋 总记录数: {total_entries} 条
⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
🔍 操作统计
{'='*80}
"""
    
    for op, count in operations.most_common():
        percentage = (count / total_entries) * 100
        report += f"  {op:15s}: {count:4d} 次 ({percentage:.1f}%)\n"
    
    report += f"""
{'='*80}
👥 代理访问统计
{'='*80}
"""
    
    for agent, count in agents.most_common():
        percentage = (count / total_entries) * 100
        report += f"  {agent:20s}: {count:4d} 次 ({percentage:.1f}%)\n"
    
    report += f"""
{'='*80}
✅ 结果统计
{'='*80}
"""
    
    for result, count in results.most_common():
        percentage = (count / total_entries) * 100
        result_emoji = "✅" if result == "success" else "❌" if result == "denied" else "⚠️"
        report += f"  {result_emoji} {result:15s}: {count:4d} 次 ({percentage:.1f}%)\n"
    
    report += f"""
{'='*80}
📅 每日访问趋势
{'='*80}
"""
    
    if dates:
        max_count = max(dates.values()) if dates.values() else 1
        
        for date_str in sorted(dates.keys(), reverse=True):
            count = dates[date_str]
            bar_length = int((count / max_count) * 30)
            bar = "█" * bar_length + "░" * (30 - bar_length)
            report += f"  {date_str}: {bar} {count:3d} 次\n"
    else:
        report += "  无日期数据\n"
    
    # 异常检测
    denied_entries = [e for e in entries if e.get("结果") == "denied"]
    error_entries = [e for e in entries if e.get("结果") == "error"]
    
    if denied_entries or error_entries:
        report += f"""
{'='*80}
🚨 异常检测
{'='*80}
"""
        
        if denied_entries:
            report += f"⚠️  权限拒绝: {len(denied_entries)} 次\n"
            for entry in denied_entries[:5]:  # 显示前5个
                report += f"   - {entry.get('时间')} | {entry.get('代理')} | {entry.get('操作')} | {entry.get('记忆ID')}\n"
            if len(denied_entries) > 5:
                report += f"   ... 还有 {len(denied_entries)-5} 次拒绝\n"
        
        if error_entries:
            report += f"❌ 系统错误: {len(error_entries)} 次\n"
            for entry in error_entries[:3]:  # 显示前3个
                report += f"   - {entry.get('时间')} | {entry.get('代理')} | {entry.get('操作')} | {entry.get('备注', '无备注')}\n"
    
    report += f"""
{'='*80}
💡 建议
{'='*80}
"""
    
    # 基于分析给出建议
    if len(denied_entries) > total_entries * 0.1:  # 拒绝率超过10%
        report += "🔸 权限拒绝率较高，建议检查代理权限配置\n"
    
    if len(error_entries) > 0:
        report += "🔸 存在系统错误，建议检查日志备注\n"
    
    if operations.get("read_memory", 0) < operations.get("add_memory", 0) * 0.5:
        report += "🔸 记忆添加频率高于读取频率，可能存在记忆冗余\n"
    
    if total_entries < 10:
        report += "🔸 系统使用率较低，建议推广使用\n"
    elif total_entries > 100:
        report += "🔸 系统使用活跃，建议定期备份和优化\n"
    
    report += "🔸 建议每周检查一次审计报告\n"
    report += "🔸 敏感操作建议启用双因素验证\n"
    
    report += f"""
{'='*80}
📞 技术支持
{'='*80}
- 查看详细日志: cat {SHARED_MEMORY_ROOT}/access_log/audit_log.md
- 检查系统状态: python3 scripts/check_system.py
- 修复权限问题: python3 scripts/fix_permissions.py
- 备份系统: python3 scripts/backup_system.py

{'='*80}
"""
    
    return report

def generate_agent_report(agent_name, entries, days=7):
    """生成代理专属报告"""
    agent_entries = [e for e in entries if e.get("代理") == agent_name]
    
    if not agent_entries:
        return f"📭 代理 '{agent_name}' 在最近 {days} 天内无访问记录"
    
    total_entries = len(agent_entries)
    
    # 统计操作类型
    operations = Counter([e.get("操作", "未知") for e in agent_entries])
    
    # 统计结果
    results = Counter([e.get("结果", "未知") for e in agent_entries])
    
    # 最近访问的记忆
    recent_memories = []
    for entry in agent_entries:
        memory_id = entry.get("记忆ID", "")
        if memory_id and memory_id not in recent_memories:
            recent_memories.append(memory_id)
    
    report = f"""
{'='*80}
👤 代理专属审计报告: {agent_name}
{'='*80}

📅 报告周期: 最近 {days} 天
📋 总访问数: {total_entries} 次
⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*80}
🔍 操作统计
{'='*80}
"""
    
    for op, count in operations.most_common():
        percentage = (count / total_entries) * 100
        report += f"  {op:15s}: {count:4d} 次 ({percentage:.1f}%)\n"
    
    report += f"""
{'='*80}
✅ 结果统计
{'='*80}
"""
    
    for result, count in results.most_common():
        percentage = (count / total_entries) * 100
        result_emoji = "✅" if result == "success" else "❌" if result == "denied" else "⚠️"
        report += f"  {result_emoji} {result:15s}: {count:4d} 次 ({percentage:.1f}%)\n"
    
    # 异常访问
    denied_entries = [e for e in agent_entries if e.get("结果") == "denied"]
    error_entries = [e for e in agent_entries if e.get("结果") == "error"]
    
    if denied_entries or error_entries:
        report += f"""
{'='*80}
🚨 异常访问
{'='*80}
"""
        
        if denied_entries:
            report += f"⚠️  权限拒绝: {len(denied_entries)} 次\n"
            for entry in denied_entries[:3]:
                report += f"   - {entry.get('时间')} | {entry.get('操作')} | {entry.get('记忆ID')}\n"
        
        if error_entries:
            report += f"❌ 系统错误: {len(error_entries)} 次\n"
            for entry in error_entries[:3]:
                report += f"   - {entry.get('时间')} | {entry.get('操作')} | {entry.get('备注', '无备注')}\n"
    
    if recent_memories:
        report += f"""
{'='*80}
📚 最近访问的记忆
{'='*80}
"""
        for i, memory_id in enumerate(recent_memories[:10], 1):
            report += f"  {i:2d}. {memory_id}\n"
        
        if len(recent_memories) > 10:
            report += f"  ... 还有 {len(recent_memories)-10} 个记忆\n"
    
    # 行为分析
    if operations.get("read_memory", 0) > operations.get("add_memory", 0) * 2:
        report += f"""
{'='*80}
📈 行为分析
{'='*80}
🔸 该代理主要进行读取操作，是信息消费者
🔸 建议鼓励其贡献记忆（添加、更新）
"""
    elif operations.get("add_memory", 0) > operations.get("read_memory", 0) * 2:
        report += f"""
{'='*80}
📈 行为分析
{'='*80}
🔸 该代理主要进行添加操作，是信息生产者
🔸 建议检查其添加的记忆质量
"""
    
    report += f"""
{'='*80}
💡 个性化建议
{'='*80}
🔸 定期检查权限配置是否满足需求
🔸 如有权限拒绝，考虑调整 allowed_tags
🔸 建议每季度审查一次权限有效期
"""
    
    return report

def main():
    parser = argparse.ArgumentParser(description="生成审计报告")
    parser.add_argument("--days", type=int, default=7, help="分析最近N天的数据")
    parser.add_argument("--agent", help="生成指定代理的报告")
    parser.add_argument("--output", help="输出到文件")
    
    args = parser.parse_args()
    
    print("📊 生成审计报告...")
    print(f"   分析周期: 最近 {args.days} 天")
    if args.agent:
        print(f"   目标代理: {args.agent}")
    print("=" * 80)
    
    # 解析日志
    all_entries = parse_audit_log()
    
    if not all_entries:
        print("📭 审计日志为空")
        return
    
    # 按时间过滤
    filtered_entries = filter_entries_by_time(all_entries, args.days)
    
    if not filtered_entries:
        print(f"📭 最近 {args.days} 天内无访问记录")
        return
    
    # 生成报告
    if args.agent:
        report = generate_agent_report(args.agent, filtered_entries, args.days)
    else:
        report = generate_summary_report(filtered_entries, args.days)
    
    # 输出报告
    if args.output:
        output_file = Path(args.output)
        output_file.write_text(report, encoding='utf-8')
        print(f"✓ 报告已保存到: {output_file}")
    else:
        print(report)
    
    print("=" * 80)
    print("💡 其他分析命令:")
    print(f"  代理专属报告: python3 {__file__} --agent alpha --days 30")
    print(f"  导出报告: python3 {__file__} --days 7 --output report.md")
    print(f"  查看原始日志: cat {SHARED_MEMORY_ROOT}/access_log/audit_log.md")

if __name__ == "__main__":
    main()