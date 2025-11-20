# ✅ Prompts Module - Centralized Prompt Management

All LLM prompts have been extracted into a dedicated [prompts.py](aifn/src/prompts.py) module for easy customization and maintenance.

---

## 🎉 What's New

### Before
Prompts were scattered throughout [summary.py](aifn/src/summary.py):

```python
# ❌ Prompts mixed with logic
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a financial analyst expert. Analyze..."""),
    ("user", "Analyze these news articles:\n\n{news_text}")
])
```

### After
Prompts are centralized in [prompts.py](aifn/src/prompts.py):

```python
# ✅ Clean separation
from .prompts import get_news_analysis_prompt

prompt = get_news_analysis_prompt()
```

---

## 📁 File Structure

```
aifn/src/
├── prompts.py      ← NEW! All prompts here
├── summary.py      ← Now imports from prompts.py
└── crawler.py
```

---

## 🚀 Quick Start

### 1. View Available Prompts

```python
from aifn.src.prompts import list_available_prompts

print(list_available_prompts())
# ['news_analysis', 'price_analysis', 'market_context',
#  'synthesis', 'concise_news', 'risk_focused', 'opportunity_focused']
```

### 2. Use Standard Prompts (Automatic)

```python
from aifn.src.summary import summarize_financial_data

# Uses standard prompts automatically
result = summarize_financial_data(ticker, news, prices, market)
```

### 3. Use Alternative Prompts

```python
from aifn.src.prompts import get_risk_focused_prompt
from aifn.src.summary import get_llm
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()
prompt = get_risk_focused_prompt()
chain = prompt | llm | StrOutputParser()

result = chain.invoke({"news_text": "Your news..."})
```

### 4. Create Custom Prompts

```python
from aifn.src.prompts import create_custom_news_prompt

my_prompt = create_custom_news_prompt(
    system_instructions="""
    You are a crypto analyst. Focus on:
    1. DeFi developments
    2. Blockchain technology
    3. Regulatory news
    """
)
```

---

## 📦 What's Included

### Standard Prompts (4)

| Prompt | Function | Used In |
|--------|----------|---------|
| **News Analysis** | `get_news_analysis_prompt()` | `summarize_news_node()` |
| **Price Analysis** | `get_price_analysis_prompt()` | `analyze_price_node()` |
| **Market Context** | `get_market_context_prompt()` | `market_context_node()` |
| **Synthesis** | `get_synthesis_prompt()` | `synthesize_final_summary_node()` |

### Alternative Prompts (3)

| Prompt | Function | Purpose |
|--------|----------|---------|
| **Concise News** | `get_concise_news_prompt()` | Brief bullet-point summary |
| **Risk Focused** | `get_risk_focused_prompt()` | Conservative risk analysis |
| **Opportunity Focused** | `get_opportunity_focused_prompt()` | Growth opportunities |

### Utility Functions

| Function | Purpose |
|----------|---------|
| `create_custom_news_prompt()` | Create custom news prompts |
| `create_custom_synthesis_prompt()` | Create custom synthesis prompts |
| `get_prompt(name)` | Get prompt by name from registry |
| `list_available_prompts()` | List all available prompts |

---

## 🎯 Benefits

### 1. **Easy Customization**
Edit prompts in one place - [prompts.py](aifn/src/prompts.py)

```python
# Before: Find and edit in multiple places
# After: Edit once in prompts.py

NEWS_ANALYSIS_SYSTEM_PROMPT = """
Your custom instructions here...
"""
```

### 2. **Reusability**
Use the same prompts across different parts of your codebase

```python
from aifn.src.prompts import get_news_analysis_prompt

# Use in workflow
prompt1 = get_news_analysis_prompt()

# Use in standalone analysis
prompt2 = get_news_analysis_prompt()
```

### 3. **Version Control**
Track prompt changes separately from logic

```bash
git log aifn/src/prompts.py  # See prompt changes
git log aifn/src/summary.py  # See logic changes
```

### 4. **A/B Testing**
Easy to test different prompts

```python
prompts = {
    "standard": get_news_analysis_prompt(),
    "risk": get_risk_focused_prompt(),
    "concise": get_concise_news_prompt(),
}

for name, prompt in prompts.items():
    # Test each prompt...
```

