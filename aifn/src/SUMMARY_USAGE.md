# AI Financial News Agent - Complete Usage Guide

This module provides AI-powered financial analysis with daily summaries, periodic reflection, and historical search capabilities using LangChain and LangGraph.

## Features

### 1. **Daily Financial Analysis**
Complete daily analysis workflow using LangGraph state machine:
- **News Summarization**: Analyzes news articles for themes, sentiment, and catalysts
- **Price Analysis**: Technical analysis of price movements and volume
- **Market Context**: Broader market and macroeconomic trends
- **Final Synthesis**: Comprehensive investment research report

### 2. **Periodic Reflection** (NEW!)
Deep analysis of historical patterns over time:
- **Pattern Recognition**: Identify recurring themes and trend changes
- **Sentiment Evolution**: Track how sentiment shifted over the period
- **Key Events**: Rank the most significant events and their impact
- **Investment Thesis**: Generate bull/bear cases with recommendations
- **Risk Assessment**: Comprehensive risk analysis with mitigation strategies

### 3. **Historical Search**
Semantic search across past analyses to find similar events and patterns.

### 4. **RAG Integration**
All analyses are automatically stored in ChromaDB for:
- Building historical context
- Periodic reflection analysis
- Pattern matching and trend identification

## Setup

### Required Environment Variables

Add to your `.env` file:
```bash
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

**Get your API keys:**
- Alpha Vantage (free): https://www.alphavantage.co/support/#api-key
- Google Gemini (free): https://makersuite.google.com/app/apikey

### Dependencies

All dependencies are in `pyproject.toml`:
- `langchain` - LangChain core
- `langchain-google-genai` - Google Gemini integration
- `langgraph` - Graph-based workflows
- `chromadb` - Vector database for RAG
- `python-dotenv` - Environment variables

Install with:
```bash
poetry install
```

## Quick Start

### Command Line Interface (Recommended)

The easiest way to use the agent is through the CLI:

```bash
# Daily analysis for a ticker
poetry run python -m aifn.main NVDA

# Weekly reflection for a ticker
poetry run python -m aifn.main NVDA --reflect week

# Portfolio-wide reflection (all tickers)
poetry run python -m aifn.main --reflect week

# Search historical analyses
poetry run python -m aifn.main NVDA --search "earnings surprises"
```

### Python API

You can also use the functions directly in your code:

```python
from aifn.src.crawler import crawl_stock_news, crawl_stock_daily_time_series, crawl_market_news
from aifn.src.summary import summarize_financial_data, reflect_on_period
from aifn.src.rag import store_embedding, get_period_summaries
```

## Usage Examples

### Example 1: Daily Comprehensive Analysis

**CLI:**
```bash
poetry run python -m aifn.main AAPL
```

**Python:**
```python
from aifn.src.crawler import crawl_stock_news, crawl_stock_daily_time_series, crawl_market_news
from aifn.src.summary import summarize_financial_data
from aifn.src.rag import store_embedding
from datetime import datetime

# Fetch data
ticker = "AAPL"
news_articles = crawl_stock_news(ticker, num_articles=50)
time_series_data = crawl_stock_daily_time_series(ticker)
market_news = crawl_market_news(num_articles=20, topics=['economy_macro', 'technology'])

# Generate comprehensive summary using LangGraph
summary = summarize_financial_data(
    ticker=ticker,
    news_articles=news_articles,
    time_series_data=time_series_data,
    market_news=market_news
)

# Access different components
print(summary['final_summary'])    # Comprehensive report
print(summary['news_summary'])     # News analysis
print(summary['price_analysis'])   # Technical analysis
print(summary['market_context'])   # Market overview

