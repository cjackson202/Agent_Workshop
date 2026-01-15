# Workshop Facilitator Guide

## 🎯 Workshop Overview

**Title:** Building AI Agents with Model Context Protocol (MCP)  
**Duration:** 90-120 minutes  
**Audience:** Developers with Python experience  
**Level:** Intermediate  
**Format:** Instructor-led with hands-on exercises

## 📋 Pre-Workshop Checklist

### 1 Week Before
- [ ] Send pre-requisites email to participants
- [ ] Verify all participants have Azure ML Notebooks access
- [ ] Verify all participants have Azure access
- [ ] Create test Azure AI Foundry project for demos
- [ ] Test all scripts on Azure ML Notebooks environment
- [ ] Prepare backup materials (offline docs, code samples)
- [ ] Ensure participants know how to create venv in Azure ML

### 1 Day Before
- [ ] Test internet connectivity and Azure access
- [ ] Prepare multiple terminal windows for demos
- [ ] Load all documentation in browser tabs
- [ ] Test screen sharing setup
- [ ] Verify Azure deployments are running

### 1 Hour Before
- [ ] Start MCP server for demos
- [ ] Test agent connection
- [ ] Open VS Code with all files
- [ ] Start recording (if applicable)
- [ ] Prepare Q&A document

## 🎓 Workshop Agenda (120 minutes)

### Part 1: Introduction (15 min) - Slides 1-11
- **0:00-0:05** Welcome & agenda overview
- **0:05-0:10** Recap Day 1 & 2, position MCP
- **0:10-0:15** What is MCP and why it matters

**Facilitator Notes:**
- Keep intro brief - participants want to code!
- Use the "tool problem" slide to build motivation
- Quick poll: "Who has built API integrations before?"

### Part 2: Live Demonstrations (20 min) - Slides 12-14
- **0:15-0:20** Demo: Starting MCP server
- **0:20-0:25** Demo: Local testing with test_mcp.py
- **0:25-0:35** Demo: Azure agent integration

**Facilitator Notes:**
- **CRITICAL:** Have all scripts tested and ready
- Use two terminals side-by-side
- Explain every command before running
- Show server logs during agent interaction
- If demo fails, have screenshot backup ready

**Demo Script:**

```bash
# Terminal 1 - Setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt --pre
az login --identity --identity

# Terminal 1 - Start Server
cd /path/to/ERM_Agents_Workshop/MCP
python server.py

# Terminal 2 - Test
source .venv/bin/activate
python test_mcp.py

# Terminal 2 (after test succeeds)
# First: Create agent in Azure portal, copy agent ID
python get_agent_mi.py
# Try: "What is 25 + 17?"
# Try: "Calculate 100 minus 45"
# Show: Switch to Terminal 1 to see server logs
```

### Part 3: Guided Exercises (45 min) - Exercises 1-4
- **0:35-0:50** Exercise 1: Understanding MCP (15 min)
  - Participants review server.py
  - Add multiplication tool
- **0:50-1:10** Exercise 2: Local Testing (20 min)
  - Start servers
  - Run tests
  - Troubleshoot issues
- **1:10-1:20** Exercise 3: Azure Integration (10 min)
  - Configure Azure settings
  - Create agents
  - Chat with agents

**Facilitator Notes:**
- Walk the room (or watch screen shares)
- Common issues: port conflicts, Azure auth
- Have solutions ready but let them struggle briefly
- Pair struggling participants with successful ones

**Key Moments to Intervene:**
1. If >50% stuck on same issue → stop and address as group
2. Azure auth errors → do group authentication walkthrough
3. Port 8080 in use → show how to change ports
4. No one finishing → extend time, reduce scope

### Part 4: Concepts & Best Practices (20 min) - Slides 15-29
- **1:20-1:30** Tool design patterns
- **1:30-1:35** Authentication approaches
- **1:35-1:40** Debugging and troubleshooting

**Facilitator Notes:**
- Refer back to their code
- Ask participants to share their solutions
- Use whiteboard/screen for architecture diagrams
- Keep engagement high - ask questions

**Engagement Questions:**
- "Who found a bug in their tool? What was it?"
- "What tool would you build for your work?"
- "Anyone hit an interesting error?"

