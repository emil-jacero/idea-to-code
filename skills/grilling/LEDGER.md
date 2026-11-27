# The ledger

A **ledger** is one YAML file that holds every question put to the owner and every choice you make yourself, for one piece of work. Read this file when the calling command or skill names a ledger. The ledger is then the record of decisions: the list at the end of the grill is written from it, and nothing is recorded in the chat alone.

## Where it lives

A ledger starts at `openspec/explore/<name>/questions.yaml`, where `<name>` is a short name of the idea in kebab-case. The file is not committed there. The propose step moves it into the change folder, as `openspec/changes/<change>/questions.yaml`, and it is archived with the change. Work with no OpenSpec folder has no ledger.

## The form

```yaml
idea: "Upload retries are configurable"     # the idea, in its current wording
idea_history: []                            # earlier wordings, oldest first
entries:
  - id: q3
    phase: explore              # explore | propose | build | verify
    scope: program-design       # product | architecture | program-design | flow
    kind: question              # question (put to the owner) | choice (your own)
    status: settled             # open | settled | dropped | replaced
    opened_by: q1               # the entry whose answer opened this one, or null
    replaces: null              # the entry that this one replaces, or null
    asked: 2026-11-27T09:58:00Z
    question: "Where does the retry count of the upload job live?"
    options:
      a: "A key in the service config, `upload.retries`"
      b: "A constant in the code"
    recommended: a
    reason: "The count is expected to change. My judgement, not researched."
    predicted_answer: a         # only for kind: question
    predicted_outcome: "One slice, and no change to the public config schema"
    answer:
      choice: b                 # a letter, or other
      text: null                # the owner's words, when the answer is not a plain letter
      by: owner                 # owner | delegated | agent | rule
      rule: null                # for by: rule, the file that holds the rule
      at: 2026-11-27T10:00:00Z
    thoughts: "The owner wants no new config key before the service has users."
    leads_to: none              # adr | glossary | guide | idea | none
    observed: null              # leave null: a later review of the change fills it
```

Take each time from `date -u +%Y-%m-%dT%H:%M:%SZ`.

Write each text value in double quotes: `idea`, `question`, each option, `reason`, `predicted_outcome`, `text` and `thoughts`. Write a `"` inside a value as `\"`. A bare value that holds `: ` or ` #`, or that starts with a backtick, breaks the file. After each write, parse the file with a YAML parser that the machine has, for example `python3 -c 'import sys, yaml; yaml.safe_load(open(sys.argv[1]))' <file>`. Done when the file parses.

## The scopes

- `product`: what the work does for its user, and how anyone can tell that it works. No technical detail.
- `architecture`: the parts and how they talk: a service, a flow, an endpoint, a stored format, a public contract, a dependency.
- `program-design`: how the code is laid out: the file or package that holds a part, a type and its fields, a function signature, the call path, the seam where the tests go.
- `flow`: a question about the work itself, such as a track question, a capture offer or a gate.

## A question

1. Check the facts of the entry first (SKILL.md, Facts are yours, decisions are the owner's): each fact that an option, the reason or a prediction rests on has a source that you read. Then write the entry before you show the question: `status: open`, `asked`, the options, `recommended`, `reason` and both predictions. A prediction counts only when it is written before the answer.
2. Ask the question in the form of The question (SKILL.md), from the entry: the same options in the same order, and the same recommendation. The entry and the question never differ.
3. After the owner answers, fill `answer` and `thoughts`, and set `status: settled`. "You decide" gives `by: delegated`, with your choice. An answer in words that picks no letter gives `choice: other`, with the owner's words in `text`.
4. Add one entry with `status: open` for each question that the answer opens, with `opened_by`. Set `status: dropped` on each open entry that the answer makes pointless.

- `predicted_answer` is the letter you expect the owner to pick. It may differ from `recommended`.
- `predicted_outcome` is what the choice you recommend causes, as something that a test, a check, the verify step or a later change can see: "one slice", "no spec delta", "the upload test passes with no network". When no such thing exists, write `none`. Never write a hope, such as "easier to maintain".
- `thoughts` holds what the answer taught you that the options did not say, in one or two sentences. It is not a transcript.
- `leads_to` names the document that an offer of the `idea-to-code:domain-modeling` skill wrote for this answer: `adr` or `glossary`. An answer that changes the idea gives `idea`: move the old wording of `idea` to `idea_history`, and write the new wording.

## Your own choice

A choice that you make yourself gets an entry when the files of the change will state it: a choice that the owner would meet as an assumption, or a point of program design.

- `kind: choice`, with the options you weighed under `options`, your pick as `recommended` and as `answer.choice`, and `by: agent`.
- When a written rule settles the choice (a rules file of the repo, a decision record, the glossary, a spec), write `by: rule`, and the file that holds the rule in `rule`. One option is then enough.
- No `predicted_answer`. Write `predicted_outcome` as for a question.
- A choice rests on facts as a question does: look them up before you write the entry (A question, step 1). When a fact has no source, the choice is an assumption: say so in `reason`, with what settles it.

## Nothing is deleted

No entry is deleted, and no answer is overwritten. When an answer replaces an earlier one, write a new entry with `replaces`, and set `status: replaced` on the old entry. A question that is asked again with a new option is a new entry too.

## After the plan

The build and the fix round write to the ledger in one case: an answer of the owner there changes what an entry settled. The owner picks another option than the entry holds, or overrules a choice of yours. An answer that makes you edit the spec, the design or the tasks of the change is the sign: read the ledger then, at `openspec/changes/<change>/questions.yaml`. A change with no ledger gets none.

Write one new entry, as Nothing is deleted says: `phase: build` or `phase: verify`, `replaces`, the question as you asked it, with its options and your recommendation, and the owner's answer. Both predictions are `null`, because neither was written before the answer. Put what the earlier entry rested on, and what proved it wrong, in `thoughts`. The commit that carries the edit of the change's files carries the ledger too. Every other answer of the build and of the fix round stays in `build-report.md`.