# Save to RAG for future reflection
store_embedding(
    summary=summary['final_summary'],
    date=datetime.now().strftime('%Y-%m-%d'),
    ticker=ticker,
    additional_metadata={'analysis_type': 'daily'}
)
```

**Output includes:**
- Executive summary of current situation
- News highlights with sentiment analysis
- Technical analysis of price movements
- Market context and macro factors
- Key takeaways and considerations

### Example 2: Weekly Reflection on Single Ticker

**CLI:**
```bash
poetry run python -m aifn.main NVDA --reflect week
```

**Python:**
```python
from aifn.src.rag import get_period_summaries
from aifn.src.summary import reflect_on_period
from datetime import datetime, timedelta

# Define period
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# Retrieve historical summaries from RAG
summaries = get_period_summaries(
    start_date=start_date,
    end_date=end_date,
    ticker="NVDA"
)

# Run periodic reflection
reflection = reflect_on_period(
    period_summaries=summaries,
    ticker="NVDA",
    period_type="week"
)

# Access reflection components
print(reflection['period_info'])          # Actual date range analyzed
print(reflection['pattern_analysis'])     # Recurring patterns
print(reflection['sentiment_evolution'])  # Sentiment timeline
print(reflection['key_events'])           # Most significant events
print(reflection['investment_thesis'])    # Bull/bear cases
print(reflection['risk_assessment'])      # Risk analysis
```

**Output includes:**
- Exact date range and trading days analyzed
- Pattern analysis with specific dates
- Sentiment evolution timeline
- 3-5 most significant events ranked by importance
- Investment thesis with bull/bear cases
- Comprehensive risk assessment

### Example 3: Portfolio-Wide Reflection (Multiple Tickers)

**CLI:**
```bash
# After running daily analyses for NVDA, AAPL, TSLA for a week
poetry run python -m aifn.main --reflect week
```

**Python:**
```python
from aifn.src.rag import get_period_summaries
from aifn.src.summary import reflect_on_period
from datetime import datetime, timedelta

# Define period
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# Retrieve ALL tickers' summaries from RAG
summaries = get_period_summaries(
    start_date=start_date,
    end_date=end_date,
    ticker=None  # None = all tickers
)

# Run portfolio-wide reflection
reflection = reflect_on_period(
    period_summaries=summaries,
    ticker=None,  # None = portfolio mode
    period_type="week"
)

# Analyzes patterns across all tickers
print(reflection['pattern_analysis'])  # Cross-ticker patterns
print(reflection['investment_thesis']) # Portfolio-level thesis
```

**Use cases:**
- Weekly portfolio review
- Cross-ticker correlation analysis
- Portfolio-level risk assessment
- Sector rotation identification

### Example 4: News-Only Quick Summary

```python
from aifn.src.crawler import crawl_stock_news
from aifn.src.summary import summarize_news_only

# Fetch and summarize news quickly
news_articles = crawl_stock_news("TSLA", num_articles=10)
summary = summarize_news_only(news_articles, ticker="TSLA")
print(summary)
```

**When to use:**
- Quick news check without full analysis
- Breaking news situations
- Testing the system

### Example 5: Historical Pattern Search

**CLI:**
```bash
poetry run python -m aifn.main NVDA --search "price drops after earnings"
poetry run python -m aifn.main AAPL --search "Fed rate decision impact" --limit 3
```

**Python:**
```python
from aifn.src.rag import search_historical_analyses

# Search for similar past events
results = search_historical_analyses(
    query="similar earnings surprises",
    ticker="NVDA",
    k=5
)

for result in results:
    print(f"Date: {result['metadata']['date']}")
    print(f"Similarity: {result['score']:.3f}")
    print(f"Content: {result['content'][:200]}...")
```

**Use cases:**
- Find similar historical events
- Learn from past market reactions
- Pattern matching for trading strategies

## CLI Reference

### Daily Analysis

```bash
# Basic daily analysis
python -m aifn.main <ticker>

