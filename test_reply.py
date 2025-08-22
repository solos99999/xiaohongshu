#!/usr/bin/env python3
"""
测试自动回复功能
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from xhs_find_and_open import (
    load_reply_content,
    get_random_reply,
    print_reply_status
)

def test_reply_functions():
    """测试回复相关函数"""
    print("=== 测试自动回复功能 ===")
    
    # 1. 加载回复内容
    print("\n1. 加载回复内容...")
    replies = load_reply_content()
    print(f"加载了 {len(replies)} 条回复内容")
    
    # 2. 测试随机回复
    print("\n2. 测试随机回复...")
    for i in range(5):
        reply = get_random_reply()
        if reply:
            print(f"随机回复 {i+1}: {reply}")
        else:
            print("随机回复失败")
    
    # 3. 测试重复性
    print("\n3. 测试重复性...")
    test_replies = []
    for i in range(10):
        reply = get_random_reply()
        if reply:
            test_replies.append(reply)
    
    unique_replies = set(test_replies)
    print(f"10次测试中，获取了 {len(unique_replies)} 条不同的回复")
    
    # 4. 打印回复状态
    print("\n4. 打印回复状态...")
    print_reply_status()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_reply_functions()