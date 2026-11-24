---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing each settled term or decision down at once, as soon as the owner agrees. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## Project rules

Before you write a term or a decision record, read these sections of the repo's rules: `## Decision records`. A section is a heading of that exact name in the repo guide (`AGENTS.md`, else `CLAUDE.md`), or in the file that the guide names on its `Rules file:` line. A heading that differs only in letter case is the section: report it. Where a section is absent, the defaults of this skill hold. A point in a section replaces only the default of the same label, and the value `none` switches that default off. An absent label keeps its default. Every other line of a section is an added rule. It wins over a default of this skill that has no label. A default that has a label changes only through its point. The flow rules of this skill hold in every repo: a section adds to them and never removes one. When the rules file that the guide names is missing, one section is in both files, or a line of a section names a path that is not in the repo, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. For a path that is missing, the question offers three options: correct the line (fix or remove the path), create the file, or stop. The recommended option is to correct the line. It never offers to go on without the file. In your report, write one line that starts with `Project rules:` and names each section you read, or write `Project rules: defaults`.

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── adr/
│   ├── 001-event-sourced-orders.md
│   └── 002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── adr/                              ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── adr/                      ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── adr/
```

Create files lazily: only when you have something to write. Write every term into the repo's glossary (`GLOSSARY.md`, or the glossary file the repo guide names). When the repo has neither, create `GLOSSARY.md` when the owner agrees to write the first term.

## During the session

Put every question and every capture offer to the owner in the form of the `idea-to-code:grilling` skill: one lettered question per message. The quoted lines below show what to ask, not how to ask it.

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in the repo's glossary, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?"

### Write a settled term at once

When a term is resolved, put its write to the owner as a capture question. On the owner's yes, write it into the repo's glossary at once, before the change is built, so the test writer, the code writer and the reviewer all read it. When the `Term backing:` of `## Decision records` (default: no backing rule) requires a term to be backed by its spec or code, the term reaches the default branch in the same PR as its backing, and a term whose backing the change dropped is removed before that PR merges. Inside a read-only step such as OpenSpec explore, pause that step for the write and resume it after. Commit nothing there: the file stays uncommitted like the change folder. The build asks the owner whether its first commit carries the file into the change's own pull request. When explore ends with no change, report the uncommitted file, and commit it or open a pull request only when the owner asks. Don't batch these up. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md), or, in a glossary file the repo guide names, that file's own form and the guide's rules for it.

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Put ADRs to the owner sparingly

Only put an ADR-sized decision to the owner, as a capture question, when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR.

A decision that binds more than one repo is not an ADR. Follow the `Cross-repo decisions:` of `## Decision records` (default: the decision is not written into this repo: name it to the owner as an open next step). An ADR may record this repo's own rule that follows from it.

On the owner's yes, write the ADR at once, in the same way as a term, in the form of [ADR-FORMAT.md](./ADR-FORMAT.md), into the ADR folder: the `ADR folder:` of `## Decision records` (default: `adr/` where it exists). Never create the ADR folder, whether `adr/`, `docs/adr/` or the folder that point names. With the value `none`, or with no point and no `adr/` folder, the repo has no ADR folder. A folder of the same name inside a context's folder holds that context's ADRs.

In a repo with no ADR folder, write the same decision, on the owner's yes and at once, into the decision home: the place that the `Decision home:` of `## Decision records` names for decisions a future maintainer needs (default: no decision home), in that place's form. Never write it only into the change's design: that is archived with the change. With no ADR folder and no decision home, the capture question offers a new reference file of the repo, with one line that names it. On the owner's yes, write both at once. That line is the `Decision home:` point of `## Decision records`, so that the next decision finds the file. Write it in the file that holds that section. Where no such section exists, add the heading to the repo guide and write the line under it. Where the repo has no repo guide, the capture question also offers a new `AGENTS.md` that holds the heading and that line.