# With options
python -m aifn.main NVDA --num-articles 100
python -m aifn.main AAPL --no-save  # Don't save to RAG
```

**Options:**
- `--num-articles <n>`: Number of news articles (default: 50)
- `--no-save`: Don't save to RAG database

### Periodic Reflection

```bash
# Single ticker reflection
python -m aifn.main <ticker> --reflect <period>
python -m aifn.main NVDA --reflect week
python -m aifn.main AAPL --reflect month
python -m aifn.main TSLA --reflect quarter

# Portfolio reflection (all tickers)
python -m aifn.main --reflect week
python -m aifn.main --reflect month

# Custom period
python -m aifn.main NVDA --reflect week --days 14
```

**Periods:**
- `week`: Last 7 days (default)
- `month`: Last 30 days
- `quarter`: Last 90 days

**Options:**
- `--days <n>`: Override number of days to analyze

### Historical Search

```bash
python -m aifn.main <ticker> --search "<query>"
python -m aifn.main NVDA --search "earnings surprise"
python -m aifn.main TSLA --search "production concerns" --limit 3
```

**Options:**
- `--limit <n>`: Number of results (default: 5)

## Function Reference

### Daily Analysis Functions

#### `summarize_financial_data(ticker, news_articles, time_series_data, market_news=None)`
Generates comprehensive daily analysis using LangGraph workflow.

**Parameters:**
- `ticker` (str): Stock symbol (e.g., 'AAPL')
- `news_articles` (List[Dict]): News from `crawl_stock_news()`
- `time_series_data` (Dict): Price data from `crawl_stock_daily_time_series()`
- `market_news` (List[Dict], optional): Market news from `crawl_market_news()`

**Returns:**
```python
{
    'news_summary': str,      # News analysis
    'price_analysis': str,    # Technical analysis
    'market_context': str,    # Market overview
    'final_summary': str      # Comprehensive report
}
```

#### `summarize_news_only(news_articles, ticker=None)`
Quick news summarization without price analysis.

**Parameters:**
- `news_articles` (List[Dict]): News articles to analyze
- `ticker` (str, optional): Stock symbol for context

**Returns:** String containing news summary

### Reflection Functions

#### `reflect_on_period(period_summaries, ticker=None, period_type="week")`
Performs deep analysis on historical summaries to identify patterns and generate insights.

**Parameters:**
- `period_summaries` (List[Dict]): Daily summaries from `get_period_summaries()`
- `ticker` (str, optional): Stock symbol. If None, analyzes all tickers (portfolio mode)
- `period_type` (str): "week", "month", or "quarter"

**Returns:**
```python
{
    'period_info': str,           # "Period: 2024-11-27 to 2024-12-04 (7 trading days) for NVDA"
    'pattern_analysis': str,      # Recurring patterns and trends
    'sentiment_evolution': str,   # Timeline of sentiment changes
    'key_events': str,            # 3-5 most significant events
    'investment_thesis': str,     # Bull/bear cases with recommendation
    'risk_assessment': str        # Comprehensive risk analysis
}
```

### RAG Functions

#### `store_embedding(summary, date, ticker=None, additional_metadata=None)`
Stores analysis in ChromaDB for future retrieval.

**Parameters:**
- `summary` (str): Analysis text to store
- `date` (str): Date in YYYY-MM-DD format
- `ticker` (str, optional): Stock ticker
- `additional_metadata` (dict, optional): Extra metadata

#### `get_period_summaries(start_date, end_date, ticker=None)`
Retrieves daily summaries for a date range.

**Parameters:**
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format
- `ticker` (str, optional): Stock ticker. If None, retrieves all tickers.

**Returns:** List of summaries with date, ticker, content, and metadata

#### `search_historical_analyses(query, ticker=None, k=5, date_range=None)`
Semantic search across historical analyses.

**Parameters:**
- `query` (str): Search query
- `ticker` (str, optional): Filter by ticker
- `k` (int): Number of results
- `date_range` (tuple, optional): (start_date, end_date)

**Returns:** List of similar analyses with similarity scores

## Workflow Architecture

### Daily Analysis Workflow (LangGraph)

```
[Start]
   ↓
