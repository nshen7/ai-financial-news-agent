# Prompts Guide - Customizing Financial Analysis

All LLM prompts are centralized in [aifn/src/prompts.py](aifn/src/prompts.py) for easy customization and maintenance.

---

## 📚 Available Prompts

### Standard Prompts

| Prompt Name | Function | Purpose |
|-------------|----------|---------|
| `news_analysis` | `get_news_analysis_prompt()` | Analyze news articles for themes, sentiment, events |
| `price_analysis` | `get_price_analysis_prompt()` | Technical analysis of price data |
| `market_context` | `get_market_context_prompt()` | Macroeconomic and market trends |
| `synthesis` | `get_synthesis_prompt()` | Combine all analyses into final report |

### Alternative Prompts

| Prompt Name | Function | Purpose |
|-------------|----------|---------|
| `concise_news` | `get_concise_news_prompt()` | Brief, bullet-point news summary |
| `risk_focused` | `get_risk_focused_prompt()` | Focus on risks and red flags |
| `opportunity_focused` | `get_opportunity_focused_prompt()` | Focus on growth opportunities |

---

## 🎯 Basic Usage

### Using Standard Prompts

The system uses standard prompts by default:

```python
from aifn.src.summary import summarize_financial_data
from aifn.src.crawler import crawl_stock_news, crawl_stock_daily_time_series

# Uses standard prompts automatically
result = summarize_financial_data(
    ticker="AAPL",
    news_articles=crawl_stock_news("AAPL", 5),
    time_series_data=crawl_stock_daily_time_series("AAPL"),
    market_news=[]
)
```

### Accessing Prompts Directly

```python
from aifn.src.prompts import (
    get_news_analysis_prompt,
    get_price_analysis_prompt,
    get_market_context_prompt,
    get_synthesis_prompt
)

# Get a prompt template
news_prompt = get_news_analysis_prompt()

# Use with LLM
from aifn.src.summary import get_llm
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()
chain = news_prompt | llm | StrOutputParser()

result = chain.invoke({"news_text": "Your news text here..."})
```

### Using Alternative Prompts

```python
from aifn.src.prompts import get_risk_focused_prompt
from aifn.src.summary import get_llm
from langchain_core.output_parsers import StrOutputParser

# Use risk-focused analysis
llm = get_llm()
risk_prompt = get_risk_focused_prompt()
chain = risk_prompt | llm | StrOutputParser()

result = chain.invoke({"news_text": "Your news text..."})
```

---

## 🔧 Customizing Prompts

### Method 1: Edit Existing Prompts

Open [aifn/src/prompts.py](aifn/src/prompts.py) and modify the prompt constants:

```python
# In prompts.py
NEWS_ANALYSIS_SYSTEM_PROMPT = """You are a financial analyst expert.
Analyze the provided news articles and create a concise summary...

[Your custom instructions here]
"""
```

### Method 2: Create Custom Prompts

Use the helper functions to create custom prompts:

```python
from aifn.src.prompts import create_custom_news_prompt

# Create a custom prompt for your specific use case
my_prompt = create_custom_news_prompt(
    system_instructions="""
    You are a cryptocurrency analyst focusing on DeFi news.
    Analyze articles with emphasis on:
    1. Blockchain technology developments
    2. DeFi protocol changes
    3. Regulatory implications
    4. Market sentiment in crypto space

    Be technical and focus on protocol-level details.
    """
)

# Use your custom prompt
from aifn.src.summary import get_llm
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()
chain = my_prompt | llm | StrOutputParser()
result = chain.invoke({"news_text": "Your crypto news..."})
```

### Method 3: Add to Prompt Registry

Add your custom prompt to the registry in [prompts.py](aifn/src/prompts.py):

