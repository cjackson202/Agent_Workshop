# Workshop Exercise Solutions

## Exercise 1.2: Add a Multiplication Tool

```python
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers
    
    Args:
        a: First number to multiply
        b: Second number to multiply
        
    Returns:
        The product of a and b
    """
    print('-'*50)
    print(f"Multiply tool being used for product of:")
    print(a)
    print('×')
    print(b)
    print('-'*50)
    return a * b
```

**Test it:**
- Run: `python test_mcp.py`
- Ask agent: "What is 7 times 8?"

---

## Exercise 5.1: Add a Weather Tool

```python
@mcp.tool()
def get_temperature_advice(temperature: int) -> str:
    """Get clothing advice based on temperature in Fahrenheit
    
    Args:
        temperature: The temperature in Fahrenheit
        
    Returns:
        Clothing advice based on the temperature
    """
    print('-'*50)
    print(f"Temperature advice requested for: {temperature}°F")
    print('-'*50)
    
    if temperature < 32:
        return "It's freezing! Wear a heavy coat, gloves, and a hat."
    elif temperature < 50:
        return "It's cold. A jacket and long pants are recommended."
    elif temperature < 70:
        return "It's mild. A light sweater or long sleeves would be good."
    elif temperature < 85:
        return "It's warm. T-shirt and shorts weather!"
    else:
        return "It's hot! Stay hydrated and wear light clothing."
```

**Test it:**
- Ask agent: "What should I wear if it's 45 degrees?"

---

## Exercise 5.2: Additional Custom Tools

### Tool 1: Calculate Percentage

```python
@mcp.tool()
def calculate_percentage(value: float, total: float) -> float:
    """Calculate what percentage a value is of a total
    
    Args:
        value: The partial value
        total: The total value
        
    Returns:
        The percentage (0-100)
    """
    if total == 0:
        return 0.0
    percentage = (value / total) * 100
    print('-'*50)
    print(f"Calculating: {value} is {percentage:.2f}% of {total}")
    print('-'*50)
    return round(percentage, 2)
```

**Test prompts:**
- "What percentage is 45 out of 180?"
- "If I scored 85 out of 100, what's my percentage?"

---

### Tool 2: Currency Converter (Mock Data)

```python
@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency between USD, EUR, and GBP (mock rates)
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code (USD, EUR, GBP)
        to_currency: Target currency code (USD, EUR, GBP)
        
    Returns:
        Converted amount with currency
    """
    # Mock exchange rates (not real-time!)
    rates = {
        "USD": {"EUR": 0.92, "GBP": 0.79, "USD": 1.0},
        "EUR": {"USD": 1.09, "GBP": 0.86, "EUR": 1.0},
        "GBP": {"USD": 1.27, "EUR": 1.16, "GBP": 1.0}
    }
    
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency not in rates or to_currency not in rates[from_currency]:
        return f"Unsupported currency conversion: {from_currency} to {to_currency}"
    
    rate = rates[from_currency][to_currency]
    converted = amount * rate
    
    print('-'*50)
    print(f"Converting: {amount} {from_currency} → {converted:.2f} {to_currency}")
    print(f"Rate: 1 {from_currency} = {rate} {to_currency}")
    print('-'*50)
    
    return f"{converted:.2f} {to_currency}"
```

**Test prompts:**
- "Convert 100 USD to EUR"
- "How much is 50 GBP in USD?"

---

### Tool 3: Email Validator

```python
import re

@mcp.tool()
def validate_email(email: str) -> str:
    """Validate email format using regex
    
    Args:
        email: Email address to validate
        
    Returns:
        Validation result message
    """
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    is_valid = bool(re.match(pattern, email))
    
    print('-'*50)
    print(f"Validating email: {email}")
    print(f"Valid: {is_valid}")
    print('-'*50)
    
    if is_valid:
        return f"✓ '{email}' is a valid email format"
    else:
        return f"✗ '{email}' is not a valid email format"
```

**Test prompts:**
- "Is user@example.com a valid email?"
- "Validate the email address: invalid@email"

---

### Tool 4: Password Generator

```python
import random
import string

@mcp.tool()
def generate_password(length: int = 12) -> str:
    """Generate a random secure password
    
    Args:
        length: Desired password length (default: 12, min: 8, max: 64)
        
    Returns:
        Generated password
    """
    # Ensure reasonable length
    length = max(8, min(64, length))
    
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*"
    
    # Ensure at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols)
    ]
    
    # Fill the rest randomly
    all_chars = lowercase + uppercase + digits + symbols
    password += random.choices(all_chars, k=length - 4)
    
    # Shuffle to randomize positions
    random.shuffle(password)
    result = ''.join(password)
    
    print('-'*50)
    print(f"Generated password of length {length}")
    print('-'*50)
    
    return result
```