[Summarize News] → Analyzes news articles
   ↓
[Analyze Price] → Technical analysis
   ↓
[Market Context] → Macro environment
   ↓
[Synthesize] → Comprehensive report
   ↓
[End]
```

Each node:
1. Receives current state
2. Performs specialized analysis with LLM
3. Updates state
4. Passes to next node

### Periodic Reflection Workflow

```
[Retrieve Historical Summaries from RAG]
   ↓
[Extract Period Information]
   ↓ (Parallel LLM Calls)
   ├─ [Pattern Analysis]
   ├─ [Sentiment Evolution]
   ├─ [Key Events]
   ├─ [Investment Thesis]
   └─ [Risk Assessment]
   ↓
[Combine Results]
   ↓
[Save Reflection to RAG]
```

## Model Configuration

**Current model:** Google Gemini 2.5-flash
- Free tier available
- Fast and cost-effective
- Supports long context windows
- Temperature: 0.3 (balanced)

**To change model:**
```python
# In summary.py, modify get_llm():
return ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # or other model
    temperature=0.5,
    google_api_key=api_key
)
```

## Prompt Engineering

All prompts are centralized in `prompts.py` with consistent structure:

### Daily Analysis Prompts
- **News Analysis**: Role-based news analyst
- **Price Analysis**: Technical analyst perspective
- **Market Context**: Macroeconomic analyst view
- **Synthesis**: Senior research analyst synthesis

### Reflection Prompts
- **Pattern Analysis**: Pattern recognition analyst
- **Sentiment Evolution**: Sentiment tracker timeline
- **Key Events**: Events analyst with impact assessment
- **Investment Thesis**: Investment strategist with bull/bear cases
- **Risk Assessment**: Chief risk officer perspective

**All prompts include:**
- META_PROMPT_PRINCIPLES for consistency
- Role-based instructions
- Structured output specifications
- Evidence-based requirements
- Professional tone

## Recommended Workflows

### Daily Routine (Monday-Friday)
```bash
# Morning: Analyze your watchlist
poetry run python -m aifn.main NVDA
poetry run python -m aifn.main AAPL
poetry run python -m aifn.main TSLA
```

### Weekly Review (Friday)
```bash
# Individual ticker deep dives
poetry run python -m aifn.main NVDA --reflect week
poetry run python -m aifn.main AAPL --reflect week

# Portfolio-wide reflection
poetry run python -m aifn.main --reflect week
```

### Monthly Review (End of Month)
```bash
# Comprehensive monthly analysis
poetry run python -m aifn.main --reflect month

# Compare individual tickers
poetry run python -m aifn.main NVDA --reflect month
```

### Ad-hoc Analysis
```bash
# Search for similar historical events
poetry run python -m aifn.main NVDA --search "similar earnings reactions"

