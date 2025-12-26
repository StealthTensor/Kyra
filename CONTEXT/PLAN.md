Perfect. Now we stop ideating and **turn this into an execution weapon**.

I’ll give you a **week-by-week PHASE PLAN**, with:

* **Clear deliverables**
* **Exact responsibilities** (YOU vs ANTIGRAVITY)
* **Anti-skipping guards** (so he can’t rush and ruin fundamentals)
* **Only free-tier + open-source stack**
* Built in a way that **forces correctness before speed**

No code. No fluff. This is an **engineering battle plan**.

---

# 🧠 EMAIL AI OS — WEEK-BY-WEEK BUILD PLAN (V1)

Assumption:

* Solo + AI agent (Antigravity)
* Time horizon: **8 weeks**
* Stack: **Open-source, free tiers only**
* Goal: **Working, intelligent MVP — not a demo**

---

## 🧱 PHASE 0 (Week 0) — FOUNDATIONS & RULES (NON-NEGOTIABLE)

### Goal

Lock constraints, prevent architecture debt, and tame Antigravity.

### Deliverables

* `PRODUCT.md` → MVP scope (frozen)
* `ARCHITECTURE.md` → system diagram + data flow
* `RULES.md` → agent rules (VERY IMPORTANT)
* Repo initialized

### YOU do

* Write **RULES.md**:

  * ❌ No skipping schemas
  * ❌ No “we’ll do later”
  * ❌ No UI before data correctness
  * ❌ No LLM magic without logging
* Define **Definition of Done** for each phase

### ANTIGRAVITY does

* Repo setup
* Folder structure (empty, no logic yet)

### Tech decisions (locked now)

* **Frontend**: Next.js (App Router) + Tailwind + shadcn/ui
* **Backend**: FastAPI (Python)
* **Auth**: Google OAuth (manual, no Auth0)
* **DB**: PostgreSQL
* **Vector DB**: pgvector (inside Postgres)
* **Jobs**: Celery + Redis
* **Realtime**: WebSockets (FastAPI native)
* **LLMs**: Provider-agnostic wrapper (Gemini free → default)

📌 **Gate**: If this phase isn’t solid, the project dies later.

---

## 📩 PHASE 1 (Week 1) — GMAIL INGESTION (READ-ONLY, CLEAN)

### Goal

Get emails **correctly and reproducibly** into your system.

### Deliverables

* Gmail OAuth flow
* Multi-account support
* Raw email ingestion
* Clean text extraction

### YOU do

* Define **email document contract** (immutable)
* Review Gmail scopes (read-only first)

### ANTIGRAVITY does

* Gmail API integration
* Fetch:

  * message_id
  * thread_id
  * headers
  * raw body
* HTML → clean text
* Store metadata in Postgres

### Hard rules

* ❌ NO importance scoring yet
* ❌ NO LLM calls yet
* ❌ NO UI beyond “email list dump”

📌 **Gate**:

* Restart backend → emails rehydrate perfectly
* Multiple Gmail accounts don’t collide

---

## 🧠 PHASE 2 (Week 2) — MEMORY & DATA MODELS (THE HEART)

### Goal

Build **memory before intelligence**.

### Deliverables

* Email schema (final)
* Preference memory
* Interaction logging
* Vector embeddings pipeline (offline)

### YOU do

* Design memory tables:

  * `preferences`
  * `sender_profiles`
  * `interaction_events`
* Decide what is **structured vs vectorized**

### ANTIGRAVITY does

* pgvector setup
* Email embedding generation
* Store embeddings per email + per thread
* Interaction event logger:

  * open
  * ignore
  * reply
  * manual priority change

### Hard rules

* ❌ No ranking yet
* ❌ No summaries yet
* ❌ No chat yet

📌 **Gate**:

* You can answer: *“Why does the system think this email matters?”* using stored data alone

---

## 🧮 PHASE 3 (Week 3) — PRIORITY ENGINE (NO CHAT, NO UI MAGIC)

### Goal

Build the **importance score engine**.

### Deliverables

