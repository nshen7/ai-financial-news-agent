"""
Financial News and Data Summarization using LangChain/LangGraph.

This module provides functions to summarize financial news articles and stock data
using LLM-powered analysis through LangChain.
"""

import os
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# Import prompts from centralized prompts module
from .prompts import (
    get_news_analysis_prompt,
    get_price_analysis_prompt,
    get_market_context_prompt,
    get_synthesis_prompt
)

# Import data formatting functions from crawler module
from .crawler import format_news_articles, format_time_series_data

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


def get_llm(temperature: float = 0.3):
    """
    Get configured LLM instance (Google Gemini).

    Args:
        temperature: Temperature for response generation (0.0-1.0)

    Returns:
        Configured ChatGoogleGenerativeAI instance

    Note:
        Requires GOOGLE_API_KEY environment variable to be set.
        Get your free API key at: https://makersuite.google.com/app/apikey
    """
    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables. "
            "Get your free API key at: https://makersuite.google.com/app/apikey"
        )

    # Using gemini-2.5-flash model for financial summarization
    # This model is:
    # - Free tier available
    # - Lightweight and fast
    # - Supports long context windows
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=temperature,
        google_api_key=api_key,
        convert_system_message_to_human=True  # Gemini compatibility
    )


class FinancialDataState(TypedDict):
    """State for the financial analysis workflow."""
    ticker: str
    news_articles: List[Dict[str, Any]]
    time_series_data: Dict[str, Any]
    market_news: List[Dict[str, Any]]
    news_summary: str
    price_analysis: str
    market_context: str
    final_summary: str


