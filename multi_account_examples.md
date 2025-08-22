# 多账户功能使用示例

## 基本用法

### 1. 查看账户状态
```bash
python xhs_find_and_open.py --account-status
```

### 2. 启用多账户模式
```bash
python xhs_find_and_open.py --keyword "推荐" --multi-account
```

### 3. 指定切换间隔
```bash
python xhs_find_and_open.py --keyword "推荐" --multi-account --account-switch-interval 5
```

### 4. 使用特定账户
```bash
python xhs_find_and_open.py --keyword "推荐" --multi-account --account account1
```

## 高级用法

### 1. 完整的多账户配置
```bash
python xhs_find_and_open.py \
  --keyword "推荐" \
  --multi-account \
  --account-switch-interval 8 \
  --headless \
  --no-like \
  --max-refresh 50
```

### 2. 监控账户使用情况
```bash
# 查看账户使用统计
python xhs_find_and_open.py --account-status

# 查看使用记录文件
cat account_usage.json
```

### 3. 账户维护
```bash
# 添加新账户
mkdir -p accounts/account3
# 将 auth_state.json 复制到 accounts/account3/

# 删除账户
rm -rf accounts/account3

# 重置使用统计
rm account_usage.json
```

## 实际应用场景

### 1. 大规模搜索
```bash
# 使用多个账户进行大规模搜索，避免单一账户过度使用
python xhs_find_and_open.py \
  --keywords-file keywords.txt \
  --multi-account \
  --account-switch-interval 10 \
  --max-refresh 100
```

### 2. 自动化任务
```bash
# 设置定时任务，定期使用不同账户
# 每小时运行一次，自动切换账户
python xhs_find_and_open.py \
  --keyword "美食" \
  --multi-account \
  --account-switch-interval 5 \
  --headless \
  --no-like
```

### 3. 负载均衡
```bash
# 在多个账户间均衡负载
python xhs_find_and_open.py \
  --keyword "旅行" \
  --multi-account \
  --account-switch-interval 3 \
  --max-refresh 30
```

## 性能优化建议

1. **合理设置切换间隔**：
   - 太频繁：影响搜索效率
   - 太稀少：失去多账户优势
   - 建议：5-15次搜索切换一次

2. **监控账户健康度**：
   - 定期检查账户使用统计
   - 及时替换失效账户
   - 保持账户活跃度

3. **维护认证状态**：
   - 定期更新 auth_state.json
   - 确保账户登录状态有效
   - 备份重要的认证文件

## 故障排除

### 常见问题
1. **账户切换失败**：检查认证文件是否有效
2. **使用统计错误**：检查 account_usage.json 文件权限
3. **搜索失败**：检查网络连接和账户状态

### 解决方案
1. 重新生成认证文件
2. 清理使用统计文件
3. 检查账户目录结构
4. 验证账户登录状态