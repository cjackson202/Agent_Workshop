# Facilitator Guide: MSFT Agent Framework Workshop

## Overview
This 20-30 minute workshop introduces participants to integrating Azure AI Foundry agents into Python applications using the Microsoft Agent Framework.

## Prerequisites for Participants
- **Must have completed**: Azure AI Foundry Agents workshop
- Working agent in Azure AI Foundry (with valid Agent ID)
- Azure CLI installed
- Python 3.10+

## Workshop Timeline

| Time | Activity | Notes |
|------|----------|-------|
| 0:00-0:05 | Introduction & Setup | Install deps, verify az login --identity |
| 0:05-0:15 | Exercise 2: Configure Connection | Get endpoint & agent ID |
| 0:15-0:25 | Exercise 3: Enable Tracing | Configure Azure Monitor |
| 0:25-0:30 | Wrap-up & Q&A | Review traces, discuss next steps |

## Key Teaching Points

### 1. Why Agent Framework?
- Provides consistent abstraction over agent services
- Built-in observability with OpenTelemetry
- Simplifies authentication handling
- Enables multi-agent orchestration patterns

### 2. The Connection Pattern
Emphasize the layered architecture:
```
Credential → Project Client → AI Client → Agent
```

### 3. Tracing Value
- Production monitoring
- Debugging agent behavior
- Token usage tracking
- Latency analysis

## Common Participant Issues

### Issue: "Where is my Project Endpoint?"
**Solution**: Walk them through:
1. ai.azure.com
2. Select project
3. Settings → Project Endpoint

### Issue: "Where is my Agent ID?"
**Solution**: Walk them through:
1. Agents section
2. Click on their agent
3. Agent ID shown at top (or in URL)

### Issue: "AuthenticationError"
**Solution**: 
```bash
az login --identity
az account set --subscription "Your Subscription Name"
```

### Issue: "Traces not showing"
**Solution**: 
- Wait 1-2 minutes
- Refresh the Tracing page
- Ensure `configure_azure_monitor` is uncommented

## Demo Script

### Before the Workshop
1. Pre-create an agent in a demo project
2. Have the completed `foundry_agent.py` ready to show
3. Open Azure AI Foundry Tracing page in a browser tab

### Live Demo Flow
1. Show the starter script with TODOs
2. Walk through getting credentials from portal
3. Run the script, show agent response
4. Enable tracing, run again
5. Switch to portal, show traces appearing

## Discussion Questions
- "Why would you want to run agents from code vs the playground?"
- "What kind of metrics would you want to track in production?"
- "How might you use multiple agents together?"

## Bonus Content (If Time Permits)
- Show sensitive data logging for debugging
- Demonstrate multiple queries in sequence
- Preview the Multi-Agent Workshop as next steps

## Files Overview

| File | Purpose |
|------|---------|
| `foundry_agent_starter.py` | Student version with TODOs |
| `foundry_agent.py` | Completed reference solution |
| `README.md` | Full workshop instructions |
| `docs/QUICKSTART.md` | Condensed 5-min guide |

## Post-Workshop
- Ensure participants can see traces in portal
- Point them to Multi-Agent Workshop as next module
- Share documentation links for deeper learning