```python
# In prompts.py

# Define your prompt
CRYPTO_FOCUSED_SYSTEM_PROMPT = """You are a crypto analyst..."""

def get_crypto_focused_prompt() -> ChatPromptTemplate:
    """Get crypto-focused analysis prompt."""
    return ChatPromptTemplate.from_messages([
        ("system", CRYPTO_FOCUSED_SYSTEM_PROMPT),
        ("user", NEWS_ANALYSIS_USER_PROMPT)
    ])

# Add to registry
PROMPT_REGISTRY = {
    # ... existing prompts ...
    "crypto_focused": get_crypto_focused_prompt,
}
```

Then use it:

```python
from aifn.src.prompts import get_prompt

crypto_prompt = get_prompt("crypto_focused")
```

---

## 📋 Prompt Examples

### Example 1: Sentiment-Only Analysis

```python
from aifn.src.prompts import create_custom_news_prompt

sentiment_prompt = create_custom_news_prompt(
    system_instructions="""
    You are a sentiment analysis expert. Analyze the news and provide:
    1. Overall sentiment (bullish/bearish/neutral)
    2. Sentiment score (-1 to +1)
    3. Key phrases indicating sentiment
    4. Sentiment trend (improving/declining/stable)

    Focus ONLY on sentiment, ignore other factors.
    """
)
```

### Example 2: ESG-Focused Analysis

```python
from aifn.src.prompts import create_custom_news_prompt

esg_prompt = create_custom_news_prompt(
    system_instructions="""
    You are an ESG (Environmental, Social, Governance) analyst.
    Analyze news articles focusing on:
    1. Environmental impact and sustainability
    2. Social responsibility and labor practices
    3. Corporate governance and ethics
    4. ESG risks and opportunities

    Rate each category and provide ESG score.
    """
)
```

### Example 3: Technical Trader Focus

```python
from aifn.src.prompts import create_custom_news_prompt

trader_prompt = create_custom_news_prompt(
    system_instructions="""
    You are a technical trader. Analyze news for immediate trading signals:
    1. Potential impact on price (short-term)
    2. Volume implications
    3. Support/resistance level changes
    4. Entry/exit points

    Be concise and actionable. Focus on trading opportunities.
    """
)
```

### Example 4: Long-Term Investor Focus

```python
from aifn.src.prompts import create_custom_news_prompt

investor_prompt = create_custom_news_prompt(
    system_instructions="""
    You are a long-term value investor. Analyze news for:
    1. Business fundamentals impact
    2. Competitive positioning changes
    3. Management quality signals
    4. Long-term growth prospects

    Ignore short-term noise. Focus on 5-10 year outlook.
    """
)
```

---

## 🎨 Prompt Structure

### Anatomy of a Prompt

```python
ChatPromptTemplate.from_messages([
    ("system", "Your system-level instructions..."),
    ("user", "Your user query with {variables}...")
])
```

### System Message
- Defines the LLM's role and behavior
- Sets analysis focus and priorities
- Establishes output format

### User Message
- Contains the actual data to analyze
- Uses variables like `{news_text}`, `{ticker}`, etc.
- Can include specific questions or requirements

---

## 🔄 Modifying Summary.py to Use Custom Prompts

### Option 1: Replace Default Prompts

Edit [summary.py](aifn/src/summary.py) to import your custom prompt:

```python
# In summary.py
from .prompts import get_risk_focused_prompt  # Instead of get_news_analysis_prompt

def summarize_news_node(state: FinancialDataState) -> FinancialDataState:
    llm = get_llm(temperature=0.3)
    prompt = get_risk_focused_prompt()  # Use alternative
    chain = prompt | llm | StrOutputParser()
    # ... rest of code
```

### Option 2: Create Custom Workflow

Create your own workflow function:

```python
from aifn.src.prompts import create_custom_news_prompt
from aifn.src.summary import get_llm, format_news_articles
from langchain_core.output_parsers import StrOutputParser

def my_custom_analysis(news_articles, ticker):
    """Custom analysis with your own prompt."""

    # Define custom prompt
    my_prompt = create_custom_news_prompt(
        "Your custom instructions here..."
    )

    # Create chain
    llm = get_llm()
    chain = my_prompt | llm | StrOutputParser()

    # Format and analyze
    news_text = format_news_articles(news_articles, ticker)
    return chain.invoke({"news_text": news_text})
```

