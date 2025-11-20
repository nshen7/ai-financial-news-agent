import requests
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def crawl_market_news(num_articles=1, topics=None, api_key=None):
    """
    Fetch recent news articles about the broader market and macroeconomic environment.

    Args:
        num_articles: Maximum number of articles to return
        topics: List of topics to filter by. Common topics include:
            - Blockchain: 'blockchain'
            - Earnings: 'earnings'
            - IPO: 'ipo'
            - Mergers & Acquisitions: 'mergers_and_acquisitions'
            - Financial Markets: 'financial_markets'
            - Economy - Fiscal Policy (e.g., tax reform, government spending): 'economy_fiscal'
            - Economy - Monetary Policy (e.g., interest rates, inflation): 'economy_monetary'
            - Economy - Macro/Overall: 'economy_macro'
            - Energy & Transportation: 'energy_transportation'
            - Finance: 'finance'
            - Life Sciences: 'life_sciences'
            - Manufacturing: 'manufacturing'
            - Real Estate & Construction: 'real_estate'
            - Retail & Wholesale: 'retail_wholesale'
            - Technology: 'technology'
            If None, fetches general market news without ticker filtering
            For example: topics=technology will filter for articles that write about the technology sector;
            topics=technology,ipo will filter for articles that simultaneously cover technology and IPO in their content. 
        api_key: Alpha Vantage API key (if not provided, will use ALPHA_VANTAGE_API_KEY env variable)

    Returns:
        List of dictionaries containing article information and sentiment scores
    """
    try:
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

        if not api_key:
            print("Error: Alpha Vantage API key not provided. Set ALPHA_VANTAGE_API_KEY environment variable or pass api_key parameter.")
            return []

        # Alpha Vantage News & Sentiment API endpoint
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'NEWS_SENTIMENT',
            'apikey': api_key,
            'limit': num_articles  # Request more to ensure we get enough after filtering
        }

        # Add topics filter if provided
        if topics:
            if isinstance(topics, list):
                params['topics'] = ','.join(topics)
            else:
                params['topics'] = topics

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if 'Error Message' in data:
            print(f"API Error: {data['Error Message']}")
            return []

        if 'Note' in data:
            print(f"API Note: {data['Note']}")
            return []

        if 'Information' in data:
            print(f"API Information: {data['Information']}")
            return []

        # Extract news feed
        news_feed = data.get('feed', [])

        if not news_feed:
            print("No market news found")
            return []

        articles = []
        for item in news_feed[:num_articles]:
            # Parse publish date
            pub_date_str = item.get('time_published', '')
            try:
                if pub_date_str:
                    # Alpha Vantage format: "20251117T210641" (YYYYMMDDTHHmmss)
                    pub_date = datetime.strptime(pub_date_str, '%Y%m%dT%H%M%S')
                    publish_time = pub_date.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    publish_time = 'Unknown'
            except Exception:
                publish_time = pub_date_str

            # Build article dictionary with sentiment data
            article = {
                'title': item.get('title', 'No title'),
                'publisher': item.get('source', 'Unknown'),
                'link': item.get('url', ''),
                'publish_time': publish_time,
                'summary': item.get('summary', ''),
                'banner_image': item.get('banner_image', ''),
                'category': item.get('category_within_source', ''),
                'topics': [topic.get('topic', '') for topic in item.get('topics', [])],
                # Overall sentiment for the article
                'overall_sentiment_score': float(item.get('overall_sentiment_score', 0)),
                'overall_sentiment_label': item.get('overall_sentiment_label', 'Neutral'),
                # Include all ticker sentiments for market news
                'ticker_sentiments': [
                    {
                        'ticker': ts.get('ticker', ''),
                        'sentiment_score': float(ts.get('ticker_sentiment_score', 0)),
                        'sentiment_label': ts.get('ticker_sentiment_label', 'Neutral'),
                        'relevance_score': float(ts.get('relevance_score', 0))
                    }
                    for ts in item.get('ticker_sentiment', [])
                ]
            }
            articles.append(article)

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching market news: {e}")
        return []
    except Exception as e:
        import traceback
        print(f"Error fetching market news: {e}")
        traceback.print_exc()
        return []

