# Solutions: MSFT Agent Framework Workshop

## Exercise 2: Configure Connection - Solution

### Step 2.1: Project Endpoint
Your project endpoint should look like:
```python
PROJECT_ENDPOINT = "https://<your-account>.services.ai.azure.com/api/projects/<your-project>"
```

Example:
```python
PROJECT_ENDPOINT = "https://contoso-workshop.services.ai.azure.com/api/projects/contoso-sales"
```

### Step 2.2: Agent ID
Your agent ID should look like:
```python
AGENT_ID = "asst_xxxxxxxxxxxxxxxxxxxx"
```

Example:
```python
AGENT_ID = "asst_RAaC0bqdGcOGJT34ysxP2tvq"
```

---

## Exercise 3: Enable Tracing - Solution

### Step 3.2: Uncomment the tracing line

**Before:**
```python
# await client.configure_azure_monitor(enable_live_metrics=True)
```

**After:**
```python
await client.configure_azure_monitor(enable_live_metrics=True)
```

---

## Complete Solution

Here is the fully completed script:

```python
"""
MSFT Agent Framework Workshop - COMPLETED Solution
"""

import asyncio
from agent_framework import ChatAgent
from agent_framework.azure import AzureAIAgentClient, AzureAIClient
from azure.ai.projects.aio import AIProjectClient
from azure.identity.aio import AzureCliCredential
import os

# Exercise 1: Configure Your Azure AI Foundry Project
PROJECT_ENDPOINT = "https://your-account.services.ai.azure.com/api/projects/your-project"
os.environ["AZURE_AI_PROJECT_ENDPOINT"] = PROJECT_ENDPOINT
os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"] = "gpt-4o"

# Optional: Enable sensitive data logging (development only!)
# os.environ["ENABLE_SENSITIVE_DATA"] = "true"

# Exercise 2: Connect to Your Foundry Agent
AGENT_ID = "asst_your_agent_id_here"


async def main():
    """Main function demonstrating agent interaction with tracing."""
    
    async with (
        AzureCliCredential() as credential,
        AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client,
        AzureAIClient(project_client=project_client) as client,
        ChatAgent(
            chat_client=AzureAIAgentClient(
                credential=credential,
                agent_id=AGENT_ID
            ),
            name="FoundryAgent",
        ) as agent,
    ):
        # Exercise 3: Configure OpenTelemetry Tracing
        await client.configure_azure_monitor(enable_live_metrics=True)
        
        print("Sending message to your Foundry agent...")
        print("-" * 50)
        
        result = await agent.run("Tell me more about the tents Contoso offers.")
        print(result.text)
        
        print("-" * 50)
        print("Agent response complete!")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Verification Checklist

After completing all exercises, you should be able to:

✅ Run `python foundry_agent_starter.py` without errors

✅ See your agent respond to the test query

✅ View traces in Azure AI Foundry → Tracing section

---

## Troubleshooting Common Errors

### Error: `ModuleNotFoundError: No module named 'agent_framework'`
**Solution:**
```bash
pip install -r requirements.txt
```

### Error: `azure.core.exceptions.ClientAuthenticationError`
**Solution:**
```bash
az login --identity
az account show  # Verify correct subscription
```

### Error: `ResourceNotFoundError: (ResourceNotFound)`
**Solution:** Double-check your `PROJECT_ENDPOINT`:
1. Go to ai.azure.com
2. Open your project
3. Settings → Copy the exact endpoint

### Error: `Agent not found` or `Invalid agent ID`
**Solution:** Verify your `AGENT_ID`:
1. Go to Agents in your Foundry project
2. Click on your agent
3. Copy the ID from the agent details

### Traces Not Appearing
**Solutions:**
1. Wait 1-2 minutes (propagation delay)
2. Refresh the Tracing page
3. Ensure you uncommented `configure_azure_monitor`
4. Check you're viewing the correct project
