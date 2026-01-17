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
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# Import prompts from centralized prompts module
from .prompts import (
    get_news_analysis_prompt,
    get_price_analysis_prompt,
    get_synthesis_prompt,
    get_pattern_analysis_prompt,
    get_sentiment_evolution_prompt,
    get_key_events_prompt,
    get_investment_thesis_prompt,
    get_risk_assessment_prompt
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
    """
    State for the financial analysis workflow.

    The 'target' field can be:
    - A stock ticker (e.g., 'AAPL', 'GOOGL')
    - A market topic (e.g., 'market:general', 'market:crypto', 'topic:fed_policy')

    This allows the same workflow to process both ticker-specific news/data
    and general market news without redundancy.
    """
    target: str
    news_articles: List[Dict[str, Any]]
    time_series_data: Optional[Dict[str, Any]]  # Optional: market topics won't have price data
    temperature: float  # Temperature for LLM response generation
    news_summary: str
    price_analysis: str
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
        llm = get_llm(temperature=state.get('temperature', 0.3))
    except ValueError as e:
        state['news_summary'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_news_analysis_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Format and process news - pass target only if it's a ticker (not a market topic)
    target = state['target']
    ticker_for_format = target if not target.startswith('market:') and not target.startswith('topic:') else None
    news_text = format_news_articles(state['news_articles'], ticker_for_format)

    try:
        state['news_summary'] = chain.invoke({
            "news_text": news_text,
            "ticker": target
        })
    except Exception as e:
        state['news_summary'] = f"Error generating news summary: {str(e)}"

    return state


def analyze_price_node(state: FinancialDataState) -> FinancialDataState:
    """
    LangGraph node to analyze price data using LLM.
    Skips analysis if no time series data is available (e.g., for market topics).

    Args:
        state: Current workflow state

    Returns:
        Updated state with price analysis
    """
    # Skip price analysis for market topics or if no data available
    if not state.get('time_series_data'):
        state['price_analysis'] = "No price data available for this target."
        return state

    try:
        llm = get_llm(temperature=state.get('temperature', 0.3))
    except ValueError as e:
        state['price_analysis'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_price_analysis_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    # Format and process time series data
    price_text = format_time_series_data(state['time_series_data'], state['target'])

    # Calculate number of days of data
    n_days = len(state['time_series_data']) if state['time_series_data'] else 0

    try:
        state['price_analysis'] = chain.invoke({
            "price_text": price_text,
            "ticker": state['target'],
            "n": n_days
        })
    except Exception as e:
        state['price_analysis'] = f"Error generating price analysis: {str(e)}"

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
        llm = get_llm(temperature=state.get('temperature', 0.3))
    except ValueError as e:
        state['final_summary'] = f"Error: {str(e)}"
        return state

    # Get prompt from centralized prompts module
    prompt = get_synthesis_prompt()

    # Create chain
    chain = prompt | llm | StrOutputParser()

    try:
        state['final_summary'] = chain.invoke({
            "ticker": state['target'],
            "news_summary": state.get('news_summary', 'No news analysis available.'),
            "price_analysis": state.get('price_analysis', 'No price analysis available.'),
            "market_context": ""  # No longer a separate field
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
    workflow.add_node("synthesize_summary", synthesize_final_summary_node)

    # Define edges (workflow flow)
    workflow.set_entry_point("summarize_news")
    workflow.add_edge("summarize_news", "analyze_price")
    workflow.add_edge("analyze_price", "synthesize_summary")
    workflow.add_edge("synthesize_summary", END)

    # Compile the graph
    return workflow.compile()


def summarize_financial_data(
    target: str,
    news_articles: List[Dict[str, Any]],
    time_series_data: Optional[Dict[str, Any]] = None,
    temperature: float = 0.3
) -> Dict[str, str]:
    """
    Main function to summarize financial news and data using LangChain/LangGraph.

    Args:
        target: Target identifier - either a stock ticker (e.g., 'AAPL') or
                a market topic (e.g., 'market:general', 'market:crypto')
        news_articles: List of news articles from crawler
        time_series_data: Optional time series price data (only for tickers, not market topics)
        temperature: Temperature for LLM response generation (0.0-1.0)

    Returns:
        Dictionary containing:
        - news_summary: Summary of news articles
        - price_analysis: Analysis of price data (if available)
        - final_summary: Comprehensive final summary

    Examples:
        # For a stock ticker with price data
        summarize_financial_data(
            target="AAPL",
            news_articles=aapl_news,
            time_series_data=aapl_prices
        )

        # For general market news without price data
        summarize_financial_data(
            target="market:general",
            news_articles=market_news
        )
    """
    # Initialize state
    initial_state = FinancialDataState(
        target=target,
        news_articles=news_articles or [],
        time_series_data=time_series_data,
        temperature=temperature,
        news_summary="",
        price_analysis="",
        final_summary=""
    )

    # Create and run the graph
    graph = create_financial_summary_graph()
    result = graph.invoke(initial_state)

    return {
        "news_summary": result['news_summary'],
        "price_analysis": result['price_analysis'],
        "final_summary": result['final_summary']
    }


def summarize_news_only(
    news_articles: List[Dict[str, Any]],
    target: Optional[str] = None,
    temperature: float = 0.3
) -> str:
    """
    Simplified function to summarize only news articles.

    Args:
        news_articles: List of news articles from crawler
        target: Optional target identifier (ticker or market topic)
        temperature: Temperature for LLM response generation (0.0-1.0)

    Returns:
        String containing news summary
    """
    try:
        llm = get_llm(temperature=temperature)
    except ValueError as e:
        return f"Error: {str(e)}"

    # Get prompt from centralized prompts module
    prompt = get_news_analysis_prompt()

    chain = prompt | llm | StrOutputParser()

    # Only pass ticker to format_news_articles if it's actually a ticker
    ticker_for_format = None
    if target and not target.startswith('market:') and not target.startswith('topic:'):
        ticker_for_format = target

    news_text = format_news_articles(news_articles, ticker_for_format)

    try:
        return chain.invoke({
            "news_text": news_text,
            "ticker": target if target else "the target"
        })
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def reflect_on_period(
    period_summaries: List[Dict[str, Any]],
    target: Optional[str] = None,
    period_type: str = "week",
    temperature: float = 0.3
) -> Dict[str, str]:
    """
    Periodic reflection on historical analyses to identify patterns and trends.
    Call this weekly/monthly to synthesize insights from daily analyses.

    Args:
        period_summaries: List of daily summaries from the period, each with:
            - date: Date of analysis
            - target: Target identifier (ticker or market topic)
            - final_summary: The daily summary
            - metadata: Optional additional data
        target: Optional target identifier. If None, reflects on all targets.
        period_type: Type of period ("week", "month", "quarter")
        temperature: Temperature for LLM response generation (0.0-1.0)

    Returns:
        Dictionary containing:
        - period_info: Actual date range analyzed
        - pattern_analysis: Identified patterns and trends
        - sentiment_evolution: How sentiment changed over time
        - key_events: Most significant events during period
        - investment_thesis: Updated investment perspective
        - risk_assessment: Key risks identified
    """
    try:
        llm = get_llm(temperature=temperature)
    except ValueError as e:
        return {
            "period_info": "",
            "pattern_analysis": f"Error: {str(e)}",
            "sentiment_evolution": "",
            "key_events": "",
            "investment_thesis": "",
            "risk_assessment": ""
        }

    if not period_summaries:
        return {
            "period_info": "No data available",
            "pattern_analysis": "No summaries found for analysis",
            "sentiment_evolution": "",
            "key_events": "",
            "investment_thesis": "",
            "risk_assessment": ""
        }

    # Extract actual period information from summaries
    dates = [s.get('date') for s in period_summaries if s.get('date')]
    start_date = min(dates) if dates else 'Unknown'
    end_date = max(dates) if dates else 'Unknown'
    num_days = len(set(dates))

    # Get unique targets in the period
    targets = sorted(set([s.get('target', 'N/A') for s in period_summaries if s.get('target')]))

    # Format period info
    if target:
        period_info = f"Period: {start_date} to {end_date} ({num_days} days) for {target}"
        analysis_target = target
    else:
        targets_list = ', '.join(targets[:5])
        if len(targets) > 5:
            targets_list += f" and {len(targets) - 5} others"
        period_info = f"Period: {start_date} to {end_date} ({num_days} days) across {len(targets)} targets: {targets_list}"
        analysis_target = "the portfolio"

    # Format the historical summaries with target information
    summaries_text = "\n\n".join([
        f"Date: {s.get('date', 'Unknown')} | Target: {s.get('target', 'N/A')}\n{s.get('final_summary', '')}"
        for s in period_summaries
    ])

    # Get prompts from centralized prompts module
    pattern_prompt = get_pattern_analysis_prompt(analysis_target, period_type)
    sentiment_prompt = get_sentiment_evolution_prompt(analysis_target, period_type)
    events_prompt = get_key_events_prompt(analysis_target, period_type)
    thesis_prompt = get_investment_thesis_prompt(analysis_target, period_type)
    risk_prompt = get_risk_assessment_prompt(analysis_target, period_type)

    # Execute all analyses
    result = {"period_info": period_info}

    try:
        pattern_chain = pattern_prompt | llm | StrOutputParser()
        result['pattern_analysis'] = pattern_chain.invoke({
            "ticker": analysis_target,
            "period_type": period_type,
            "summaries_text": summaries_text
        })
    except Exception as e:
        result['pattern_analysis'] = f"Error: {str(e)}"

    try:
        sentiment_chain = sentiment_prompt | llm | StrOutputParser()
        result['sentiment_evolution'] = sentiment_chain.invoke({
            "ticker": analysis_target,
            "period_type": period_type,
            "summaries_text": summaries_text
        })
    except Exception as e:
        result['sentiment_evolution'] = f"Error: {str(e)}"

    try:
        events_chain = events_prompt | llm | StrOutputParser()
        result['key_events'] = events_chain.invoke({
            "ticker": analysis_target,
            "period_type": period_type,
            "summaries_text": summaries_text
        })
    except Exception as e:
        result['key_events'] = f"Error: {str(e)}"

    try:
        thesis_chain = thesis_prompt | llm | StrOutputParser()
        result['investment_thesis'] = thesis_chain.invoke({
            "ticker": analysis_target,
            "period_type": period_type,
            "summaries_text": summaries_text
        })
    except Exception as e:
        result['investment_thesis'] = f"Error: {str(e)}"

    try:
        risk_chain = risk_prompt | llm | StrOutputParser()
        result['risk_assessment'] = risk_chain.invoke({
            "ticker": analysis_target,
            "period_type": period_type,
            "summaries_text": summaries_text
        })
    except Exception as e:
        result['risk_assessment'] = f"Error: {str(e)}"

    return result


# Example usage
if __name__ == "__main__":
    from .crawler import crawl_stock_news, crawl_stock_daily_time_series, crawl_market_news

    # Example 1: Stock ticker with price data
    ticker = "AAPL"

    print("=" * 80)
    print(f"EXAMPLE 1: FINANCIAL SUMMARY FOR {ticker}")
    print("=" * 80)

    # Fetch data using crawler functions
    print("\nFetching news articles...")
    news_articles = crawl_stock_news(ticker, num_articles=2)

    print("Fetching time series data...")
    time_series_data = crawl_stock_daily_time_series(ticker)

    # Generate comprehensive summary for ticker
    print("\nGenerating AI-powered summary for ticker...\n")
    ticker_summary = summarize_financial_data(
        target=ticker,
        news_articles=news_articles,
        time_series_data=time_series_data
    )

    # Print results
    print("\n" + "=" * 80)
    print("FINAL COMPREHENSIVE SUMMARY")
    print("=" * 80)
    print(ticker_summary['final_summary'])

    print("\n" + "=" * 80)
    print("DETAILED ANALYSES")
    print("=" * 80)

    print("\n--- News Summary ---")
    print(ticker_summary['news_summary'])

    print("\n--- Price Analysis ---")
    print(ticker_summary['price_analysis'])

    # Example 2: Market news (no price data)
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: MARKET NEWS SUMMARY")
    print("=" * 80)

    print("\nFetching market news...")
    market_news = crawl_market_news(num_articles=2)

    # Generate summary for market news
    print("\nGenerating AI-powered summary for market news...\n")
    market_summary = summarize_financial_data(
        target="market:general",
        news_articles=market_news
    )

    print("\n" + "=" * 80)
    print("MARKET NEWS SUMMARY")
    print("=" * 80)
    print(market_summary['final_summary'])
