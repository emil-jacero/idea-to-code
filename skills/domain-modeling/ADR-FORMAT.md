# ADR Format

ADRs live in the repo's ADR folder, the `ADR folder:` of the repo's `## Decision records` (the `idea-to-code:domain-modeling` skill says where the section sits; default: `adr/` where it exists). They use three-digit sequential numbering: `001-slug.md`, `002-slug.md`, and so on. An added rule of that section on the numbering or on the template replaces the default of this file.

## Template

Use `TEMPLATE.md` in the ADR folder. Where the folder has no template, follow the form of its newest ADR. Where the folder has neither, write a title line (`# <short title of the decision>`) and then one to three sentences: the context, the decision and why. Keep each section short: the value is in recording *that* a decision was made and *why*.

## Numbering

Scan the ADR folder for the highest existing number and add one, in three digits.

## When to put an ADR to the owner

The three tests are in [SKILL.md](./SKILL.md), Put ADRs to the owner sparingly. The kinds below usually pass them.

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced, the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library: just the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only." The explicit no-s are as valuable as the yes-s.
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X." Anything where a reasonable reader would assume the opposite. These stop the next engineer from "fixing" something that was deliberate.
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements." "Response times must be under 200ms because of the partner API contract."
- **Rejected alternatives when the rejection is non-obvious.** If you considered GraphQL and picked REST for subtle reasons, record it; otherwise someone will suggest GraphQL again in six months.