* Importance scoring function
* Confidence score
* Bucketing logic

### YOU do

* Define importance formula (initial weights):

  ```
  score = sender_weight
        + content_signal
        + interaction_signal
        + temporal_signal
  ```
* Decide decay curves

### ANTIGRAVITY does

* Classifier LLM calls (email type)
* Store classification results
* Compute importance score
* Bucket emails

### Hard rules

* ❌ No auto-reply
* ❌ No chat UI
* ❌ No “magic ranking”

📌 **Gate**:

* System gives **stable rankings** across restarts
* Same input → same output (deterministic enough)

---

## 💬 PHASE 4 (Week 4) — AGENT CHAT (CONTROL, NOT FRIEND)

### Goal

Chat = **command + training**, not conversation.

### Deliverables

* Chat UI
* Conversation memory
* “Why?” explanations

### YOU do

* Define allowed intents:

  * explain
  * filter
  * teach
  * command
* Reject everything else

### ANTIGRAVITY does

* Chat endpoint
* Conversation history storage
* RAG over:

  * email docs
  * memory
* Explanation engine

### Hard rules

* ❌ No chit-chat
* ❌ No personality tuning
* ❌ Every answer must cite internal reasons

📌 **Gate**:

* You can say “Why urgent?”
* Agent answers with **data-backed reasoning**

---

## ✉️ PHASE 5 (Week 5) — COMPOSE, SEND, AUTO-REPLY (CONTROLLED)

### Goal

AI helps, **human approves**.

### Deliverables

* Compose UI
* Draft suggestions
* Safe auto-reply system

### YOU do

* Define safety rules:

  * No promises
  * No emotions
  * No decisions

### ANTIGRAVITY does

* Draft generation
* Tone control
* Gmail send API
* Auto-reply suggestions

### Hard rules

* ❌ No silent sends
* ❌ No background replies
* ❌ Every send logged

📌 **Gate**:

* Every email sent is explainable and reversible

---

## 📅 PHASE 6 (Week 6) — CALENDAR & TASK INTELLIGENCE

### Goal

Turn emails into **time awareness**.

### Deliverables

* Google Calendar sync
* Deadline detection
* Task suggestions

### YOU do

* Define what counts as:

  * meeting
  * deadline
  * task

### ANTIGRAVITY does

* Calendar API integration
* Event creation (after confirmation)
* Email → task detection

📌 **Gate**:

* Agent suggests calendar events but **never creates silently**

---

## 🧾 PHASE 7 (Week 7) — SUMMARIES, DIGESTS, ATTACHMENTS

### Goal

Reduce cognitive load.

### Deliverables

* Daily digest
* Thread summaries
* PDF/DOC summarization

### YOU do

* Define digest tone (no fluff)
* Decide summary length caps

### ANTIGRAVITY does

* Scheduled digest jobs
* Attachment text extraction
* Summary generation

📌 **Gate**:

* Digest takes <30 seconds to read
* Attachments searchable via chat

---

## 🔄 PHASE 8 (Week 8) — REALTIME + POLISH + HARDENING

### Goal

Make it feel **alive and reliable**.

### Deliverables

* WebSocket updates
* Cross-device sync
* UX polish
* Metrics dashboard (internal)

### YOU do

* Decide what triggers realtime
* Define “too many notifications”

### ANTIGRAVITY does

* WebSocket layer
* Optimistic UI
* Sync deltas
* Failure recovery

📌 **Final Gate**:

* Open inbox on phone + laptop → same state
* Agent improves after 1 week of use

---

# 🧠 COMMANDMENTS FOR ANTIGRAVITY (PRINT THIS)

1. **Memory before intelligence**
2. **Determinism before automation**
3. **Explainability over cleverness**
4. **User approval over autonomy**
5. **If it’s not logged, it didn’t happen**

---

## 🎯 FINAL WORD (IMPORTANT)

This is not just an app.
This is:

* Agent systems
* Human-in-the-loop AI
* Real-world API orchestration
* UX psychology

If executed even **70% correctly**, this beats most “AI email startups”.
