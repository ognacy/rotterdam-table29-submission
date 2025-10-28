# Team 29 - Workshop Management System

## Parent Agent (Coordinator)

The **Parent Agent** serves as the central coordinator for the workshop management system, intelligently routing requests to specialized agents and providing comprehensive care oversight.

### Architecture

```
┌─────────────────────────────────────────┐
│         PARENT AGENT                    │
│      (Central Coordinator)              │
│                                         │
│  • Intelligent Routing                  │
│  • Daily Summaries                      │
│  • Irregularity Monitoring              │
│  • Trend Analysis                       │
└─────────────────────────────────────────┘
         │          │          │
         ▼          ▼          ▼
    ┌────────┐ ┌────────┐ ┌────────────┐
    │Caregiver│Doctor   │Data Collection│
    │ Agent  ││ Agent  ││   Agent     │
    └────────┘ └────────┘ └────────────┘
    (Team)     (Team)     (Team)
```

### Files Structure

```
team29/
├── agent.py              # Main parent agent definition
├── parent_tools.py       # Tools used by parent agent
├── tools.py              # Shared utility functions
├── mock_data.py          # Mock data generators for testing
├── .env                  # Environment configuration
├── README.md             # This file
└── SESSION_INFO.md       # Session management documentation
```

### Parent Agent Capabilities

#### 1. Memory & Context Retention
The agent includes **persistent memory** that:
- Remembers care recipient information (names, relationships)
- Tracks ongoing health concerns across conversations
- Recalls previous irregularities and actions taken
- Provides conversation continuity with context-aware responses
- Maintains up to 50 messages of conversation history
- Personalizes responses based on previous interactions

#### 2. Intelligent Routing
Routes questions to appropriate specialist agents:
- **Caregiver Agent**: Schedules, daily tasks, care instructions
- **Doctor Agent**: Medical records, prescriptions, appointments
- **Data Collection Agent**: Movement, sensors, behavioral data

#### 3. Direct Information Provision
Provides immediate access to:
- Daily summaries (comprehensive overview of all metrics)
- Upcoming appointments
- Irregularity alerts
- Medical documentation summaries
- Trend analysis (7-day, 30-day patterns)

#### 4. Proactive Monitoring
- Monitors for irregularities in daily patterns
- Alerts on high-severity issues
- Tracks medication compliance
- Analyzes long-term trends

#### 5. Session Management
- **Automatic conversation tracking**: Each chat is a separate session
- **History preservation**: All messages stored in `session.events`
- **Cross-session memory**: Past sessions searchable via memory service
- **Persistent options**: Can use Vertex AI for production persistence

See [SESSION_INFO.md](SESSION_INFO.md) for detailed session documentation.

### Available Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `route_to_caregiver()` | Route to caregiver agent | Schedule/task questions |
| `route_to_doctor()` | Route to doctor agent | Medical questions |
| `route_to_data_collector()` | Route to data agent | Sensor/movement queries |
| `get_daily_summary()` | Comprehensive daily report | "How was today?" |
| `get_upcoming_appointments()` | View scheduled appointments | "What's coming up?" |
| `check_irregularities()` | Find concerning patterns | "Any issues?" |
| `get_medical_summary()` | Recent medical docs | "Show medical records" |
| `analyze_trends()` | Multi-day analysis | "Show trends" |
| `answer_common_question()` | Simple inquiries | General questions |

### Integration with Other Agents

The parent agent is designed to work seamlessly with the specialized agents your teammates are building:

1. **Caregiver Agent** (Your teammate)
   - Will handle: Daily schedules, task lists, caregiver profiles, instructions
   - Parent routes: Schedule changes, task management, care preferences

2. **Doctor Agent** (Your teammate)
   - Will handle: Medical documentation, prescriptions, doctor appointments
   - Parent routes: Medical history, medication questions, appointment booking

3. **Data Collection Agent** (Your teammate)
   - Will handle: Real-time sensor data, movement tracking, pattern detection
   - Parent routes: Activity queries, sensor readings, behavioral analysis

### Mock Data for Testing

Since the other agents aren't built yet, the parent agent uses mock data from `mock_data.py`:
- Appointments
- Movement/activity data
- Presence and location tracking
- Motion sensor data
- Medical documentation
- Behavioral patterns
- Irregularities and alerts

This allows you to test the parent agent independently while your teammates build their agents.

### How Session + Memory Work Together

The parent agent uses **Sessions** for current conversations and **Memory** for long-term recall:

#### Architecture

