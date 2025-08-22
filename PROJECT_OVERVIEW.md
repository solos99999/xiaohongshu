# 📋 项目文件概览

## 📁 完整项目结构

```
xiaohongshu/
├── 🎯 核心程序
│   ├── xhs_find_and_open.py      # 主程序文件
│   ├── start.py                  # 交互式启动脚本
│   └── requirements.txt          # Python依赖
│
├── 📚 文档说明
│   ├── README.md                 # 完整项目文档
│   ├── QUICKSTART.md             # 快速开始指南
│   ├── auto_reply_guide.md       # 自动回复使用指南
│   └── multi_account_examples.md # 多账户使用示例
│
├── ⚙️ 配置文件
│   ├── project.json              # 项目配置信息
│   ├── keywords.txt              # 关键词文件（可选）
│   ├── reply_content.txt         # 回复内容文件
│   └── auth_state.json           # 单账户认证状态
│
├── 👥 多账户支持
│   ├── accounts/                 # 多账户目录
│   │   ├── README.md            # 多账户使用说明
│   │   ├── account1/            # 账户1
│   │   │   └── auth_state.json
│   │   └── account2/            # 账户2
│   │       └── auth_state.json
│   └── account_usage.json        # 账户使用统计
│
├── 🧪 测试工具
│   ├── test_reply.py            # 回复功能测试
│   ├── test_multi_account.py    # 多账户功能测试
│   ├── verify_integration.py    # 集成验证
│   └── usage_examples.py        # 使用示例
│
└── 🖼️ 运行文件
    └── detail_snapshot.png       # 详情页截图（运行时生成）
```

## 📊 文件功能说明

### 核心程序文件
- **xhs_find_and_open.py** - 主程序，包含所有核心功能
- **start.py** - 交互式启动界面，适合新手使用
- **requirements.txt** - 项目依赖包列表

### 文档文件
- **README.md** - 完整的项目文档，包含所有功能说明
- **QUICKSTART.md** - 快速开始指南，一分钟上手
- **auto_reply_guide.md** - 自动回复功能详细使用指南
- **multi_account_examples.md** - 多账户功能使用示例

### 配置文件
- **project.json** - 项目元数据和配置信息
- **keywords.txt** - 关键词列表文件（可选）
- **reply_content.txt** - 回复内容库，包含35条预设回复
- **auth_state.json** - 单账户模式下的登录状态

### 多账户文件
- **accounts/** - 多账户目录
- **accounts/README.md** - 多账户使用说明
- **account_usage.json** - 账户使用统计和状态记录

### 测试和示例
- **test_reply.py** - 回复功能测试脚本
- **test_multi_account.py** - 多账户功能测试脚本
- **verify_integration.py** - 功能集成验证脚本
- **usage_examples.py** - 使用示例展示

### 运行时文件
- **detail_snapshot.png** - 程序运行时生成的详情页截图

## 🚀 快速开始

### 方法1：交互式启动（推荐新手）
```bash
python start.py
```

### 方法2：直接运行
```bash
# 基础搜索
python xhs_find_and_open.py --keyword "推荐"

# 自动回复
python xhs_find_and_open.py --keyword "美食" --auto-reply

# 多账户模式
python xhs_find_and_open.py --keyword "旅行" --multi-account
```

### 方法3：查看文档
```bash
# 查看完整文档
cat README.md

# 查看快速开始
cat QUICKSTART.md

# 查看状态
python xhs_find_and_open.py --account-status
python xhs_find_and_open.py --reply-status
```

## 🎯 核心功能

1. **智能搜索** - 关键词匹配、多种搜索模式
2. **自动点赞** - 智能检测点赞状态并自动点赞
3. **自动回复** - 发现已点赞时自动评论
4. **多账户支持** - 账户轮换、负载均衡
5. **灵活配置** - 丰富的命令行参数

## 📈 项目特点

- ✅ **功能完整** - 搜索、点赞、回复、多账户全覆盖
- ✅ **易于使用** - 交互式界面 + 详细文档
- ✅ **高度可配置** - 丰富的命令行参数
- ✅ **稳定可靠** - 完善的错误处理和重试机制
- ✅ **文档完善** - 从快速开始到详细说明的全套文档
- ✅ **测试充分** - 多个测试脚本验证功能

## 🔧 技术栈

- **Python 3.7+** - 主要编程语言
- **Playwright** - 浏览器自动化
- **argparse** - 命令行参数解析
- **json** - 配置文件管理
- **random** - 随机回复选择

## 📝 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和平台规则。

---

🎊 恭喜！你现在拥有了一个功能完整、文档齐全的小红书自动化工具！