def summarize_news_node(state: FinancialDataState) -> FinancialDataState:
    """
    LangGraph node to summarize news articles using LLM.

    Args:
        state: Current workflow state

    Returns:
        Updated state with news summary
    """
    try:
        llm = get_llm(temperature=0.3)
    except ValueError as e:
        state['news_summary'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_news_analysis_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Format and process news
    news_text = format_news_articles(state['news_articles'], state.get('ticker'))

    try:
        state['news_summary'] = chain.invoke({
            "news_text": news_text,
            "ticker": state['ticker']
        })
    except Exception as e:
        state['news_summary'] = f"Error generating news summary: {str(e)}"

    return state


def analyze_price_node(state: FinancialDataState) -> FinancialDataState:
    """
    LangGraph node to analyze price data using LLM.

    Args:
        state: Current workflow state

    Returns:
        Updated state with price analysis
    """
    try:
        llm = get_llm(temperature=0.3)
    except ValueError as e:
        state['price_analysis'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_price_analysis_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Format and process time series data
    price_text = format_time_series_data(state['time_series_data'], state['ticker'])

    # Calculate number of days of data
    n_days = len(state['time_series_data']) if state['time_series_data'] else 0

    try:
        state['price_analysis'] = chain.invoke({
            "price_text": price_text,
            "ticker": state['ticker'],
            "n": n_days
        })
    except Exception as e:
        state['price_analysis'] = f"Error generating price analysis: {str(e)}"

    return state


def market_context_node(state: FinancialDataState) -> FinancialDataState:
    """
    LangGraph node to summarize broader market context.

    Args:
        state: Current workflow state

    Returns:
        Updated state with market context
    """
    try:
        llm = get_llm(temperature=0.3)
    except ValueError as e:
        state['market_context'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_market_context_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Format and process market news
    market_text = format_news_articles(state['market_news'])

    try:
        state['market_context'] = chain.invoke({"market_text": market_text})
    except Exception as e:
        state['market_context'] = f"Error generating market context: {str(e)}"

    return state


def synthesize_final_summary_node(state: FinancialDataState) -> FinancialDataState:
    """
    LangGraph node to synthesize all analyses into a final comprehensive summary.

    Args:
        state: Current workflow state

    Returns:
        Updated state with final summary
    """
    try:
        llm = get_llm(temperature=0.3)
    except ValueError as e:
        state['final_summary'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_synthesis_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    try:
        state['final_summary'] = chain.invoke({
            "ticker": state['ticker'],
            "news_summary": state.get('news_summary', 'No news analysis available.'),
            "price_analysis": state.get('price_analysis', 'No price analysis available.'),
            "market_context": state.get('market_context', 'No market context available.')
        })
    except Exception as e:
        state['final_summary'] = f"Error generating final summary: {str(e)}"

    return state


def create_financial_summary_graph() -> StateGraph:
    """
    Create a LangGraph workflow for financial data summarization.

    Returns:
        Compiled StateGraph for processing financial data
    """
    # Create the graph
    workflow = StateGraph(FinancialDataState)

    # Add nodes
    workflow.add_node("summarize_news", summarize_news_node)
    workflow.add_node("analyze_price", analyze_price_node)
    workflow.add_node("market_context", market_context_node)
    workflow.add_node("synthesize_summary", synthesize_final_summary_node)

    # Define edges (workflow flow)
    workflow.set_entry_point("summarize_news")
    workflow.add_edge("summarize_news", "analyze_price")
    workflow.add_edge("analyze_price", "market_context")
    workflow.add_edge("market_context", "synthesize_summary")
    workflow.add_edge("synthesize_summary", END)

    # Compile the graph
    return workflow.compile()


def summarize_financial_data(
    ticker: str,
    news_articles: List[Dict[str, Any]],
    time_series_data: Dict[str, Any],
    market_news: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, str]:
    """
    Main function to summarize financial news and data using LangChain/LangGraph.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        news_articles: List of news articles from crawler
        time_series_data: Time series price data from crawler
        market_news: Optional list of broader market news articles

    Returns:
        Dictionary containing:
        - news_summary: Summary of news articles
        - price_analysis: Analysis of price data
        - market_context: Summary of market news
        - final_summary: Comprehensive final summary
    """
    # Initialize state
    initial_state = FinancialDataState(
        ticker=ticker,
        news_articles=news_articles or [],
        time_series_data=time_series_data or {},
        market_news=market_news or [],
        news_summary="",
        price_analysis="",
        market_context="",
        final_summary=""
    )

    # Create and run the graph
    graph = create_financial_summary_graph()
    result = graph.invoke(initial_state)

    return {
        "news_summary": result['news_summary'],
        "price_analysis": result['price_analysis'],
        "market_context": result['market_context'],
        "final_summary": result['final_summary']
    }


def summarize_news_only(
    news_articles: List[Dict[str, Any]],
    ticker: Optional[str] = None
) -> str:
    """
    Simplified function to summarize only news articles.

    Args:
        news_articles: List of news articles from crawler
        ticker: Optional ticker symbol for context

    Returns:
        String containing news summary
    """
    try:
        llm = get_llm(temperature=0.3)
    except ValueError as e:
        return f"Error: {str(e)}"

    # Get prompt from centralized prompts module
    prompt = get_news_analysis_prompt()

    chain = prompt | llm | StrOutputParser()
    news_text = format_news_articles(news_articles, ticker)

    try:
        return chain.invoke({
            "news_text": news_text,
            "ticker": ticker if ticker else "the stock"
        })
    except Exception as e:
        return f"Error generating summary: {str(e)}"


# Example usage
if __name__ == "__main__":
    from .crawler import crawl_stock_news, crawl_stock_daily_time_series, crawl_market_news

    # Example ticker
    ticker = "AAPL"

    print("=" * 80)
    print(f"FINANCIAL SUMMARY FOR {ticker}")
    print("=" * 80)

    # Fetch data using crawler functions
    print("\nFetching news articles...")
    news_articles = crawl_stock_news(ticker, num_articles=2)

    print("Fetching time series data...")
    time_series_data = crawl_stock_daily_time_series(ticker)

    print("Fetching market news...")
    market_news = crawl_market_news(num_articles=2)

    # Generate comprehensive summary
    print("\nGenerating AI-powered summary...\n")
    summary = summarize_financial_data(
        ticker=ticker,
        news_articles=news_articles,
        time_series_data=time_series_data,
        market_news=market_news
    )

    # Print results
    print("\n" + "=" * 80)
    print("FINAL COMPREHENSIVE SUMMARY")
    print("=" * 80)
    print(summary['final_summary'])

    print("\n" + "=" * 80)
    print("DETAILED ANALYSES")
    print("=" * 80)

    print("\n--- News Summary ---")
    print(summary['news_summary'])

    print("\n--- Price Analysis ---")
    print(summary['price_analysis'])

    print("\n--- Market Context ---")
    print(summary['market_context'])