```
┌────────────────────────────────────────────────────┐
│        Parent Agent (Current Turn)                 │
│                                                    │
│  Tools: PreloadMemoryTool + Coordination Tools    │
└────────────────────────────────────────────────────┘
              ↕                          ↕
    ┌─────────────────┐        ┌─────────────────────┐
    │     SESSION     │        │       MEMORY        │
    │   (Short-term)  │        │    (Long-term)      │
    │                 │        │                     │
    │ • Current chat  │        │ • Past sessions     │
    │ • Events list   │←saved→ │ • Care recipient    │
    │ • Temp state    │        │ • Health concerns   │
    │ • This convo    │        │ • Cross-session     │
    │                 │        │                     │
    │ InMemory or     │        │ InMemory or         │
    │ VertexAI        │        │ VertexAI MemBank    │
    └─────────────────┘        └─────────────────────┘

Session = "What's happening NOW in this conversation?"
Memory  = "What do I remember from ALL past conversations?"
```

#### Memory Features

1. **Automatic Memory Saving**: The `after_agent_callback` automatically saves each conversation to memory
2. **Preload Tool**: `PreloadMemoryTool()` automatically loads relevant past context at the start of each turn
3. **Semantic Search**: Memory service finds relevant past conversations based on meaning (with Vertex AI)
4. **Cross-Session Recall**: Information from past sessions is available in new conversations

#### Memory in Action

**First Conversation:**
```
User: "This is for my mother, Margaret. She's 78."
Agent: "Got it! I'll remember that we're monitoring Margaret's health. How can I help you today?"
→ Session saved to memory automatically
```

**New Session - Next Day:**
```
User: "How is she doing today?"
Agent: [PreloadMemoryTool retrieves: "monitoring Margaret"]
       "Let me check how Margaret is doing today..." [Uses remembered name from past session]
```

**Follow-up with Context:**
```
User: "Any updates on those sleep issues?"
Agent: [Searches memory for "sleep issues"]
       "Following up on the sleep concerns from our previous conversation - let me check the latest data..."
```

**Memory Persistence:**
- **InMemoryMemoryService**: Remembers within server runtime (lost on restart)
- **VertexAiMemoryBankService**: Persists indefinitely (survives restarts)

### Example Interactions

**Daily Overview:**
```
User: "How was mom doing today?"
Parent Agent: [Calls get_daily_summary()]
→ Shows comprehensive report with activity, sleep, meals, medications, mood
```

**Schedule Management:**
```
User: "What's on the schedule tomorrow?"
Parent Agent: [Routes to caregiver agent]
→ "I'll connect you with the caregiver agent who manages schedules..."
```

**Health Monitoring:**
```
User: "Is there anything concerning?"
Parent Agent: [Calls check_irregularities() + analyze_trends()]
→ Shows any alerts and 7-day trend analysis
```

**Medical Questions:**
```
User: "What medications is dad taking?"
Parent Agent: [Routes to doctor agent]
→ "I'll connect you with the doctor agent who manages medical records..."
```

### Environment Setup

The `.env` file contains:
```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-04-b310107eab82
GOOGLE_CLOUD_LOCATION=eu-west4
GOOGLE_API_KEY=<your-key>
```

### Running the Agent

#### Option 1: With In-Memory Memory Service (Default - For Development)

```bash
# Activate virtual environment
source .venv/bin/activate

# Start the ADK web server (uses InMemoryMemoryService by default)
adk web

# Access at http://127.0.0.1:8000
```

**Note:** This stores memory only during runtime. Memory is lost when server restarts.

#### Option 2: With Vertex AI Memory Bank (For Production)

First, create an Agent Engine in Vertex AI and get the Agent Engine ID. Then:

```bash
# Set up authentication
gcloud auth application-default login

# Export required environment variables
export GOOGLE_CLOUD_PROJECT="qwiklabs-gcp-04-b310107eab82"
export GOOGLE_CLOUD_LOCATION="eu-west4"

# Start with Memory Bank
adk web --memory_service_uri="agentengine://YOUR_AGENT_ENGINE_ID"

# Access at http://127.0.0.1:8000
```

**Benefits of Vertex AI Memory Bank:**
- Persistent memory across server restarts
- Semantic search (understands meaning, not just keywords)
- Intelligent memory extraction and consolidation
- Scalable for production use

### Testing

Try these sample queries with your parent agent:
1. "Give me a daily summary"
2. "Are there any irregularities?"
3. "What appointments are coming up?"
4. "Show me the medical records"
5. "Analyze the trends from this week"
6. "I need to update tomorrow's schedule" (should route to caregiver)
7. "What medications should be taken?" (should route to doctor)

### Next Steps

1. ✅ Parent Agent is complete
2. ⏳ Teammates building: Caregiver Agent, Doctor Agent, Data Collection Agent
3. ⏳ Replace mock data with real integrations
4. ⏳ Connect to actual sensor data sources
5. ⏳ Implement forum monitoring and medical documentation management

---

**Note**: This parent agent is production-ready for the hackathon demo. It can work independently with mock data or coordinate with the other agents once your teammates complete them.
