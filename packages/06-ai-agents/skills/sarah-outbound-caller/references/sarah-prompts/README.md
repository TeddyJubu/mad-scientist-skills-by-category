# Sarah - 4 Isolated System Prompts

These are **strict, isolated system prompts** for Sarah's four business verticals. Each prompt enforces **zero cross-contamination** between businesses.

---

## Files

1. **SARAH-ACQUISITION-PROMPT.md** → Chucky Buys Lucky Houses (REI property acquisition)
2. **SARAH-RDM-PROMPT.md** → Real Deal Meetup (event reminders and RSVPs)
3. **SARAH-SKOOL-PROMPT.md** → REI AI Skool Community (community engagement)
4. **SARAH-MMS-PROMPT.md** → Mad Marketing Success (AI/GHL agency services)

---

## Implementation Steps

### 1. Create 4 VAPI Assistant IDs

Go to **https://vapi.ai/dashboard** and create 4 separate assistants:

1. **Sarah - Acquisition** (Chucky Buys Lucky Houses)
2. **Sarah - RDM** (Real Deal Meetup)
3. **Sarah - Skool** (REI AI Skool)
4. **Sarah - MMS** (Mad Marketing Success)

For each assistant:
- Copy the corresponding prompt file (e.g., `SARAH-ACQUISITION-PROMPT.md`)
- Paste into the **System Prompt** field
- Save and note the **Assistant ID**

### 2. Update `/api/call.js`

Replace the assistant ID routing logic:

```javascript
const ASSISTANT_IDS = {
    'acquisition': '2e7609a1-dcfd-430e-9111-1426cb3cb38e',  // Current (or new ID)
    'rdm': '[NEW_RDM_ASSISTANT_ID]',
    'skool': '[NEW_SKOOL_ASSISTANT_ID]',
    'mms': '[NEW_MMS_ASSISTANT_ID]'
};

// Determine call type
let callType = 'acquisition';  // default
if (message) {
    if (type === 'rdm') callType = 'rdm';
    else if (type === 'mms') callType = 'mms';
    else callType = 'skool';  // default when message exists but no type
}

const targetAssistantId = ASSISTANT_IDS[callType];
```

### 3. Test Each Call Type

After deployment, test each vertical independently:

| Test | Input | Expected Opening |
|------|-------|------------------|
| **Acquisition** | Name: John, Phone: +1..., Address: 1234 Main St | "...calling from Chucky Buys Lucky Houses. I'm calling about your property at..." |
| **RDM** | Name: Jane, Phone: +1..., Message: "Event on March 30th", Type: rdm | "...at the Real Deal Meetup. Charles asked me to give you a quick update: Event on March 30th..." |
| **Skool** | Name: Bob, Phone: +1..., Message: "New AI tutorial posted", Type: skool | "...at the REI AI Skool Community. Charles wanted me to reach out and remind you: New AI tutorial posted..." |
| **MMS** | Name: Sue, Phone: +1..., Message: "Custom GHL setup offer", Type: mms | "...at Mad Marketing Success. I'm calling because Charles has a custom message for you: Custom GHL setup offer..." |

### 4. Verify Script Isolation

During testing, **intentionally ask Sarah off-topic questions**:

- On an **Acquisition** call, ask: "Do you guys do any events?"  
  → She should say: "I'm specifically calling about your property. If you're interested in other services, I can have Charles reach out separately."

- On an **RDM** call, ask: "Do you buy houses?"  
  → She should say: "I'm specifically calling about the Real Deal Meetup event. If you're interested in other things, I can have Charles reach out separately."

- On a **Skool** call, ask: "Can you help with my marketing?"  
  → She should say: "I'm specifically calling about the REI AI Skool Community. If you're interested in other things, I can have Charles reach out separately."

- On an **MMS** call, ask: "Do you have any meetups?"  
  → She should say: "I'm specifically calling about our AI and marketing automation services. If you're interested in other things, I can have Charles reach out separately."

If she starts cross-promoting or mixing scripts, **the prompt needs immediate patching**.

---

## Why This Approach?

**Problem:** One assistant ID for all four verticals means the system prompt must be generic enough to handle all cases, which creates risk of script leakage.

**Solution:** Four isolated assistant IDs with **hyper-specific prompts** that explicitly forbid mentioning other businesses.

**Result:** Strict boundaries, zero cross-contamination, and clean, professional conversations per vertical.

---

## Maintenance

- If you add new objections or questions, **update the relevant prompt file only**
- If you change messaging for one vertical, **do NOT touch the others**
- Test in isolation after any changes

---

**Last Updated:** 2026-03-22  
**Status:** Ready for VAPI setup  
**Action Required:** Create 4 assistant IDs and update `/api/call.js` with new IDs
