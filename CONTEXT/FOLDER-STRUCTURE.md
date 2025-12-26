/email-assis
├── /backend                # FastAPI (Hugging Face Space)
│   ├── main.py             # Entry point
│   ├── /api                # Endpoints (auth, emails, chat)
│   ├── /services           # Logic (Gmail sync, AI classification)
│   ├── /brain              # Gemini-1.5-flash wrappers & tool definitions
│   ├── /models             # Pydantic schemas for API requests
│   └── requirements.txt    # Python dependencies
├── /frontend               # Next.js (Vercel)
│   ├── /src
│   │   ├── /app            # App router (inbox, chat, settings)
│   │   ├── /components     # UI (shadcn/ui, email cards, chat bubble)
│   │   ├── /hooks          # SWR/React Query for data fetching
│   │   └── /lib            # Utilities & API clients
│   ├── tailwind.config.ts
│   └── package.json
├── /context                # Documentation
│   ├── CONTEXT.md
│   ├── MVP.md
│   ├── PLAN.md
│   └── System Architecture.md
├── /prompts                # System prompts for Gemini
│   ├── classifier.txt
│   ├── summarizer.txt
│   └── agent_core.txt
├── RULES.md                # The constitution we just made
├── SCHEMA.sql              # Database structure
└── .env.example            # Template for your keys