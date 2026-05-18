# Sarah's Four Outbound Call Types

Sarah handles **four distinct business verticals**, each with its own messaging and context.

---

## 1. REI Acquisition (Chucky Buys Lucky Houses)
**Type:** `acquisition` (default, no `type` param needed)  
**Purpose:** Cold outreach to property owners for cash offers  
**Key Info Passed:**
- `name` — Lead name
- `phone` — Contact number
- `address` — Property address (formatted for speech)

**Opening Script:**
> "Hi, can I speak with [first_name]? This is Sarah, the personal AI assistant for Tammie and Charles calling from Chucky Buys Lucky Houses. I'm calling about your property at [spoken_address]."

**Conversation Goal:**
- Confirm property ownership
- Qualify motivation, timeline, condition
- Schedule follow-up with Charles/Tammie

---

## 2. Real Deal Meetup Outbound (RDM)
**Type:** `rdm`  
**Purpose:** Event reminders, updates, or invitations for monthly REI/AI meetup  
**Key Info Passed:**
- `name` — Member name
- `phone` — Contact number
- `message` — Custom meetup announcement or reminder

**Opening Script:**
> "Hi [first_name], this is Sarah, the personal AI assistant for Tammie and Charles at the Real Deal Meetup. Charles asked me to give you a quick update: [custom_message]. See you soon!"

**Conversation Goal:**
- Deliver meetup-related message
- Confirm attendance or answer questions
- Keep it brief and friendly

---

## 3. Skool Community (REI AI Skool)
**Type:** `skool`  
**Purpose:** Community engagement, reminders, or support outreach  
**Key Info Passed:**
- `name` — Member name
- `phone` — Contact number
- `message` — Custom community message or reminder

**Opening Script:**
> "Hi [first_name], this is Sarah, the personal AI assistant for Tammie and Charles at the REI AI Skool Community. Charles wanted me to reach out and remind you: [custom_message]. Thanks, and have a great day!"

**Conversation Goal:**
- Deliver community update or reminder
- Answer questions about Skool platform or resources
- Nurture engagement

---

## 4. AI Agency / Mad Marketing Success (MMS)
**Type:** `mms`  
**Purpose:** Lead outreach for AI consultancy and GHL reseller services  
**Key Info Passed:**
- `name` — Lead name
- `phone` — Contact number
- `message` — Custom agency pitch or value proposition

**Opening Script:**
> "Hi [first_name], this is Sarah, the personal AI assistant for Tammie and Charles at Mad Marketing Success. I'm calling because Charles has a custom message for you: [custom_message]. Let me know if you're interested!"

**Conversation Goal:**
- Deliver agency pitch
- Qualify interest in AI automation or GHL setup
- Schedule discovery call with Charles

---

## Call Type Routing (in code)

```javascript
const { name, phone, address, message, type } = req.body;

if (message) {
    if (type === 'rdm') {
        // Real Deal Meetup script
    } else if (type === 'mms') {
        // Mad Marketing Success script
    } else {
        // Default to Skool (when message exists but no type specified)
    }
} else {
    // REI Acquisition (default - uses address)
}
```

---

## Dashboard Mapping

| Business Vertical | Dashboard Section | Call Type Param |
|------------------|-------------------|-----------------|
| Chucky Buys Lucky Houses | REI Acquisitions | `(none)` or `acquisition` |
| Real Deal Meetup | RDM Outbound | `rdm` |
| REI AI Skool | Skool Community | `skool` |
| Mad Marketing Success | AI Agency Ops | `mms` |

---

## Key Differences

| Call Type | Address Used? | Custom Message? | Goal |
|-----------|---------------|-----------------|------|
| **Acquisition** | ✅ Yes (required) | ❌ No | Property offer |
| **RDM** | ❌ No | ✅ Yes (required) | Event reminder |
| **Skool** | ❌ No | ✅ Yes (required) | Community engagement |
| **MMS** | ❌ No | ✅ Yes (required) | Agency pitch |

---

## VAPI Assistant Strategy

**Current Setup:**
- One assistant ID for all four types: `2e7609a1-dcfd-430e-9111-1426cb3cb38e` (Sarah)
- First message is dynamically generated per call type
- System prompt is generic enough to handle all contexts

**Future Enhancement Option:**
- Create **4 separate assistant IDs** (one per business vertical)
- Each with a custom system prompt tuned for that specific conversation style
- Better qualification questions per vertical
- Specific objection handling per business

---

**Last Updated:** 2026-03-22  
**Status:** Active and tested ✅
