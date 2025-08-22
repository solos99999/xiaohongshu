#!/usr/bin/env python3
"""
小红书自动化工具快速启动脚本
"""
import os
import sys
import subprocess

def print_banner():
    """打印启动横幅"""
    print("=" * 60)
    print("🔥 小红书自动化搜索与互动工具")
    print("=" * 60)
    print()

def check_requirements():
    """检查依赖"""
    print("📋 检查系统要求...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查依赖包
    try:
        import playwright
        print("✅ Playwright已安装")
    except ImportError:
        print("❌ Playwright未安装")
        print("请运行: pip install playwright")
        return False
    
    # 检查浏览器
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            browser.close()
        print("✅ 浏览器正常")
    except Exception as e:
        print(f"❌ 浏览器问题: {e}")
        print("请运行: playwright install")
        return False
    
    return True

def show_menu():
    """显示菜单"""
    print("\n🎯 请选择功能:")
    print("1. 基础搜索")
    print("2. 自动点赞")
    print("3. 自动回复")
    print("4. 多账户模式")
    print("5. 完整功能")
    print("6. 查看状态")
    print("7. 帮助文档")
    print("8. 退出")
    print()

def get_keyword():
    """获取搜索关键词"""
    keyword = input("请输入搜索关键词: ").strip()
    if not keyword:
        print("❌ 关键词不能为空")
        return None
    return keyword

def basic_search():
    """基础搜索"""
    keyword = get_keyword()
    if not keyword:
        return
    
    headless = input("是否使用无头模式? (y/n): ").lower() == 'y'
    
    cmd = ["python", "xhs_find_and_open.py", "--keyword", keyword]
    if headless:
        cmd.append("--headless")
    
    print(f"\n🚀 执行命令: {' '.join(cmd)}")
    subprocess.run(cmd)

def auto_like():
    """自动点赞"""
    keyword = get_keyword()
    if not keyword:
        return
    
    headless = input("是否使用无头模式? (y/n): ").lower() == 'y'
    
    cmd = ["python", "xhs_find_and_open.py", "--keyword", keyword]
    if headless:
        cmd.append("--headless")
    
    print(f"\n🚀 执行命令: {' '.join(cmd)}")
    subprocess.run(cmd)

def auto_reply():
    """自动回复"""
    keyword = get_keyword()
    if not keyword:
        return
    
    headless = input("是否使用无头模式? (y/n): ").lower() == 'y'
    
    cmd = ["python", "xhs_find_and_open.py", "--keyword", keyword, "--auto-reply"]
    if headless:
        cmd.append("--headless")
    
    print(f"\n🚀 执行命令: {' '.join(cmd)}")
    subprocess.run(cmd)

def multi_account():
    """多账户模式"""
    keyword = get_keyword()
    if not keyword:
        return
    
    headless = input("是否使用无头模式? (y/n): ").lower() == 'y'
    interval = input("账户切换间隔 (默认10): ").strip()
    interval = interval if interval.isdigit() else "10"
    
    cmd = [
        "python", "xhs_find_and_open.py",
        "--keyword", keyword,
        "--multi-account",
        "--account-switch-interval", interval
    ]
    if headless:
        cmd.append("--headless")
    
    print(f"\n🚀 执行命令: {' '.join(cmd)}")
    subprocess.run(cmd)

def full_function():
    """完整功能"""
    keyword = get_keyword()
    if not keyword:
        return
    
    headless = input("是否使用无头模式? (y/n): ").lower() == 'y'
    interval = input("账户切换间隔 (默认10): ").strip()
    interval = interval if interval.isdigit() else "10"
    
    cmd = [
        "python", "xhs_find_and_open.py",
        "--keyword", keyword,
        "--auto-reply",
        "--multi-account",
        "--account-switch-interval", interval
    ]
    if headless:
        cmd.append("--headless")
    
    print(f"\n🚀 执行命令: {' '.join(cmd)}")
    subprocess.run(cmd)

def show_status():
    """显示状态"""
    print("\n📊 状态信息:")
    print("1. 账户状态")
    print("2. 回复内容状态")
    print("3. 返回主菜单")
    
    choice = input("请选择: ").strip()
    
    if choice == "1":
        subprocess.run(["python", "xhs_find_and_open.py", "--account-status"])
    elif choice == "2":
        subprocess.run(["python", "xhs_find_and_open.py", "--reply-status"])
    
    input("\n按回车键继续...")

def show_help():
    """显示帮助"""
    print("\n📖 帮助文档:")
    print("1. 查看完整README")
    print("2. 自动回复指南")
    print("3. 多账户示例")
    print("4. 返回主菜单")
    
    choice = input("请选择: ").strip()
    
    if choice == "1":
        try:
            with open("README.md", "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ README.md文件不存在")
    elif choice == "2":
        try:
            with open("auto_reply_guide.md", "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ auto_reply_guide.md文件不存在")
    elif choice == "3":
        try:
            with open("multi_account_examples.md", "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("❌ multi_account_examples.md文件不存在")
    
    input("\n按回车键继续...")

def main():
    """主函数"""
    print_banner()
    
    # 检查依赖
    if not check_requirements():
        input("按回车键退出...")
        return
    
    # 主循环
    while True:
        show_menu()
        
        try:
            choice = input("请选择功能 (1-8): ").strip()
            
            if choice == "1":
                basic_search()
            elif choice == "2":
                auto_like()
            elif choice == "3":
                auto_reply()
            elif choice == "4":
                multi_account()
            elif choice == "5":
                full_function()
            elif choice == "6":
                show_status()
            elif choice == "7":
                show_help()
            elif choice == "8":
                print("👋 感谢使用！")
                break
            else:
                print("❌ 无效选择，请重试")
            
            print("\n" + "="*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 程序已终止")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            input("按回车键继续...")

if __name__ == "__main__":
    main()