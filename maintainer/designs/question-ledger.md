# The question ledger and the improve step

**Status:** design, agreed with the owner on 2026-11-27. Nothing is built.

This file holds the design of two additions to the flow, so that a fresh session can build them.
Each decision is marked: **owner** (the owner's answer) or **agent** (the agent's own choice, open
to change).

## Why

- Explore's record of decisions lives only in the conversation. Propose must run in the same
  session, and a compaction can lose the options that were rejected and the reasons.
- A choice that the agent makes itself is written as an assumption: no options, no reason and no
  prediction. Nobody can count how often such a choice was wrong.
- When a rule is added to a repo guide or a decision record, nothing records what the rule was
  meant to change, or whether it did.

The design takes its method from one paper, *Self-Improvement Memory Enables Continual Recursive
Self-Improvement* (see Sources). The paper keeps a record for the agent that improves an agent
harness. Its findings, as far as they matter here:

- A record grouped by recurring problem, with each attempt's reason, its prediction and its
  measured outcome, beat the harness alone in all 10 matched settings.
- A record that holds only the names of the problems was unreliable: from 1.82 points worse than
  no record to 2.40 points better.
- A prediction counts only when it is written before the outcome is known.
- Accepted edits often missed their target. Only the written prediction showed it.
- Failed attempts and replaced attempts stay in the record.

**Limit:** the paper tested harness edits against scored benchmarks. It did not test a record of
design questions. This design takes the shape of the record and the predict-then-check rule, and
no number.

The three scopes come from the Software Factory playbook of Dex Horthy (secondary sources only,
see Sources): product, architecture and program design, in that order, before any code.

## The loop

1. **Capture, inside the flow.** Explore and propose write every question and every choice to one
   file per change, the *question ledger*.
2. **Improve, on the owner's command.** A command reads the ledgers since its last run, checks the
   open predictions with the owner, and proposes improvements.
3. **Outcome documents.** An accepted improvement is a rule in a document that the repo already
   has: a decision record, the glossary, the repo guide. Explore reads those documents, so a
   written rule stops the question.
4. **The improvement record.** One file per repo logs each improvement with its reason, its
   prediction and, later, its outcome. The next improve run checks those predictions first.

## Decisions

| # | Decision | By |
| --- | --- | --- |
| 1 | Explore writes a question ledger per change, as structured data (YAML). | owner |
| 2 | Each entry holds two predictions and an `observed` field. The outcomes are checked by hand in the first version: verify does not change. | owner |
| 3 | The ledger records the questions put to the owner and the choices the agent makes itself. | owner |
| 4 | Explore also asks program-design questions. Goal: the asked architecture and program-design questions fall over time, because earlier answers settle them. | owner |
| 5 | The raw answers stay in the ledger. A rule that comes out of them is written to a document: a decision record, the glossary, the repo guide. | owner |
| 6 | The improvement step never runs by itself. The owner starts it with a command, and a skill does the work. | owner |
| 7 | Build order: capture first. The improve step is built after 2 or 3 real changes have a ledger. | owner |
| 8 | Every step of the flow is captured in the end. The first version captures explore and propose. The improve step reads `gates.json` and the build report as they are. | owner |
| 9 | `prediction` is two fields: `predicted_answer` and `predicted_outcome`. | agent |
| 10 | The ledger is a tree: each entry has a status and names the entry that opened it. The chat question is rendered from the entry, so nothing is written twice. | agent |
| 11 | Explore reads only the outcome documents, never the raw answers of earlier changes. A question repeats until an improve run turns its answer into a rule. | agent |
| 12 | Questions go in scope order: product, architecture, program design. A test seam counts as program design. | agent |
| 13 | A program-design choice is asked only when it has two real options and no written rule settles it. Otherwise the agent decides, and the entry records the choice. | agent |
| 14 | An explore that ends with no change keeps its ledger only on the owner's word, as explore treats an uncommitted file today. | agent |
| 15 | Only explore and propose ask. The build keeps its rule: a sub-agent hands back an owner decision, makes every other choice itself, and lists it as an assumption. | agent |
| 16 | The build and the fix round add an entry in one case: an owner's answer there replaces what an entry settled. Every other answer of the build stays in the build report. | owner |

## First version: capture

### The ledger file

