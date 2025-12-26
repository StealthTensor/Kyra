📜 RULES.md — THE CONSTITUTION

Note to Antigravity: You are building a high-stakes Personal AI Email OS. Precision is more important than speed. If you skip a detail, you create technical debt that we cannot afford. Follow these rules or don't code at all.



1\. THE "NO SKIP" DIRECTIVES

No Placeholders: Never use // TODO, // implement later, or // ... logic here. If a function is needed, write the full logic or ask for clarification.



Error Handling: Every API call (Gmail, Gemini, DB) must have a try-catch block with specific error logging. No generic "Something went wrong" errors.



Data Integrity: Never "simulate" data. If we are building a schema, it must be the production-ready version.



2\. ARCHITECTURAL CONSTRAINTS (Vibe: Broke but Pro)

Stack: Next.js (Frontend) + FastAPI/Python (Backend on Hugging Face) + PostgreSQL (Supabase/Neon).



Brain: Use gemini-1.5-flash. Optimize prompts for token efficiency.



Statelessness: Hugging Face Spaces can restart anytime. Never store state in memory. Everything must be in the DB or Vector Store.



Rate Limiting: Implement slowapi (Python) or a custom middleware to limit requests per User ID. We are not paying for overages.



3\. UI/UX STANDARDS

Vibe: Dark mode by default. High contrast. Minimalist.



Speed: Use "Optimistic UI" patterns. When I archive an email, it should disappear instantly from the UI while the backend processes in the background.



Scannability: The UI must be easy to skim. Use clear typography and consistent spacing.



4\. CODE QUALITY \& COMMENTS

NO COMMENTS: Per user preference, do not write comments in the code unless it is a complex Regex or a hacky workaround for a known API bug.



Type Safety: TypeScript is mandatory for the frontend. No any types.



Modular LLM: Wrap the Gemini call in a Brain class/service so we can swap it with Groq or Perplexity in 5 seconds.



5\. RECOVERY \& LOGGING

Audit Trail: Every time the AI Agent makes a decision (e.g., "Marking as Urgent"), it must log the "Reasoning" into the agent\_logs table.



Sync Logic: Use a "Delta Sync" approach. Don't fetch the whole inbox every time—only fetch what changed since the last historyId.