### Part 5: Advanced Topics (10 min) - Slides 30-36
- **1:40-1:45** Tool chaining, resources, multi-agent
- **1:45-1:50** Security, deployment, production considerations

**Facilitator Notes:**
- These are "future topics" - don't go deep
- Focus on possibilities, not implementation
- Share real-world examples if you have them

### Part 6: Open Work Time (25 min) - Slide 37
- **1:50-2:15** Exercise 5: Build custom tools
  - Participants choose their own adventure
  - Facilitator provides individual help

**Facilitator Strategy:**
- Circulate to each participant/group
- Ask: "What are you building?"
- Provide specific help, not general lectures
- Identify interesting solutions to share later

**Suggested Prompts:**
- Build a tool for your daily work
- Integrate with an API you use
- Create a domain-specific calculator
- Make a data validation tool

### Part 7: Wrap-Up (10 min) - Slides 38-40
- **2:15-2:20** Share & tell (3-4 participants)
- **2:20-2:25** Final Q&A
- **2:25-2:30** Next steps and resources

**Facilitator Notes:**
- Celebrate successes!
- Share contact info for follow-up questions
- Provide link to materials repository

## 🎭 Facilitation Tips

### Creating Engagement
1. **Start with a question:** "Has anyone struggled with managing agent tools?"
2. **Use real examples:** Share production agent stories
3. **Encourage experimentation:** "Try breaking it! That's how we learn."
4. **Celebrate errors:** "Great error! Let's learn from it together."

### Managing Different Skill Levels

**For Advanced Participants:**
- Point to SOLUTIONS.md for extension ideas
- Suggest they help others
- Challenge: "Can you build a tool that..."

**For Struggling Participants:**
- Pair with successful participant
- Provide more guided steps
- Focus on getting server.py running first
- Skip advanced exercises if needed

**For Mixed Groups:**
- Use breakout rooms by skill level (if virtual)
- Assign peer mentors
- Provide different challenge levels

### Handling Common Scenarios

**Scenario: "My server won't start"**
```powershell
# Check port
netstat -ano | findstr :8080

# Check dependencies
pip list | grep mcp

# Try different port
# Edit server.py: port=8081
```

**Scenario: "Azure authentication failed"**
```bash
# Re-authenticate (Azure ML Notebooks with Managed Identity)
az login --identity --identity
az account show
az account set --subscription "subscription-name"
```

**Scenario: "Agent not using tools"**
- Restart MCP server
- Check docstrings present
- Verify `@mcp.tool()` decorator
- Review agent instructions

**Scenario: "Everything works but confused about why"**
- This is OK! Understanding comes with time
- Walk through the flow diagram
- Explain: "Agent sees tool schema → decides to use it → calls MCP server"

## 📊 Success Metrics

### Minimum Success (Everyone should achieve)
- ✅ MCP server running
- ✅ test_mcp.py passing
- ✅ Agent created and responding
- ✅ At least one custom tool added

### Target Success (Most should achieve)
- ✅ All of minimum
- ✅ Understanding MCP architecture
- ✅ 2-3 custom tools built
- ✅ Can explain tools to others

### Stretch Success (Some will achieve)
- ✅ All of target
- ✅ Complex custom tool (API integration, etc.)
- ✅ Production-ready error handling
- ✅ Helping other participants

## 🐛 Troubleshooting Decision Tree

```
Issue: Participant stuck
├── Server not starting?
│   ├── Port in use → netstat, change port
│   ├── Import errors → pip install
│   └── Syntax error → review server.py
├── Test client failing?
│   ├── Server not running → check Terminal 1
│   ├── Wrong URL → verify localhost:8080
│   └── Tool not found → restart server
├── Azure agent failing?
│   ├── Auth error → az login --identity
│   ├── Wrong endpoint → check Azure portal
│   └── Model error → verify deployment
└── Tool not working?
    ├── Not listed → check decorator
    ├── Error on call → add debugging
    └── Wrong result → test function directly
```

## 📝 Q&A Response Guide

**Q: "Can I use MCP in production?"**
A: Yes! Add authentication, HTTPS, monitoring. See Deployment slide.

**Q: "How much does this cost?"**
A: Server hosting (~$50-200/mo Azure) + model usage (per call). MCP itself is free.

**Q: "What if the tool call fails?"**
A: Agent sees error message, can retry or try different approach.

