# Azure AI Foundry Agents - Quick Start Guide

## What You'll Build
A Contoso sales agent that searches internal product data and external competitive intelligence.

## Quick Steps

### 1. Create Project & Agent (10 mins)
```
1. Go to https://ai.azure.com
2. Create Project: "contoso-sales-workshop" → Wait for provisioning
3. Create Agent: "Contoso Sales Agent"
4. Add Instructions:
   - Role: Sales assistant for Contoso outdoor gear
   - Tone: Friendly and professional
   - Focus: Camping and outdoor sports products
5. Save → Test in Playground
```

**Test:** "Hello, what can you help me with?"

### 2. Add File Search Tool (10 mins)
```
Foundry Portal → Agent → Tools → Add "File Search"
File Search → Upload data/contoso-tents-datasheet.pdf
Wait for processing → Verify file appears
Agent → Instructions → Paste from instructions/sales_agent_instructions_filesearch_only.txt
```

**Test:** "What brands of tents do we sell?"

**Note:** File Search is a built-in knowledge tool that creates vector embeddings automatically, similar to Azure AI Search.

### 3. Add Bing Grounding (10 mins)
```
Azure Portal → Create "Grounding with Bing Search"
Foundry Portal → Agent → Tools → Add "Bing Grounding"
Agent → Instructions → Replace with instructions/instructions_bing_grounding_optimized.txt
```

**Test:** "What beginner tents do our competitors sell?"

## Sample Queries

### With File Search Tool Only
- "What brands of hiking shoes do we sell?"
- "Show tents by price range"
- "What features do the tents have?"
- "Compare the technical specifications of different tent models"

### With Bing Grounding Added
- "What beginner tents do competitors sell? Include prices."
- "Show tents similar to competitors' prices by region"

## Architecture
```
┌─────────────────────────────────────┐
│   Azure AI Foundry Agent            │
│   (Contoso Sales Agent)             │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────────────┐  ┌─▼─────────────────┐
│ File Search Tool   │  │ Bing Grounding      │
│ (Internal Docs)    │  │ (External Web)      │
│ • Uploads files    │  │ • Real-time data    │
│ • Vector embeddings│  │ • Competitive intel │
└────────────────────┘  └─────────────────────┘
```

## Common Issues

**File upload failed**
→ Check file size (max 512MB) and format (PDF, TXT, DOCX supported)

**File still processing**
→ Wait 2-5 minutes for embeddings to be created

**File Search tool not working**
→ Verify tool is enabled and file appears in file list

**Insufficient TPM**
→ Ensure model deployment has 30k+ TPM (check Models + Endpoints)

**Bing connection failed**
→ Verify Bing Grounding resource is provisioned and connection authorized

**Agent gives generic responses**
→ Check tools are enabled and instructions reference them correctly

## Time Estimates
- Exercise 1: 20 mins (Create project & agent with instructions)
- Exercise 2: 20 mins (File Search tool)
- Exercise 3: 25 mins (Bing Grounding tool)
- Exercise 4: 10 mins (Testing)
- **Total: ~75 minutes**

**Prerequisites Check:** 5 mins (Azure access verification)
