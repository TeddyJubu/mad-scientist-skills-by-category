# GoHighLevel API — Master Prompt Examples

This file contains ready-to-use prompt patterns for every major GHL API action. Use these as templates when the user's request maps to a known operation.

---

## Contacts

**Create:** "Create a new contact in location [locId] with firstName=[X], lastName=[Y], email=[Z], phone=[P], tags=[t1,t2]."  
**Search by email:** "Find the contact with email [email] in location [locId]."  
**Search by phone:** "Find the contact with phone [phone] in location [locId]."  
**Get all:** "Get all contacts in location [locId]."  
**Update:** "Update contact [contactId] in location [locId]: set city=[X], add tag=[Y]."  
**Add tags:** "Add tags [tag1, tag2] to contact [contactId] in location [locId]."  
**Remove tags:** "Remove tags [tag1] from contact [contactId] in location [locId]."  
**Add note:** "Add a note to contact [contactId]: '[note text]'."  
**Add task:** "Create a task '[title]' for contact [contactId] due [date]."  
**Delete:** "Delete contact [contactId] from location [locId]."

---

## Opportunities

**Get pipelines:** "List all pipelines in location [locId]."  
**Create:** "Create an opportunity named '[name]' in pipeline [pipelineId] stage [stageId] for contact [contactId], value $[amount]."  
**Update stage:** "Move opportunity [oppId] to stage [stageId]."  
**Mark won/lost:** "Mark opportunity [oppId] as won/lost."  
**Search:** "Find all open opportunities in pipeline [pipelineId] in location [locId]."

---

## Calendars & Appointments

**Get calendars:** "List all calendars in location [locId]."  
**Available slots:** "Show available slots for calendar [calId] from [startDate] to [endDate] in timezone [tz]."  
**Book:** "Book an appointment on calendar [calId] for contact [contactId] from [startTime] to [endTime]."  
**Update:** "Reschedule appointment [eventId] to [newStart] – [newEnd]."  
**Cancel:** "Cancel appointment [eventId]."

---

## Messaging

**Send SMS:** "Send SMS to contact [contactId] in location [locId]: '[message]'."  
**Send email:** "Send email to contact [contactId] with subject '[subject]' and body '[html]'."  
**Get conversations:** "Get all conversations for contact [contactId] in location [locId]."  
**Get messages:** "Get all messages in conversation [conversationId]."

---

## Workflows & Campaigns

**List workflows:** "List all workflows in location [locId]."  
**Enroll:** "Add contact [contactId] to workflow [workflowId] in location [locId]."  
**Remove:** "Remove contact [contactId] from workflow [workflowId]."  
**List campaigns:** "List all active campaigns in location [locId]."

---

## Payments & Invoices

**Create invoice:** "Create an invoice for contact [contactId] in location [locId] with items: [item1 qty price], [item2 qty price]. Due [date]."  
**List invoices:** "List all invoices in location [locId]."  
**Send invoice:** "Send invoice [invoiceId] to the contact now."  
**Get transactions:** "Get all transactions in location [locId] between [startDate] and [endDate]."  
**Get orders:** "List all orders in location [locId]."

---

## Users & Location

**Get users:** "List all users in location [locId]."  
**Get location:** "Get the details for location [locId]."  
**Update location:** "Update location [locId]: set businessName=[X], phone=[Y], website=[Z]."

---

## Forms & Surveys

**Get forms:** "List all forms in location [locId]."  
**Get submissions:** "Get all submissions for form [formId] in location [locId]."  
**Get surveys:** "List all surveys in location [locId]."

---

## Webhooks

**Create:** "Create a webhook for location [locId] that POSTs to [url] on events: ContactCreate, AppointmentCreate."  
**List:** "List all webhooks in location [locId]."  
**Delete:** "Delete webhook [webhookId]."

---

## Social Media

**Create post:** "Post '[content]' to [platform] for location [locId], scheduled for [datetime]."  
**List posts:** "List all scheduled social media posts for location [locId]."

---

## Blogs

**List posts:** "List all blog posts for location [locId]."  
**Create post:** "Create a blog post titled '[title]' with content '[html]' in location [locId], status draft."
