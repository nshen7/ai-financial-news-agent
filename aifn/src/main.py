#!/usr/bin/env python3
"""
AI Financial News Agent - Main CLI

Provides commands for:
- Daily financial analysis
- Weekly/monthly reflection on historical data
- Historical analysis search
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from .crawler import crawl_stock_news, crawl_market_news, crawl_stock_daily_time_series
from .summary import summarize_financial_data, reflect_on_period
from .rag import store_embedding, search_historical_analyses, retrieve_summaries_period


def daily_analysis(ticker: str, num_articles: int = 50, save_to_rag: bool = True):
    """
    Run daily financial analysis for a ticker.

    Args:
        ticker: Stock ticker symbol
        num_articles: Number of news articles to fetch
        save_to_rag: Whether to save analysis to RAG database
    """
    print(f"\n{'='*80}")
    print(f"AI FINANCIAL ANALYSIS: {ticker}")
    print(f"{'='*80}\n")

    # Fetch data
    print("📰 Fetching stock news...")
    news = crawl_stock_news(ticker, num_articles=num_articles)
    if not news:
        print("⚠️  No news articles found")
        return

    print("📊 Fetching price data...")
    prices = crawl_stock_daily_time_series(ticker, outputsize='compact')
    if not prices:
        print("⚠️  No price data found")
        return

    print("🌍 Fetching market context...")
    market = crawl_market_news(num_articles=20, topics=['economy_macro', 'technology'])

    # Analyze
    print("🤖 Running AI analysis...\n")
    result = summarize_financial_data(
        target=ticker,
        news_articles=news,
        time_series_data=prices
    )

    # Display
    print(f"\n{'='*80}")
    print("COMPREHENSIVE ANALYSIS")
    print(f"{'='*80}\n")
    print(result['final_summary'])

    print(f"\n{'-'*80}")
    print("DETAILED COMPONENT ANALYSES")
    print(f"{'-'*80}\n")

    print("📰 News Summary:")
    print(result['news_summary'])

    print(f"\n📊 Price Analysis:")
    print(result['price_analysis'])

    # Save to RAG if requested
    if save_to_rag:
        try:
            print(f"\n💾 Saving to RAG database...")
            store_embedding(
                summary=result['final_summary'],
                date=datetime.now().strftime('%Y-%m-%d'),
                ticker=ticker,
                additional_metadata={
                    'num_articles': len(news),
                    'analysis_type': 'daily'
                }
            )
            print("✅ Analysis saved to RAG database")
        except Exception as e:
            print(f"⚠️  Could not save to RAG: {e}")


def periodic_reflection(ticker: str = None, period: str = "week", num_days: int = None):
    """
    Run periodic reflection on historical analyses.

    Args:
        ticker: Optional stock ticker symbol. If None, analyzes all tickers.
        period: Type of period ("week", "month", "quarter")
        num_days: Override number of days to look back
    """
    if ticker:
        print(f"\n{'='*80}")
        print(f"PERIODIC REFLECTION: {ticker} ({period})")
        print(f"{'='*80}\n")
    else:
        print(f"\n{'='*80}")
        print(f"PERIODIC PORTFOLIO REFLECTION ({period})")
        print(f"{'='*80}\n")

    # Calculate date range
    end_date = datetime.now().strftime('%Y-%m-%d')

    if num_days:
        days_back = num_days
    elif period == "week":
        days_back = 7
    elif period == "month":
        days_back = 30
    elif period == "quarter":
        days_back = 90
    else:
        days_back = 7

    start_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    print(f"📅 Date Range: {start_date} to {end_date}\n")

    # Retrieve historical summaries from RAG
    print("🔍 Retrieving historical analyses...")
    summaries = retrieve_summaries_period(start_date, end_date, ticker=ticker)

    if not summaries:
        if ticker:
            print(f"⚠️  No historical analyses found for {ticker} in this period")
            print(f"🔄 Running daily analysis for missing days to populate database...")

            # Generate daily analyses for the missing date range
            current_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d')

            while current_date <= end_datetime:
                date_str = current_date.strftime('%Y-%m-%d')
                print(f"\n📅 Analyzing {ticker} for {date_str}...")

                try:
                    daily_analysis(ticker, num_articles=5, save_to_rag=True)
                except Exception as e:
                    print(f"⚠️  Error analyzing {date_str}: {e}")

                current_date += timedelta(days=1)

            # Retrieve summaries again after generating analyses
            print("\n🔍 Retrieving historical analyses after generation...")
            summaries = retrieve_summaries_period(start_date, end_date, ticker=ticker)

            if not summaries:
                print(f"⚠️  Still no analyses found after generation. Please check the data sources.")
                return
        else:
            print(f"⚠️  No historical analyses found in this period")
            print("💡 Tip: Run daily analysis with save-to-rag enabled to build historical data")
            print("💡 Note: Automatic daily analysis generation requires a specific ticker")
            return

    print(f"✅ Found {len(summaries)} daily analyses\n")

    # Run reflection
    print("🤖 Running periodic reflection analysis...\n")
    reflection = reflect_on_period(
        period_summaries=summaries,
        ticker=ticker,
        period_type=period
    )

    # Display period information
    print(f"\n{'='*80}")
    print(reflection['period_info'])
    print(f"{'='*80}\n")

    # Display results
    print(f"\n{'='*80}")
    print("PATTERN ANALYSIS")
    print(f"{'='*80}\n")
    print(reflection['pattern_analysis'])

    print(f"\n{'='*80}")
    print("SENTIMENT EVOLUTION")
    print(f"{'='*80}\n")
    print(reflection['sentiment_evolution'])

    print(f"\n{'='*80}")
    print("KEY EVENTS")
    print(f"{'='*80}\n")
    print(reflection['key_events'])

    print(f"\n{'='*80}")
    print("INVESTMENT THESIS")
    print(f"{'='*80}\n")
    print(reflection['investment_thesis'])

    print(f"\n{'='*80}")
    print("RISK ASSESSMENT")
    print(f"{'='*80}\n")
    print(reflection['risk_assessment'])

    # Save reflection to RAG
    try:
        print(f"\n💾 Saving reflection to RAG database...")
        reflection_summary = f"""PERIODIC REFLECTION ({period.upper()})
{reflection['period_info']}