- **Home:** during explore, an uncommitted file inside the repo,
  `openspec/explore/<name>/questions.yaml`, so that it survives the end of a session. Explore's
  record names it. Propose moves it into the change folder,
  `openspec/changes/<change>/questions.yaml`. It is archived with the change.
- **The form** has one home, `skills/grilling/LEDGER.md`. The example below shows the idea; that
  file holds the exact fields, with `asked` and `replaces` added.
- **Write order:** the agent writes an entry with its options, its recommendation and both
  predictions before it shows the question. It fills the answer and its thoughts after the owner
  answers. Then it adds each question that the answer opens, with the status `open`.
- **Append only:** no entry is deleted. An answer that replaces an earlier one is a new entry with
  `replaces`, and the old entry gets the status `replaced`. A question that an answer makes
  pointless gets the status `dropped`.

```yaml
idea: Upload retries are configurable        # the idea, in its current wording
idea_history: []                             # earlier wordings, oldest first
entries:
  - id: q3
    phase: explore              # explore | propose
    scope: program-design       # product | architecture | program-design | flow
    kind: question              # question (put to the owner) | choice (the agent's own)
    status: settled             # open | settled | dropped | replaced
    opened_by: q1               # the entry whose answer opened this one, or null
    question: Where does the retry count live?
    options:
      a: A key in the service config, `upload.retries`
      b: A constant in the code
    recommended: a
    reason: The count is expected to change. My judgement, not researched.
    predicted_answer: a         # only for kind: question
    predicted_outcome: One slice, and no change to the public config schema   # or none
    answer:
      choice: b                 # a letter, or other
      text: null                # the owner's words, when the answer is not a plain letter
      by: owner                 # owner | delegated | agent | rule
      rule: null                # for by: rule, the file that holds the rule
      at: 2026-11-27T10:00:00Z
    thoughts: The owner wants no new config key before the service has users.
    leads_to: none              # adr | glossary | guide | idea | none
    observed: null              # held | missed | not-seen; the improve step fills it
```

- `scope: flow` is for a question about the work itself, such as the track question.
- `predicted_outcome` names something that verify or a later change can see. When no such thing
  exists, the value is `none`.
- `by: rule` marks a choice that a written rule settled without a question. These entries are the
  measure of decision 4: asked entries against entries settled by a rule, per scope and per change.
- `leads_to` records the document that the existing offers write at answer time (a decision record,
  a glossary term). The bar for a decision record stays where it is.

### What changes

- **`skills/grilling`:** its Record section already writes each decision to a file that the caller
  names. Extend it: when that file is a ledger, write the entry first and render the question from
  it. Record the change in the Local changes table of `skills/CREDITS.md`, because this skill has an
  upstream.
- **`skills/explore`:** the grill step names the ledger as the file for decisions, asks in scope
  order and asks program-design questions by decision 13. The record step is rendered from the
  ledger and names its path.
- **`skills/propose`:** when a ledger exists, it is the record of decisions. Propose appends its own
  questions (test seams, owner decisions) and its own choices with `phase: propose`, and moves the
  file into the change folder. Each assumption that propose writes into the change has an entry.
- **`WORKFLOW.md` and `workflow.html`:** the explore, grill and propose chapters, and the page.
- **`skills/CREDITS.md`:** credit the playbook as the source of the three scopes, as an idea and not
  as copied text.
- **`maintainer/check_tree.py`:** add a fixed phrase only when a new phrase recurs in several files.

The five kinds of owner decision stay as they are, and each is still always asked. Program-design
questions are a new class beside them. `gates.json`, the build report, the test lock and verify do
not change.

### Done when

One real change has run with the first version, and:

1. the change folder holds a ledger with an entry for every question of explore and propose, and
   for every assumption in the change's files;
2. each entry held its recommendation and its predictions before its answer was written;
3. the questions in the chat match their entries;
4. `openspec validate <change> --strict` passes, and the archive keeps the file;
5. both maintainer checks pass.

### Predictions for this change

These are written before the first trial, and checked after it and by the first improve runs.

- Explore asks about 5 to 10 more questions per change at first.
- Propose can read every decision from the ledger alone, with no line of the conversation.
- Per scope, the share of asked entries (asked, against asked plus settled by a rule) falls from
  change to change, once an improve run has written rules.

### Build state

Done, not committed (2026-11-27). The tree check passes.

- `skills/grilling/LEDGER.md` is new, and the Record section of `skills/grilling/SKILL.md` points
  at it.
