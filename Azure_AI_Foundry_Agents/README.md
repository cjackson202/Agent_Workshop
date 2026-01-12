# Azure AI Foundry Agents Workshop

## Overview
This workshop module teaches participants how to create and enhance an Azure AI Foundry agent with multiple tools. Participants will progressively build a Contoso sales agent that can search product information and competitive insights.

## Learning Objectives
By the end of this module, participants will be able to:
- Create an agent in Azure AI Foundry portal
- Index documents in Azure AI Search
- Connect Azure AI Search as a tool to the agent
- Configure Bing Grounding for competitive intelligence
- Update agent instructions to leverage multiple tools
- Test and iterate on agent capabilities

## Prerequisites
- Access to Azure AI Foundry portal
- Azure subscription with permissions to create resources
- Access to Azure AI Search and Bing Grounding services

## Workshop Flow

### Exercise 1: Create Your First Agent (20 mins)
**Goal:** Set up a Foundry project and create a basic Contoso sales agent with instructions

#### Step 1.1: Access Azure AI Foundry Portal
1. Navigate to [Azure AI Foundry portal](https://ai.azure.com)
2. Sign in with your Azure credentials
3. Ensure you have the necessary permissions:
   - Azure subscription access
   - Contributor or Owner role at subscription level, OR
   - Azure AI User role at project level (if project already exists)

#### Step 1.2: Create a Foundry Project (if needed)
**If you already have a project, skip to Step 1.3**

1. From the Foundry Home page, click **"Create an agent"** or **"+ New project"**
2. In the project creation dialog:
   - **Project name**: `contoso-sales-workshop` (or your preferred name)
   - **Region**: Select a region close to you
   - Click **"Advanced options"** to review (optional):
     - Account name (auto-generated or customize)
     - Storage account settings
     - Key Vault settings
3. Click **"Create"**
4. Wait for provisioning (2-3 minutes):
   - A Foundry account is created
   - A project is created within that account
   - GPT-4o model is automatically deployed
5. Once complete, you'll land in the project workspace

#### Step 1.3: Create Your First Agent
1. If not already there, navigate to the **"Agent"** section (left sidebar)
2. Click **"+ Create agent"** or **"New agent"**
3. Configure the agent:
   
   **Basic Settings:**
   - **Agent Name**: `Contoso Sales Agent`
   - **Description**: `Helps customers with product inquiries and information about Contoso's outdoor gear`
   - **Model**: Select `gpt-4o` (or the deployed model in your project)

#### Step 1.4: Add Basic Agent Instructions
In the **Instructions** field, paste the following basic instructions:

```
You are a helpful sales assistant for Contoso, an online retailer specializing in outdoor camping and sports gear.

Your role:
- Assist customers with product inquiries
- Provide helpful information in a friendly and professional tone
- Be concise and accurate in your responses

Guidelines:
- Greet customers warmly
- If you don't have specific information, acknowledge it honestly
- Suggest that customers can ask about tents, hiking gear, camping equipment, and outdoor sports products
- Stay focused on outdoor gear and camping-related topics

Example greeting:
"Hello! I'm your Contoso sales assistant. I can help you with information about our outdoor camping and sports gear. What can I help you find today?"
```

#### Step 1.5: Save and Test the Agent
1. Click **"Save"** or **"Create"** to save your agent configuration
2. You'll be taken to the **Agent Playground**
3. Test the agent with simple queries:
   - "Hello, what can you help me with?"
   - "Tell me about Contoso"
   - "What types of products do you sell?"
4. Observe the agent's responses:
   - Notice how it follows the instructions
   - See how it maintains the friendly, professional tone
   - Confirm it identifies itself as a Contoso assistant

#### Step 1.6: Understand the Agent Interface
Familiarize yourself with the Playground:
- **Chat panel** (right): Where you interact with the agent
- **Configuration panel** (left): Where you edit instructions, add tools, adjust settings
- **Chat history**: Previous conversations with the agent
- **Settings**: Model parameters (temperature, max tokens, etc.)

**Key Observations:**
- The agent currently only uses the model's base knowledge
- It doesn't have access to specific Contoso product information yet
- In the next exercises, we'll enhance it with tools for knowledge grounding

**Checkpoint Questions:**
- Can you see your agent in the playground?
- Does it respond following the instructions you provided?
- Does it maintain the Contoso sales assistant persona?

### Exercise 2: Add File Search Tool for Knowledge Grounding (20 mins)
**Goal:** Use the File Search tool to upload product data and ground your agent in knowledge

#### What is File Search?
The **File Search tool** in Azure AI Foundry augments your agent with knowledge from documents you upload. It functions similarly to Azure AI Search but is built directly into Foundry for simplicity. When you upload files, Foundry automatically:
- Chunks the documents
- Creates vector embeddings
- Enables semantic search capabilities
- Allows the agent to retrieve relevant information

This grounds your agent in domain-specific knowledge without requiring external Azure AI Search resources.

#### Step 2.1: Upload File Using File Search Tool
1. In Azure AI Foundry portal, open your Contoso Sales Agent project
2. Navigate to your agent in the Playground
3. In the agent configuration panel, find the **"Tools"** section (right side bar)
4. In the **"Knowledge"** section, choose ***"Add+"***
4. Add the **"Files"** tool
5. Click **"Upload files"** within the File Search tool settings
6. Select `data/contoso-tents-datasheet (1).pdf` from your local directory
7. Wait for processing to complete:
   - The system chunks the document
   - Creates vector embeddings automatically
   - Makes content searchable for the agent

#### Step 2.2: Verify File Search is Enabled
1. Confirm the File Search tool shows as active
2. Verify your uploaded file appears in the tool's file list
3. The agent can now semantically search this knowledge base to answer queries

**Note:** Ensure your model deployment has at least 30k Tokens-Per-Minute (TPM) allocated for optimal performance.

#### Step 2.3: Update Agent Instructions
1. In the agent settings, locate "Instructions"
2. Copy content from `instructions/sales_agent_instructions_filesearch_only.txt`
3. Paste into agent instructions field
4. Review the instructions to understand:
   - **Primary Objective**: Product specialist helping customers
   - **Tool Usage**: When and how to use File Search tool
   - **Example Queries**: Suggested product questions
   - **Response Guidelines**: Citing sources, being specific
   - **Triggers**: What types of queries should invoke File Search
5. Save the updated instructions

**Best Practice:** Instructions should describe the tool's purpose and triggers. Notice how these instructions emphasize **"Always search the File Search tool"** and provide specific triggers for when to use it.

#### Step 2.4: Test File Search Integration
Test with queries like:
- "What brands of tents does Contoso sell?"
- "What is the best tent for rainy weather conditions?"
- "What type of fabrics are each tent created with?"

### Exercise 3: Add Bing Grounding Tool (25 mins)
**Goal:** Add competitive intelligence capabilities using Bing Search

#### Step 3.1: Create Bing Grounding Resource
1. Navigate to Azure Portal
2. Search for "Grounding with Bing Search"
3. Create new resource:
   - Select subscription and resource group
   - Choose pricing tier
   - Complete creation
4. Note the resource details for connection

#### Step 3.2: Connect Bing Grounding to Agent
1. Return to Azure AI Foundry portal
2. Open your Contoso Sales Agent
3. In the agent configuration panel, find the **"Tools"** section (right side bar)
4. In the **"Knowledge"** section, choose ***"Add+"***
4. Add **"Grounding with Bing Search"** tool
5. Configure connection:
   - Select your Bing Grounding resource
   - Authorize connection
   - Test connection
6. Save tool configuration

#### Step 3.3: Update Agent Instructions with Bing Capabilities
1. In agent settings, open "Instructions"
2. Replace existing instructions with content from `instructions/instructions_bing_grounding_optimized.txt`
3. Review the enhanced instructions to understand:
   - How agent uses **both File Search and Bing Grounding** tools
   - **Tool Selection Strategy**: When to use each tool
   - New competitive analysis capabilities
   - Query examples that trigger each tool
4. Save the updated instructions

**Key Enhancement:** Notice how these instructions build on Exercise 2 by adding external intelligence while keeping internal product knowledge via File Search.

#### Step 3.4: Test Complete Agent
Test with advanced queries like:
1. "What are the themes of Contoso tents?"
2. "How do these themes compare to competitor tents?"
3. "What is one competitor tent that is most similar to Contoso's TrailMaster X4 tent?"

### Exercise 4: Explore and Experiment (10 mins)
**Goal:** Test the fully enhanced agent

1. Try various query combinations
2. Observe how the agent uses different tools
3. Experiment with instruction modifications
4. Share interesting findings with the group

## Key Concepts

### Agent Tools & Knowledge Grounding

**Knowledge Tools** (provide data/context):
- **File Search**: Augments agent with knowledge from uploaded documents
  - Built-in tool in Azure AI Foundry
  - Creates vector embeddings automatically
  - Provides semantic search capabilities (similar to Azure AI Search)
  - No separate Azure resource needed
- **Grounding with Bing Search**: Provides external, real-time information from the web

**How Tool Selection Works:**
- The agent analyzes user queries and automatically selects appropriate tools
- Instructions guide the model on when to use each tool
- Tools can be invoked multiple times per query for comprehensive answers
- Example: "What tents do we sell?" → File Search | "Competitor tent prices" → Bing Search

### Agent Instructions
- Guide agent behavior and tone
- Define tool usage strategies
- Provide example queries for users
- Set boundaries for appropriate responses

### Progressive Enhancement
- Start simple with base agent
- Add tools incrementally
- Test after each addition
- Iterate on instructions based on testing

## Files in This Module

### Workshop Documentation
- `README.md` - Complete workshop guide (this file)
- `docs/QUICKSTART.md` - Quick reference guide
- `docs/FACILITATOR_GUIDE.md` - Detailed teaching guide

### Data Files
- `data/contoso-tents-datasheet (1).pdf` - Sample product data to upload via File Search tool

### Agent Instructions
- `instructions/sales_agent_instructions_filesearch_only.txt` - **Exercise 2**: Optimized for File Search tool only
- `instructions/instructions_bing_grounding_optimized.txt` - **Exercise 3**: Optimized for File Search + Bing Grounding
- `instructions/sales_agent_instructions_original.txt` - Original reference (not used in workshop)
- `instructions/instructions_bing_grounding_original.txt` - Original reference (not used in workshop)

## Reference Documentation
- [Azure AI Foundry Agents Quickstart](https://learn.microsoft.com/azure/ai-foundry/agents/quickstart?view=foundry-classic&pivots=ai-foundry-portal)
- [Tools Overview](https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools-classic/overview?view=foundry-classic)
- [Microhack: Agentic AI](https://github.com/Boykai/octo-microhack-agentic-ai)

## Tips and Troubleshooting

### File Search Tool Issues
- Wait for file processing to complete before testing (usually 2-5 mins for small PDFs)
- Check that File Search tool is enabled in agent settings
- Ensure document uploaded successfully (file size limits typically 512MB)
- Verify the file appears in the File Search tool's file list
- Check model deployment has sufficient TPM (minimum 30k recommended)

### Bing Grounding Issues
- Confirm resource is fully provisioned
- Check that connection is authorized
- Verify pricing tier supports your query volume

### Agent Behavior
- Instructions are crucial - be specific and clear
- Test incrementally after each change
- Use example queries to guide user behavior

## Next Steps
After completing this module:
- Explore additional tools available in Azure AI Foundry
- Learn about agent deployment options
- Integrate agents with custom applications
- Proceed to the MCP (Model Context Protocol) module to learn about programmatic agent access

## Additional Resources
- [Azure AI Foundry Documentation](https://learn.microsoft.com/azure/ai-studio/)
- [Azure AI Search Documentation](https://learn.microsoft.com/azure/search/)
- [Bing Grounding Documentation](https://learn.microsoft.com/bing/search-apis/)
