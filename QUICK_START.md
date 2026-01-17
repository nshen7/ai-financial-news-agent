# Quick Start Guide - Financial News Summarization

## 🚀 Quick Setup (30 seconds)

1. **Get FREE Google Gemini API key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in and click "Create API Key"

2. **Add your API keys to `.env`:**
```bash
GOOGLE_API_KEY=your-gemini-api-key-here
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key-here
```

3. **Install dependencies:**
```bash
poetry install
```

4. **Run a test:**
```bash
python test_summary.py
```

## 📊 Quick Usage Examples

### One-Liner: Full Analysis
```python
from aifn.src.summary import summarize_financial_data
from aifn.src.crawler import crawl_stock_news, crawl_stock_daily_time_series, crawl_market_news

result = summarize_financial_data(
    "AAPL",
    crawl_stock_news("AAPL", num_articles=5),
    crawl_stock_daily_time_series("AAPL"),
    crawl_market_news(num_articles=3)
)
print(result['final_summary'])
```

### Simple News Summary
```python
from aifn.src.summary import summarize_news_only
from aifn.src.crawler import crawl_stock_news

summary = summarize_news_only(crawl_stock_news("AAPL", 5), "AAPL")
print(summary)
```

## 🎯 What You Get

### Comprehensive Summary Output:
- ✅ **Executive Summary** - Quick overview
- ✅ **News Analysis** - Sentiment & key themes
- ✅ **Price Analysis** - Technical indicators
- ✅ **Market Context** - Broader trends
- ✅ **Key Takeaways** - Actionable insights

### Simple News Summary Output:
- ✅ **Key Themes** - Main topics
- ✅ **Sentiment Analysis** - Market mood
- ✅ **Important Events** - Critical updates
- ✅ **Impact Assessment** - Market implications

## 🔧 Test Commands

```bash
# Full comprehensive analysis
python test_summary.py 1

# News-only quick summary
python test_summary.py 2

# Test data formatting
python test_summary.py 3
```

## 💡 Pro Tips

1. **More articles = Better analysis**
   - Recommended: 5-10 articles per query

2. **Always include market context**
   - Provides broader perspective
   - Helps contextualize stock movements

3. **Use appropriate model**
   - `gemini-1.5-flash`: Fast & FREE (default, T4 optimized)
   - `gemini-1.5-pro`: More powerful analysis

4. **Watch API limits**
   - Alpha Vantage: 25 requests/day (free)
   - Gemini: 60 requests/min, 1500/day (FREE tier)

## 📦 What's Included

- `summary.py` - Main summarization module with LangGraph workflow (uses Gemini)
- `test_summary.py` - Test suite with 3 test modes
- `SUMMARY_USAGE.md` - Detailed documentation
- `GEMINI_SETUP.md` - **Google Gemini setup guide** ⭐
- `QUICK_START.md` - This file

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "GOOGLE_API_KEY not found" | Add Gemini key to `.env` file |
| Import errors | Run `poetry install` |
| Rate limits (429 error) | Wait 1 minute, limits reset |
| Slow responses | Already using fastest model (flash) |

## 📚 Next Steps

1. **NEW:** Read [GEMINI_SETUP.md](GEMINI_SETUP.md) for Gemini-specific info ⭐
2. Read [SUMMARY_USAGE.md](SUMMARY_USAGE.md) for detailed docs
3. Check [crawler.py](aifn/src/crawler.py) for data fetching options
4. Customize prompts in [summary.py](aifn/src/summary.py)
5. Integrate into your main workflow

---

**Need help?** Check [GEMINI_SETUP.md](GEMINI_SETUP.md) for Gemini setup or [SUMMARY_USAGE.md](SUMMARY_USAGE.md) for usage docs
