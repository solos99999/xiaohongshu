import os
import time
import argparse
import json
import glob
import random
from typing import Optional, List, Tuple, Set, Dict, Any
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
from urllib.parse import urljoin


HOMEPAGE_URL = "https://www.xiaohongshu.com/explore"
AUTH_STATE_PATH = "auth_state.json"
ACCOUNTS_DIR = "accounts"
ACCOUNT_USAGE_FILE = "account_usage.json"
REPLY_CONTENT_FILE = "reply_content.txt"


def setup_accounts_directory():
    """设置账户目录结构"""
    accounts_path = Path(ACCOUNTS_DIR)
    accounts_path.mkdir(exist_ok=True)
    return accounts_path


def get_available_accounts() -> List[str]:
    """获取所有可用的账户列表"""
    accounts_path = Path(ACCOUNTS_DIR)
    if not accounts_path.exists():
        return []
    
    # 查找所有账户状态文件
    auth_files = list(accounts_path.glob("*/auth_state.json"))
    accounts = []
    for auth_file in auth_files:
        account_name = auth_file.parent.name
        accounts.append(account_name)
    
    return sorted(accounts)


def get_account_auth_path(account_name: str) -> str:
    """获取指定账户的认证状态文件路径"""
    return os.path.join(ACCOUNTS_DIR, account_name, "auth_state.json")