---

## 💡 Best Practices

### 1. Be Specific
```python
# ❌ Vague
"Analyze the news"

# ✅ Specific
"Analyze news articles focusing on earnings impact, management commentary,
and forward guidance. Rate conviction level for each finding."
```

### 2. Set Clear Output Format
```python
# ✅ Good
"Provide analysis in this format:
1. Key Finding (one sentence)
2. Supporting Evidence (bullet points)
3. Confidence Level (0-100%)
4. Trading Implication (buy/sell/hold)"
```

### 3. Define the Role
```python
# ✅ Good
"You are a quantitative analyst with 10 years of experience in algorithmic
trading. You focus on data-driven insights and statistical patterns."
```

### 4. Control Verbosity
```python
# For brief outputs
"Be extremely concise. Maximum 3 bullet points, each under 20 words."

# For detailed outputs
"Provide comprehensive analysis with supporting data, examples, and reasoning."
```

### 5. Set Objectivity Level
```python
# Balanced
"Be objective and present both bullish and bearish perspectives."

# Conservative
"Focus on risks and potential downsides. Be conservative in estimates."

# Optimistic
"Highlight opportunities and growth potential. Be forward-looking."
```

---

## 🧪 Testing Custom Prompts

### Quick Test

```python
from aifn.src.prompts import create_custom_news_prompt
from aifn.src.summary import get_llm
from langchain_core.output_parsers import StrOutputParser

# Your custom prompt
test_prompt = create_custom_news_prompt(
    "Analyze news in haiku format. Be creative."
)

# Test it
llm = get_llm(temperature=0.7)  # Higher temp for creativity
chain = test_prompt | llm | StrOutputParser()

result = chain.invoke({
    "news_text": "Apple releases new iPhone with advanced AI features..."
})

print(result)
```

### A/B Testing Prompts

```python
prompts_to_test = {
    "standard": get_news_analysis_prompt(),
    "risk_focused": get_risk_focused_prompt(),
    "concise": get_concise_news_prompt(),
}

news_text = "Your test news..."

for name, prompt in prompts_to_test.items():
    llm = get_llm()
    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"news_text": news_text})

    print(f"\n{'='*60}")
    print(f"Prompt: {name}")
    print(f"{'='*60}")
    print(result)
```

---

## 📚 Prompt Library

Browse available prompts:

```python
from aifn.src.prompts import list_available_prompts

print("Available prompts:")
for prompt_name in list_available_prompts():
    print(f"  - {prompt_name}")
```

Output:
```
Available prompts:
  - news_analysis
  - price_analysis
  - market_context
  - synthesis
  - concise_news
  - risk_focused
  - opportunity_focused
```

---

## 🎓 Advanced: Prompt Engineering Tips

### 1. Few-Shot Examples

Include examples in your prompt:

```python
system_prompt = """
Analyze financial news and provide sentiment score.

Examples:
Input: "Company beats earnings estimates by 20%"
Output: Sentiment: Bullish (0.8)

Input: "CEO resigns amid investigation"
Output: Sentiment: Bearish (-0.7)

Now analyze the following news:
"""
```

### 2. Chain-of-Thought

Encourage step-by-step reasoning:

```python
system_prompt = """
Analyze the news using this reasoning process:
1. First, identify key facts
2. Then, assess immediate impact
3. Next, consider long-term implications
4. Finally, synthesize into overall assessment

Show your reasoning for each step.
"""
```

### 3. Constraints

Set explicit limits:

```python
system_prompt = """
Analyze the news with these constraints:
- Maximum 5 key points
- Each point under 15 words
- No speculation beyond data provided
- Cite specific phrases from articles
"""
```

---

## 📖 Further Reading

- [LangChain Prompts Documentation](https://python.langchain.com/docs/modules/model_io/prompts/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)

---

**Questions?** Open an issue or check the [main documentation](README_SUMMARY_MODULE.md).
