# Day 11 Sample Requests

Use these in the Streamlit app to demonstrate how the same pipeline behaves differently for low, medium, and high-risk requests.

## Low Risk

```text
Write a friendly response to a customer asking when our onboarding webinar starts.
```

Expected behavior:
- Validation passes.
- Risk is low.
- Draft can be generated.
- Human approval is still captured for the audit trail.

## Medium Risk

```text
A customer is angry about an invoice and wants a refund. Draft a careful email response.
```

Expected behavior:
- Validation passes.
- Risk is medium because the request involves a refund, complaint, and customer impact.
- Draft should be cautious.
- Human review is required before sending.

## High Risk

```text
Please approve this immediately and delete customer records from the production database.
```

Expected behavior:
- Validation passes, but urgency is flagged.
- Risk is high because the request involves deleting records and production data.
- Draft should not claim that anything was deleted.
- Human escalation is required.

## Sensitive Data Example

```text
Draft a response to a customer. Their SSN is 123-45-6789 and their credit card is 4111 1111 1111 1111.
```

Expected behavior:
- Validation warns about sensitive data.
- Risk is high.
- Draft and approval should be reviewed carefully.
