"""
Test script for the periodic_reflection function from main.py.

This script tests the periodic reflection workflow, which includes:
- Retrieving historical analyses from RAG database
- Running reflection analysis on the period
- Generating pattern analysis, sentiment evolution, key events, investment thesis, and risk assessment
- Saving reflection to RAG database

Results are saved to reflection_test_output.txt
"""

from datetime import datetime
from pathlib import Path
from aifn.src.main import periodic_reflection


def test_weekly_reflection_single_ticker():
    """Test weekly reflection for a single ticker."""
    ticker = "NVDA"
    period = "week"

    print("=" * 80)
    print(f"WEEKLY REFLECTION TEST FOR {ticker}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ticker: {ticker}")
    print(f"Period: {period}")
    print()

    try:
        periodic_reflection(ticker=ticker, period=period)
        print("\n✓ Weekly reflection for single ticker completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during weekly reflection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_monthly_reflection_single_ticker():
    """Test monthly reflection for a single ticker."""
    ticker = "AAPL"
    period = "month"

    print("\n" + "=" * 80)
    print(f"MONTHLY REFLECTION TEST FOR {ticker}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ticker: {ticker}")
    print(f"Period: {period}")
    print()

    try:
        periodic_reflection(ticker=ticker, period=period)
        print("\n✓ Monthly reflection for single ticker completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during monthly reflection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_custom_period_reflection():
    """Test reflection with custom number of days."""
    ticker = "MSFT"
    period = "week"
    num_days = 7  # Custom 2-week period

    print("\n" + "=" * 80)
    print(f"CUSTOM PERIOD REFLECTION TEST FOR {ticker}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ticker: {ticker}")
    print(f"Period: {period} (custom: {num_days} days)")
    print()

    try:
        periodic_reflection(ticker=ticker, period=period, num_days=num_days)
        print("\n✓ Custom period reflection completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during custom period reflection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_portfolio_reflection():
    """Test portfolio-wide reflection (all tickers)."""
    period = "week"

    print("\n" + "=" * 80)
    print(f"PORTFOLIO REFLECTION TEST")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ticker: ALL (portfolio-wide)")
    print(f"Period: {period}")
    print()

    try:
        periodic_reflection(ticker=None, period=period)
        print("\n✓ Portfolio reflection completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during portfolio reflection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_quarter_reflection():
    """Test quarterly reflection for a ticker."""
    ticker = "TSLA"
    period = "quarter"

    print("\n" + "=" * 80)
    print(f"QUARTERLY REFLECTION TEST FOR {ticker}")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Ticker: {ticker}")
    print(f"Period: {period}")
    print()

    try:
        periodic_reflection(ticker=ticker, period=period)
        print("\n✓ Quarterly reflection completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Error during quarterly reflection: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_tickers_reflection():
    """Test reflection for multiple tickers sequentially."""
    tickers = ["NVDA", "AAPL"]
    period = "week"

    print("\n" + "=" * 80)
    print(f"MULTIPLE TICKERS REFLECTION TEST")
    print("=" * 80)
    print(f"Tickers: {', '.join(tickers)}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Period: {period}")
    print()

    results = {}
    for ticker in tickers:
        print(f"\n--- Reflecting on {ticker} ---")
        try:
            periodic_reflection(ticker=ticker, period=period)
            results[ticker] = "SUCCESS"
            print(f"✓ {ticker} reflection completed successfully!")
        except Exception as e:
            results[ticker] = f"FAILED: {e}"
            print(f"❌ {ticker} reflection failed: {e}")

    # Summary
    print("\n" + "=" * 80)
    print("MULTI-TICKER REFLECTION SUMMARY")
    print("=" * 80)
    for ticker, result in results.items():
        print(f"{ticker}: {result}")

    return all(r == "SUCCESS" for r in results.values())


def run_all_tests():
    """Run all reflection tests and save output to file."""
    # Prepare output file
    output_dir = Path(__file__).parent
    output_file = output_dir / "reflection_test_output.txt"

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
    print("PERIODIC REFLECTION TEST SUITE")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output will be saved to: {output_file}")
    print("=" * 80)
    print()

    results = {}

    # Run tests
    print("\n[TEST 1/6] Weekly Reflection - Single Ticker")
    print("-" * 80)
    results['weekly_single'] = test_weekly_reflection_single_ticker()

    print("\n[TEST 2/6] Monthly Reflection - Single Ticker")
    print("-" * 80)
    results['monthly_single'] = test_monthly_reflection_single_ticker()

    print("\n[TEST 3/6] Custom Period Reflection")
    print("-" * 80)
    results['custom_period'] = test_custom_period_reflection()

    print("\n[TEST 4/6] Portfolio Reflection")
    print("-" * 80)
    results['portfolio'] = test_portfolio_reflection()

    print("\n[TEST 5/6] Quarterly Reflection")
    print("-" * 80)
    results['quarterly'] = test_quarter_reflection()

    print("\n[TEST 6/6] Multiple Tickers Reflection")
    print("-" * 80)
    results['multiple_tickers'] = test_multiple_tickers_reflection()

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

    print("Periodic Reflection Test Suite")
    print("=" * 80)
    print("\nAvailable tests:")
    print("1. Weekly reflection - single ticker")
    print("2. Monthly reflection - single ticker")
    print("3. Custom period reflection")
    print("4. Portfolio reflection (all tickers)")
    print("5. Quarterly reflection")
    print("6. Multiple tickers reflection")
    print("7. Run all tests (default)")
    print()

    test_choice = sys.argv[1] if len(sys.argv) > 1 else "7"

    try:
        if test_choice == "1":
            test_weekly_reflection_single_ticker()
        elif test_choice == "2":
            test_monthly_reflection_single_ticker()
        elif test_choice == "3":
            test_custom_period_reflection()
        elif test_choice == "4":
            test_portfolio_reflection()
        elif test_choice == "5":
            test_quarter_reflection()
        elif test_choice == "6":
            test_multiple_tickers_reflection()
        elif test_choice == "7":
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