### 5. **Experimentation**
Try alternative prompts without modifying core code

```python
# Try different analysis styles
from aifn.src.prompts import get_opportunity_focused_prompt

prompt = get_opportunity_focused_prompt()
# Test it without touching summary.py
```

---

## 📝 Common Tasks

### Task 1: Change Default News Analysis Tone

**File**: [aifn/src/prompts.py](aifn/src/prompts.py)

```python
# Find and edit:
NEWS_ANALYSIS_SYSTEM_PROMPT = """
You are a financial analyst expert. Be more conservative in your analysis...
[Your changes here]
"""
```

### Task 2: Add a New Prompt Type

**File**: [aifn/src/prompts.py](aifn/src/prompts.py)

```python
# 1. Define the prompt
MOMENTUM_FOCUSED_SYSTEM_PROMPT = """
You are a momentum trader. Focus on...
"""

# 2. Create getter function
def get_momentum_focused_prompt() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", MOMENTUM_FOCUSED_SYSTEM_PROMPT),
        ("user", NEWS_ANALYSIS_USER_PROMPT)
    ])

# 3. Add to registry
PROMPT_REGISTRY = {
    # ... existing ...
    "momentum_focused": get_momentum_focused_prompt,
}
```

### Task 3: Use Custom Prompt in Workflow

**File**: [aifn/src/summary.py](aifn/src/summary.py)

```python
# Change import:
from .prompts import get_momentum_focused_prompt  # Your new prompt

# Use in node:
def summarize_news_node(state: FinancialDataState):
    llm = get_llm()
    prompt = get_momentum_focused_prompt()  # Use custom
    chain = prompt | llm | StrOutputParser()
    # ... rest
```

### Task 4: Create Analysis-Specific Prompts

```python
# For different stock types
from aifn.src.prompts import create_custom_news_prompt

tech_prompt = create_custom_news_prompt(
    "Focus on innovation, product launches, tech trends..."
)

healthcare_prompt = create_custom_news_prompt(
    "Focus on FDA approvals, clinical trials, regulations..."
)

def analyze_by_sector(ticker, sector):
    prompt = tech_prompt if sector == "tech" else healthcare_prompt
    # Use appropriate prompt...
```

---

## 🔧 Configuration Examples

### Example 1: Sentiment-Only Analysis

**Use Case**: Only interested in sentiment, not detailed analysis

```python
from aifn.src.prompts import create_custom_news_prompt

sentiment_only = create_custom_news_prompt(
    system_instructions="""
    Provide ONLY sentiment analysis:
    1. Overall sentiment: Bullish/Bearish/Neutral
    2. Sentiment score: -1.0 to +1.0
    3. Confidence: 0-100%

    No other analysis. Be brief.
    """
)
```

### Example 2: Retail Investor Focus

**Use Case**: Simple language for retail investors

```python
from aifn.src.prompts import create_custom_news_prompt

retail_friendly = create_custom_news_prompt(
    system_instructions="""
    Explain news in simple terms for retail investors:
    - Avoid jargon
    - Use analogies
    - Explain like I'm 5
    - Focus on "what this means for me"

    Be educational and encouraging.
    """
)
```

### Example 3: Institutional Analysis

**Use Case**: Professional, detailed analysis

```python
from aifn.src.prompts import create_custom_news_prompt

institutional = create_custom_news_prompt(
    system_instructions="""
    Provide institutional-grade analysis:
    - Detailed financial metrics
    - Comparative analysis
    - Risk-adjusted returns
    - Portfolio implications
    - Confidence intervals

    Use professional terminology.
    """
)
```

---

## 📊 Prompt Registry

Access prompts by name:

```python
from aifn.src.prompts import get_prompt

# Get by name
news_prompt = get_prompt("news_analysis")
risk_prompt = get_prompt("risk_focused")

# List all
from aifn.src.prompts import list_available_prompts
print(list_available_prompts())
```

---

## 🧪 Testing

Test the prompts module:

```bash
# Run module directly
poetry run python aifn/src/prompts.py
```

