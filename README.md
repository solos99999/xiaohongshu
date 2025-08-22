# 小红书自动化搜索与互动工具

一个功能强大的小红书自动化工具，支持关键词搜索、自动点赞、多账户轮流登录和智能回复功能。

## 🌟 功能特性

### 🔍 智能搜索
- **关键词匹配**：支持标题和链接内容的关键词搜索
- **灵活匹配**：支持包含匹配、精确匹配、正则表达式匹配
- **批量搜索**：支持从文件读取多个关键词
- **排除规则**：支持排除特定关键词或URL

### 👍 自动互动
- **智能点赞**：自动检测点赞状态并进行点赞
- **自动回复**：发现已点赞笔记时自动评论
- **回复内容管理**：支持随机回复内容，避免重复
- **灵活控制**：可独立控制点赞和回复功能

### 👥 多账户支持
- **账户轮换**：支持多个账户轮流使用
- **负载均衡**：智能选择使用次数最少的账户
- **使用统计**：记录每个账户的使用情况和成功率
- **状态管理**：每个账户独立的认证状态

### ⚙️ 高级配置
- **无头模式**：支持后台运行
- **代理支持**：支持HTTP/SOCKS代理
- **调试模式**：详细的调试信息和截图
- **灵活配置**：丰富的命令行参数

## 📦 安装要求

### 系统要求
- Python 3.7+
- Windows/Linux/macOS

### 依赖包
```bash
pip install playwright
playwright install
```

## 🚀 快速开始

### 1. 基础使用
```bash
# 简单搜索
python xhs_find_and_open.py --keyword "推荐"

# 启用自动点赞
python xhs_find_and_open.py --keyword "美食" --headless

# 禁用点赞功能
python xhs_find_and_open.py --keyword "旅行" --no-like
```

### 2. 自动回复功能
```bash
# 启用自动回复
python xhs_find_and_open.py --keyword "推荐" --auto-reply

# 查看回复内容状态
python xhs_find_and_open.py --reply-status

# 使用自定义回复文件
python xhs_find_and_open.py --keyword "科技" --auto-reply --reply-file "my_replies.txt"
```

### 3. 多账户模式
```bash
# 启用多账户轮换
python xhs_find_and_open.py --keyword "时尚" --multi-account

# 查看账户状态
python xhs_find_and_open.py --account-status

# 指定切换间隔
python xhs_find_and_open.py --keyword "运动" --multi-account --account-switch-interval 5
```

### 4. 完整功能组合
```bash
# 启用所有功能
python xhs_find_and_open.py \
  --keyword "美食" \
  --auto-reply \
  --multi-account \
  --headless \
  --max-refresh 50 \
  --account-switch-interval 10
```

## 📁 项目结构

```
xiaohongshu/
├── xhs_find_and_open.py          # 主脚本
├── reply_content.txt             # 回复内容文件
├── auth_state.json               # 单账户认证状态
├── account_usage.json           # 账户使用统计
├── accounts/                     # 多账户目录
│   ├── account1/
│   │   └── auth_state.json
│   └── account2/
│       └── auth_state.json
├── keywords.txt                 # 关键词文件（可选）
├── detail_snapshot.png           # 详情页截图
├── auto_reply_guide.md           # 自动回复使用指南
├── multi_account_examples.md     # 多账户使用示例
└── README.md                     # 项目说明
```

## 🔧 配置说明

### 关键词配置
创建 `keywords.txt` 文件：
```
# 单关键词
旅行

# 指定匹配字段
title:美食
link:/explore/

# 多关键词组合
title:科技,数码

# 使用注释
# 这是一个注释行
```

### 回复内容配置
编辑 `reply_content.txt` 文件：
```
# 赞美类
这个内容太棒了！学到了很多
写得真好，很有帮助
感谢分享，非常有用

# 互动类
说得很有道理，赞同
这个观点很新颖
深有同感，确实如此
```

### 多账户配置
1. 创建账户目录：
```bash
mkdir -p accounts/account1 accounts/account2
```

2. 复制认证文件：
```bash
# 将 auth_state.json 复制到各账户目录
cp auth_state.json accounts/account1/
cp auth_state.json accounts/account2/
```

## 📖 命令行参数

### 基础参数
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--keyword` | 搜索关键词（可多次使用） | - |
| `--keywords-file` | 从文件读取关键词 | keywords.txt |
| `--match-fields` | 匹配字段（title,link,any） | title |
| `--max-refresh` | 最大刷新次数 | 30 |
| `--scroll-steps` | 每轮滚动步数 | 6 |
| `--interval` | 刷新间隔（秒） | 3.0 |

### 匹配参数
| 参数 | 说明 |
|------|------|
| `--regex` | 使用正则表达式匹配 |
| `--exact` | 精确匹配 |
| `--case-sensitive` | 区分大小写 |

### 运行参数
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--headless` | 无头模式运行 | False |
| `--login-timeout` | 登录超时（秒） | 180 |
| `--proxy` | 代理服务器 | - |
| `--home-url` | 首页URL | 小红书官网 |
| `--debug` | 调试模式 | False |

