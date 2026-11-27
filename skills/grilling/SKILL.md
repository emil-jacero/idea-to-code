---
name: grilling
description: Grill the owner, one lettered question per message. Use when the user wants to stress-test a plan, a decision or an idea, or uses any 'grill' trigger phrase, and whenever any command or skill puts a question to the owner.
---

# Grilling

One home for how you ask the owner. A grill stress-tests a plan, a decision or an idea until you and the owner share one picture of it. The background rule and the question template hold for every question a command or skill puts to the owner, whether it comes from a grill or not. One exception: a quiz or exercise question in a lesson of a teaching skill tests the learner, so it keeps that skill's own form, with no recommendation. A request for an input that is missing, such as the idea or what to build, is not a decision: ask it in one plain sentence.

## The tree

Map the decision as a **design tree**: every answer opens the decisions that hang off it. The **frontier** is every node whose prerequisites are settled, so you can ask it without guessing an answer you have not heard.

- Ask first the frontier node that opens the most other nodes.
- Ask one decision per question. Two decisions joined by "and" are two nodes.
- A node that waits on running work is off the frontier. Ask another node; hold nothing for one report.
- After each answer, recompute the frontier: an answer settles a node, opens others or drops a branch.

## Facts are yours, decisions are the owner's

Look up every fact yourself in the repo, the tools or the docs; for a wide search, use the `idea-to-code:research` skill, which can run as a background agent. When only running code can settle a fact, it is an open assumption: name it and settle it with the `idea-to-code:prototype` skill. Research and prototypes run as their own step, never inside a read-only step such as OpenSpec explore. A prototype pauses that step, which resumes with the finding; while a research run reads in the background, grill the other frontier nodes. Never ask the owner for a fact you can look up, and never record an open assumption as settled. A decision is the owner's: scope, a public contract, a breaking change, a security trade-off, a new dependency. Put each to the owner with a recommendation and wait.

The text of a question holds facts too. An option, a background or a reason that names what the code, a tool or a service does (a state that it reports, a field that it writes, an output that it gives) rests on that fact: look it up before you show the question. Done when each such fact has a source that you read in this session. A fact with no source is an open assumption, and the question names it as one.

## The background rule

The owner has not seen your plan, reports or records. The background of every question to the owner reads in plain English for that reader.

- Describe a decision, a review, a task or a change in words: "the review of the empty-file-name change found a gap". Never name it by an id.
- Name a file, a field or a command only when the owner will touch it.
- Angle the background so the stake is clear: what exists today and why this choice matters.

## The question

Write the question as a message in the chat, in the form below. A question dialog of the harness (in Claude Code, the `AskUserQuestion` tool) shows a short label for each option and no background, so it cannot hold this form: put no question to the owner through it.

One question per message, never a batch. Two to four options, lettered. Each option has three bullets: what it means with a concrete example, a `Pro:` and a `Con:`. The owner answers by letter, or in words.

An offer to write files (a "capture" offer) and a pick among review findings are grill questions too, with lettered options. Offer review findings as classes of fixes, each described in words, never by an id.

```text
### <short name of the decision>, Q<k> of about <m>: <the question, as a question>

**Background:** <what exists today and why this choice matters, in plain English>

**Options:**

**A. <short name> (recommended)**
- <what it means, with a concrete example: a value, a command, a snippet>
- Pro: <...>
- Con: <...>

**B. <short name>**
- <what it means, with a concrete example>
- Pro: <...>
- Con: <...>

**C. ...**   (and D when there is one)

**Recommendation: A.** <the reason in one or two sentences, with its source>

Next: answer A, B or C.
```

The source of a recommendation is a file, a report, or a skill and subject. With no evidence, write "my judgement, not researched".

Example:

```text
### Retry count, Q1 of about 3: Where does the retry count of the upload job live?

**Background:** The upload job retries a failed call. Today the count is fixed at
3 in the code. Two places can hold it, and a change of the count is expected.

**Options:**

**A. A config key (recommended)**
- The service config holds the count: `upload.retries: 3`.
- Pro: an operator changes it with no release.
- Con: one more key to document and to test.

**B. A constant in the code**
- The code holds the count: `const maxRetries = 3`.
- Pro: simplest.
- Con: every change needs a release.

**Recommendation: A.** The count is expected to change, and a config key avoids a
release for each change. My judgement, not researched.

Next: answer A or B.
```

## Record

Keep a running list of decisions: the question, the answer, the reason. Mark each as the owner's answer or your assumption. When the calling command or skill names a file for decisions, write each decision there as it settles. Otherwise keep the running list in the chat.

When the calling command or skill names a ledger, read [LEDGER.md](LEDGER.md) and follow it. A ledger is a YAML file of every question and every choice. Each question is written there before it is asked, with a prediction, and the running list is written from it.

- "You decide" is an answer: decide, record it as delegated, and go on.
- An answer that contradicts an earlier one: say so, ask which stands, and record the one that replaces the other.
- A requirement that the owner states outright is the owner's answer: record it, and put the decisions that it opens on the frontier.
- Only an answer that offers a new option in place of a choice becomes an option: add it, and ask the question again.

When a grill settles a new domain term, or a decision that may need an ADR, call the Skill tool with `idea-to-code:domain-modeling`: it puts the capture question and writes the file at once.

## Stop

Stop when the frontier is empty: no open decision remains that the work needs. Do not pad: a question whose answer would not change the outcome is not asked. After two exchanges in which no node settled, stop asking and say what blocks: a missing fact (find it), an option nobody likes (find new ones) or a decision not ready (offer "decide later").

## No owner in the conversation

When nobody can answer (a sub-agent, an unattended run), never ask the owner yourself. A decision of the five kinds above stops your work: hand it back with the question drafted in this form, so the session that talks to the owner asks it and a fresh agent continues with the answer. Decide every other open choice yourself and list it as an assumption in your report, with the question it answered. Never invent an owner answer.
