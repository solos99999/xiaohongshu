#!/usr/bin/env python3
"""
测试多账户功能
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xhs_find_and_open import (
    setup_accounts_directory,
    get_available_accounts,
    get_next_account,
    record_account_usage,
    print_account_status,
    load_account_usage
)

def test_multi_account_functions():
    """测试多账户相关函数"""
    print("=== 测试多账户功能 ===")
    
    # 1. 设置账户目录
    print("\n1. 设置账户目录...")
    setup_accounts_directory()
    print("账户目录设置完成")
    
    # 2. 获取可用账户
    print("\n2. 获取可用账户...")
    accounts = get_available_accounts()
    print(f"可用账户: {accounts}")
    
    # 3. 测试账户选择逻辑
    print("\n3. 测试账户选择逻辑...")
    if accounts:
        # 测试选择下一个账户
        next_account = get_next_account()
        print(f"选择的下一个账户: {next_account}")
        
        # 测试轮换逻辑
        if len(accounts) > 1:
            current_account = accounts[0]
            next_account = get_next_account(current_account)
            print(f"当前账户 {current_account} -> 下一个账户: {next_account}")
    
    # 4. 测试使用记录
    print("\n4. 测试使用记录...")
    if accounts:
        test_account = accounts[0]
        print(f"记录账户 {test_account} 的使用...")
        record_account_usage(test_account, success=True)
        print("使用记录已保存")
        
        # 检查使用数据
        usage_data = load_account_usage()
        account_stats = usage_data.get(test_account, {})
        print(f"账户 {test_account} 使用次数: {account_stats.get('usage_count', 0)}")
        print(f"账户 {test_account} 成功次数: {account_stats.get('success_count', 0)}")
    
    # 5. 打印账户状态
    print("\n5. 打印账户状态...")
    print_account_status()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_multi_account_functions()