# Quick news check without full analysis
poetry run python -m aifn.main MSFT --no-save
```

## Tips for Best Results

### Data Quality
1. **Fetch More Articles**: More data = better analysis
   ```bash
   poetry run python -m aifn.main NVDA --num-articles 100
   ```

2. **Build Historical Data**: Run daily analyses consistently for accurate reflections
   - Minimum 3-5 days for weekly reflection
   - Minimum 15-20 days for monthly reflection

3. **Use Market Context**: Always include market news for comprehensive analysis
   - Automatically fetched in CLI
   - Helps contextualize individual stock movements

### Analysis Optimization

4. **Leverage Reflection**: Use periodic reflection to identify patterns
   ```bash
   poetry run python -m aifn.main NVDA --reflect week
   ```

5. **Cross-Reference History**: Search for similar past events
   ```bash
   poetry run python -m aifn.main NVDA --search "10% drop after earnings"
   ```

6. **Portfolio View**: Analyze correlations across tickers
   ```bash
   poetry run python -m aifn.main --reflect week
   ```

### Cost Management

7. **Google Gemini Free Tier**: Very generous limits
   - Each daily analysis = 4 LLM calls
   - Each reflection = 5 LLM calls
   - News-only = 1 LLM call

8. **Alpha Vantage Free Tier**: 25 requests/day
   - Each daily analysis = 3 API calls
   - Space out analyses if needed

## Troubleshooting

### "Error: GOOGLE_API_KEY not found"
Make sure `GOOGLE_API_KEY` is set in your `.env` file:
```bash
GOOGLE_API_KEY=your_key_here
```

### "Error: ALPHA_VANTAGE_API_KEY not provided"
Make sure `ALPHA_VANTAGE_API_KEY` is set in your `.env` file:
```bash
ALPHA_VANTAGE_API_KEY=your_key_here
```

### "No historical analyses found"
You need to run daily analyses first to build RAG data:
```bash
# Run for a few days
poetry run python -m aifn.main NVDA
# Then try reflection
poetry run python -m aifn.main NVDA --reflect week
```

### Rate Limit Errors
Alpha Vantage free tier: 25 requests/day
- Cache data when possible
- Space out requests
- Consider upgrading to paid tier

### ChromaDB Errors
If you get database errors:
```bash
# Remove existing database and start fresh
rm -rf ./chroma_db
```

## Advanced Usage

### Custom Date Ranges for Reflection
```bash
poetry run python -m aifn.main NVDA --reflect week --days 14
```

### Programmatic Batch Processing
```python
tickers = ["NVDA", "AAPL", "TSLA", "MSFT"]

for ticker in tickers:
    # Daily analysis
    summary = daily_analysis(ticker)

    # Weekly reflection
    reflection = periodic_reflection(ticker, "week")
```

### Export to File
```python
# Add to main.py or use output redirection
poetry run python -m aifn.main NVDA > analysis_nvda.txt
```

## Future Enhancements

Potential improvements:
- [ ] PDF export for reports
- [ ] Email notifications for significant events
- [ ] Slack/Discord integration
- [ ] Real-time alerts based on patterns
- [ ] Backtesting framework
- [ ] Multi-model comparison
- [ ] Custom prompt templates via config
- [ ] Integration with broker APIs
- [ ] Automated scheduled runs

## Example Output Formats

### Daily Analysis Output
```markdown
# Executive Summary
NVDA shows mixed signals with strong revenue growth offset by China concerns...

## News Highlights
Recent developments indicate... [detailed analysis]

## Technical Picture
Price action shows... [technical analysis]

## Market Context
Broader semiconductor sector... [macro context]

## Key Takeaways & Considerations
- Bull case: AI demand remains strong
- Bear case: China exposure risk
- Key catalyst: Upcoming earnings call
```

### Reflection Output
```markdown
Period: 2024-11-27 to 2024-12-04 (7 trading days) for NVDA

PATTERN ANALYSIS
Throughout the week, three recurring themes emerged... [detailed patterns]

SENTIMENT EVOLUTION
Sentiment began the week positive but shifted on Tuesday... [timeline]

KEY EVENTS
Event 1: Earnings announcement (Dec 1)
- Beat estimates by 15%
- Guidance exceeded expectations
- Stock up 8% on the day

INVESTMENT THESIS
Bull Case: [3-4 evidence-based points]
Bear Case: [3-4 evidence-based points]
Recommendation: Buy with 75% confidence

RISK ASSESSMENT
Risk 1: China regulatory exposure - Likelihood: Medium
- Could impact 20% of revenue
- Monitor: Export license updates
```

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check this usage guide
2. Review [WORKFLOW_GUIDE.md](../../WORKFLOW_GUIDE.md)
3. Review [REFLECTION_UPDATE.md](../../REFLECTION_UPDATE.md)
4. Open an issue on GitHub
