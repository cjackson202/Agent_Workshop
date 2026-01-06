# Facilitator Guide - Azure AI Foundry Agents Module

## Module Overview
**Duration:** 75 minutes  
**Level:** Beginner to Intermediate  
**Format:** Hands-on workshop with progressive exercises

## Learning Objectives
1. Understand Azure AI Foundry agent creation
2. Learn knowledge grounding using the File Search tool
3. Integrate external tools (Bing Grounding) for competitive intelligence
4. Understand tool selection and agent reasoning
5. Practice iterative agent enhancement
6. Experience instruction-driven agent behavior

## Pre-Workshop Setup (30 mins before)

### For Facilitators
- [ ] Verify all participants have Azure access
- [ ] Pre-create resource groups for each participant (optional)
- [ ] Test the complete flow end-to-end
- [ ] Prepare demo environment for troubleshooting
- [ ] Print/share QUICKSTART.md reference

### For Participants
- [ ] Azure subscription access confirmed (Contributor or Owner role preferred)
- [ ] Azure AI Foundry portal login tested (https://ai.azure.com)
- [ ] Workshop files downloaded (contoso-tents-datasheet.pdf, instructions)
- [ ] Browser with Azure portal open
- [ ] Sufficient quota for Foundry resources in chosen region
- [ ] Basic instructions text ready to copy/paste

## Module Timeline

### Introduction (5 mins)
**Key Points:**
- Azure AI Foundry enables no-code/low-code agent creation
- **Hierarchy**: Account > Project > Agent
- Instructions define agent behavior (role, tone, boundaries)
- Tools extend capabilities (knowledge, actions)
- Progressive enhancement: start simple, add complexity

**Demo:**
- Show completed Contoso agent answering queries
- Briefly show: project structure, agent with tools enabled
- Set expectations: "You'll build this step-by-step"

**Workshop Flow Preview:**
1. Create project & agent (foundation)
2. Add File Search (internal knowledge)
3. Add Bing Grounding (external data)
4. Test complete system

### Exercise 1: Create Project & Agent with Instructions (20 mins)

#### Project Creation (8 mins)

**Key Teaching Point:**
"A Foundry **project** is your workspace where you build agents. An **agent** is the AI assistant you configure with instructions and tools. Think of it as: Account > Project > Agent hierarchy."

**Facilitation Tips:**
- Do this section together as a group
- Share screen or use instructor machine on projector
- Go slowly through project creation:
  1. Click "Create an agent" from home page
  2. Show project naming conventions
  3. Explain region selection impacts (latency, data residency)
  4. Point out Advanced options but use defaults for workshop
  5. Emphasize waiting for provisioning to complete

**Common Issues:**
| Issue | Solution |
|-------|----------|
| "Create" button disabled | Check permissions, subscription access |
| Provisioning fails | Verify quota, try different region |
| No model deployed | Should auto-deploy gpt-4o; if not, deploy manually |
| Can't see projects | Check Azure subscription is selected |

**Checkpoint 1:**
"Raise your hand when you see 'Provisioning succeeded' or land in your project workspace."

#### Agent Creation (7 mins)

**Key Teaching Point:**
"**Instructions** are the foundation of agent behavior. They tell the agent its role, tone, and boundaries. Unlike code, instructions are natural language guidance that the model interprets."

**Facilitation Tips:**
- Walk through agent creation step-by-step:
  1. Navigate to Agent section
  2. Click "Create agent"
  3. Enter name: "Contoso Sales Agent"
  4. Add description (helps you remember purpose)
  5. Select model (gpt-4o should be default)
- **Instruction Writing Tips to Share:**
  - Start with role definition: "You are a..."
  - Set tone expectations: "friendly and professional"
  - Provide scope/boundaries: "outdoor gear topics only"
  - Give example responses or greetings
- Have everyone paste the provided basic instructions
- Explain why good instructions matter before adding tools

**Sample Instructions to Provide:**
```
You are a helpful sales assistant for Contoso, an online retailer 
specializing in outdoor camping and sports gear.

Your role:
- Assist customers with product inquiries
- Provide helpful information in a friendly and professional tone
- Be concise and accurate in your responses

Guidelines:
- Greet customers warmly
- If you don't have specific information, acknowledge it honestly
- Suggest that customers can ask about tents, hiking gear, camping 
  equipment, and outdoor sports products
- Stay focused on outdoor gear and camping-related topics
```

**Common Issues:**
| Issue | Solution |
|-------|----------|
| Can't find "Create agent" | Check left sidebar, Agent section |
| Model not available | Deploy gpt-4o in Models + Endpoints |
| Instructions not saving | Check field isn't empty, try again |
| Agent creation hangs | Refresh page, check network connection |

**Checkpoint 2:**
"Has everyone created their agent and added instructions? Try sending your first message!"

#### Testing & Interface Tour (5 mins)

**Facilitation Tips:**
- Have everyone test with same queries:
  - "Hello, what can you help me with?"
  - "What is Contoso?"
  - "Do you sell hiking boots?" (tests boundaries)
- Point out key interface elements:
  - **Chat panel** (right) - conversation happens here
  - **Configuration panel** (left) - edit instructions, add tools
  - **Settings** - temperature, max tokens (don't change yet)
  - **Chat history** - previous sessions
- Discuss observations:
  - Agent follows persona from instructions
  - But has no real product data (generic answers)
  - This is where tools come in (next exercise)

**Discussion Prompts:**
- "What did your agent say about Contoso products?"
- "Notice it doesn't have specific product details?"
- "How well did it follow the tone you set in instructions?"

**Watch For:**
- Participants not waiting for project provisioning
- Skipping instructions (emphasize importance!)
- Confusion about agent vs. project
- Questions about model temperature/parameters (defer to later)

**Checkpoint 3:**
- "Everyone should have a working agent that responds in the playground"
- "If your agent responds with Contoso's persona, you're ready for Exercise 2!"

### Exercise 2: Add File Search Tool (20 mins)

#### Part A: Upload & Process (10 mins)

**Key Teaching Point:**
"The File Search tool is one of Foundry's built-in **knowledge tools**. It augments your agent with knowledge from documents you upload. Similar to Azure AI Search, but built directly into Foundry for simplicity. When you upload a file, Foundry automatically chunks it, creates vector embeddings, and makes it searchable."

**Official Microsoft Terminology:**
- Knowledge Tools = provide data/context (File Search, Azure AI Search, Bing Grounding)
- Action Tools = take actions/workflows (Azure Functions, Logic Apps, Function Calling)

**Facilitation Tips:**
- Demo the upload process first (3 mins)
  1. Navigate to agent → Tools section
  2. Add "File Search" tool
  3. Upload file within tool settings
- Explain what's happening: chunking, embedding, vector indexing
- Mention TPM requirements (30k minimum recommended)
- Emphasize waiting for processing to complete
- Show where to check processing status

**Common Issues:**
- File upload fails → Check file size (max 512MB), supported formats (PDF, TXT, DOCX)
- Processing takes time → Set expectations (2-5 mins for small PDFs)
- Can't find File Search → Show exact navigation: Agent → Tools → Add Tool
- Tool added but disabled → Verify toggle is ON

**Checkpoint:**
"Has everyone's file finished processing? You should see it in the File Search tool's file list."

#### Part B: Configure Instructions (10 mins)

**Key Teaching Point:**
"Instructions are crucial for guiding the agent's tool usage. Microsoft recommends describing:
1. Primary objective
2. Tool purpose and triggers
3. Example queries that should use each tool"

**Facilitation Tips:**
- Have participants read `instructions/sales_agent_instructions_filesearch_only.txt` before pasting
- Highlight instruction best practices:
  - **Tool Purpose**: "Search the File Search tool for Contoso product information"
  - **Triggers**: When users ask about products, brands, specifications
  - **Examples**: "What brands of tents do we sell?"
- Explain `tool_choice` parameter (auto vs. forced)
- Show how instructions are non-deterministic guidance vs. code logic

**Common Issues:**
- File Search tool not appearing → Refresh page, verify processing completed
- Agent not using tool → Check tool is enabled (toggle ON)
- Agent gives generic answers → Verify instructions reference tool explicitly
- Instructions formatting issues → Show proper paste location

**Testing Checkpoint:**
Everyone test with: "What brands of tents do we sell?"
- Discuss: How did the agent know to use File Search?
- Observe: Check if response cites the uploaded document
- Explain: Agent reasoning process (query analysis → tool selection → response)
- Compare: File Search (built-in) vs. Azure AI Search (external service)

### Exercise 3: Add Bing Grounding (25 mins)

#### Part A: Create Resource (10 mins)

**Facilitation Tips:**
- Create resource as a group (avoid mistakes)
- Explain pricing/tier implications briefly
- Note provisioning time varies

**Common Issues:**
- Resource creation fails → Check quotas/permissions
- Can't find Bing Grounding → Show exact navigation path
- Provisioning slow → Set expectations (3-5 mins)

**Checkpoint:**
"Raise your hand when your Bing Grounding resource shows 'Succeeded'"

#### Part B: Connect & Enhance (15 mins)

**Key Teaching Point:**
"Now you're adding a second tool! The optimized instructions show **tool selection strategy** - when to use File Search (internal) vs. Bing Grounding (external) vs. BOTH (comparisons). This demonstrates multi-tool agent reasoning."

**Facilitation Tips:**
- Demonstrate authorization flow
- Have participants compare `instructions/sales_agent_instructions_filesearch_only.txt` vs. `instructions/instructions_bing_grounding_optimized.txt`
- Highlight the new "Tool Selection Strategy" section
- Emphasize the 3-result limit for Bing (prevents overwhelming responses)
- Show how instructions now reference BOTH tools with clear triggers

**Key Discussion Points:**
- How instructions evolved from single-tool to multi-tool
- Tool selection strategy (internal vs. external data)
- New example queries using both tools together
- Competitive intelligence use cases
- Best practices: citing sources, limiting Bing results

**Testing Checkpoint:**
Everyone test: "What beginner tents do our competitors sell?"
- Discuss: External vs. internal data
- Show: Agent using multiple tools together

### Exercise 4: Exploration (10 mins)

**Facilitation Tips:**
- Encourage creative queries
- Walk around to help individually
- Collect interesting examples to share

**Suggested Activities:**
- Modify instructions slightly and test
- Try complex multi-step queries
- Compare results between participants

**Group Sharing:**
"Who found an interesting query result? Let's see a few examples."

## Discussion Topics

### After Exercise 2 (5 mins)
- How does vector store ground the agent in knowledge?
- What's the advantage of in-project vector stores vs. external services?
- What types of documents work well for upload?
- When would you still use Azure AI Search separately?

### After Exercise 3 (5 mins)
- How do the instructions define tool selection strategy?
- What's the difference between internal (File Search) and external (Bing) data sources?
- Why limit Bing results to 3? (conciseness, relevance, cost)
- When would the agent use BOTH tools together?
- Real-world use cases for multi-tool agents?
- How does this compare to Exercise 2 with only one tool?

## Common Questions & Answers

**Q: Can I use my own data instead of the PDF?**  
A: Yes! File Search supports PDF, TXT, DOCX, and other formats. You can upload multiple files.

**Q: What's the difference between File Search and Azure AI Search?**  
A: File Search is built into Foundry for simplicity—just upload and go. Azure AI Search is a separate service with advanced features like custom analyzers, skillsets, and can be shared across multiple agents/projects. Both provide semantic search.

**Q: How does the agent decide which tool to use?**  
A: The model analyzes the user query and selects tools automatically (when `tool_choice="auto"`). Your instructions guide this decision by describing what each tool does and when to use it.

**Q: Can I force the agent to use a specific tool?**  
A: Yes, using the `tool_choice` parameter in code (covered in MCP module). In the portal, instructions are the primary way to influence tool selection.

**Q: How does the agent know which tool to use?**  
A: Instructions guide this + agent reasoning about the query.

**Q: Is this agent accessible via API?**  
A: Yes, and that connects to the MCP module coming next!

**Q: Can I add more tools?**  
A: Absolutely. Azure AI Foundry supports various tool types.

**Q: What if Bing returns too many results?**  
A: Instructions can specify result limits (we set to 3).

## Troubleshooting Guide

### Project & Agent Creation Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Can't create project | Permissions | Need Contributor/Owner at subscription |
| Provisioning fails | Quota/region | Try different region, check quotas |
| Can't create agent | Permissions | Need Azure AI User at project level |
| No project available | Not created yet | Complete project creation first |
| Model not deployed | Auto-deploy failed | Go to Models + Endpoints, deploy gpt-4o |
| Instructions not saving | Network/validation | Check connection, ensure not empty |

### File Search Tool Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Upload fails | File size/format | Check max 512MB, supported formats |
| Processing stuck | System load | Wait 2-5 mins, refresh, or retry |
| Tool not listed | Not added | Go to Tools → Add "File Search" |
| Agent doesn't use it | Not enabled/triggered | Verify toggle ON, check instructions |
| No results | Processing incomplete | Wait for embeddings to be created |
| Rate limit errors | Insufficient TPM | Check model deployment (need 30k+ TPM) |

### Bing Grounding Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Resource won't create | Quota/region | Try different region |
| Connection unauthorized | Permissions | Re-authorize connection |
| No external results | Configuration | Check resource status |

## Transition to MCP Module

**Bridge Message (2 mins):**
"You've built an agent in the portal - great for testing and demos. But what about integrating agents into applications? That's where Model Context Protocol (MCP) comes in. In the next module, we'll connect to Azure AI Foundry agents programmatically using Python and MCP."

**Key Connections:**
- Portal = visual configuration
- MCP = programmatic access
- Same agents, different interfaces
- MCP enables automation and integration

## Post-Module Resources
- Share completed agent examples
- Provide additional instruction templates
- Link to Azure AI Foundry documentation
- Preview MCP module materials

## Feedback Collection
- What worked well?
- What was confusing?
- Pacing appropriate?
- Technical difficulties encountered?

## Notes Section
_Use this space during delivery to track:_
- Common sticking points
- Good questions from participants
- Timing adjustments needed
- Examples to reuse next time