{reflection['pattern_analysis']}

{reflection['sentiment_evolution']}

{reflection['key_events']}

{reflection['investment_thesis']}

{reflection['risk_assessment']}
"""
        # Get unique tickers from summaries
        unique_tickers = list(set([s.get('ticker') for s in summaries if s.get('ticker')]))

        # If single ticker, store with ticker metadata
        if ticker or len(unique_tickers) == 1:
            store_ticker = ticker or unique_tickers[0]
            store_embedding(
                summary=reflection_summary,
                date=end_date,
                ticker=store_ticker,
                additional_metadata={
                    'analysis_type': f'reflection_{period}',
                    'period_start': start_date,
                    'period_end': end_date,
                    'num_days_analyzed': len(summaries),
                    'num_tickers': 1
                }
            )
        else:
            # Portfolio reflection - store without ticker filter
            store_embedding(
                summary=reflection_summary,
                date=end_date,
                additional_metadata={
                    'analysis_type': f'reflection_{period}_portfolio',
                    'period_start': start_date,
                    'period_end': end_date,
                    'num_days_analyzed': len(summaries),
                    'num_tickers': len(unique_tickers),
                    'tickers': ','.join(unique_tickers[:10])  # Store first 10
                }
            )
        print("✅ Reflection saved to RAG database")
    except Exception as e:
        print(f"⚠️  Could not save reflection to RAG: {e}")


def search_history(ticker: str, query: str, k: int = 5):
    """
    Search historical analyses for similar patterns or events.

    Args:
        ticker: Stock ticker symbol
        query: Search query
        k: Number of results to return
    """
    print(f"\n{'='*80}")
    print(f"SEARCHING HISTORICAL ANALYSES: {ticker}")
    print(f"{'='*80}\n")
    print(f"Query: {query}\n")

    results = search_historical_analyses(query=query, ticker=ticker, k=k)

    if not results:
        print(f"⚠️  No historical analyses found for {ticker}")
        print("💡 Tip: Run daily analysis with --save-to-rag to build historical data")
        return

    print(f"✅ Found {len(results)} relevant analyses:\n")

    for i, result in enumerate(results, 1):
        metadata = result['metadata']
        date = metadata.get('date', 'Unknown')
        analysis_type = metadata.get('analysis_type', 'daily')
        score = result['score']

        print(f"{'-'*80}")
        print(f"Result {i} - {date} ({analysis_type}) - Similarity: {score:.3f}")
        print(f"{'-'*80}")
        print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
        print()


def print_usage():
    """Print usage information."""
    print("""