def crawl_stock_news(stock_symbol, num_articles=1, api_key=None):
    """
    Fetch recent news articles and sentiment for a given stock symbol using Alpha Vantage.

    Args:
        stock_symbol: Stock ticker symbol (e.g., 'AAPL')
        num_articles: Maximum number of articles to return
        api_key: Alpha Vantage API key (if not provided, will use ALPHA_VANTAGE_API_KEY env variable)

    Returns:
        List of dictionaries containing article information and sentiment scores
    """
    try:
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

        if not api_key:
            print("Error: Alpha Vantage API key not provided. Set ALPHA_VANTAGE_API_KEY environment variable or pass api_key parameter.")
            return []

        # Alpha Vantage News & Sentiment API endpoint
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': stock_symbol,
            'apikey': api_key,
            'limit': num_articles * 2  # Request more to ensure we get enough after filtering
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if 'Error Message' in data:
            print(f"API Error: {data['Error Message']}")
            return []

        if 'Note' in data:
            print(f"API Note: {data['Note']}")
            return []

        if 'Information' in data:
            print(f"API Information: {data['Information']}")
            return []

        # Extract news feed
        news_feed = data.get('feed', [])

        if not news_feed:
            print(f"No news found for {stock_symbol}")
            return []

        articles = []
        for item in news_feed[:num_articles]:
            # Parse publish date
            pub_date_str = item.get('time_published', '')
            try:
                if pub_date_str:
                    # Alpha Vantage format: "20251117T210641" (YYYYMMDDTHHmmss)
                    pub_date = datetime.strptime(pub_date_str, '%Y%m%dT%H%M%S')
                    publish_time = pub_date.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    publish_time = 'Unknown'
            except Exception:
                publish_time = pub_date_str

            # Extract sentiment scores for the specific ticker
            ticker_sentiment = None
            for ticker_data in item.get('ticker_sentiment', []):
                if ticker_data.get('ticker') == stock_symbol:
                    ticker_sentiment = ticker_data
                    break

            # Build article dictionary with sentiment data
            article = {
                'title': item.get('title', 'No title'),
                'publisher': item.get('source', 'Unknown'),
                'link': item.get('url', ''),
                'publish_time': publish_time,
                'summary': item.get('summary', ''),
                'banner_image': item.get('banner_image', ''),
                'category': item.get('category_within_source', ''),
                'topics': [topic.get('topic', '') for topic in item.get('topics', [])],
                # Overall sentiment for the article
                'overall_sentiment_score': float(item.get('overall_sentiment_score', 0)),
                'overall_sentiment_label': item.get('overall_sentiment_label', 'Neutral'),
                # Ticker-specific sentiment
                'ticker_sentiment_score': float(ticker_sentiment.get('ticker_sentiment_score', 0)) if ticker_sentiment else None,
                'ticker_sentiment_label': ticker_sentiment.get('ticker_sentiment_label', 'N/A') if ticker_sentiment else 'N/A',
                'ticker_relevance_score': float(ticker_sentiment.get('relevance_score', 0)) if ticker_sentiment else None
            }
            articles.append(article)

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching news for {stock_symbol}: {e}")
        return []
    except Exception as e:
        import traceback
        print(f"Error fetching news for {stock_symbol}: {e}")
        traceback.print_exc()
        return []


def crawl_stock_daily_time_series(stock_symbol, outputsize='compact', api_key=None):
    """
    Fetch daily time series data for a given stock symbol using Alpha Vantage.

    Args:
        stock_symbol: Stock ticker symbol (e.g., 'AAPL')
        outputsize: 'compact' returns last 100 data points, 'full' returns full-length data (up to 20+ years)
        api_key: Alpha Vantage API key (if not provided, will use ALPHA_VANTAGE_API_KEY env variable)

    Returns:
        Dictionary containing time series data with dates as keys and OHLCV data as values
    """
    try:
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

        if not api_key:
            print("Error: Alpha Vantage API key not provided. Set ALPHA_VANTAGE_API_KEY environment variable or pass api_key parameter.")
            return {}

        # Alpha Vantage Time Series Daily API endpoint
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': stock_symbol,
            'apikey': api_key,
            'outputsize': outputsize
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Check for API errors
        if 'Error Message' in data:
            print(f"API Error: {data['Error Message']}")
            return {}

        if 'Note' in data:
            print(f"API Note: {data['Note']}")
            return {}

        if 'Information' in data:
            print(f"API Information: {data['Information']}")
            return {}

        # Extract time series data
        time_series_key = 'Time Series (Daily)'
        if time_series_key not in data:
            print(f"No time series data found for {stock_symbol}")
            return {}

        time_series = data[time_series_key]

        # Process and format the data
        formatted_data = {}
        for date_str, values in time_series.items():
            formatted_data[date_str] = {
                'open': float(values.get('1. open', 0)),
                'high': float(values.get('2. high', 0)),
                'low': float(values.get('3. low', 0)),
                'close': float(values.get('4. close', 0)),
                'volume': int(values.get('5. volume', 0))
            }

        return formatted_data

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching time series data for {stock_symbol}: {e}")
        return {}
    except Exception as e:
        import traceback
        print(f"Error fetching time series data for {stock_symbol}: {e}")
        traceback.print_exc()
        return {}


