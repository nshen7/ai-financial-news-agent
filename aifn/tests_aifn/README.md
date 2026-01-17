# Test Suite for AI Financial News Agent

This directory contains comprehensive tests for the main functions in the AI Financial News Agent.

## Test Scripts

### 1. test_daily_analysis.py
Tests the `daily_analysis` function from main.py

**Tests included:**
- Daily analysis with RAG database saving (NVDA)
- Daily analysis without RAG saving (AAPL)
- Multiple tickers analysis (MSFT, TSLA)

**Output:** Results saved to `daily_analysis_test_output.txt`

### 2. test_reflection.py
Tests the `periodic_reflection` function from main.py

**Tests included:**
- Weekly reflection for single ticker (NVDA)
- Monthly reflection for single ticker (AAPL)
- Custom period reflection (MSFT, 14 days)
- Portfolio-wide reflection (all tickers)
- Quarterly reflection (TSLA)
- Multiple tickers reflection (NVDA, AAPL)

**Output:** Results saved to `reflection_test_output.txt`

## Running Tests

### Prerequisites
Make sure you have installed all dependencies using Poetry:
```bash
poetry install
```

### Run All Tests (Default)
```bash
# Run all daily analysis tests
poetry run python -m aifn.tests_aifn.test_daily_analysis

# Run all reflection tests
poetry run python -m aifn.tests_aifn.test_reflection
```

### Run Specific Tests
```bash
# Run test 1 from daily analysis
poetry run python -m aifn.tests_aifn.test_daily_analysis 1

# Run test 3 from reflection
poetry run python -m aifn.tests_aifn.test_reflection 3
```

### Test Options

**test_daily_analysis.py:**
- `1` - Daily Analysis with RAG save
- `2` - Daily Analysis without RAG save
- `3` - Multiple tickers analysis
- `4` - Run all tests (default)

**test_reflection.py:**
- `1` - Weekly reflection - single ticker
- `2` - Monthly reflection - single ticker
- `3` - Custom period reflection
- `4` - Portfolio reflection (all tickers)
- `5` - Quarterly reflection
- `6` - Multiple tickers reflection
- `7` - Run all tests (default)

## Output Files

Test results are automatically saved to:
- `daily_analysis_test_output.txt` - Output from daily analysis tests
- `reflection_test_output.txt` - Output from reflection tests

These files contain the complete console output including:
- Test execution details
- Analysis results
- Error messages (if any)
- Test summary

## Known Issues

### NumPy 2.0 Compatibility Warning
There's a known compatibility issue between ChromaDB and NumPy 2.0 that produces the following warning:
```
⚠️  Could not save to RAG: `np.float_` was removed in the NumPy 2.0 release. Use `np.float64` instead.
```

**Impact:** This prevents saving results to the RAG database but does not affect the core analysis functionality.

**Workaround:** If you need RAG database functionality, you can downgrade NumPy:
```bash
poetry add "numpy<2.0"
```

### Python Version Warning
You may see a FutureWarning about Python 3.10 support from Google API. This is informational and does not affect functionality.

## Test Customization

You can modify the test scripts to:
- Change ticker symbols
- Adjust number of articles fetched
- Modify time periods for reflection
- Add new test cases

Simply edit the respective test file and run again.
