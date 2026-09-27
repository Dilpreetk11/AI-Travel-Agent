# ✈️ AI Travel Agent — Multi-Agent Travel Booking System

An AI-powered travel planning system built with **LangGraph** that uses multiple specialized AI agents to search for flights and hotels, generate a personalized itinerary, and produce a final travel plan. The system uses **long-term memory with PostgreSQL** so user conversations and travel preferences can persist across sessions.

## 🚀 Features

* 🤖 **Multi-Agent Architecture** using LangGraph
* ✈️ **Flight Search Agent** for flight-related information
* 🏨 **Hotel Search Agent** powered by Tavily web search
* 🗺️ **Itinerary Agent** that creates a personalized day-by-day travel plan
* 🧠 **Final AI Agent** that combines all gathered information into a complete response
* 💾 **Long-Term Memory** using PostgreSQL checkpointer
* 🔄 **Stateful Conversations** across multiple queries and sessions
* 🌐 **Streamlit UI** for an interactive travel-planning experience
* 🔑 Environment-based API key management using `.env`
* ⚡ Graph-based agent orchestration with LangGraph

## 🏗️ Architecture

The application follows a sequential multi-agent workflow:

```text
                    User Query
                        │
                        ▼
              ┌──────────────────┐
              │   Flight Agent   │
              │  Flight Search   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Hotel Agent    │
              │  Tavily Search   │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Itinerary Agent  │
              │ Trip Planning    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   Final Agent    │
              │ Response Builder │
              └────────┬─────────┘
                       │
                       ▼
                 Final Travel Plan
                       │
                       ▼
                PostgreSQL Memory
```

## 🧩 Agents

### 1. Flight Agent

Processes the user's flight requirements and retrieves relevant flight information using the configured flight search tool.

### 2. Hotel Agent

Uses **Tavily** to search the web for relevant hotel information based on the destination and travel requirements.

### 3. Itinerary Agent

Combines the user's requirements and search results to generate a structured travel itinerary.

### 4. Final Agent

Synthesizes the flight, hotel, and itinerary information into a concise final travel recommendation.

## 🧠 Long-Term Memory

The application uses **LangGraph's PostgreSQL checkpointer** to maintain conversation state.

A unique `thread_id` is used for each user/session, allowing the system to maintain context across multiple queries.

```text
User Query
    ↓
LangGraph State
    ↓
PostgreSQL Checkpointer
    ↓
Persistent Conversation Memory
```

This allows users to continue refining their trip instead of starting from scratch with every query.

## 🛠️ Tech Stack

| Technology    | Purpose                            |
| ------------- | ---------------------------------- |
| Python        | Core application                   |
| LangGraph     | Multi-agent workflow orchestration |
| LangChain     | LLM/tool integration               |
| Groq          | LLM inference                      |
| GPT-OSS 120B  | Language model                     |
| Tavily        | Web search                         |
| PostgreSQL    | Persistent conversation memory     |
| Psycopg       | PostgreSQL connectivity            |
| Streamlit     | Web interface                      |
| python-dotenv | Environment variable management    |

## 📁 Project Structure

```text
AI-Travel-Agent/
│
├── main.py
├── frontend.py
├── file.py
│
├── tools/
│   └── tavily_tool.py
│
├── travel_plans/
│
├── .gitignore
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Dilpreetk11/AI-Travel-Agent.git
cd AI-Travel-Agent
```

### 2. Create a virtual environment

```bash
python -m venv langgraph_env3
```

Activate it on Windows:

```powershell
langgraph_env3\Scripts\activate
```

### 3. Install dependencies

Install the required Python packages according to the project's dependencies.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
DATABASE_URL=your_postgresql_connection_string
```

> Never commit your `.env` file or expose API keys publicly.

### 5. Run the application

Start the Streamlit interface:

```powershell
streamlit run frontend.py
```

The application will open in your browser.

## 💡 Example Query

```text
Plan a 5-day trip to Dubai for two people with a moderate budget.
Find suitable flights and hotels and create a day-wise itinerary.
```

The system processes the request through the agent workflow and generates a complete travel plan.

## 🔄 Workflow

```text
User
 ↓
Streamlit Frontend
 ↓
LangGraph State
 ↓
Flight Agent ──────→ Flight Results
 ↓
Hotel Agent ───────→ Hotel Results
 ↓
Itinerary Agent ───→ Day-wise Itinerary
 ↓
Final Agent ───────→ Final Travel Plan
 ↓
PostgreSQL Checkpointer
```

## 🔐 Security

API credentials are stored using environment variables and excluded from version control through `.gitignore`.

The following files/directories should not be committed:

```text
.env
langgraph_env3/
__pycache__/
travel_plans/
```

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

* Multi-agent AI systems
* LangGraph state management
* Agent orchestration
* Tool calling
* Web search integration
* LLM-based reasoning
* Persistent conversation memory
* PostgreSQL checkpointing
* Streamlit application development
* Environment and API key management

## 👩‍💻 Author

**Dilpreet Kaur**

B.Tech Information Technology
Guru Tegh Bahadur Institute of Technology

GitHub: https://github.com/Dilpreetk11