**Q: "Can I use languages other than Python?"**
A: Yes! MCP is language-agnostic. Server can be in any language.

**Q: "How do I version my tools?"**
A: Version your MCP server. Use different URLs for different versions.

**Q: "What about sensitive data?"**
A: Never put secrets in code. Use Azure Key Vault. Implement auth on MCP server.

**Q: "Can one agent use multiple MCP servers?"**
A: Yes! Pass multiple MCPStreamableHTTPTool instances.

**Q: "How do I test tools without running the agent?"**
A: Use test_mcp.py or call functions directly in Python.

## 🎯 Workshop Outcomes

By the end, participants should be able to:

1. **Explain** MCP architecture and benefits
2. **Create** MCP servers with custom tools
3. **Test** tools using local client
4. **Integrate** MCP servers with Azure AI agents
5. **Debug** common tool and agent issues
6. **Design** tools for their specific use cases

## 📚 Post-Workshop Follow-Up

### Immediately After
- [ ] Share workshop materials (GitHub link, slides)
- [ ] Send feedback survey
- [ ] Answer follow-up questions in email/Slack
- [ ] Share photos/recordings (if permitted)

### Within 1 Week
- [ ] Compile FAQ from workshop questions
- [ ] Update materials based on feedback
- [ ] Share additional resources
- [ ] Schedule office hours for advanced questions

### Within 1 Month
- [ ] Check in on participant progress
- [ ] Share success stories
- [ ] Plan advanced workshop if interest
- [ ] Update workshop based on lessons learned

## 🔄 Continuous Improvement

### After Each Workshop, Review:
1. What questions came up repeatedly?
2. Where did most participants struggle?
3. What exercises took longer than expected?
4. What demos were most engaging?
5. What would you change?

### Update Materials:
- Add clarifications to README
- Improve error messages in scripts
- Add more examples to SOLUTIONS.md
- Update troubleshooting guide
- Refine timing estimates

## 🎬 Virtual Workshop Adaptations

### Additional Prep
- [ ] Test screen sharing quality
- [ ] Prepare breakout rooms
- [ ] Set up virtual whiteboard
- [ ] Enable chat monitoring
- [ ] Have co-facilitator for chat/troubleshooting

### Modifications
- **More breaks:** 5 min every 30 min
- **More checks:** "Thumbs up if server running"
- **Chat monitoring:** Co-facilitator watches chat
- **Recording:** "I'm recording for notes only"
- **Screen share:** Ask participants to share when stuck

### Engagement Techniques
- Use polls: "How far are you? A) Server running B) Testing C) Agent working"
- Breakout rooms for exercises
- Virtual hand raises
- Chat for questions
- Reactions for quick feedback

## 🏆 Success Stories

*Document real examples as they happen!*

### Example 1: Custom Business Tool
"Participant built tool to query internal database, connected to agent, now has conversational interface to company data"

### Example 2: API Integration
"Participant integrated weather API, showed how agent could answer: 'Should I bring an umbrella tomorrow?'"

### Example 3: Multi-Tool Workflow
"Participant created tools for data fetch, transform, and visualize. Agent chained them automatically!"

*Your success stories:*
- ________________________________
- ________________________________
- ________________________________

---

## 📞 Support Contacts

**During Workshop:**
- Primary Facilitator: [Your Name/Contact]
- Technical Support: [Assistant Name/Contact]
- Azure Help: [Azure Admin Contact]

**After Workshop:**
- Email: [Your Email]
- Slack: [Your Slack]
- Office Hours: [Schedule]

---

## ✅ Final Checklist

**Start of Workshop:**
- [ ] Tested all demos
- [ ] Participants have materials
- [ ] Azure access verified
- [ ] Backup plans ready
- [ ] Timer set for each section

**During Workshop:**
- [ ] Monitor participant progress
- [ ] Answer questions promptly
- [ ] Keep to schedule (roughly)
- [ ] Document interesting issues
- [ ] Note feedback for improvements

**End of Workshop:**
- [ ] Share materials
- [ ] Send feedback survey
- [ ] Thank participants
- [ ] Schedule follow-up
- [ ] Back up workshop notes

---

**Remember:** Participants learn by doing! Keep lectures short, examples practical, and exercises hands-on.

**Good luck! You've got this! 🚀**
