Good. Now we **lock the MVP properly**—not bloated, not half-baked, but *shippable and intelligent*.

I’ll do this in **founder mode**, not tutorial mode.

---

# ✅ EMAIL AI AGENT — LOCKED MVP PLAN

This MVP answers **one question**:

> “Can an AI reliably manage my email workload *better than I do*, and improve over time?”

Everything below exists to serve that.

---

## 1️⃣ MVP SCOPE (Hard Boundaries)

### INCLUDED

✔ Multi-Gmail support
✔ Priority inbox (AI-driven)
✔ Agent memory (learning behavior)
✔ Auto-reply (controlled)
✔ Email sending
✔ Calendar / task sync
✔ Daily summaries
✔ Voice (basic)
✔ Attachment processing (text-first)
✔ Cross-device sync

### EXCLUDED (for now)

❌ Autonomous replies without approval
❌ Heavy automation rules UI
❌ Complex analytics dashboards
❌ Enterprise features

---

## 2️⃣ CORE MVP MODULES (Locked)

---

## MODULE A — EMAIL INGESTION & SYNC

### Responsibilities

* Connect multiple Gmail accounts
* Fetch emails + metadata
* Maintain sync state

### Design decisions

* **Event-based sync first**
* Polling fallback (smart frequency)
* Thread-aware ingestion

### Stored per email:

* Cleaned text (HTML → text)
* Sender profile reference
* Thread context pointer
* Attachment references
* Embedding (for retrieval)

📌 **Rule:** Inbox is *derived*, never stored manually.

---

## MODULE B — PRIORITY & IMPORTANCE ENGINE (CRITICAL)

### Importance Score = f(behavior, sender, content, time)

Signals:

* Sender history
* Keywords + intent
* Thread state
* Past user actions
* Calendar proximity

Output:

```
importance_score: 0 → 100
urgency_flag: true/false
confidence: %
```

### Priority Buckets (UI-facing)

* 🔴 Needs action
* 🟡 Important but can wait
* 🟢 FYI / Safe to ignore

---

## MODULE C — AGENT MEMORY (NON-NEGOTIABLE)

### Memory Layers (MVP)

#### 1. Preference Memory (Structured)

Examples:

* “Emails from X are important”
* “Never auto-reply to Y”
* “Deadlines > promotions”

#### 2. Interaction Memory

* Opened
* Ignored
* Replied
* Corrected agent

#### 3. Conversation Memory

* Chat corrections
* Explanations requested

📌 Memory **changes behavior**, not just answers.

---

## MODULE D — AUTO-REPLY SYSTEM (CONTROLLED)

This is where people screw up. You won’t.

### MVP Rules

* Auto-reply = **suggestion first**
* User approves OR enables auto-mode per sender/type

### Auto-reply types

* Acknowledgment (“Received, will respond soon”)
* Delay responses
* Template-based replies
* Calendar-aware replies (“I’m busy until X”)

### Safety

* No emotional replies
* No decisions
* No promises

---

## MODULE E — EMAIL COMPOSING & SENDING

### Features

* AI-assisted drafting
* Tone control (formal / casual)
* Context-aware replies (thread understanding)

### Agent can:

* Draft
* Edit
* Improve clarity
* Shorten / expand

But:

> **User always owns send action (MVP rule).**

---

## MODULE F — CALENDAR & TASK SYNC

### What gets synced

* Google Calendar
* Email-derived tasks

### Agent abilities

* Detect meetings / deadlines
* Suggest adding to calendar
* Detect task-like emails
* Ask confirmation

### Example:

> “This email implies a deadline on Friday. Add to tasks?”

This is **high leverage**.

---

## MODULE G — SUMMARIES & DIGESTS

### MVP Digests

* Daily morning summary
* Evening wrap-up (optional)

### Content

* Urgent items
* Upcoming deadlines
* Emails ignored (with justification)
* Suggested follow-ups

Tone:

* Calm
* Short
* Action-oriented

No “AI fluff”.

---

## MODULE H — VOICE (MVP-LITE)

### Scope

* Voice input for:

  * “What’s urgent?”
  * “Summarize my inbox”
  * “Reply to this”

### Output

* Optional TTS summaries

📌 Voice is **control**, not primary UI (yet).

---

## MODULE I — ATTACHMENT PROCESSING

### MVP Support

✔ PDF
✔ DOCX
✔ PPT (text only)

Agent can:

* Extract text
* Summarize
* Answer questions

Later:
❌ Images
❌ Tables-heavy analysis

---

## MODULE J — CROSS-DEVICE SYNC OPTIMIZATION

### Principles

* Server = source of truth
* Client = cached views
* Sync only deltas

### UX tricks

* Optimistic UI
* Background refresh
* Minimal battery usage

📌 User should **never feel sync delays**.

---

## 3️⃣ MVP UI (LOCKED)

### Screens

1. **Priority Inbox**
2. **Email Detail View**
3. **Agent Chat**
4. **Compose**
5. **Settings (minimal)**

### Chat Box Purpose

* Ask “why”
* Correct agent
* Teach preferences
* Issue commands

This is **training**, not chatting.

---

## 4️⃣ MVP EXPERIENCE IMPROVEMENTS (SUBTLE BUT POWERFUL)

### Explainability by default

Every decision can be questioned.

### Confidence display

Agent says:

* “I’m confident”
* “I’m unsure”

This builds trust.

### Silence is allowed

No constant notifications.
Only signal > noise.

---

## 5️⃣ MVP SUCCESS CRITERIA (REAL METRICS)

You win if:

* Inbox time reduces by **50%**
* Agent corrections decrease over time
* User stops opening “All Mail”
* User trusts summaries

---

## 6️⃣ WHAT THIS MVP IS *NOT*

* Not an email client replacement
* Not a chatbot glued to Gmail
* Not a rule-based filter

It is a **learning system**.

---

## NEXT STEP (LOCKED PATH)

Say **one word** and we move forward:

### Options:

* **ARCHITECTURE** → full system diagram
* **DATA** → schemas & memory models
* **TECH** → stack decisions (backend, LLMs, vector DB, UI)
* **PHASES** → week-by-week build plan

Don’t rush. Choose deliberately.