### 功能参数
| 参数 | 说明 |
|------|------|
| `--no-like` | 禁用自动点赞 |
| `--auto-reply` | 启用自动回复 |
| `--reply-file` | 回复内容文件 | reply_content.txt |
| `--multi-account` | 启用多账户模式 |
| `--account-switch-interval` | 账户切换间隔 | 10 |
| `--account` | 指定特定账户 |

### 状态参数
| 参数 | 说明 |
|------|------|
| `--account-status` | 显示账户状态并退出 |
| `--reply-status` | 显示回复内容状态并退出 |

## 🎯 使用场景

### 1. 内容发现
```bash
# 发现特定类型的内容
python xhs_find_and_open.py --keyword "美食推荐" --headless
```

### 2. 自动互动
```bash
# 自动点赞和回复
python xhs_find_and_open.py --keyword "旅行攻略" --auto-reply
```

### 3. 大规模操作
```bash
# 使用多账户进行大规模操作
python xhs_find_and_open.py \
  --keywords-file keywords.txt \
  --multi-account \
  --account-switch-interval 8 \
  --headless \
  --max-refresh 100
```

### 4. 定时任务
```bash
# 配合系统定时任务使用
# 每小时运行一次
0 * * * * cd /path/to/xiaohongshu && python xhs_find_and_open.py --keyword "科技" --auto-reply --headless
```

## ⚠️ 注意事项

### 使用规范
1. **遵守平台规则**：请遵守小红书的社区规范和使用条款
2. **合理使用频率**：避免过于频繁的操作，防止被限制
3. **内容质量**：确保回复内容有价值，避免垃圾信息
4. **账户安全**：保护好账户信息，避免违规操作

### 技术限制
1. **反爬虫机制**：平台可能有反爬虫机制，请合理使用
2. **页面变化**：小红书页面结构可能变化，影响选择器效果
3. **网络环境**：确保网络连接稳定，必要时使用代理
4. **认证状态**：定期更新认证状态，确保登录有效

### 最佳实践
1. **逐步测试**：先在小范围内测试，确认功能正常
2. **监控运行**：定期检查运行状态和日志
3. **备份配置**：备份重要的配置文件和认证状态
4. **更新维护**：根据平台变化及时更新脚本

## 🔍 故障排除

### 常见问题

1. **登录失败**
   - 检查认证文件是否存在
   - 确认账户登录状态有效
   - 尝试重新登录获取认证状态

2. **搜索无结果**
   - 检查关键词是否正确
   - 确认网络连接正常
   - 尝试调整搜索参数

3. **点赞/回复失败**
   - 检查元素选择器是否有效
   - 确认页面已完全加载
   - 查看调试日志和截图

4. **多账户切换失败**
   - 检查账户目录结构
   - 确认认证文件有效
   - 查看账户使用统计

### 调试方法

1. **启用调试模式**
   ```bash
   python xhs_find_and_open.py --keyword "测试" --debug
   ```

2. **查看状态信息**
   ```bash
   python xhs_find_and_open.py --account-status
   python xhs_find_and_open.py --reply-status
   ```

3. **检查截图文件**
   - 查看 `detail_snapshot.png` 了解页面状态

4. **测试单个功能**
   - 分别测试点赞、回复、多账户等功能

## 📊 性能优化

### 搜索效率
- 合理设置 `--max-refresh` 和 `--scroll-steps`
- 使用 `--keywords-file` 批量处理关键词
- 启用 `--headless` 模式提高性能

### 账户管理
- 合理设置 `--account-switch-interval`
- 定期检查账户使用统计
- 及时替换失效账户

### 网络优化
- 使用稳定的网络环境
- 必要时配置代理服务器
- 设置合理的 `--interval` 参数

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境
1. 克隆项目
2. 安装依赖：`pip install -r requirements.txt`
3. 安装Playwright：`playwright install`
4. 运行测试：`python test_reply.py`

### 代码规范
- 遵循PEP 8规范
- 添加适当的注释
- 确保功能正常工作

### 功能建议
- 新功能请先提交Issue讨论
- 提供详细的使用场景和需求
- 尽量提供实现方案

## 📄 许可证

本项目仅供学习和研究使用，请勿用于商业用途。

使用本工具时请遵守相关法律法规和平台规则，作者不承担任何责任。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue：[GitHub Issues]
- 邮箱：[your-email@example.com]

## 🔄 更新日志

### v1.0.0 (2024-01-XX)
- ✅ 基础搜索功能
- ✅ 自动点赞功能
- ✅ 多账户支持
- ✅ 自动回复功能
- ✅ 完整的命令行参数
- ✅ 详细的文档和示例

---

**免责声明**：本工具仅供学习和研究使用，使用者应遵守相关法律法规和平台规则。作者不对使用本工具造成的任何后果负责。