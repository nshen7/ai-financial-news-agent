# Financial News Summarization with LangChain/LangGraph

This module provides AI-powered summarization of financial news and stock data using LangChain and LangGraph.

## Features

### 1. **Comprehensive Analysis with LangGraph Workflow**
The main function uses a LangGraph state machine with multiple specialized analysis nodes:
- **News Summarization Node**: Analyzes news articles for key themes and sentiment
- **Price Analysis Node**: Performs technical analysis on price data
- **Market Context Node**: Summarizes broader market trends
- **Synthesis Node**: Combines all analyses into a comprehensive report

### 2. **Simplified News-Only Analysis**
Quick function for analyzing just news articles without price data.

### 3. **Flexible Data Formatting**
Utilities to format crawler output into LLM-readable text.

## Setup

### Required Environment Variables

Add to your `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here
```

### Dependencies

All dependencies are already added to `pyproject.toml`:
- `langchain` - LangChain core
- `langchain-openai` - OpenAI integration
- `langgraph` - Graph-based workflows
- `python-dotenv` - Environment variables

Install with:
```bash
poetry install
```

## Usage Examples

### Example 1: Comprehensive Financial Summary (Recommended)

```python
from aifn.src.crawler import crawl_stock_news, crawl_stock_daily_time_series, crawl_market_news
from aifn.src.summary import summarize_financial_data

# Fetch data
ticker = "AAPL"
news_articles = crawl_stock_news(ticker, num_articles=5)
time_series_data = crawl_stock_daily_time_series(ticker)
market_news = crawl_market_news(num_articles=3)

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
```

### Example 2: News-Only Quick Summary

```python
from aifn.src.crawler import crawl_stock_news
from aifn.src.summary import summarize_news_only

# Fetch and summarize news
news_articles = crawl_stock_news("TSLA", num_articles=10)
summary = summarize_news_only(news_articles, ticker="TSLA")
print(summary)
```

### Example 3: Market News Summary

```python
from aifn.src.crawler import crawl_market_news
from aifn.src.summary import summarize_news_only

# Fetch market news with specific topics
market_news = crawl_market_news(
    num_articles=5,
    topics=['economy_macro', 'financial_markets']
)

# Summarize
summary = summarize_news_only(market_news)
print(summary)
```

## Running Tests

Three test modes are available:

```bash
# Test 1: Comprehensive summary (default)
python test_summary.py 1

# Test 2: News-only summary
python test_summary.py 2

# Test 3: Data formatting functions
python test_summary.py 3
```

Or run directly from the module:
```bash
python -m aifn.src.summary
```

## Function Reference

### Main Functions

#### `summarize_financial_data(ticker, news_articles, time_series_data, market_news=None)`
Generates comprehensive analysis using LangGraph workflow.

**Parameters:**
- `ticker` (str): Stock symbol (e.g., 'AAPL')
- `news_articles` (List[Dict]): News from `crawl_stock_news()`
- `time_series_data` (Dict): Price data from `crawl_stock_daily_time_series()`
- `market_news` (List[Dict], optional): Market news from `crawl_market_news()`

**Returns:**
Dictionary with keys:
- `news_summary`: Analysis of news articles
- `price_analysis`: Technical analysis of prices
- `market_context`: Market overview
- `final_summary`: Comprehensive markdown report

#### `summarize_news_only(news_articles, ticker=None)`
Quick news summarization without price analysis.

**Parameters:**
- `news_articles` (List[Dict]): News articles to analyze
- `ticker` (str, optional): Stock symbol for context

**Returns:**
String containing news summary

### Utility Functions

#### `format_news_articles(articles, ticker=None)`
Formats news articles into LLM-readable text.

#### `format_time_series_data(time_series, ticker, num_days=5)`
Formats price data into LLM-readable text with price change calculations.

## LangGraph Workflow Architecture

The comprehensive analysis uses a LangGraph state machine:

```
[Start] → [Summarize News] → [Analyze Price] → [Market Context] → [Synthesize] → [End]
```

Each node:
1. Receives the current state
2. Performs specialized analysis using LLM
3. Updates the state
4. Passes to next node

This modular approach ensures:
- Clear separation of concerns
- Easy to extend with new analysis types
- Consistent state management
- Parallel processing potential (can be extended)

## Model Configuration

Current settings in the code:
- **Model**: `gpt-4o-mini` (fast and cost-effective)
- **Temperature**: 0.3 (balanced creativity and consistency)

To use a different model, modify the `ChatOpenAI` initialization:
```python
llm = ChatOpenAI(
    model="gpt-4",  # or "gpt-4-turbo", "gpt-3.5-turbo"
    temperature=0.5,
    api_key=api_key
)
```

## Example Output Format

The comprehensive summary produces a structured markdown report:

```markdown
# Executive Summary
Brief overview of key findings...

# News Highlights
- Major announcements
- Sentiment analysis
- Key themes

# Technical Analysis
- Price trends
- Volume analysis
- Support/resistance levels

# Market Context
- Broader market sentiment
- Macroeconomic factors
- Sector trends

# Key Takeaways and Considerations
- Actionable insights
- Risk factors
- Investment considerations
```

## Tips for Best Results

1. **Fetch More Data**: More articles = better analysis
   ```python
   news_articles = crawl_stock_news(ticker, num_articles=10)
   ```

2. **Include Market Context**: Always fetch market news for comprehensive analysis
   ```python
   market_news = crawl_market_news(num_articles=5, topics=['economy_macro'])
   ```

3. **Adjust Time Range**: Use more historical data for trend analysis
   ```python
   time_series = crawl_stock_daily_time_series(ticker, outputsize='full')
   ```

4. **Handle API Rate Limits**: Alpha Vantage free tier has limits
   - 25 requests per day
   - Add delays between calls if needed

5. **Cost Management**: GPT-4o-mini is cost-effective, but monitor usage
   - Each comprehensive summary = 4 API calls
   - News-only summary = 1 API call

## Troubleshooting

### "Error: OpenAI API key not configured"
Make sure `OPENAI_API_KEY` is set in your `.env` file.

### "Error: Alpha Vantage API key not provided"
Make sure `ALPHA_VANTAGE_API_KEY` is set in your `.env` file.

### Rate Limit Errors
Alpha Vantage free tier allows 25 requests/day. Consider:
- Using cached data
- Upgrading to paid tier
- Spacing out requests

### Import Errors
Ensure all dependencies are installed:
```bash
poetry install
```

## Future Enhancements

Potential improvements:
- [ ] Add caching for API responses
- [ ] Implement parallel node execution in LangGraph
- [ ] Add sentiment trend analysis over time
- [ ] Include competitor comparison
- [ ] Export reports to PDF/HTML
- [ ] Add custom analysis templates
- [ ] Integrate more data sources (SEC filings, earnings calls)

## License

MIT License - See LICENSE file for details