# =============================================================================
# DATA FORMATTING FUNCTIONS
# =============================================================================

def format_news_articles(articles, ticker=None):
    """
    Format news articles into a readable text format for LLM processing.

    Args:
        articles: List of article dictionaries from crawler
        ticker: Optional ticker symbol for context

    Returns:
        Formatted string containing article information
    """
    if not articles:
        return "No news articles available."

    formatted_text = []
    article_type = f"for {ticker}" if ticker else "(Market News)"
    formatted_text.append(f"=== News Articles {article_type} ===\n")

    for i, article in enumerate(articles, 1):
        formatted_text.append(f"Article {i}:")
        formatted_text.append(f"Title: {article.get('title', 'N/A')}")
        formatted_text.append(f"Publisher: {article.get('publisher', 'N/A')}")
        formatted_text.append(f"Published: {article.get('publish_time', 'N/A')}")
        formatted_text.append(f"Summary: {article.get('summary', 'N/A')}")
        formatted_text.append(f"Topics: {', '.join(article.get('topics', []))}")
        formatted_text.append(f"Overall Sentiment: {article.get('overall_sentiment_label', 'N/A')} "
                            f"(Score: {article.get('overall_sentiment_score', 0):.4f})")

        # Include ticker-specific sentiment if available
        if 'ticker_sentiment_score' in article:
            ticker_score = article.get('ticker_sentiment_score')
            if ticker_score is not None:
                formatted_text.append(f"Ticker Sentiment: {article.get('ticker_sentiment_label', 'N/A')} "
                                    f"(Score: {ticker_score:.4f})")
                formatted_text.append(f"Relevance Score: {article.get('ticker_relevance_score', 0):.4f}")

        # Include related tickers for market news
        if 'ticker_sentiments' in article:
            tickers = [ts['ticker'] for ts in article['ticker_sentiments'][:5]]
            if tickers:
                formatted_text.append(f"Related Tickers: {', '.join(tickers)}")

        formatted_text.append(f"Link: {article.get('link', 'N/A')}")
        formatted_text.append("")

    return "\n".join(formatted_text)


def format_time_series_data(time_series, ticker, num_days=5):
    """
    Format time series data into a readable text format for LLM processing.

    Args:
        time_series: Dictionary of time series data from crawler
        ticker: Stock ticker symbol
        num_days: Number of recent days to include

    Returns:
        Formatted string containing price data
    """
    if not time_series:
        return f"No time series data available for {ticker}."

    formatted_text = []
    formatted_text.append(f"=== Recent Price Data for {ticker} ===\n")

    # Sort dates in descending order (most recent first)
    sorted_dates = sorted(time_series.keys(), reverse=True)[:num_days]

    for date in sorted_dates:
        data = time_series[date]
        formatted_text.append(f"Date: {date}")
        formatted_text.append(f"  Open:   ${data['open']:.2f}")
        formatted_text.append(f"  High:   ${data['high']:.2f}")
        formatted_text.append(f"  Low:    ${data['low']:.2f}")
        formatted_text.append(f"  Close:  ${data['close']:.2f}")
        formatted_text.append(f"  Volume: {data['volume']:,}")
        formatted_text.append("")

    # Calculate price change if we have enough data
    if len(sorted_dates) >= 2:
        latest_close = time_series[sorted_dates[0]]['close']
        previous_close = time_series[sorted_dates[-1]]['close']
        change = latest_close - previous_close
        change_pct = (change / previous_close) * 100
        formatted_text.append(f"Price Change (Last {len(sorted_dates)} days): ${change:.2f} ({change_pct:+.2f}%)")

    return "\n".join(formatted_text)


