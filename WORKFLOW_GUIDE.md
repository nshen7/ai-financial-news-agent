# AI Financial News Agent - Workflow Guide

## Overview

Your financial news agent now has two complementary workflows:

1. **Daily Analysis** - Quick daily summary of news, price, and market context
2. **Periodic Reflection** - Deep analysis of patterns and trends over time (weekly/monthly)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY WORKFLOW                            │
│  (Run every day, saves to RAG for historical tracking)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  1. Fetch Data            │
              │  - Stock news             │
              │  - Price data             │
              │  - Market context         │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  2. LangGraph Analysis    │
              │  - News summary           │
              │  - Price analysis         │
              │  - Market context         │
              │  - Final synthesis        │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  3. Save to RAG           │
              │  ChromaDB with metadata   │
              └───────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  PERIODIC REFLECTION                         │
│  (Run weekly/monthly to identify patterns)                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  1. Retrieve History      │
              │  Get all daily analyses   │
              │  from RAG for period      │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  2. Deep Reflection       │
              │  - Pattern analysis       │
              │  - Sentiment evolution    │
              │  - Key events             │
              │  - Investment thesis      │
              │  - Risk assessment        │
              └───────────────────────────┘
                              ↓
              ┌───────────────────────────┐
              │  3. Save Reflection       │
              │  Store as special type    │
              └───────────────────────────┘
```

## Usage Examples

### 1. Daily Analysis

Run this every day to track a stock:

```bash
# Basic daily analysis
poetry run python -m aifn.main NVDA

# With custom article count
poetry run python -m aifn.main AAPL --num-articles 100

# Don't save to RAG (just view analysis)
poetry run python -m aifn.main TSLA --no-save
```

**Output:**
- Comprehensive analysis combining news, price, and market context
- Detailed breakdowns of each component
- Automatically saved to RAG database for future reflection

### 2. Weekly Reflection

Run this at the end of each week:

```bash
# Weekly reflection (analyzes last 7 days)
poetry run python -m aifn.main NVDA --reflect week

# Monthly reflection (analyzes last 30 days)
poetry run python -m aifn.main NVDA --reflect month

# Quarterly reflection (analyzes last 90 days)
poetry run python -m aifn.main NVDA --reflect quarter

# Custom period (last 14 days)
poetry run python -m aifn.main NVDA --reflect week --days 14
```

**Output:**
- Pattern analysis across the period
- How sentiment evolved over time
- 3-5 most significant events
- Updated investment thesis (bull/bear cases)
- Risk assessment with likelihood ratings

### 3. Search Historical Analyses

Find similar past events or patterns:

```bash
# Search for similar price movements
poetry run python -m aifn.main NVDA --search "price drops after earnings"

# Search for sentiment patterns
poetry run python -m aifn.main AAPL --search "bullish sentiment during Fed announcements"

# Limit results
poetry run python -m aifn.main TSLA --search "production concerns" --limit 3
```

**Output:**
- Most similar historical analyses
- Similarity scores
- Dates and context

## Workflow Comparison with AI-Q Research Assistant

| Feature | AI-Q Research | Your Financial Agent |
|---------|--------------|---------------------|
| **Main Use Case** | One-time deep research reports | Daily tracking + periodic reflection |
| **Frequency** | On-demand | Daily + Weekly/Monthly |
| **Query Generation** | Automated from topic | Pre-defined (news, price, market) |
| **Reflection** | Built into report generation | Separate periodic analysis |
| **Historical Context** | RAG documents | Past daily analyses |
| **Output** | Single comprehensive report | Daily summaries + periodic synthesis |
| **Time Horizon** | Point-in-time analysis | Trend tracking over time |

## Key Differences from Original Proposal

### What Changed (Based on Your Feedback):

1. **Separated Daily from Reflection** - Instead of adding reflection to daily workflow, created two independent workflows
2. **Simplified Structure** - Kept your existing file organization (no major refactoring)
3. **Added Periodic Reflection Function** - New `reflect_on_period()` in summary.py analyzes multiple days at once

### What We Added:

**In `summary.py`:**
- `reflect_on_period()` - Analyzes historical summaries to identify patterns, sentiment evolution, key events, investment thesis, and risks

**In `rag.py`:**
- `search_historical_analyses()` - Semantic search across past analyses
- `get_period_summaries()` - Retrieve all analyses for a date range

**In `main.py`:**
- `daily_analysis()` - Run daily workflow
- `periodic_reflection()` - Run weekly/monthly reflection
- `search_history()` - Search past analyses
- Full CLI with argument parsing

## Recommended Workflow

### Daily (Monday-Friday):
```bash
# Morning: Analyze your watchlist
poetry run python -m aifn.main NVDA
poetry run python -m aifn.main AAPL
poetry run python -m aifn.main TSLA
```

### Weekly (Friday afternoon):
```bash
# Reflect on the week's patterns
poetry run python -m aifn.main NVDA --reflect week
poetry run python -m aifn.main AAPL --reflect week
```

### Monthly (End of month):
```bash
# Deep monthly reflection
poetry run python -m aifn.main NVDA --reflect month
```

### Ad-hoc (When needed):
```bash
# Search for similar historical events
poetry run python -m aifn.main NVDA --search "similar earnings reactions"
```

## RAG Database

Your analyses are stored in `./chroma_db` with metadata:

**Daily analyses include:**
- Date
- Ticker
- Number of articles analyzed
- Analysis type: "daily"

**Periodic reflections include:**
- Date range (start/end)
- Ticker
- Number of days analyzed
- Analysis type: "reflection_week", "reflection_month", "reflection_quarter"

This allows you to:
1. Track how your understanding evolved over time
2. Search for similar past situations
3. Build institutional knowledge about each stock

## Next Steps

1. **Test Daily Analysis:**
   ```bash
   poetry run python -m aifn.main NVDA
   ```

2. **Run for a few days** to build historical data

3. **Test Weekly Reflection:**
   ```bash
   poetry run python -m aifn.main NVDA --reflect week
   ```

4. **Test Historical Search:**
   ```bash
   poetry run python -m aifn.main NVDA --search "your query here"
   ```

## Tips

- Run daily analysis with `--no-save` to test without polluting your RAG database
- Weekly reflections require at least a few days of historical data
- The more daily analyses you have, the better the periodic reflections
- Use specific search queries for better historical search results
- Consider setting up a cron job or scheduled task for automated daily runs

## File Changes Summary

✅ **Enhanced (minimal changes):**
- `summary.py` - Added `reflect_on_period()` function (~170 lines)
- `rag.py` - Added search functions (~120 lines)
- `main.py` - Full CLI implementation (~345 lines)

✅ **No breaking changes** to existing functions
✅ **Backwards compatible** with your existing code
✅ **Total additions**: ~635 lines across 3 files
