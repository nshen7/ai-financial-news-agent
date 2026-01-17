"""
Test script for the daily_analysis function from main.py.

This script tests the daily financial analysis workflow, which includes:
- Fetching stock news
- Fetching price data
- Fetching market context
- Running AI analysis
- Saving to RAG database

Results are saved to daily_analysis_test_output.txt
"""

from datetime import datetime
from pathlib import Path
from aifn.src.main import daily_analysis


def test_daily_analysis_with_save():
    """Test daily analysis with RAG database saving enabled."""
    ticker = "NVDA"
    num_articles = 5  # Reduced for faster testing

    print("=" * 80)
    print(f"DAILY ANALYSIS TEST (WITH RAG SAVE) FOR {ticker}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Number of articles: {num_articles}")
    print(f"Save to RAG: True")
    print()

    try:
        daily_analysis(ticker, num_articles=num_articles, save_to_rag=True)
        print("\n✓ Daily analysis with RAG save completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during daily analysis with RAG save: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_daily_analysis_without_save():
    """Test daily analysis without saving to RAG database."""
    ticker = "AAPL"
    num_articles = 10  # Reduced for faster testing

    print("\n" + "=" * 80)
    print(f"DAILY ANALYSIS TEST (WITHOUT RAG SAVE) FOR {ticker}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Number of articles: {num_articles}")
    print(f"Save to RAG: False")
    print()

    try:
        daily_analysis(ticker, num_articles=num_articles, save_to_rag=False)
        print("\n✓ Daily analysis without RAG save completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during daily analysis without RAG save: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_daily_analysis_multiple_tickers():
    """Test daily analysis for multiple tickers."""
    tickers = ["MSFT", "TSLA"]
    num_articles = 5  # Reduced for faster testing

    print("\n" + "=" * 80)
    print(f"DAILY ANALYSIS TEST FOR MULTIPLE TICKERS")
    print("=" * 80)
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Number of articles per ticker: {num_articles}")
    print()

    results = {}
    for ticker in tickers:
        print(f"\n--- Testing {ticker} ---")
        try:
            daily_analysis(ticker, num_articles=num_articles, save_to_rag=True)
            results[ticker] = "SUCCESS"
            print(f"✓ {ticker} analysis completed successfully!")
        except Exception as e:
            results[ticker] = f"FAILED: {e}"
            print(f"❌ {ticker} analysis failed: {e}")

    # Summary
    print("\n" + "=" * 80)
    print("MULTI-TICKER TEST SUMMARY")
    print("=" * 80)
    for ticker, result in results.items():
        print(f"{ticker}: {result}")

    return all(r == "SUCCESS" for r in results.values())


def run_all_tests():
    """Run all daily analysis tests and save output to file."""
    # Prepare output file
    output_dir = Path(__file__).parent
    output_file = output_dir / "daily_analysis_test_output.txt"

    # Redirect stdout to both console and file
    import sys
    from io import StringIO

    # Create a custom writer that writes to both stdout and a string buffer
    buffer = StringIO()
    original_stdout = sys.stdout

    class DualWriter:
        def __init__(self, *writers):
            self.writers = writers

        def write(self, text):
            for writer in self.writers:
                writer.write(text)

        def flush(self):
            for writer in self.writers:
                writer.flush()

    sys.stdout = DualWriter(original_stdout, buffer)

    print("=" * 80)
    print("DAILY ANALYSIS TEST SUITE")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output will be saved to: {output_file}")
    print("=" * 80)
    print()

    results = {}

    # Run tests
    print("\n[TEST 1/3] Daily Analysis with RAG Save")
    print("-" * 80)
    results['with_save'] = test_daily_analysis_with_save()

    print("\n[TEST 2/3] Daily Analysis without RAG Save")
    print("-" * 80)
    results['without_save'] = test_daily_analysis_without_save()

    print("\n[TEST 3/3] Multiple Tickers Analysis")
    print("-" * 80)
    results['multiple_tickers'] = test_daily_analysis_multiple_tickers()

    # Final summary
    print("\n" + "=" * 80)
    print("FINAL TEST SUMMARY")
    print("=" * 80)
    print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Test Results:")
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "❌ FAILED"
        print(f"  {test_name}: {status}")

    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    print()
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    print("=" * 80)

    # Restore stdout and save to file
    sys.stdout = original_stdout

    with open(output_file, 'w') as f:
        f.write(buffer.getvalue())

    print(f"\n✓ Test output saved to: {output_file}")

    return all(results.values())


if __name__ == "__main__":
    import sys

    print("Daily Analysis Test Suite")
    print("=" * 80)
    print("\nAvailable tests:")
    print("1. Daily Analysis with RAG save")
    print("2. Daily Analysis without RAG save")
    print("3. Multiple tickers analysis")
    print("4. Run all tests (default)")
    print()

    test_choice = sys.argv[1] if len(sys.argv) > 1 else "4"

    try:
        if test_choice == "1":
            test_daily_analysis_with_save()
        elif test_choice == "2":
            test_daily_analysis_without_save()
        elif test_choice == "3":
            test_daily_analysis_multiple_tickers()
        elif test_choice == "4":
            success = run_all_tests()
            sys.exit(0 if success else 1)
        else:
            print("Invalid test choice. Running all tests...")
            success = run_all_tests()
            sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