Output:
```
Available Prompt Templates:
- news_analysis
- price_analysis
- market_context
- synthesis
- concise_news
- risk_focused
- opportunity_focused
```

Test in your code:

```python
from aifn.src.prompts import get_news_analysis_prompt
from aifn.src.summary import get_llm
from langchain_core.output_parsers import StrOutputParser

# Test a prompt
llm = get_llm()
prompt = get_news_analysis_prompt()
chain = prompt | llm | StrOutputParser()

test_news = "Apple announces new AI chip with 50% performance boost..."
result = chain.invoke({"news_text": test_news})
print(result)
```

---

## 📚 Documentation

- **[PROMPTS_GUIDE.md](PROMPTS_GUIDE.md)** - Complete guide with examples
- **[prompts.py](aifn/src/prompts.py)** - Source code with inline docs
- **[summary.py](aifn/src/summary.py)** - See how prompts are used

---

## 💡 Best Practices

### 1. Keep Prompts in prompts.py
Don't create prompts inline in summary.py

```python
# ✅ Good
from .prompts import get_news_analysis_prompt
prompt = get_news_analysis_prompt()

# ❌ Bad
prompt = ChatPromptTemplate.from_messages([...])
```

### 2. Use Registry for Custom Prompts
Add new prompts to the registry for discoverability

```python
# ✅ Good - In prompts.py
PROMPT_REGISTRY = {
    # ...
    "my_custom": get_my_custom_prompt,
}

# Now discoverable
from aifn.src.prompts import list_available_prompts
print(list_available_prompts())  # Shows 'my_custom'
```

### 3. Document Your Prompts
Add docstrings to custom prompt functions

```python
def get_my_custom_prompt() -> ChatPromptTemplate:
    """
    Get custom prompt for cryptocurrency analysis.

    Focuses on DeFi, blockchain tech, and regulatory news.
    Best used with temperature=0.5 for balanced creativity.

    Returns:
        ChatPromptTemplate configured for crypto analysis
    """
    # ...
```

### 4. Version Control Prompts
Track prompt changes in git

```bash
git add aifn/src/prompts.py
git commit -m "feat: add momentum-focused analysis prompt"
```

---

## 🎓 Advanced Usage

### Dynamic Prompt Selection

```python
from aifn.src.prompts import get_prompt

def analyze_with_strategy(news, strategy="standard"):
    """Analyze news with different strategies."""

    prompt_mapping = {
        "standard": "news_analysis",
        "conservative": "risk_focused",
        "aggressive": "opportunity_focused",
        "brief": "concise_news",
    }

    prompt = get_prompt(prompt_mapping[strategy])
    # Use prompt...
```

### Prompt Chaining

```python
from aifn.src.prompts import (
    get_news_analysis_prompt,
    get_synthesis_prompt
)

# First pass: detailed analysis
news_prompt = get_news_analysis_prompt()
detailed = chain1.invoke({"news_text": news})

# Second pass: synthesize
synthesis_prompt = get_synthesis_prompt()
final = chain2.invoke({
    "ticker": "AAPL",
    "news_summary": detailed,
    # ...
})
```

---

## ✅ Summary

**What Changed**:
- ✅ Created [aifn/src/prompts.py](aifn/src/prompts.py) with all prompts
- ✅ Updated [summary.py](aifn/src/summary.py) to import from prompts.py
- ✅ Added 7 pre-built prompts (4 standard + 3 alternative)
- ✅ Added utility functions for custom prompts
- ✅ Added prompt registry for easy access
- ✅ Created [PROMPTS_GUIDE.md](PROMPTS_GUIDE.md) documentation

**Benefits**:
- 🎯 Easy to customize prompts
- 🔄 Reusable across codebase
- 📝 Better version control
- 🧪 Simple A/B testing
- 🚀 Quick experimentation

**Next Steps**:
1. Read [PROMPTS_GUIDE.md](PROMPTS_GUIDE.md) for examples
2. Customize prompts in [prompts.py](aifn/src/prompts.py)
3. Test with: `poetry run python aifn/src/prompts.py`

---

**Questions?** See [PROMPTS_GUIDE.md](PROMPTS_GUIDE.md) for detailed examples and tutorials.