**Test prompts:**
- "Generate a password"
- "Create a 16-character password for me"

---

### Tool 5: Division with Error Handling

```python
@mcp.tool()
def divide(a: float, b: float) -> str:
    """Divide two numbers with error handling
    
    Args:
        a: Numerator (dividend)
        b: Denominator (divisor)
        
    Returns:
        Result or error message
    """
    print('-'*50)
    print(f"Divide tool: {a} ÷ {b}")
    print('-'*50)
    
    if b == 0:
        return "Error: Cannot divide by zero!"
    
    result = a / b
    return f"{a} ÷ {b} = {result}"
```

**Test prompts:**
- "What is 100 divided by 4?"
- "Try dividing 10 by 0"  (tests error handling)

---

### Tool 6: List Statistics

```python
from typing import List

@mcp.tool()
def calculate_statistics(numbers: List[float]) -> str:
    """Calculate statistics for a list of numbers
    
    Args:
        numbers: List of numbers to analyze
        
    Returns:
        Statistical summary (mean, median, min, max)
    """
    if not numbers:
        return "Error: Empty list provided"
    
    sorted_nums = sorted(numbers)
    count = len(numbers)
    total = sum(numbers)
    mean = total / count
    
    # Calculate median
    if count % 2 == 0:
        median = (sorted_nums[count//2 - 1] + sorted_nums[count//2]) / 2
    else:
        median = sorted_nums[count//2]
    
    minimum = min(numbers)
    maximum = max(numbers)
    
    print('-'*50)
    print(f"Calculating statistics for {count} numbers")
    print('-'*50)
    
    result = f"""Statistics:
    Count: {count}
    Mean: {mean:.2f}
    Median: {median:.2f}
    Min: {minimum}
    Max: {maximum}
    Sum: {total}"""
    
    return result
```

**Test prompts:**
- "Calculate statistics for the numbers: 5, 10, 15, 20, 25"
- "What's the average and median of 1, 5, 3, 9, 7?"

---

## Advanced: MCP Resource Example

```python
@mcp.resource("time://{timezone}")
def get_current_time(timezone: str = "UTC") -> str:
    """Get current time for a timezone
    
    Args:
        timezone: Timezone name (UTC, EST, PST, etc.)
        
    Returns:
        Current time in the specified timezone
    """
    from datetime import datetime
    import pytz
    
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        print('-'*50)
        print(f"Time resource accessed for timezone: {timezone}")
        print('-'*50)
        
        return f"Current time in {timezone}: {formatted_time}"
    except:
        return f"Invalid timezone: {timezone}"
```

**Note:** This requires `pytz` package: `pip install pytz`

**Access via URI:** `time://America/New_York`

---

## Complete Example: server.py with All Solutions

See [server_with_solutions.py](server_with_solutions.py) for a complete server implementation with all workshop solutions.

---

## Testing Your Solutions

### Method 1: Local Test Client

```powershell
# Start server
python server.py

# In another terminal, run test
python test_mcp.py
```

### Method 2: With Agent

```powershell
# Make sure server is running
python create_agent_mi.py

# Try prompts:
You: What is 25% of 80?
You: Convert 100 USD to EUR
You: Validate this email: user@example.com
You: Generate a password for me
```

### Method 3: Direct Tool Call in test_mcp.py

Add test cases to `test_mcp.py`:

```python
# Test your custom tool
print("🧮 Testing 'calculate_percentage' tool...")
result = await session.call_tool("calculate_percentage", {"value": 45, "total": 180})
print(f"✅ Result: {result.content[0].text}")
```

---

## Common Issues and Solutions

### Issue: Tool not appearing in agent
**Solution:** 
- Restart MCP server after adding tool
- Check tool has `@mcp.tool()` decorator
- Verify docstring is present
- Check for syntax errors

### Issue: Type errors with List parameters
**Solution:**
```python
from typing import List
def my_tool(items: List[float]) -> str:
    # Agent will pass JSON array: [1, 2, 3]
```

### Issue: Tool returns but agent shows "no result"
**Solution:** Always return a string or basic type (int, float, bool)

---

## Extension Ideas

Want to go further? Try these:
1. **Weather API**: Integrate real weather data from OpenWeatherMap
2. **Database Tool**: Query a SQLite database
3. **File Operations**: Read/write files with safety checks
4. **Web Scraper**: Fetch data from websites (with rate limiting)
5. **Data Visualizer**: Generate charts and save as images
6. **Natural Language Dates**: Parse dates like "next Monday"
7. **Unit Converter**: Temperature, distance, weight, etc.
8. **Text Analyzer**: Count words, sentiment, readability score

---

**Remember:** Always test your tools independently before using with agents!
