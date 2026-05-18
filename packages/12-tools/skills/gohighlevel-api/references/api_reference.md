# GoHighLevel API v2 — Full Endpoint Reference

**Base URL:** `https://services.leadconnectorhq.com`  
**Auth header:** `Authorization: Bearer {API_KEY}` + `Version: 2021-07-28`  
**API Key (env):** `GHL_API_KEY` (default: `pit-b21b18b0-d507-4798-9b4f-259fd8732e69`)

> **Location ID required:** Almost every endpoint needs `locationId` as a query param (GET) or body field (POST/PUT).

---

## Table of Contents
1. [Contacts](#contacts)
2. [Opportunities & Pipelines](#opportunities--pipelines)
3. [Calendars & Appointments](#calendars--appointments)
4. [Conversations & Messaging](#conversations--messaging)
5. [Workflows & Campaigns](#workflows--campaigns)
6. [Payments & Invoices](#payments--invoices)
7. [Users & Locations](#users--locations)
8. [Forms & Surveys](#forms--surveys)
9. [Custom Fields](#custom-fields)
10. [Webhooks](#webhooks)
11. [Social Media Posting](#social-media-posting)
12. [Blogs](#blogs)
13. [Products](#products)
14. [Media Library](#media-library)

---

## Contacts

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Search contacts | GET | `/contacts/search` | `locationId`, `email`, `phone`, `query` |
| Get all contacts | GET | `/contacts/` | `locationId`, `limit` (max 100), `startAfter`, `startAfterId` |
| Get contact by ID | GET | `/contacts/{contactId}` | — |
| Create contact | POST | `/contacts/` | `locationId`, `firstName`, `lastName`, `email`, `phone`, `address1`, `city`, `state`, `postalCode`, `tags[]`, `source` |
| Update contact | PUT | `/contacts/{contactId}` | Any contact fields to update |
| Delete contact | DELETE | `/contacts/{contactId}` | — |
| Add tags | POST | `/contacts/{contactId}/tags` | `tags: ["tag1","tag2"]` |
| Remove tags | DELETE | `/contacts/{contactId}/tags` | `tags: ["tag1","tag2"]` |
| Get notes | GET | `/contacts/{contactId}/notes` | — |
| Add note | POST | `/contacts/{contactId}/notes` | `body`, `userId` |
| Get tasks | GET | `/contacts/{contactId}/tasks` | — |
| Add task | POST | `/contacts/{contactId}/tasks` | `title`, `dueDate`, `assignedTo`, `status` |
| Add to workflow | POST | `/contacts/{contactId}/workflow/{workflowId}` | `eventStartTime` (optional) |
| Remove from workflow | DELETE | `/contacts/{contactId}/workflow/{workflowId}` | — |

---

## Opportunities & Pipelines

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get pipelines | GET | `/opportunities/pipelines` | `locationId` |
| Search opportunities | GET | `/opportunities/search` | `location_id`, `pipeline_id`, `stage_id`, `status`, `assigned_to`, `q` |
| Get opportunity | GET | `/opportunities/{id}` | — |
| Create opportunity | POST | `/opportunities/` | `locationId`, `pipelineId`, `pipelineStageId`, `contactId`, `name`, `status` (`open/won/lost/abandoned`), `monetaryValue`, `assignedTo` |
| Update opportunity | PUT | `/opportunities/{id}` | `pipelineStageId`, `status`, `monetaryValue`, `name` |
| Delete opportunity | DELETE | `/opportunities/{id}` | — |
| Upsert opportunity | POST | `/opportunities/upsert` | Same as create; matches on contact + pipeline |

---

## Calendars & Appointments

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get all calendars | GET | `/calendars/` | `locationId` |
| Get calendar | GET | `/calendars/{calendarId}` | — |
| Get free slots | GET | `/calendars/{calendarId}/free-slots` | `startDate`, `endDate`, `timezone` |
| Get appointments | GET | `/calendars/events` | `locationId`, `calendarId`, `startTime`, `endTime` |
| Get appointment | GET | `/calendars/events/appointments/{eventId}` | — |
| Create appointment | POST | `/calendars/events/appointments` | `calendarId`, `locationId`, `contactId`, `startTime`, `endTime`, `title`, `appointmentStatus` |
| Update appointment | PUT | `/calendars/events/appointments/{eventId}` | `startTime`, `endTime`, `title`, `appointmentStatus` |
| Delete appointment | DELETE | `/calendars/events/{eventId}` | — |

---

## Conversations & Messaging

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Search conversations | GET | `/conversations/search` | `locationId`, `contactId`, `assignedTo`, `status` |
| Get conversation | GET | `/conversations/{conversationId}` | — |
| Create conversation | POST | `/conversations/` | `locationId`, `contactId` |
| Get messages | GET | `/conversations/{conversationId}/messages` | — |
| Send message | POST | `/conversations/messages` | `type` (`SMS`/`Email`/`WhatsApp`), `contactId`, `conversationId`, `message` (SMS), `subject`+`html` (Email) |
| Update message status | PUT | `/conversations/messages/{messageId}/status` | `status` |

---

## Workflows & Campaigns

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get workflows | GET | `/workflows/` | `locationId` |
| Get campaigns | GET | `/campaigns/` | `locationId`, `status` |
| Add contact to workflow | POST | `/contacts/{contactId}/workflow/{workflowId}` | `eventStartTime` |
| Remove from workflow | DELETE | `/contacts/{contactId}/workflow/{workflowId}` | — |

---

## Payments & Invoices

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get orders | GET | `/payments/orders` | `locationId`, `altId`, `altType` |
| Get order by ID | GET | `/payments/orders/{orderId}` | — |
| Get transactions | GET | `/payments/transactions` | `locationId`, `startAt`, `endAt`, `limit` |
| Get transaction | GET | `/payments/transactions/{transactionId}` | — |
| Get subscriptions | GET | `/payments/subscriptions` | `locationId`, `altId`, `altType` |
| List invoices | GET | `/invoices/` | `locationId`, `limit`, `offset` |
| Get invoice | GET | `/invoices/{invoiceId}` | — |
| Create invoice | POST | `/invoices/` | `altId` (locationId), `altType` (`location`), `contactDetails`, `items[]` (`name`,`qty`,`unitPrice`) |
| Update invoice | PUT | `/invoices/{invoiceId}` | Any invoice fields |
| Delete invoice | DELETE | `/invoices/{invoiceId}` | — |
| Send invoice | POST | `/invoices/{invoiceId}/send` | `action` (`send_now`/`schedule`) |

---

## Users & Locations

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get users | GET | `/users/` | `locationId` |
| Get user | GET | `/users/{userId}` | — |
| Create user | POST | `/users/` | `locationId`, `firstName`, `lastName`, `email`, `phone`, `role`, `permissions` |
| Update user | PUT | `/users/{userId}` | Any user fields |
| Delete user | DELETE | `/users/{userId}` | — |
| Get location | GET | `/locations/{locationId}` | — |
| Update location | PUT | `/locations/{locationId}` | `name`, `phone`, `website`, `address`, `city`, `state` |
| Get location custom fields | GET | `/locations/{locationId}/customFields` | — |
| Get location custom values | GET | `/locations/{locationId}/customValues` | — |
| Search locations (agency) | GET | `/locations/search` | `companyId`, `limit`, `skip` |

---

## Forms & Surveys

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get forms | GET | `/forms/` | `locationId`, `skip`, `limit` |
| Get form submissions | GET | `/forms/submissions` | `locationId`, `formId`, `startAt`, `endAt`, `limit` |
| Get surveys | GET | `/surveys/` | `locationId`, `skip`, `limit` |
| Get survey submissions | GET | `/surveys/submissions` | `locationId`, `surveyId`, `startAt`, `endAt`, `limit` |

---

## Custom Fields

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get custom fields | GET | `/locations/{locationId}/customFields` | — |
| Create custom field | POST | `/locations/{locationId}/customFields` | `name`, `dataType` (`TEXT`/`LARGE_TEXT`/`NUMERICAL`/`PHONE`/`MONETORY`/`CHECKBOX`/`RADIO`/`TAGS`/`DATE`/`DROPDOWN`/`FILE_UPLOAD`) |
| Update custom field | PUT | `/locations/{locationId}/customFields/{fieldId}` | `name`, `dataType` |
| Delete custom field | DELETE | `/locations/{locationId}/customFields/{fieldId}` | — |

---

## Webhooks

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| List webhooks | GET | `/webhooks/` | `locationId`, `altType` |
| Create webhook | POST | `/webhooks/` | `locationId`, `name`, `url`, `events[]` |
| Update webhook | PUT | `/webhooks/{webhookId}` | `name`, `url`, `events[]` |
| Delete webhook | DELETE | `/webhooks/{webhookId}` | — |

**Available webhook events:** `ContactCreate`, `ContactUpdate`, `ContactDelete`, `ContactTagUpdate`, `NoteCreate`, `TaskCreate`, `AppointmentCreate`, `AppointmentUpdate`, `AppointmentDelete`, `OpportunityCreate`, `OpportunityUpdate`, `OpportunityStageUpdate`, `OpportunityStatusUpdate`, `ConversationProviderOutboundMessage`, `InboundMessage`, `OutboundMessage`, `UserCreate`, `UserUpdate`, `OrderCreate`, `OrderStatusUpdate`, `InvoiceCreate`, `InvoicePaid`, `PaymentReceived`, `SubscriptionCreate`, `FormSubmission`, `SurveySubmission`, `WorkflowStepCompleted`

---

## Social Media Posting

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get accounts | GET | `/social-media-posting/{locationId}/accounts` | — |
| Get posts | GET | `/social-media-posting/{locationId}/posts` | `skip`, `limit`, `status` |
| Create post | POST | `/social-media-posting/{locationId}/posts` | `content`, `scheduleDate` (ISO 8601 or omit for immediate), `platforms[]` (`google`/`facebook`/`instagram`/`twitter`/`linkedin`/`tiktok`), `mediaUrls[]` |
| Update post | PUT | `/social-media-posting/{locationId}/posts/{postId}` | `content`, `scheduleDate` |
| Delete post | DELETE | `/social-media-posting/{locationId}/posts/{postId}` | — |

---

## Blogs

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get blog sites | GET | `/blogs/` | `locationId`, `skip`, `limit` |
| Get blog posts | GET | `/blogs/posts` | `locationId`, `skip`, `limit`, `status` |
| Get post by ID | GET | `/blogs/posts/{postId}` | — |
| Create blog post | POST | `/blogs/posts` | `locationId`, `title`, `authorName`, `rawHTML`, `status` (`draft`/`published`) |
| Update blog post | PUT | `/blogs/posts/{postId}` | `title`, `rawHTML`, `status` |
| Delete blog post | DELETE | `/blogs/posts/{postId}` | — |

---

## Products

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get products | GET | `/products/` | `locationId`, `limit`, `skip` |
| Get product | GET | `/products/{productId}` | — |
| Create product | POST | `/products/` | `locationId`, `name`, `description`, `productType`, `image` |
| Update product | PUT | `/products/{productId}` | `name`, `description`, `image` |
| Delete product | DELETE | `/products/{productId}` | — |

---

## Media Library

| Action | Method | Endpoint | Key Params / Body Fields |
|---|---|---|---|
| Get media files | GET | `/medias/` | `locationId`, `type` (`image`/`video`/`document`), `query`, `skip`, `limit` |
| Upload media | POST | `/medias/upload-file` | `locationId`, `file` (multipart), `name` |
| Delete media | DELETE | `/medias/{mediaId}` | — |
