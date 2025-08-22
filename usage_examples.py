#!/usr/bin/env python3
"""
自动回复功能完整使用示例
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def show_usage_examples():
    """显示使用示例"""
    print("=== 自动回复功能使用示例 ===")
    
    print("\n1. 基本使用")
    print("启用自动回复功能:")
    print("  python xhs_find_and_open.py --keyword '推荐' --auto-reply")
    
    print("\n2. 查看状态")
    print("查看回复内容状态:")
    print("  python xhs_find_and_open.py --reply-status")
    
    print("\n3. 自定义回复文件")
    print("使用自定义回复文件:")
    print("  python xhs_find_and_open.py --keyword '美食' --auto-reply --reply-file 'my_replies.txt'")
    
    print("\n4. 组合功能")
    print("启用所有功能:")
    print("  python xhs_find_and_open.py --keyword '旅行' --auto-reply --multi-account --headless --no-like")
    
    print("\n5. 高级配置")
    print("完整配置示例:")
    print("  python xhs_find_and_open.py \\")
    print("    --keyword '科技' \\")
    print("    --auto-reply \\")
    print("    --reply-file 'tech_replies.txt' \\")
    print("    --multi-account \\")
    print("    --account-switch-interval 8 \\")
    print("    --headless \\")
    print("    --max-refresh 50 \\")
    print("    --no-like")
    
    print("\n6. 实际应用场景")
    print("大规模自动互动:")
    print("  python xhs_find_and_open.py \\")
    print("    --keywords-file keywords.txt \\")
    print("    --auto-reply \\")
    print("    --multi-account \\")
    print("    --account-switch-interval 10 \\")
    print("    --headless \\")
    print("    --max-refresh 100")
    
    print("\n=== 注意事项 ===")
    print("1. 确保回复内容文件存在且格式正确")
    print("2. 回复内容要友好、有价值")
    print("3. 不要过于频繁回复，避免被限制")
    print("4. 定期检查回复成功率")
    print("5. 遵守平台规则和社区规范")
    
    print("\n=== 文件结构 ===")
    print("项目目录结构:")
    print("  xiaohongshu/")
    print("  ├── xhs_find_and_open.py")
    print("  ├── reply_content.txt")
    print("  ├── auto_reply_guide.md")
    print("  ├── accounts/")
    print("  │   ├── account1/")
    print("  │   │   └── auth_state.json")
    print("  │   └── account2/")
    print("  │       └── auth_state.json")
    print("  └── account_usage.json")
    
    print("\n=== 示例完成 ===")

if __name__ == "__main__":
    show_usage_examples()