## test
# if __name__ == "__main__":

#     ### Test market news crawling
#     print("\n" + "=" * 80)
#     print("FETCHING BROADER MARKET AND MACROECONOMIC NEWS")
#     print("=" * 80)
#     market_articles = crawl_market_news(num_articles=1, topics=['economy_macro'])

#     print(f'Number of market articles found: {len(market_articles)}')
#     if market_articles:
#         print(f'\nExample market article:')
#         print('-----------------------------------')
#         print(market_articles[0])
#         print('-----------------------------------')

#         for i, article in enumerate(market_articles):
#             print(f'\nMarket Article {i+1}:')
#             print(f'Title: {article["title"]}')
#             print(f'Publisher: {article["publisher"]}')
#             print(f'Link: {article["link"]}')
#             print(f'Published: {article["publish_time"]}')
#             print(f'Summary: {article["summary"][:200]}...' if len(article["summary"]) > 200 else f'Summary: {article["summary"]}')
#             print(f'Topics: {", ".join(article["topics"])}')
#             print(f'Overall Sentiment: {article["overall_sentiment_label"]} (Score: {article["overall_sentiment_score"]:.4f})')
#             if article["ticker_sentiments"]:
#                 tickers = [ts["ticker"] for ts in article["ticker_sentiments"][:5]]
#                 print(f'Related Tickers: {", ".join(tickers)}')
#             else:
#                 print('Related Tickers: None')
#     else:
#         print('No market articles found - check your API key and network connection')

#     ### Test stock news crawling
#     stock_symbol = "AAPL"

#     # Test news crawling
#     print("=" * 80)
#     print(f"FETCHING NEWS DATA FOR {stock_symbol}")
#     print("=" * 80)
#     articles = crawl_stock_news(stock_symbol)

#     print(f'Number of articles found: {len(articles)}')
#     if articles:
#         print(f'\nExample crawled article for {stock_symbol}:')
#         print('-----------------------------------')
#         print(articles[0])
#         print('-----------------------------------')

#         for i, article in enumerate(articles):
#             print(f'\nArticle {i+1}:')
#             print(f'Title: {article["title"]}')
#             print(f'Publisher: {article["publisher"]}')
#             print(f'Link: {article["link"]}')
#             print(f'Published: {article["publish_time"]}')
#             print(f'Summary: {article["summary"][:200]}...' if len(article["summary"]) > 200 else f'Summary: {article["summary"]}')
#             print(f'Topics: {", ".join(article["topics"])}')
#             print(f'Overall Sentiment: {article["overall_sentiment_label"]} (Score: {article["overall_sentiment_score"]:.4f})')
#             ticker_score = f'{article["ticker_sentiment_score"]:.4f}' if article["ticker_sentiment_score"] is not None else "N/A"
#             print(f'Ticker Sentiment: {article["ticker_sentiment_label"]} (Score: {ticker_score})')
#             relevance_score = f'{article["ticker_relevance_score"]:.4f}' if article["ticker_relevance_score"] is not None else "N/A"
#             print(f'Relevance Score: {relevance_score}')
#     else:
#         print('No articles found - check your API key and network connection')

#     # Test time series data crawling
#     print("\n" + "=" * 80)
#     print(f"FETCHING DAILY TIME SERIES DATA FOR {stock_symbol}")
#     print("=" * 80)
#     time_series = crawl_stock_daily_time_series(stock_symbol)

#     if time_series:
#         print(f'Number of data points retrieved: {len(time_series)}')

#         # Get the most recent dates (sorted)
#         sorted_dates = sorted(time_series.keys(), reverse=True)

#         print(f'\nToday for {stock_symbol}:')
#         print('-----------------------------------')
#         for i, date in enumerate(sorted_dates[:1]):
#             data = time_series[date]
#             print(f'\nDate: {date}')
#             print(f'  Open:   ${data["open"]:.2f}')
#             print(f'  High:   ${data["high"]:.2f}')
#             print(f'  Low:    ${data["low"]:.2f}')
#             print(f'  Close:  ${data["close"]:.2f}')
#             print(f'  Volume: {data["volume"]:,}')
#     else:
#         print('No time series data found - check your API key and network connection')

