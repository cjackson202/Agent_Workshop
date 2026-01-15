# Workshop Solutions

This folder contains completed versions of the workshop exercises for reference.

## Exercise 2: Adding Custom Tools to Sequential Agent

### Example Solution: Temperature Converter Tool

```python
def temperature_converter(
    temp: Annotated[float, "Temperature value to convert"],
    from_unit: Annotated[str, "Source unit: celsius or fahrenheit"],
    to_unit: Annotated[str, "Target unit: celsius or fahrenheit"]
) -> str:
    """Convert temperature between Celsius and Fahrenheit."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit == to_unit:
        return f"Temperature is already in {to_unit}: {temp}°"
    
    if from_unit == "celsius" and to_unit == "fahrenheit":
        result = (temp * 9/5) + 32
        return f"{temp}°C = {result:.1f}°F"
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        result = (temp - 32) * 5/9
        return f"{temp}°F = {result:.1f}°C"
    else:
        return f"Error: Invalid units. Use 'celsius' or 'fahrenheit'"
```

### How to Add It:

1. Add the function after the existing tools (calculator, word_counter)
2. Register it with the Writer agent:

```python
writer = chat_client.create_agent(
    instructions="""You are a creative copywriter. Create compelling content.
    
Use available tools:
- calculator for arithmetic
- word_counter for text analysis
- temperature_converter for temperature conversions""",
    name="Writer",
    functions=[calculator, word_counter, temperature_converter]
)
```

3. Test with: `"Write a tagline for a heater that works at 72 fahrenheit. Convert that to celsius."`

---

## Additional Tool Ideas

### Text Reverser
```python
def text_reverser(
    text: Annotated[str, "Text to reverse"]
) -> str:
    """Reverse the characters in a text string."""
    return f"Reversed text: {text[::-1]}"
```

### Simple Sentiment Analyzer
```python
def sentiment_analyzer(
    text: Annotated[str, "Text to analyze"]
) -> str:
    """Analyze text sentiment based on positive and negative words."""
    positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic"]
    negative_words = ["bad", "poor", "terrible", "awful", "horrible", "disappointing"]
    
    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)
    
    if pos_count > neg_count:
        sentiment = "Positive"
    elif neg_count > pos_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return f"Sentiment: {sentiment} (Positive: {pos_count}, Negative: {neg_count})"
```

### Character Replacer
```python
def character_replacer(
    text: Annotated[str, "Text to process"],
    old_char: Annotated[str, "Character to replace"],
    new_char: Annotated[str, "Replacement character"]
) -> str:
    """Replace all occurrences of a character in text."""
    result = text.replace(old_char, new_char)
    count = text.count(old_char)
    return f"Replaced {count} occurrences. Result: {result}"
```

---

## Best Practices for Tool Creation

### 1. Always Use Type Annotations
```python
# ✅ Good
def my_tool(
    param: Annotated[str, "Description"]
) -> str:
    pass

# ❌ Bad
def my_tool(param):
    pass
```

### 2. Provide Clear Descriptions
```python
# ✅ Good
def calculator(
    operation: Annotated[str, "The operation: add, subtract, multiply, divide"],
    a: Annotated[float, "First number"],
    b: Annotated[float, "Second number"]
) -> str:
    """Perform basic arithmetic operations on two numbers."""
    pass

# ❌ Bad
def calculator(a, b, op):
    """Do math."""
    pass
```

### 3. Handle Errors Gracefully
```python
def divide(
    a: Annotated[float, "Numerator"],
    b: Annotated[float, "Denominator"]
) -> str:
    """Divide two numbers."""
    if b == 0:
        return "Error: Cannot divide by zero"
    result = a / b
    return f"Result: {result}"
```

### 4. Return Strings or JSON-Serializable Data
```python
# ✅ Good
def get_info() -> str:
    return "Information as string"

# ✅ Good
def get_data() -> dict:
    return {"key": "value"}

# ❌ Bad (complex objects)
def get_object() -> CustomClass:
    return CustomClass()
```

---

## Workshop Exercise Solutions

### Exercise 1: Sequential Patterns
**No code changes needed** - Focus on understanding the flow by running different workflows:
- Basic: Writer → Reviewer
- Extended: Writer → Reviewer → Editor
- Advanced: Writer → Reviewer → Editor → ContentAnalyzer

Key insight: Each agent receives the full conversation history.

### Exercise 2: Add Custom Tool
See temperature_converter example above.

Test prompts:
- "Write about a product that works at 25 celsius. Convert that to fahrenheit."
- "Create a tagline mentioning 98.6 fahrenheit body temperature in celsius."

### Exercise 3: Handoff Patterns
**No code changes needed** - Run with different scenarios:

1. Refund scenario: "My order 12345 arrived damaged. I need a refund."
   - Expected: Triage → Refund Agent → Approval request
   
2. Order tracking: "Where is my order 67890?"
   - Expected: Triage → Order Agent → Tracking info (no approval)
   
3. Complex: "I can't log in and need to track my order 54321"
   - Expected: Triage → Account Agent → (potential handoff to Order Agent)

### Exercise 4: Group Chat Workflows
**No code changes needed** - Compare strategies:

Run same question with different workflows:
- `workflow_simple`: Fixed sequential order
- `workflow_iterative`: Can loop back if quality issues found
- `workflow_agent_manager`: Manager decides speaker order

Question: "What are the benefits of async/await in Python?"

Compare:
- Speed (simple is fastest)
- Quality (iterative may be highest)
- Flexibility (agent-managed is most adaptive)

---

## Advanced Challenges

### Challenge 1: Create a Custom Executor
Build an executor that formats agent output as JSON:

```python
class JsonFormatter(Executor):
    @handler
    async def format_json(
        self,
        conversation: list[ChatMessage],
        ctx: WorkflowContext[list[ChatMessage]]
    ) -> None:
        """Format conversation as JSON."""
        import json
        
        output = {
            "messages": [
                {
                    "author": msg.author_name or "user",
                    "role": msg.role.value,
                    "text": msg.text
                }
                for msg in conversation
            ],
            "total_messages": len(conversation)
        }
        
        json_output = json.dumps(output, indent=2)
        summary_msg = ChatMessage(
            role=Role.ASSISTANT,
            text=f"```json\n{json_output}\n```",
            author_name="JsonFormatter"
        )
        
        await ctx.send_message(list(conversation) + [summary_msg])
```

### Challenge 2: Add Web Search Tool
Create a simple web search tool using a search API:

```python
def web_search(
    query: Annotated[str, "Search query"]
) -> str:
    """Search the web for information."""
    # In real implementation, use Bing API or similar
    return f"Mock search results for: {query}\n1. Result 1\n2. Result 2\n3. Result 3"
```

### Challenge 3: Build a New Pipeline
Create a code review pipeline:
1. Coder: Writes code
2. Security Reviewer: Checks for security issues
3. Performance Reviewer: Checks for performance issues
4. Approver: Final approval decision

---

## Tips for Success

1. **Start Simple**: Test each tool individually before combining
2. **Clear Instructions**: Tell agents explicitly to use tools
3. **Error Handling**: Always handle edge cases in tools
4. **Test Iteratively**: Add one tool at a time
5. **Log Events**: Print events to understand agent behavior

---

## Questions?

If you're stuck:
1. Check the error message carefully
2. Verify type annotations are correct
3. Ensure tool is registered with the agent
4. Add explicit instruction to use the tool
5. Test with simple examples first
