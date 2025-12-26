# 🧠 EMAIL AI OS — PROJECT TASK LIST

Based on `CONTEXT/PLAN.md`.

## 🧱 PHASE 0 (Week 0) — FOUNDATIONS & RULES (NON-NEGOTIABLE)
- [ ] **Deliverables**
    - [ ] `PRODUCT.md` → MVP scope (frozen)
    - [ ] `ARCHITECTURE.md` → system diagram + data flow
    - [ ] `RULES.md` → agent rules (VERY IMPORTANT)
    - [ ] Repo initialized
- [ ] **YOU (User) do**
    - [ ] Write `RULES.md`
    - [ ] Define **Definition of Done** for each phase
- [ ] **ANTIGRAVITY does**
    - [ ] Repo setup
    - [ ] Folder structure (empty, no logic yet)

---

## 📩 PHASE 1 (Week 1) — GMAIL INGESTION (READ-ONLY, CLEAN)
- [x] **Phase 0 Recovery (Foundations)**
    - [x] Request missing .env keys (Google ID, Secret, DB URL) <!-- id: 4 -->
    - [x] Scaffold `Backend` (FastAPI, Python requirements) <!-- id: 5 -->
    - [x] Scaffold `Frontend` (Next.js, Tailwind, Shadcn) <!-- id: 6 -->
- [x] **Deliverables**
    - [x] Gmail OAuth flow
    - [x] Multi-account support
    - [x] Raw email ingestion
    - [x] Clean text extraction
- [x] **YOU (User) do**
    - [x] Define **email document contract** (immutable)
    - [x] Review Gmail scopes (read-only first)
- [x] **ANTIGRAVITY does**
    - [x] Gmail API integration
    - [x] Fetch: message_id, thread_id, headers, raw body
    - [x] HTML → clean text
    - [x] Store metadata in Postgres

---

## 🧠 PHASE 2 (Week 2) — MEMORY & DATA MODELS (THE HEART)
- [x] **Deliverables**
    - [x] Email schema (final)
    - [x] Preference memory
    - [x] Interaction logging
    - [x] Vector embeddings pipeline (offline)
- [ ] **YOU (User) do**
    - [ ] Design memory tables: preferences, sender_profiles, interaction_events
    - [ ] Decide what is structured vs vectorized
- [x] **ANTIGRAVITY does**
    - [x] pgvector setup
    - [x] Email embedding generation
    - [x] Store embeddings per email + per thread
    - [x] Interaction event logger (open, ignore, reply, manual priority change)

---

## 🧮 PHASE 3 (Week 3) — PRIORITY ENGINE (NO CHAT, NO UI MAGIC)
- [x] **Deliverables**
    - [x] Importance scoring function
    - [x] Confidence score
    - [x] Bucketing logic
- [x] **YOU (User) do**
    - [x] Define importance formula (initial weights)
    - [x] Decide decay curves
- [x] **ANTIGRAVITY does**
    - [x] Classifier LLM calls (email type)
    - [x] Store classification results
    - [x] Compute importance score
    - [x] Bucket emails

---

## 💬 PHASE 4 (Week 4) — AGENT CHAT (CONTROL, NOT FRIEND)
- [x] **Deliverables**
    - [x] Chat UI
    - [x] Conversation memory
    - [x] “Why?” explanations
- [ ] **YOU (User) do**
    - [ ] Define allowed intents (explain, filter, teach, command)
    - [ ] Reject everything else
- [ ] **ANTIGRAVITY does**
    - [ ] Chat endpoint
    - [ ] Conversation history storage
    - [ ] RAG over: email docs, memory
    - [ ] Explanation engine

---

## ✉️ PHASE 5 (Week 5) — COMPOSE, SEND, AUTO-REPLY (CONTROLLED)
- [x] **Rebrand & Overhaul (Prep)**
    - [x] Rename "Sasthri Garu" -> "Kyra"
    - [x] UI Overhaul (Dark/Zinc, Shadcn)
    - [x] Scopes Update (Send/Compose)
- [ ] **Deliverables**
    - [x] Compose UI (Drawer/Dialog)
    - [x] Draft suggestions (Kyra + Tone)
    - [x] Human-in-the-loop Send API
- [ ] **YOU (User) do**
    - [ ] Define safety rules (No promises, No emotions, No decisions)
    - [ ] Approve Scopes (Send/Compose)
- [ ] **ANTIGRAVITY does**
    - [x] DraftService (Context + Tone)
    - [x] Tone control (Professional, Casual, Short)
    - [x] POST /api/v1/gmail/send
    - [ ] Auto-reply suggestions

---

## 📅 PHASE 6 (Week 6) — CALENDAR & TASK INTELLIGENCE
- [x] **Data & Scopes**
    - [x] DB: `tasks` table
    - [x] OAuth: `calendar.events` scope
    - [x] Backend: `Task` model
- [x] **Calendar Core**
    - [x] `CalendarService` (fetch/create events)
    - [x] Conflict checker
- [x] **Intelligence**
    - [x] `TaskDetector` (LLM extraction)
    - [x] Ingestion Hook (Auto-create tasks)
    - [x] Chat Context (Schedule awareness)
- [x] **UI**
    - [x] Calendar/Task Widget
    - [x] Dashboard Integration

---

## 🧾 PHASE 7 (Week 7) — SUMMARIES, DIGESTS, ATTACHMENTS
- [ ] **Deliverables**
    - [x] Daily digest
    - [x] Thread summaries
    - [x] PDF/DOC summarization
- [ ] **YOU (User) do**
    - [ ] Define digest tone (no fluff)
    - [ ] Decide summary length caps
- [x] **ANTIGRAVITY does**
    - [x] Scheduled digest jobs
    - [x] Attachment text extraction
    - [x] Summary generation

---

## 🔄 PHASE 8 (Week 8) — REALTIME + POLISH + HARDENING
- [ ] **Deliverables**
    - [ ] WebSocket updates
    - [ ] Cross-device sync
    - [ ] UX polish
    - [ ] Metrics dashboard (internal)
- [ ] **YOU (User) do**
    - [ ] Decide what triggers realtime
    - [ ] Define “too many notifications”
- [ ] **ANTIGRAVITY does**
    - [ ] WebSocket layer
    - [ ] Optimistic UI
    - [ ] Sync deltas
    - [ ] Failure recovery
