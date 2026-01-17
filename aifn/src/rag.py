from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from typing import Optional, Dict, Any
from datetime import datetime

# Initialize embeddings model
embeddings = VertexAIEmbeddings(model_name="gemini-embedding-001")

def store_embedding(
    summary: str,
    date: str,
    ticker: Optional[str] = None,
    macro_category: Optional[str] = None,
    sentiment_score: Optional[float] = None,
    price_change: Optional[float] = None,
    additional_metadata: Optional[Dict[str, Any]] = None,
    persist_directory: str = "./chroma_db"
) -> Chroma:
    """
    Store daily summary as embeddings in ChromaDB with metadata.

    Args:
        summary: The daily news summary text to embed
        date: Date of the summary (format: YYYY-MM-DD)
        ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
        macro_category: Macro economic category (e.g., 'inflation', 'gdp', 'employment')
        sentiment_score: Sentiment score (-1.0 to 1.0)
        price_change: Time series price change percentage
        additional_metadata: Any additional metadata to store
        persist_directory: Directory to persist ChromaDB data

    Returns:
        Chroma: The vector store instance
    """
    # Build metadata dictionary
    metadata = {
        "date": date,
        "timestamp": datetime.now().isoformat(),
    }

    # Add ticker or macro category
    if ticker:
        metadata["ticker"] = ticker.upper()
        metadata["category"] = "stock"
    elif macro_category:
        metadata["macro_category"] = macro_category
        metadata["category"] = "macro"

    # Add optional metrics
    if sentiment_score is not None:
        metadata["sentiment_score"] = sentiment_score

    if price_change is not None:
        metadata["price_change"] = price_change

    # Add any additional metadata
    if additional_metadata:
        metadata.update(additional_metadata)

    # Create document with summary and metadata
    document = Document(
        page_content=summary,
        metadata=metadata
    )

    # Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=[document],
        embedding=embeddings,
        persist_directory=persist_directory
    )

    return vectorstore


def search_historical_analyses(
    query: str,
    ticker: Optional[str] = None,
    k: int = 5,
    date_range: Optional[tuple[str, str]] = None,
    persist_directory: str = "./chroma_db"
) -> list[Dict[str, Any]]:
    """
    Search for similar historical analyses from ChromaDB.

    Args:
        query: Search query (e.g., "similar price drops", "earnings surprises")
        ticker: Optional ticker to filter by
        k: Number of results to return
        date_range: Optional tuple of (start_date, end_date) in YYYY-MM-DD format
        persist_directory: Directory where ChromaDB data is persisted

    Returns:
        List of dictionaries containing:
        - content: The summary text
        - metadata: Associated metadata (date, ticker, sentiment, etc.)
        - score: Similarity score
    """
    try:
        # Load existing ChromaDB
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

        # Build filter if ticker specified
        filter_dict = None
        if ticker:
            filter_dict = {"ticker": ticker.upper()}

        # Perform similarity search
        results = vectorstore.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter_dict
        )

        # Format results
        formatted_results = []
        for doc, score in results:
            # Filter by date range if specified
            if date_range:
                doc_date = doc.metadata.get('date', '')
                if not (date_range[0] <= doc_date <= date_range[1]):
                    continue

            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': float(score)
            })

        return formatted_results

    except Exception as e:
        print(f"Error searching historical analyses: {e}")
        return []


def retrieve_summaries_period(
    start_date: str,
    end_date: str,
    ticker: Optional[str] = None,
    k: int = 50,
    persist_directory: str = "./chroma_db"
) -> list[Dict[str, Any]]:
    """
    Retrieve all daily summaries within a date range.
    Useful for periodic reflection (weekly/monthly reviews).

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        ticker: Optional stock ticker symbol. If None, retrieves all tickers.
        k: Number of results to retrieve from vector store
        persist_directory: Directory where ChromaDB data is persisted

    Returns:
        List of summaries sorted by date, each containing:
        - date: The date
        - ticker: The ticker symbol (if applicable)
        - final_summary: The summary text
        - metadata: Additional metadata (sentiment, price change, etc.)
    """
    try:
        # Load existing ChromaDB
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

        # Build filter for ticker if specified
        filter_dict = None
        if ticker:
            filter_dict = {"ticker": ticker.upper()}
            query = f"{ticker} analysis"
        else:
            query = "financial analysis"

        # Get all documents for the period
        # We use a broad query to get all documents, then filter by date
        results = vectorstore.similarity_search(
            query=query,
            k=k,
            filter=filter_dict
        )

        # Filter by date range and format
        summaries = []
        for doc in results:
            doc_date = doc.metadata.get('date', '')
            if start_date <= doc_date <= end_date:
                # Skip reflection summaries (only get daily analyses)
                analysis_type = doc.metadata.get('analysis_type', 'daily')
                if 'reflection' in analysis_type:
                    continue

                summaries.append({
                    'date': doc_date,
                    'ticker': doc.metadata.get('ticker', 'N/A'),
                    'final_summary': doc.page_content,
                    'metadata': doc.metadata
                })

        # Sort by date, then by ticker
        summaries.sort(key=lambda x: (x['date'], x['ticker']))

        return summaries

    except Exception as e:
        print(f"Error retrieving period summaries: {e}")
        return []