AI Financial News Agent - Usage

COMMANDS:

1. Daily Analysis (default):
   python -m aifn.main <ticker>
   python -m aifn.main NVDA

   Options:
   --num-articles <n>    Number of news articles (default: 50)
   --no-save            Don't save to RAG database

2. Periodic Reflection:
   # Single ticker reflection
   python -m aifn.main <ticker> --reflect <period>
   python -m aifn.main NVDA --reflect week
   python -m aifn.main AAPL --reflect month

   # Portfolio reflection (all tickers)
   python -m aifn.main --reflect <period>
   python -m aifn.main --reflect week

   Periods: week (7 days), month (30 days), quarter (90 days)

   Options:
   --days <n>           Override number of days to analyze

3. Search History:
   python -m aifn.main <ticker> --search "<query>"
   python -m aifn.main NVDA --search "earnings surprise"
   python -m aifn.main TSLA --search "similar price drops"

   Options:
   --limit <n>          Number of results (default: 5)

EXAMPLES:

# Daily analysis for NVDA
python -m aifn.main NVDA

# Weekly reflection for AAPL
python -m aifn.main AAPL --reflect week

# Monthly reflection for TSLA
python -m aifn.main TSLA --reflect month

# Portfolio-wide weekly reflection (all tickers)
python -m aifn.main --reflect week

# Search for similar events
python -m aifn.main NVDA --search "price drops after earnings"

# Daily analysis without saving to RAG
python -m aifn.main MSFT --no-save
""")


def main():
    """Main CLI entry point."""
    args = sys.argv[1:]

    if not args or '--help' in args or '-h' in args:
        print_usage()
        return

    # Check if first arg is a ticker or a flag
    ticker = None
    if args and not args[0].startswith('--'):
        ticker = args[0].upper()

    # Determine command
    if '--reflect' in args:
        # Periodic reflection
        reflect_idx = args.index('--reflect')
        period = args[reflect_idx + 1] if len(args) > reflect_idx + 1 else 'week'

        num_days = None
        if '--days' in args:
            days_idx = args.index('--days')
            num_days = int(args[days_idx + 1]) if len(args) > days_idx + 1 else None

        periodic_reflection(ticker, period, num_days)

    elif '--search' in args:
        # Search history - requires ticker
        if not ticker:
            print("Error: --search requires a ticker symbol")
            print("Usage: python -m aifn.main <ticker> --search \"query\"")
            return

        search_idx = args.index('--search')
        query = args[search_idx + 1] if len(args) > search_idx + 1 else ""

        k = 5
        if '--limit' in args:
            limit_idx = args.index('--limit')
            k = int(args[limit_idx + 1]) if len(args) > limit_idx + 1 else 5

        search_history(ticker, query, k)

    else:
        # Daily analysis (default) - requires ticker
        if not ticker:
            print("Error: Daily analysis requires a ticker symbol")
            print("Usage: python -m aifn.main <ticker>")
            print("Or use: python -m aifn.main --help")
            return

        num_articles = 50
        if '--num-articles' in args:
            num_idx = args.index('--num-articles')
            num_articles = int(args[num_idx + 1]) if len(args) > num_idx + 1 else 50

        save_to_rag = '--no-save' not in args

        daily_analysis(ticker, num_articles, save_to_rag)


if __name__ == "__main__":
    main()
