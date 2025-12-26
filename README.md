# **Kyra 🧠📩**

**Kyra** is a high-performance Personal Email Operating System. It’s built to move beyond simple filtering and auto-replies, acting as a cognitive layer that learns your behavior and manages your email workload autonomously.

Unlike standard email clients, Kyra treats emails as documents and uses a modular, multi-brain architecture to reduce cognitive load and provide data-backed explainability for every action it takes.

## **🏗️ Core Architecture (The Three Brains)**

Kyra is powered by three distinct intelligence layers:

1. **Classifier Brain**: Analyzes incoming mail to determine intent and urgency (Urgent, Informational, Promotional, Human, or Automated).  
2. **Memory Brain**: A layered system consisting of Short-term (session context), Long-term (structured preferences), and Interaction memory (learning from opens, replies, and ignores).  
3. **Conversation Brain**: A command-centric chat interface that allows you to ask "Why was this urgent?", teach the agent new rules, and issue proactive commands.

## **✨ Key Features**

* **Priority Inbox**: An AI-curated view that focuses on "Needs Action" vs "FYI," moving away from the "unread count" anxiety.  
* **Explainability by Default**: Every decision made by the agent can be questioned. Kyra provides clear reasoning based on sender history, keywords, and calendar proximity.  
* **Human-in-the-Loop Auto-replies**: Controlled draft generation where the user owns the send action.  
* **Attachment Intelligence**: Deep processing of PDFs and Docs to summarize contents and make them searchable via the chat interface.  
* **Temporal Awareness**: Understands that urgency is dynamic. A deadline approaching on Friday makes an email more urgent on Thursday than it was on Monday.

## **🛠️ Tech Stack**

| Layer | Technology |
| :---- | :---- |
| **Frontend** | Next.js (App Router), Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI (Python) |
| **Database** | PostgreSQL (Primary) \+ pgvector (Embeddings) |
| **LLM Gateway** | Gemini 1.5 Flash (Default) |
| **Task Queue** | Celery \+ Redis |
| **Real-time** | WebSockets / Supabase Realtime |

## **📂 Project Structure**
```
├── /backend                \# FastAPI logic & services  
│   ├── /api                \# Endpoints (auth, emails, chat)  
│   ├── /brain              \# Gemini wrappers & tool definitions  
│   └── /services           \# Gmail sync & AI classification  
├── /frontend               \# Next.js mobile-first UI  
│   ├── /components         \# shadcn/ui components  
│   └── /hooks              \# React Query / SWR  
├── /prompts                \# System prompts (classifier, summarizer, etc.)  
├── RULES.md                \# System constitution & agent rules  
└── SCHEMA.sql              \# Database & pgvector definitions
```

## **🚀 Getting Started**

### **Prerequisites**

* Python 3.10+  
* Node.js 18+  
* PostgreSQL with pgvector extension

### **Installation**

1. **Clone the repository**:
   ```
   git clone https://github.com/StealthTensor/Kyra.git
   cd Kyra
   ```

3. **Backend Setup**:
   ```
   cd backend  
   pip install \-r requirements.txt  
   \# Setup your .env with GOOGLE\_CLIENT\_ID and GEMINI\_API\_KEY  
   python main.py
   ```

5. **Frontend Setup**:
   ```
   cd frontend  
   npm install  
   npm run dev
   ```