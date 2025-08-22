# 🚀 快速安装与使用指南

## 一分钟快速开始

### 1. 安装依赖
```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install
```

### 2. 配置认证
```bash
# 方法1：使用现有认证文件
# 将你的小红书登录状态保存为 auth_state.json

# 方法2：运行时扫码登录
python xhs_find_and_open.py --keyword "测试"
# 在弹出的浏览器中扫码登录
```

### 3. 开始使用
```bash
# 启动交互式界面
python start.py

# 或直接使用命令行
python xhs_find_and_open.py --keyword "美食" --auto-reply
```

## 🎯 快速命令

### 基础使用
```bash
# 搜索关键词
python xhs_find_and_open.py --keyword "推荐"

# 后台运行
python xhs_find_and_open.py --keyword "美食" --headless

# 自动点赞
python xhs_find_and_open.py --keyword "旅行" --auto-reply

# 多账户模式
python xhs_find_and_open.py --keyword "时尚" --multi-account
```

### 状态查看
```bash
# 查看账户状态
python xhs_find_and_open.py --account-status

# 查看回复内容
python xhs_find_and_open.py --reply-status

# 查看帮助
python xhs_find_and_open.py --help
```

### 高级功能
```bash
# 完整功能组合
python xhs_find_and_open.py \
  --keyword "科技" \
  --auto-reply \
  --multi-account \
  --headless \
  --max-refresh 50

# 使用自定义文件
python xhs_find_and_open.py \
  --keywords-file my_keywords.txt \
  --reply-file my_replies.txt \
  --account account1
```

## 📁 必要文件

### 自动创建的文件
- `auth_state.json` - 登录状态（首次运行时生成）
- `account_usage.json` - 账户使用统计
- `detail_snapshot.png` - 详情页截图

### 可选的文件
- `keywords.txt` - 关键词列表
- `reply_content.txt` - 回复内容（已提供）
- `accounts/` - 多账户目录

## 🔧 常见问题

### Q: 如何获取认证文件？
A: 运行脚本时会在浏览器中打开登录页面，扫码登录后会自动生成 `auth_state.json`

### Q: 如何配置多账户？
A: 
```bash
mkdir -p accounts/account1 accounts/account2
cp auth_state.json accounts/account1/
cp auth_state.json accounts/account2/
```

### Q: 如何自定义回复内容？
A: 编辑 `reply_content.txt` 文件，每行一条回复内容

### Q: 脚本运行很慢怎么办？
A: 使用 `--headless` 参数，减少 `--max-refresh` 次数

## 📚 完整文档

- [详细说明](README.md) - 完整的项目文档
- [自动回复指南](auto_reply_guide.md) - 自动回复功能详解
- [多账户示例](multi_account_examples.md) - 多账户使用示例

## 🎉 开始使用

现在你已经准备好使用这个强大的小红书自动化工具了！

1. 运行 `python start.py` 开始交互式体验
2. 或直接使用命令行参数进行自动化操作
3. 查看详细文档了解所有功能

祝你使用愉快！🎊