def load_account_usage() -> Dict[str, Dict[str, Any]]:
    """加载账户使用记录"""
    if os.path.exists(ACCOUNT_USAGE_FILE):
        try:
            with open(ACCOUNT_USAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_account_usage(usage_data: Dict[str, Dict[str, Any]]):
    """保存账户使用记录"""
    try:
        with open(ACCOUNT_USAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(usage_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存账户使用记录失败: {e}")


def get_next_account(current_account: Optional[str] = None) -> Optional[str]:
    """获取下一个应该使用的账户"""
    accounts = get_available_accounts()
    if not accounts:
        return None
    
    if len(accounts) == 1:
        return accounts[0]
    
    usage_data = load_account_usage()
    
    # 如果没有当前账户，选择使用次数最少的账户
    if current_account is None:
        # 计算每个账户的使用次数
        account_stats = {}
        for account in accounts:
            stats = usage_data.get(account, {})
            account_stats[account] = stats.get('usage_count', 0)
        
        # 选择使用次数最少的账户
        next_account = min(account_stats, key=account_stats.get)
        return next_account
    
    # 如果有当前账户，选择下一个账户
    try:
        current_index = accounts.index(current_account)
        next_index = (current_index + 1) % len(accounts)
        return accounts[next_index]
    except ValueError:
        # 如果当前账户不在列表中，选择第一个账户
        return accounts[0]


def record_account_usage(account_name: str, success: bool = True):
    """记录账户使用情况"""
    usage_data = load_account_usage()
    
    if account_name not in usage_data:
        usage_data[account_name] = {
            'usage_count': 0,
            'success_count': 0,
            'last_used': None,
            'last_success': None
        }
    
    account_stats = usage_data[account_name]
    account_stats['usage_count'] += 1
    account_stats['last_used'] = time.time()
    
    if success:
        account_stats['success_count'] += 1
        account_stats['last_success'] = time.time()
    
    save_account_usage(usage_data)


def print_account_status():
    """打印账户状态信息"""
    accounts = get_available_accounts()
    usage_data = load_account_usage()
    
    print("=== 多账户状态 ===")
    print(f"可用账户数量: {len(accounts)}")
    
    if accounts:
        print("账户列表:")
        for account in accounts:
            stats = usage_data.get(account, {})
            usage_count = stats.get('usage_count', 0)
            success_count = stats.get('success_count', 0)
            last_used = stats.get('last_used')
            
            print(f"  - {account}: 使用{usage_count}次, 成功{success_count}次", end="")
            if last_used:
                last_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_used))
                print(f", 最后使用: {last_time}")
            else:
                print()
    else:
        print("没有找到可用账户")
        print("请创建账户目录结构：")
        print("  mkdir accounts")
        print("  mkdir accounts/account1")
        print("  # 将每个账户的 auth_state.json 文件放到对应目录中")
    
    print("================")


def load_reply_content(reply_file_path: str = REPLY_CONTENT_FILE) -> List[str]:
    """加载回复内容列表"""
    if not os.path.exists(reply_file_path):
        print(f"回复内容文件不存在: {reply_file_path}")
        return []
    
    try:
        with open(reply_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 按行分割回复内容
        replies = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('//'):
                replies.append(line)
        
        print(f"加载了 {len(replies)} 条回复内容")
        return replies
        
    except Exception as e:
        print(f"加载回复内容失败: {e}")
        return []


def get_random_reply(reply_file_path: str = REPLY_CONTENT_FILE) -> Optional[str]:
    """随机获取一条回复内容"""
    replies = load_reply_content(reply_file_path)
    if not replies:
        return None
    
    return random.choice(replies)


def print_reply_status(reply_file_path: str = REPLY_CONTENT_FILE):
    """打印回复内容状态信息"""
    replies = load_reply_content(reply_file_path)
    
    print("=== 回复内容状态 ===")
    print(f"回复内容文件: {reply_file_path}")
    print(f"可用回复数量: {len(replies)}")
    
    if replies:
        print("回复内容示例:")
        for i, reply in enumerate(replies[:5]):
            print(f"  {i+1}. {reply}")
        if len(replies) > 5:
            print(f"  ... 还有 {len(replies) - 5} 条")
    else:
        print("没有找到可用回复内容")
        print("请创建回复内容文件：")
        print(f"  创建 {reply_file_path} 文件")
        print("  每行写入一条回复内容")
        print("  支持 # 和 // 开头的注释")
    
    print("================")


def post_comment(page, comment_text: str, *, max_retries: int = 3) -> bool:
    """在详情页发表评论"""
    try:
        print(f"准备发表评论: {comment_text}")
        
        # 查找评论框
        comment_selectors = [
            "textarea[placeholder*='评论']",
            "textarea[placeholder*='说点什么']",
            ".comment-input textarea",
            "[class*='comment'] textarea",
            "[data-testid='comment-input']"
        ]
        
        comment_input = None
        for selector in comment_selectors:
            try:
                input_elem = page.locator(selector).first
                if input_elem.count() > 0 and input_elem.is_visible():
                    comment_input = input_elem
                    print(f"找到评论框: {selector}")
                    break
            except Exception:
                continue
        
        if not comment_input:
            print("未找到评论框")
            return False
        
        # 点击评论框并输入内容
        try:
            comment_input.click(timeout=3000)
            page.wait_for_timeout(500)
            
            # 清空现有内容
            comment_input.clear(timeout=2000)
            page.wait_for_timeout(200)
            
            # 输入评论内容
            comment_input.fill(comment_text, timeout=3000)
            page.wait_for_timeout(500)
            
            print(f"已输入评论内容: {comment_text}")
            
        except Exception as e:
            print(f"输入评论内容失败: {e}")
            return False
        
        # 查找发表按钮
        post_selectors = [
            "button:has-text('发表')",
            "button:has-text('发送')",
            "button:has-text('评论')",
            ".post-button",
            "[class*='post'] button",
            "[data-testid='post-button']"
        ]
        
        post_button = None
        for selector in post_selectors:
            try:
                btn = page.locator(selector).first
                if btn.count() > 0 and btn.is_visible():
                    post_button = btn
                    print(f"找到发表按钮: {selector}")
                    break
            except Exception:
                continue
        
        if not post_button:
            print("未找到发表按钮")
            return False
        
        # 尝试发表评论
        for attempt in range(max_retries):
            try:
                print(f"尝试发表评论 (第 {attempt + 1} 次)")
                
                # 滚动到按钮位置
                try:
                    post_button.scroll_into_view_if_needed(timeout=2000)
                    page.wait_for_timeout(300)
                except:
                    pass
                
                # 点击发表按钮
                post_button.click(timeout=3000)
                page.wait_for_timeout(2000)
                
                # 检查是否发表成功
                # 方法1：检查按钮是否变为不可用
                try:
                    if not post_button.is_visible() or post_button.is_disabled():
                        print("评论发表成功 (按钮状态变化)")
                        return True
                except:
                    pass
                
                # 方法2：检查页面是否出现新评论
                try:
                    # 等待页面更新
                    page.wait_for_timeout(2000)
                    
                    # 查找是否包含我们的评论内容
                    comment_elements = page.locator(f"text={comment_text}")
                    if comment_elements.count() > 0:
                        print("评论发表成功 (内容已显示)")
                        return True
                except:
                    pass
                
                # 方法3：检查是否有成功提示
                success_indicators = [
                    "text=发表成功",
                    "text=发送成功",
                    "text=评论成功",
                    "[class*='success']",
                    "[class*='toast']"
                ]
                
                for indicator in success_indicators:
                    try:
                        elem = page.locator(indicator).first
                        if elem.count() > 0 and elem.is_visible():
                            print("评论发表成功 (成功提示)")
                            return True
                    except:
                        continue
                
                print("发表结果不确定，继续等待...")
                page.wait_for_timeout(2000)
                
            except Exception as e:
                print(f"发表评论失败 (第 {attempt + 1} 次): {e}")
                if attempt < max_retries - 1:
                    page.wait_for_timeout(1000)
                    continue
        
        print("评论发表失败")
        return False
        
    except Exception as e:
        print(f"发表评论异常: {e}")
        return False


def _is_login_page(url: str) -> bool:
    u = (url or "").lower()
    return ("login" in u) or ("passport" in u)


def _dom_looks_like_login(page) -> bool:
    try:
        # 更严格：仅识别登录相关 iframe 或明显的登录弹层容器且可见
        selectors = [
            "iframe[src*='login']",
            "iframe[src*='passport']",
            "div[class*='login']",
            "div[id*='login']",
            "div[role='dialog'] div:has-text('扫码登录')",
        ]
        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if loc.count() > 0 and loc.is_visible():
                    return True
            except Exception:
                continue
    except Exception:
        pass
    return False


def _parse_fields_token(token: str) -> Optional[Set[str]]:
    token_low = token.strip().lower()
    if token_low in {"title", "链接", "link"}:
        # 单一字段
        if token_low == "链接":
            token_low = "link"
        return {token_low}
    if token_low in {"any", "全部", "all"}:
        return {"title", "link"}
    # 逗号分隔
    parts = [p.strip().lower() for p in token_low.split(",") if p.strip()]
    valid_map = {"title": "title", "link": "link", "链接": "link"}
    fields: Set[str] = set()
    for p in parts:
        if p in valid_map:
            fields.add(valid_map[p])
    if fields:
        return fields
    return None


def read_keywords_from_file(file_path: str, default_fields: Set[str]) -> List[Tuple[Set[str], str]]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"关键词文件不存在: {file_path}")
    rules: List[Tuple[Set[str], str]] = []
    with open(file_path, "r", encoding="utf-8-sig") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith("//"):
                continue
            # 支持形如： title:旅行 | link:/explore/abc | any:美食
            # 也支持一行多个关键词用逗号分隔： title:旅行, 科技
            fields = None
            content = line
            if ":" in line:
                prefix, rest = line.split(":", 1)
                maybe_fields = _parse_fields_token(prefix)
                if maybe_fields is not None:
                    fields = maybe_fields
                    content = rest.strip()
            # 按逗号分割多个关键词
            parts = [p.strip() for p in content.split(",") if p.strip()]
            for part in parts:
                rules.append((fields or set(default_fields), part))
    # 去重（按 字段集合+小写关键词）并保持顺序
    seen: Set[str] = set()
    unique_rules: List[Tuple[Set[str], str]] = []
    for fields, kw in rules:
        key = ",".join(sorted(fields)) + "|" + kw.lower()
        if key in seen:
            continue
        seen.add(key)
        unique_rules.append((fields, kw))
    if not unique_rules:
        raise ValueError("关键词文件为空或无有效关键词")
    return unique_rules


def get_first_text(page, selectors: List[str], timeout_ms: int = 3000) -> Optional[str]:
    for css in selectors:
        try:
            loc = page.locator(css).first
            # 等待可见（若不可见也尝试读文本，避免严格阻塞）
            try:
                loc.wait_for(state="visible", timeout=timeout_ms)
            except Exception:
                pass
            text = loc.inner_text(timeout=timeout_ms).strip()
            if text:
                return text
        except Exception:
            continue
    return None


def _normalize_text(text: str, case_sensitive: bool) -> str:
    if text is None:
        return ""
    t = text.strip()
    if not case_sensitive:
        t = t.lower()
    # 折叠多余空白
    t = " ".join(t.split())
    return t


def _extract_card_texts(anchor) -> Dict[str, str]:
    # 提取卡片的标题相关文本（锚点文本 + 近邻标题/段落）
    title_texts: List[str] = []
    try:
        txt = anchor.inner_text(timeout=150)
        if txt:
            title_texts.append(txt)
    except Exception:
        pass
    # 锚点上的可读属性
    try:
        aria_label = anchor.get_attribute("aria-label")
        if aria_label:
            title_texts.append(aria_label)
    except Exception:
        pass
    try:
        title_attr = anchor.get_attribute("title")
        if title_attr:
            title_texts.append(title_attr)
    except Exception:
        pass
    container = None
    try:
        loc = anchor.locator("xpath=ancestor::article[1]").first
        if loc.count() > 0:
            container = loc
    except Exception:
        container = None
    if container is None:
        try:
            loc = anchor.locator("xpath=ancestor::div[1]").first
            if loc.count() > 0:
                container = loc
        except Exception:
            container = None
    if container is None:
        try:
            loc = anchor.locator("xpath=ancestor::li[1]").first
            if loc.count() > 0:
                container = loc
        except Exception:
            container = None
    if container is not None:
        try:
            # 常见标题/文本位置
            cand = container.locator("h1, h2, h3, [class*='title'], [title], [aria-label], p, span")
            inner = cand.all_inner_texts()
            for t in inner:
                t = (t or "").strip()
                if t:
                    title_texts.append(t)
        except Exception:
            pass
        # 提取图片 alt 文本作为可能的标题来源
        try:
            alt_values = container.locator("img[alt]").evaluate_all("els => els.map(e => e.getAttribute('alt'))")
            for t in alt_values or []:
                t = (t or "").strip()
                if t:
                    title_texts.append(t)
        except Exception:
            pass
        # 兜底抓取容器整体的内文本（避免过大）
        try:
            bulk_text = container.inner_text(timeout=200)
            bulk_text = (bulk_text or "").strip()
            if bulk_text:
                title_texts.append(bulk_text)
        except Exception:
            pass
    # 去重
    seen = set()
    merged = []
    for t in title_texts:
        if t not in seen:
            seen.add(t)
            merged.append(t)
    try:
        href = anchor.get_attribute("href") or ""
    except Exception:
        href = ""
    return {"title": " \n".join(merged), "link": href}


def _pattern_matches(value: str, pattern: str, *, use_regex: bool, exact: bool, case_sensitive: bool) -> bool:
    val = _normalize_text(value or "", case_sensitive)
    if use_regex:
        import re
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            return re.search(pattern, value or "", flags) is not None
        except re.error:
            return False
    patt = _normalize_text(pattern, case_sensitive)
    if exact:
        return val == patt
    return patt in val


def _expr_matches(value: str, expr: str, *, use_regex: bool, exact: bool, case_sensitive: bool) -> bool:
    # 支持 AND/OR： "a && b"，"a || b"
    if "&&" in expr:
        parts = [p.strip() for p in expr.split("&&") if p.strip()]
        return all(_pattern_matches(value, p, use_regex=use_regex, exact=exact, case_sensitive=case_sensitive) for p in parts)
    if "||" in expr:
        parts = [p.strip() for p in expr.split("||") if p.strip()]
        return any(_pattern_matches(value, p, use_regex=use_regex, exact=exact, case_sensitive=case_sensitive) for p in parts)
    return _pattern_matches(value, expr, use_regex=use_regex, exact=exact, case_sensitive=case_sensitive)


def wait_for_feed_ready(page, timeout_ms: int = 12000) -> bool:
    # 等待推荐流中至少出现若干卡片链接
    selectors = [
        "a[href*='/explore/']:not([href*='login']):not([href*='passport'])",
        "article:has(a[href*='/explore/']) a[href*='/explore/']",
        "div.note-item a[href*='/explore/']",
        "section:has(a[href*='/explore/']) a[href*='/explore/']",
        "div[class*='note'] a[href*='/explore/']",
    ]
    deadline = time.time() + (timeout_ms / 1000.0)
    while time.time() < deadline:
        try:
            total = 0
            for sel in selectors:
                total += page.locator(sel).count()
            if total >= 1:
                return True
        except Exception:
            pass
        page.wait_for_timeout(300)
    return False


def find_card_link_by_keywords(
    page,
    rules: List[Tuple[Set[str], str]],
    exclude_rules: Optional[List[Tuple[Set[str], str]]] = None,
    exclude_urls: Optional[Set[str]] = None,
    max_scroll_steps: int = 6,
    scroll_pause_ms: int = 800,
) -> Optional[Tuple[object, str, str]]:
    seen_hrefs = set()
    # 预处理为小写
    lowered_rules: List[Tuple[Set[str], str]] = [(fields, kw) for fields, kw in rules]
    lowered_excludes: List[Tuple[Set[str], str]] = list(exclude_rules or [])
    selector_list = [
        "a[href*='/explore/']:not([href*='login']):not([href*='passport'])",
        "article:has(a[href*='/explore/']) a[href*='/explore/']",
        "div.note-item a[href*='/explore/']",
        "section:has(a[href*='/explore/']) a[href*='/explore/']",
        "div[class*='note'] a[href*='/explore/']",
    ]
    for step_idx in range(max_scroll_steps):
        # 等待推荐流渲染一些卡片
        wait_for_feed_ready(page, timeout_ms=3000 if step_idx == 0 else 1500)
        anchors = []
        for sel in selector_list:
            try:
                anchors.extend(page.locator(sel).all())
            except Exception:
                continue
        debug_sample_printed = False
        for a in anchors:
            try:
                field_values = _extract_card_texts(a)
                href = field_values.get("link", "")
                if not href or href in seen_hrefs:
                    continue
                seen_hrefs.add(href)
            except Exception:
                continue

            # 排除规则命中则跳过该卡片
            excluded = False
            for fields, expr in lowered_excludes:
                if ("title" in fields and _expr_matches(field_values.get("title", ""), expr, use_regex=find_card_link_by_keywords.use_regex, exact=find_card_link_by_keywords.exact, case_sensitive=find_card_link_by_keywords.case_sensitive)) or (
                    "link" in fields and _expr_matches(field_values.get("link", ""), expr, use_regex=find_card_link_by_keywords.use_regex, exact=find_card_link_by_keywords.exact, case_sensitive=find_card_link_by_keywords.case_sensitive)
                ):
                    excluded = True
                    break
            
            # 检查是否在排除URL列表中
            if exclude_urls and href in exclude_urls:
                excluded = True
                
            if excluded:
                continue

            for fields, expr in lowered_rules:
                if "title" in fields and _expr_matches(field_values.get("title", ""), expr, use_regex=find_card_link_by_keywords.use_regex, exact=find_card_link_by_keywords.exact, case_sensitive=find_card_link_by_keywords.case_sensitive):
                    return a, expr, "title"
                if "link" in fields and _expr_matches(field_values.get("link", ""), expr, use_regex=find_card_link_by_keywords.use_regex, exact=find_card_link_by_keywords.exact, case_sensitive=find_card_link_by_keywords.case_sensitive):
                    return a, expr, "link"
            # 若开启调试，打印部分候选卡片的内容，便于排查选择器/文本提取
            if getattr(find_card_link_by_keywords, "debug", False) and not debug_sample_printed and step_idx == 0:
                try:
                    print("[DEBUG] 候选卡片示例（前5条）：")
                    count = 0
                    for a2 in anchors[:5]:
                        try:
                            fv = _extract_card_texts(a2)
                            print("[DEBUG] href=", fv.get("link", ""))
                            print("[DEBUG] title=", (fv.get("title", "") or "").replace("\n", " ")[:180])
                            count += 1
                        except Exception:
                            continue
                        if count >= 5:
                            break
                except Exception:
                    pass
                debug_sample_printed = True
        page.mouse.wheel(0, 2600)
        page.wait_for_timeout(scroll_pause_ms)
    return None


def ensure_home_loaded(
    page,
    timeout_ms: int = 15000,
    home_url: str = HOMEPAGE_URL,
    retries: int = 2,
    stop_if_login: bool = False,
):
    last_err = None
    for attempt in range(retries + 1):
        try:
            print(f"尝试加载首页... (第{attempt + 1}次/共{retries + 1}次)")
            page.goto(home_url, wait_until="domcontentloaded", timeout=timeout_ms)
            # 如果当前在登录页且要求停止刷新，则直接返回，不再重试
            cur = page.url.lower()
            if stop_if_login and _is_login_page(cur):
                return
            try:
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
            except PWTimeout:
                pass
            print("首页加载成功")
            return
        except Exception as e:
            last_err = e
            print(f"加载失败: {str(e)[:100]}")
            if attempt < retries:
                wait_time = (attempt + 1) * 2000  # 递增等待时间
                print(f"等待 {wait_time/1000} 秒后重试...")
                page.wait_for_timeout(wait_time)
    if last_err:
        print(f"无法加载首页，最终错误: {last_err}")
        raise last_err


def _open_card_detail(page, anchor, *, wait_timeout_ms: int = 20000):
    old_url = page.url
    tabs_page = page
    href = ""
    try:
        href = anchor.get_attribute("href") or ""
    except Exception:
        pass
    abs_href = urljoin(page.url, href) if href else None
    
    print(f"[DEBUG] 尝试访问笔记链接: {abs_href}")
    
    # 等待页面稳定
    page.wait_for_timeout(1000)
    
    # 1) 尝试多种模拟点击方式
    click_methods = [
        # 方法1: 强制点击
        lambda: anchor.click(force=True, timeout=5000),
        # 方法2: JS点击
        lambda: anchor.evaluate("element => element.click()"),
        # 方法3: 模拟用户点击
        lambda: anchor.click(button="left", delay=100, timeout=5000),
        # 方法4: 双击
        lambda: anchor.dblclick(timeout=5000),
    ]
    
    for i, method in enumerate(click_methods):
        try:
            print(f"[DEBUG] 尝试点击方法 {i+1}")
            
            # 滚动到元素位置
            try:
                anchor.scroll_into_view_if_needed(timeout=3000)
                page.wait_for_timeout(500)
            except:
                pass
            
            # 检查元素是否可见和可点击
            try:
                if not anchor.is_visible():
                    print(f"[DEBUG] 元素不可见，尝试父元素")
                    # 尝试点击父元素
                    parent = anchor.locator("..")
                    if parent.count() > 0 and parent.is_visible():
                        method_result = parent.click(force=True, timeout=3000)
                    else:
                        continue
                else:
                    method_result = method()
            except Exception as click_error:
                print(f"[DEBUG] 点击方法 {i+1} 失败: {click_error}")
                continue
            
            # 等待导航
            page.wait_for_timeout(2000)
            
            # 检查是否成功导航
            if page.url != old_url:
                print(f"[DEBUG] 同页导航成功: {page.url}")
                return page
            
            # 检查是否打开了新标签页
            try:
                pages = page.context.pages
                if len(pages) > 1:
                    new_page = pages[-1]
                    new_page.wait_for_load_state("domcontentloaded", timeout=wait_timeout_ms)
                    new_page.wait_for_timeout(2000)
                    print(f"[DEBUG] 新标签页打开成功: {new_page.url}")
                    return new_page
            except:
                pass
                
        except Exception as e:
            print(f"[DEBUG] 点击方法 {i+1} 异常: {e}")
            continue
    
    # 2) 尝试直接跳转URL（备选方案）
    if abs_href:
        try:
            print(f"[DEBUG] 尝试直接跳转URL")
            new_page = page.context.new_page()
            
            # 设置更真实的请求头
            new_page.set_extra_http_headers({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            })
            
            new_page.goto(abs_href, wait_until="domcontentloaded", timeout=wait_timeout_ms)
            
            # 等待页面完全加载
            try:
                new_page.wait_for_load_state("networkidle", timeout=15000)
            except:
                pass
            
            new_page.wait_for_timeout(3000)
            print(f"[DEBUG] 直接跳转成功: {new_page.url}")
            return new_page
            
        except Exception as e:
            print(f"[DEBUG] 直接跳转失败: {e}")
            try:
                new_page.close()
            except:
                pass
    
    # 3) 尝试在当前页面直接导航
    if abs_href:
        try:
            print(f"[DEBUG] 尝试当前页面导航")
            page.goto(abs_href, wait_until="domcontentloaded", timeout=wait_timeout_ms)
            page.wait_for_timeout(2000)
            print(f"[DEBUG] 当前页面导航成功: {page.url}")
            return page
        except Exception as e:
            print(f"[DEBUG] 当前页面导航失败: {e}")
    
    return None


def _is_note_unviewable(page) -> bool:
    try:
        # 先检查URL是否包含错误代码
        url = page.url.lower()
        if "404" in url or "error" in url or "300031" in url:
            print(f"[DEBUG] 检测到错误URL: {url}")
            return True
            
        # 等待页面完全加载后再判断
        page.wait_for_timeout(3000)
        
        # 检查页面标题
        try:
            title = page.title() or ""
            if "404" in title or "错误" in title or "无法浏览" in title:
                print(f"[DEBUG] 检测到错误页面标题: {title}")
                return True
        except:
            pass
        
        keywords = [
            "无法浏览",
            "不可浏览", 
            "不可访问",
            "无法查看",
            "内容不存在",
            "已删除",
            "违规",
            "当前笔记无法浏览",
            "暂时无法浏览",
            "笔记不存在",
            "页面不存在",
            "访问受限",
        ]
        
        # 检查页面文本内容
        page_content = ""
        try:
            page_content = page.text_content("body") or ""
        except:
            pass
            
        for k in keywords:
            if k in page_content:
                print(f"[DEBUG] 检测到错误关键词: {k}")
                return True
                
        # 检查特定的错误元素
        error_selectors = [
            ".error",
            "[class*='error']", 
            "[class*='not-found']",
            "[class*='404']",
            ".note-error",
            ".content-error",
            ".error-page",
            ".error-container"
        ]
        
        for sel in error_selectors:
            try:
                err = page.locator(sel).first
                if err.count() > 0 and err.is_visible():
                    print(f"[DEBUG] 检测到错误元素: {sel}")
                    return True
            except Exception:
                continue
                
        # 检查页面是否有正常的笔记内容
        content_indicators = [
            # 标题相关
            "h1", "h2", "[class*='title']", "[data-testid='title']",
            # 内容相关
            "[class*='content']", ".note-content", "section[class*='content']", "[data-testid='content']",
            # 作者信息
            "[class*='author']", "[class*='user']", "[data-testid='author']",
            # 互动元素
            "[class*='like']", "[class*='comment']", "[class*='collect']",
            # 图片容器
            "[class*='image']", "[class*='photo']", "[class*='img']",
        ]
        
        has_content = False
        content_details = []
        
        for sel in content_indicators:
            try:
                elements = page.locator(sel)
                if elements.count() > 0:
                    for i in range(min(elements.count(), 5)):
                        try:
                            element = elements.nth(i)
                            if element.is_visible():
                                text = element.text_content() or ""
                                if text.strip() and len(text.strip()) > 3:
                                    has_content = True
                                    content_details.append(f"{sel}: {text.strip()[:50]}")
                                    break
                        except:
                            continue
                    if has_content:
                        break
            except Exception:
                continue
        
        # 如果没有检测到内容，再检查是否有小红书特有的页面结构
        if not has_content:
            try:
                # 检查是否有小红书的主要容器
                main_selectors = ["main", ".main", "[class*='main']", "#main"]
                for sel in main_selectors:
                    try:
                        main_elem = page.locator(sel).first
                        if main_elem.count() > 0 and main_elem.is_visible():
                            main_text = main_elem.text_content() or ""
                            if len(main_text.strip()) > 10:
                                has_content = True
                                break
                    except:
                        continue
            except:
                pass
        
        if not has_content:
            print(f"[DEBUG] 页面未检测到正常内容")
            print(f"[DEBUG] 页面URL: {page.url}")
            print(f"[DEBUG] 页面标题: {page.title() or '无'}")
            return True
        else:
            print(f"[DEBUG] 检测到页面内容: {content_details[:2]}")
            
    except Exception as e:
        print(f"[DEBUG] 不可浏览检测异常: {e}")
        
    return False


def run(
    rules: List[Tuple[Set[str], str]],
    max_refresh: int,
    per_refresh_scroll_steps: int,
    refresh_interval_sec: float,
    headless: bool,
    login_timeout_sec: int,
    proxy_server: Optional[str],
    home_url: str,
    no_like: bool = False,
    enable_multi_account: bool = False,
    account_switch_interval: int = 10,
    specific_account: Optional[str] = None,
    enable_auto_reply: bool = False,
    reply_file_path: str = REPLY_CONTENT_FILE,
):
    if not rules:
        raise ValueError("至少需要一个关键词")

    # 初始化多账户支持
    current_account = None
    account_switch_count = 0
    
    if enable_multi_account:
        # 设置账户目录
        setup_accounts_directory()
        
        # 打印账户状态
        print_account_status()
        
        # 获取可用账户
        available_accounts = get_available_accounts()
        if not available_accounts:
            print("警告：未找到可用账户，将使用单账户模式")
            enable_multi_account = False
        else:
            # 选择账户
            if specific_account and specific_account in available_accounts:
                current_account = specific_account
                print(f"使用指定账户: {current_account}")
            else:
                current_account = get_next_account()
                print(f"选择账户: {current_account}")

    with sync_playwright() as p:
        # 优先尝试系统 Chrome，不可用则回退到内置 Chromium
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-ipc-flooding-protection",
            "--enable-automation",
            "--start-maximized",
        ]
        launch_kwargs = {"headless": headless, "args": launch_args}
        if proxy_server:
            launch_kwargs["proxy"] = {"server": proxy_server}
        try:
            browser = p.chromium.launch(channel="chrome", **launch_kwargs)
        except Exception:
            browser = p.chromium.launch(**launch_kwargs)
        
        # 根据是否启用多账户选择认证文件
        auth_path = AUTH_STATE_PATH
        if enable_multi_account and current_account:
            auth_path = get_account_auth_path(current_account)
            print(f"使用账户认证文件: {auth_path}")
        
        context = (
            browser.new_context(
                storage_state=auth_path,
                locale="zh-CN",
                timezone_id="Asia/Shanghai",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1366, "height": 900},
                ignore_https_errors=True,
            )
            if os.path.exists(auth_path)
            else browser.new_context(
                locale="zh-CN",
                timezone_id="Asia/Shanghai",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1366, "height": 900},
                ignore_https_errors=True,
            )
        )
        page = context.new_page()
        # 首次进入首页：若跳转到登录页，则不进行任何刷新或重试，等待用户登录
        ensure_home_loaded(page, home_url=home_url, stop_if_login=True)

        if _is_login_page(page.url) or _dom_looks_like_login(page):
            print(f"检测到登录页，请在打开的浏览器中完成扫码/登录（最多等待 {login_timeout_sec} 秒）…")
            deadline = time.time() + max(5, int(login_timeout_sec))
            logged_in = False
            while time.time() < deadline:
                if (not _is_login_page(page.url)) and (not _dom_looks_like_login(page)):
                    logged_in = True
                    break
                # 不刷新，不跳转，仅等待
                page.wait_for_timeout(1000)
            if not logged_in:
                print("登录超时，退出。")
                context.storage_state(path=AUTH_STATE_PATH)
                context.close()
                browser.close()
                return
            # 登录成功后，确保跳转到首页
            ensure_home_loaded(page, home_url=home_url)

        matched = None
        matched_keyword = None
        matched_field = None
        excluded_urls = set()  # 记录已经访问过的不可浏览链接
        visited_urls = set()   # 记录已经访问过的链接
        # 关键词匹配配置（可扩展为参数）
        find_card_link_by_keywords.use_regex = False
        find_card_link_by_keywords.exact = False
        find_card_link_by_keywords.case_sensitive = False

        search_attempts = 0
        max_search_attempts = max_refresh * 2  # 增加搜索次数
        
        while search_attempts < max_search_attempts and not matched:
            # 检查是否需要切换账户
            if enable_multi_account and account_switch_count > 0 and account_switch_count % account_switch_interval == 0:
                print(f"已进行 {account_switch_count} 次搜索，准备切换账户...")
                
                # 获取下一个账户
                next_account = get_next_account(current_account)
                if next_account and next_account != current_account:
                    print(f"切换到账户: {next_account}")
                    
                    # 关闭当前context
                    try:
                        context.storage_state(path=auth_path)
                        context.close()
                    except:
                        pass
                    
                    # 切换账户
                    current_account = next_account
                    auth_path = get_account_auth_path(current_account)
                    print(f"使用新的认证文件: {auth_path}")
                    
                    # 创建新的context
                    context = (
                        browser.new_context(
                            storage_state=auth_path,
                            locale="zh-CN",
                            timezone_id="Asia/Shanghai",
                            user_agent=(
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
                            ),
                            viewport={"width": 1366, "height": 900},
                            ignore_https_errors=True,
                        )
                        if os.path.exists(auth_path)
                        else browser.new_context(
                            locale="zh-CN",
                            timezone_id="Asia/Shanghai",
                            user_agent=(
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
                            ),
                            viewport={"width": 1366, "height": 900},
                            ignore_https_errors=True,
                        )
                    )
                    page = context.new_page()
                    
                    # 重新加载首页
                    ensure_home_loaded(page, home_url=home_url, stop_if_login=True)
                    
                    # 重置搜索状态
                    search_attempts = 0
                    account_switch_count = 0
                    excluded_urls.clear()
                    visited_urls.clear()
                    
                    print(f"账户切换完成，继续搜索...")
                    continue
                else:
                    print("没有其他可切换的账户，继续使用当前账户")
            search_attempts += 1
            # 若中途仍处于登录页，暂停查找与刷新，仅等待登录完成
            if _is_login_page(page.url) or _dom_looks_like_login(page):
                print("检测到仍在登录页，暂停刷新与查找，等待扫码完成…")
                deadline = time.time() + max(2, int(refresh_interval_sec))
                while time.time() < deadline:
                    if (not _is_login_page(page.url)) and (not _dom_looks_like_login(page)):
                        break
                    page.wait_for_timeout(500)
                # 登录完成后确保跳回首页
                if (not _is_login_page(page.url)) and (not _dom_looks_like_login(page)):
                    try:
                        ensure_home_loaded(page, home_url=home_url)
                    except Exception:
                        pass
                # 进入下一轮重试（不会触发刷新分支）
                continue
            print(f"第 {search_attempts}/{max_search_attempts} 轮：在首页查找关键词规则 …")
            res = find_card_link_by_keywords(
                page,
                rules,
                exclude_urls=visited_urls,
                max_scroll_steps=per_refresh_scroll_steps,
            )
            if res:
                matched, matched_keyword, matched_field = res
                break
            # 如果处于登录页，严格不刷新，直接继续等待下一轮
            if _is_login_page(page.url):
                page.wait_for_timeout(int(max(0.2, refresh_interval_sec) * 1000))
                continue
                
            # 如果没有找到匹配的，刷新页面
            if not matched:
                # 增加账户切换计数
                if enable_multi_account:
                    account_switch_count += 1
                
                try:
                    page.reload(wait_until="domcontentloaded", timeout=20000)
                    try:
                        page.wait_for_load_state("networkidle", timeout=6000)
                    except PWTimeout:
                        pass
                except Exception:
                    # 若异常且不是登录页，再尝试回到首页
                    if not _is_login_page(page.url):
                        ensure_home_loaded(page, home_url=home_url)
                time.sleep(refresh_interval_sec)

  # 处理找到的匹配结果
        if matched:
            print(f"已命中关键词：{matched_keyword}（字段：{matched_field}），尝试进入详情…")
            try:
                href_dbg = matched.get_attribute("href")
                if href_dbg:
                    print("命中卡片 href:", href_dbg)
            except Exception:
                pass
            detail_page = _open_card_detail(page, matched, wait_timeout_ms=20000)
            if detail_page is None:
                print("进入详情失败：未能完成跳转。")
                # 重置匹配状态，继续搜索
                matched = None
                # 跳过当前循环的其余部分，直接进入下一轮
                pass
            else:
                try:
                    detail_page.wait_for_load_state("networkidle", timeout=8000)
                except PWTimeout:
                    pass

                # 检测不可浏览则记录并跳过
                if _is_note_unviewable(detail_page):
                    try:
                        bad_url = detail_page.url
                        # 将不可浏览的URL加入排除列表
                        if bad_url:
                            visited_urls.add(bad_url)
                            excluded_urls.add(bad_url)
                    except Exception:
                        bad_url = ""
                    print("检测到当前笔记不可浏览，跳过：", bad_url)
                    
                    # 关闭当前详情页
                    try:
                        detail_page.close()
                    except:
                        pass
                        
                    # 等待一段时间再继续搜索，避免频率过高
                    print("等待5秒后继续搜索其他笔记...")
                    time.sleep(5)
                    
                    # 返回首页继续搜索
                    try:
                        home_url_final = home_url or HOMEPAGE_URL
                        ensure_home_loaded(page, home_url=home_url_final)
                    except Exception:
                        pass
                        
                    print("继续搜索其他匹配的笔记...")
                    # 重置匹配状态，继续搜索
                    matched = None
                    matched_keyword = None
                    matched_field = None
                else:
                    # 只有当笔记可浏览时才提取详情
                    title = get_first_text(detail_page, ["h1", "h1[class*='title']", "div[class*='title'] h1"])
                    author = get_first_text(detail_page, ["a[href*='/user/']", "span[class*='name']", "div[class*='author'] a"])
                    content = get_first_text(detail_page, ["div[class*='content']", "section[class*='content']", "div.note-content"])
                    like = get_first_text(detail_page, ["[class*='like'] span", "button[aria-label*='赞'] span"])
                    comment = get_first_text(detail_page, ["[class*='comment'] span", "button[aria-label*='评'] span"])
                    collect = get_first_text(detail_page, ["[class*='collect'] span", "button[aria-label*='藏'] span"])

                    print("详情页URL:", detail_page.url)
                    print("标题:", title or "")
                    print("作者:", author or "")
                    print("正文预览:", (content or "")[:200])
                    print("点赞:", like or "")
                    print("评论:", comment or "")
                    print("收藏:", collect or "")

                    # 将成功访问的URL加入已访问列表
                    try:
                        success_url = detail_page.url
                        if success_url:
                            visited_urls.add(success_url)
                    except Exception:
                        pass
                    
                    # 检查是否已点赞，未点赞则进行点赞（除非禁用了点赞功能）
                    is_liked = False
                    if not no_like:
                        print("检查点赞状态...")
                        try:
                            # 查找点赞按钮
                            like_button_selectors = [
                                "button[aria-label*='赞']",
                                "button[class*='like']",
                                "[data-testid='like-button']",
                                ".like-button",
                                "button:has-text('赞')"
                            ]
                            
                            like_button = None
                            for selector in like_button_selectors:
                                try:
                                    btn = detail_page.locator(selector).first
                                    if btn.count() > 0 and btn.is_visible():
                                        like_button = btn
                                        print(f"找到点赞按钮: {selector}")
                                        break
                                except Exception:
                                    continue
                            
                            if like_button:
                                # 检查是否已点赞
                                try:
                                    # 检查按钮的激活状态或文本
                                    button_text = like_button.text_content() or ""
                                    if "已赞" in button_text or like_button.get_attribute("aria-pressed") == "true":
                                        is_liked = True
                                        print("笔记已点赞")
                                    else:
                                        print("笔记未点赞，准备点赞...")
                                        
                                        # 等待一下再点击
                                        detail_page.wait_for_timeout(1000)
                                        
                                        # 尝试多种点击方式
                                        click_methods = [
                                            lambda: like_button.click(timeout=3000),
                                            lambda: like_button.click(force=True, timeout=3000),
                                            lambda: like_button.evaluate("el => el.click()"),
                                            lambda: like_button.click(delay=100, timeout=3000)
                                        ]
                                        
                                        for i, method in enumerate(click_methods):
                                            try:
                                                method()
                                                print(f"点赞方法 {i+1} 执行成功")
                                                is_liked = True
                                                break
                                            except Exception as click_error:
                                                print(f"点赞方法 {i+1} 失败: {click_error}")
                                                continue
                                        
                                        if is_liked:
                                            print("✅ 点赞成功！")
                                            # 等待点赞完成
                                            detail_page.wait_for_timeout(2000)
                                        else:
                                            print("❌ 点赞失败")
                                except Exception as e:
                                    print(f"检查点赞状态异常: {e}")
                            else:
                                print("未找到点赞按钮")
                                
                        except Exception as e:
                            print(f"点赞功能异常: {e}")
                    else:
                        print("已禁用自动点赞功能")
                    
                    # 如果已点赞且启用了自动回复功能，则进行评论
                    if is_liked and enable_auto_reply:
                        print("检测到已点赞，准备自动回复...")
                        
                        # 获取随机回复内容
                        reply_content = get_random_reply(reply_file_path)
                        if reply_content:
                            print(f"随机获取回复内容: {reply_content}")
                            
                            # 等待一下再进行评论
                            detail_page.wait_for_timeout(2000)
                            
                            # 发表评论
                            reply_success = post_comment(detail_page, reply_content)
                            if reply_success:
                                print("✅ 自动回复成功！")
                            else:
                                print("❌ 自动回复失败")
                        else:
                            print("未找到可用回复内容，跳过自动回复")
                    elif is_liked:
                        print("笔记已点赞，但自动回复功能未启用")
                        
                    detail_page.screenshot(path="detail_snapshot.png", full_page=True)
                    
                    # 保存认证状态
                    context.storage_state(path=auth_path)
                    
                    # 记录账户使用情况
                    if enable_multi_account and current_account:
                        record_account_usage(current_account, success=True)
                        print(f"账户 {current_account} 使用成功")
                    
                    context.close()
                    browser.close()
                    return  # 成功找到并访问了可浏览的笔记，退出程序

        # 如果没有找到匹配的，刷新页面
        if not matched:
            try:
                page.reload(wait_until="domcontentloaded", timeout=20000)
                try:
                    page.wait_for_load_state("networkidle", timeout=6000)
                except PWTimeout:
                    pass
            except Exception:
                # 若异常且不是登录页，再尝试回到首页
                if not _is_login_page(page.url):
                    ensure_home_loaded(page, home_url=home_url)
            time.sleep(refresh_interval_sec)

    # 循环结束，未找到可浏览的笔记
    print(f"未找到任何可浏览的关键词对应卡片（搜索次数={search_attempts}）")
    
    # 保存认证状态
    context.storage_state(path=auth_path)
    
    # 记录账户使用情况（失败）
    if enable_multi_account and current_account:
        record_account_usage(current_account, success=False)
        print(f"账户 {current_account} 使用失败")
    
    context.close()
    browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="在小红书首页查找多关键词的卡片，未找到则刷新直至命中并进入详情"
    )
    parser.add_argument(
        "--keyword",
        action="append",
        help="匹配卡片标题的关键词（可多次提供该参数叠加多个关键词，大小写不敏感，包含匹配）",
    )
    parser.add_argument(
        "--keywords-file",
        help="从文件读取关键词（逐行，支持以 # 开头注释；一行多个可用逗号分隔）。未提供且当前目录存在 keywords.txt 时将自动读取该文件",
    )
    parser.add_argument(
        "--match-fields",
        default="title",
        help="默认匹配字段，逗号分隔，可选：title, link, any",
    )
    parser.add_argument(
        "--regex",
        action="store_true",
        help="将关键词作为正则表达式匹配（默认按子串匹配）",
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="使用精确匹配（默认为包含匹配）",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="区分大小写（默认不区分）",
    )
    parser.add_argument("--max-refresh", type=int, default=30, help="最大刷新次数")
    parser.add_argument(
        "--scroll-steps", type=int, default=6, help="每轮刷新内的最大滚动步数"
    )
    parser.add_argument(
        "--interval", type=float, default=3.0, help="每次刷新之间的间隔秒数"
    )
    parser.add_argument("--headless", action="store_true", help="无头模式运行")
    parser.add_argument("--login-timeout", type=int, default=180, help="登录等待超时时间（秒）")
    parser.add_argument("--proxy", help="可选代理，如 http://127.0.0.1:7890 或 socks5://127.0.0.1:1080")
    parser.add_argument("--home-url", default=HOMEPAGE_URL, help="首页 URL（如被墙可改为镜像域名）")
    parser.add_argument("--debug", action="store_true", help="调试模式：打印候选卡片示例文本，便于排查")
    parser.add_argument("--no-like", action="store_true", help="禁用自动点赞功能")
    parser.add_argument("--multi-account", action="store_true", help="启用多账户轮流登录模式")
    parser.add_argument("--account-switch-interval", type=int, default=10, help="多账户模式下，每隔多少次搜索切换账户（默认：10次）")
    parser.add_argument("--account", help="指定使用特定账户（仅在多账户模式下有效）")
    parser.add_argument("--account-status", action="store_true", help="显示账户状态信息并退出")
    parser.add_argument("--auto-reply", action="store_true", help="启用自动回复功能（当发现已点赞时自动评论）")
    parser.add_argument("--reply-file", default=REPLY_CONTENT_FILE, help="回复内容文件路径（默认：reply_content.txt）")
    parser.add_argument("--reply-status", action="store_true", help="显示回复内容状态信息并退出")

    args = parser.parse_args()

    # 如果只是查看账户状态，显示后退出
    if args.account_status:
        setup_accounts_directory()
        print_account_status()
        exit(0)
    
    # 如果只是查看回复状态，显示后退出
    if args.reply_status:
        print_reply_status(args.reply_file)
        exit(0)

    # 解析默认字段
    default_fields = _parse_fields_token(args.match_fields) or {"title"}

    rules: List[Tuple[Set[str], str]] = []
    # 若未指定 --keywords-file 与 --keyword，则默认读取当前目录 keywords.txt（若存在）
    if not args.keywords_file and not args.keyword:
        default_path = os.path.join(os.getcwd(), "keywords.txt")
        if os.path.exists(default_path):
            args.keywords_file = default_path

    if args.keywords_file:
        rules.extend(read_keywords_from_file(args.keywords_file, default_fields))
    if args.keyword:
        # 命令行提供的关键词使用默认字段集合
        for kw in args.keyword:
            k = (kw or "").strip()
            if not k:
                continue
            rules.append((set(default_fields), k))
    # 去重
    if rules:
        seen_keys: Set[str] = set()
        uniq_rules: List[Tuple[Set[str], str]] = []
        for fset, kw in rules:
            key = ",".join(sorted(fset)) + "|" + kw.lower()
            if key in seen_keys:
                continue
            seen_keys.add(key)
            uniq_rules.append((fset, kw))
        rules = uniq_rules

    # 将匹配配置注入到查找函数的属性上
    find_card_link_by_keywords.use_regex = bool(args.regex)
    find_card_link_by_keywords.exact = bool(args.exact)
    find_card_link_by_keywords.case_sensitive = bool(args.case_sensitive)
    find_card_link_by_keywords.debug = bool(args.debug)

    run(
        rules=rules,
        max_refresh=args.max_refresh,
        per_refresh_scroll_steps=args.scroll_steps,
        refresh_interval_sec=args.interval,
        headless=args.headless,
        login_timeout_sec=args.login_timeout,
        proxy_server=args.proxy,
        home_url=args.home_url,
        no_like=args.no_like,
        enable_multi_account=args.multi_account,
        account_switch_interval=args.account_switch_interval,
        specific_account=args.account,
        enable_auto_reply=args.auto_reply,
        reply_file_path=args.reply_file,
    )


