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
            'limit': num_articles * 2  # Request more to ensure we get enough after filtering
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

## test
if __name__ == "__main__":
    stock_symbol = "AAPL"

    # Test news crawling
    print("=" * 80)
    print(f"FETCHING NEWS DATA FOR {stock_symbol}")
    print("=" * 80)
    articles = crawl_stock_news(stock_symbol)

    print(f'Number of articles found: {len(articles)}')
    if articles:
        print(f'\nExample crawled article for {stock_symbol}:')
        print('-----------------------------------')
        print(articles[0])
        print('-----------------------------------')

        for i, article in enumerate(articles):
            print(f'\nArticle {i+1}:')
            print(f'Title: {article["title"]}')
            print(f'Publisher: {article["publisher"]}')
            print(f'Link: {article["link"]}')
            print(f'Published: {article["publish_time"]}')
            print(f'Summary: {article["summary"][:200]}...' if len(article["summary"]) > 200 else f'Summary: {article["summary"]}')
            print(f'Topics: {", ".join(article["topics"])}')
            print(f'Overall Sentiment: {article["overall_sentiment_label"]} (Score: {article["overall_sentiment_score"]:.4f})')
            ticker_score = f'{article["ticker_sentiment_score"]:.4f}' if article["ticker_sentiment_score"] is not None else "N/A"
            print(f'Ticker Sentiment: {article["ticker_sentiment_label"]} (Score: {ticker_score})')
            relevance_score = f'{article["ticker_relevance_score"]:.4f}' if article["ticker_relevance_score"] is not None else "N/A"
            print(f'Relevance Score: {relevance_score}')
    else:
        print('No articles found - check your API key and network connection')

    # Test time series data crawling
    print("\n" + "=" * 80)
    print(f"FETCHING DAILY TIME SERIES DATA FOR {stock_symbol}")
    print("=" * 80)
    time_series = crawl_stock_daily_time_series(stock_symbol)

    if time_series:
        print(f'Number of data points retrieved: {len(time_series)}')

        # Get the most recent dates (sorted)
        sorted_dates = sorted(time_series.keys(), reverse=True)

        print(f'\nToday for {stock_symbol}:')
        print('-----------------------------------')
        for i, date in enumerate(sorted_dates[:1]):
            data = time_series[date]
            print(f'\nDate: {date}')
            print(f'  Open:   ${data["open"]:.2f}')
            print(f'  High:   ${data["high"]:.2f}')
            print(f'  Low:    ${data["low"]:.2f}')
            print(f'  Close:  ${data["close"]:.2f}')
            print(f'  Volume: {data["volume"]:,}')
    else:
        print('No time series data found - check your API key and network connection')

    # Test market news crawling
    print("\n" + "=" * 80)
    print("FETCHING BROADER MARKET AND MACROECONOMIC NEWS")
    print("=" * 80)
    market_articles = crawl_market_news(num_articles=5, topics=['blockchain', 'economy_macro'])

    print(f'Number of market articles found: {len(market_articles)}')
    if market_articles:
        print(f'\nExample market article:')
        print('-----------------------------------')
        print(market_articles[0])
        print('-----------------------------------')

        for i, article in enumerate(market_articles):
            print(f'\nMarket Article {i+1}:')
            print(f'Title: {article["title"]}')
            print(f'Publisher: {article["publisher"]}')
            print(f'Link: {article["link"]}')
            print(f'Published: {article["publish_time"]}')
            print(f'Summary: {article["summary"][:200]}...' if len(article["summary"]) > 200 else f'Summary: {article["summary"]}')
            print(f'Topics: {", ".join(article["topics"])}')
            print(f'Overall Sentiment: {article["overall_sentiment_label"]} (Score: {article["overall_sentiment_score"]:.4f})')
            if article["ticker_sentiments"]:
                tickers = [ts["ticker"] for ts in article["ticker_sentiments"][:5]]
                print(f'Related Tickers: {", ".join(tickers)}')
            else:
                print('Related Tickers: None')
    else:
        print('No market articles found - check your API key and network connection')