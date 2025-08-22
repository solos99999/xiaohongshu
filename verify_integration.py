#!/usr/bin/env python3
"""
验证自动回复功能集成
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_integration():
    """验证功能集成"""
    print("=== 验证自动回复功能集成 ===")
    
    # 检查文件是否存在
    files_to_check = [
        "xhs_find_and_open.py",
        "reply_content.txt",
        "auto_reply_guide.md"
    ]
    
    print("\n1. 检查文件存在性...")
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"OK {file_path}")
        else:
            print(f"ERROR {file_path}")
    
    # 检查函数导入
    print("\n2. 检查函数导入...")
    try:
        from xhs_find_and_open import (
            load_reply_content,
            get_random_reply,
            print_reply_status,
            post_comment
        )
        print("所有回复函数导入成功")
    except Exception as e:
        print(f"函数导入失败: {e}")
    
    # 检查回复内容
    print("\n3. 检查回复内容...")
    try:
        replies = load_reply_content()
        print(f"回复内容加载成功，共 {len(replies)} 条")
        
        reply = get_random_reply()
        if reply:
            print(f"随机回复功能正常: {reply}")
        else:
            print("随机回复功能失败")
    except Exception as e:
        print(f"回复内容检查失败: {e}")
    
    # 检查命令行参数
    print("\n4. 检查命令行参数...")
    import subprocess
    try:
        result = subprocess.run([
            sys.executable, "xhs_find_and_open.py", "--help"
        ], capture_output=True, text=True, encoding='utf-8')
        
        help_text = result.stdout
        reply_params = ["--auto-reply", "--reply-file", "--reply-status"]
        
        for param in reply_params:
            if param in help_text:
                print(f"参数 {param} 存在")
            else:
                print(f"参数 {param} 不存在")
    except Exception as e:
        print(f"命令行参数检查失败: {e}")
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    verify_integration()