- `skills/explore/SKILL.md`: the ledger, the scope order and the program-design rule in step 5, the
  record in steps 8 and 9.
- `skills/propose/SKILL.md`: reads the ledger, writes its questions and choices to it, and moves it
  into the change folder in step 6.

- `WORKFLOW.md`: the question form in chapter 1, Step 1 (what happens, comes out, the explore
  command, the grill, a new section The ledger, the example), Step 2 (goes in, what happens, the
  change folder). Propose still runs in the session of explore: the ledger holds the decisions,
  and the looked-up facts live in the conversation.
- `workflow.html`: a ledger item after the grill, and the scope order in the grill item. The page
  check passes.
- `skills/CREDITS.md`: the Local changes row of `grilling`, and an idea credit for the playbook and
  the paper.
- `examples/questions.yaml`, with its sentence in the `README.md` table.

The trial of Done when ran on one real change (2026-11-27), and the five points hold. Three
corrections came out of it: the facts of an entry are looked up before it is written, each text
value is quoted, and decision 16.

## Second version: improve

A command, for example `/idea-to-code:improve`, with a skill. It runs only when the owner starts it.

**Reads:** the ledgers since its last run, the `comments` of `gates.json`, the answer records of the
build report, the verify findings, and the improvement record.

**Does:**

1. Checks the open predictions of the improvement record, then fills `observed` on the open
   predictions of the ledgers, with the owner.
2. Groups the entries by recurring question. The agent judges itself whether two entries ask the
   same question: no similarity tool.
3. Proposes each improvement as one question to the owner, in the grill's form, with a prediction.
4. Writes what the owner accepts, and appends it to the improvement record.

**Looks for:**

- the same answer given twice or more: a rule;
- a rule whose outcomes missed: revise it or retire it;
- an agent's own choice that a gate comment or a verify finding reversed: ask that kind of
  question, or write a rule. A gate comment is an answer to a question that nobody asked;
- a kind of question where the owner always takes the recommendation or delegates: stop asking it;
- a finding about the flow itself: a note for the plugin, because a project cannot change the plugin.

**The improvement record** follows the paper's shape: one entry per recurring problem, and under it
every attempt.

```yaml
problems:
  - id: p1
    name: The home of a test fixture is asked in every change
    scope: program-design
    attempts:
      - date: 2026-12-10
        what: "Rule in the repo guide: a fixture sits beside its only user"
        files: [AGENTS.md]
        evidence: [<change>/q3, <change>/q7]
        predicted: The fixture question is not asked in the next 3 changes
        observed: null            # held | missed | not-seen
        accepted_by: owner
        where: {model: <model id>, plugin: <plugin commit>}
```

`where` names the model, because a rule that patches one model's habit can hurt on the next model.
After a model change, the improve step reviews those attempts first.

The same command, run in the plugin's own repo, keeps the plugin's improvement record: the
problems of the flow, the fixes to the skills, and what each fix was predicted to change.

## Open points

Before the first version, both settled on 2026-11-27 by a prototype on OpenSpec 2.1.1:

- `openspec validate <change> --strict` accepts a change folder that holds `questions.yaml`, and the
  archive keeps the file.
- A folder `openspec/explore/` breaks neither `openspec validate --all --strict` nor
  `openspec list`. So the ledger starts inside the repo, not in a scratch folder.

Left open by the first version:

- A ledger of an explore that ends with no change stays in the tree, uncommitted. The next build
  reports it as an unrelated change.
- The ledger and the program-design questions are on in every repo. No line switches them off.

Before the second version:

- The name of the command, and the name and home of the improvement record.
- Where an accepted rule lands in a repo that takes changes only by pull request.
- Whether `gates.json` should also store where a comment was attached.
- Whether propose may run in a fresh session, now that the ledger holds the record.
- When the gates, the build and verify write to the ledger themselves (decision 8).

## Sources

- The paper: <https://arxiv.org/abs/2611.18856> (read in full: body and appendices).
- The playbook, secondary sources only. The original text was not read:
  - <https://gist.github.com/Maciejdziuba/88890d7e0eeefa5a8738bbe9fd5e20b8>
  - <https://openclawdatabase.com/news/videos/2026-08-07-program-design-system-agentic-engineering/>
  - <https://posthog.com/newsletter/software-factories>
