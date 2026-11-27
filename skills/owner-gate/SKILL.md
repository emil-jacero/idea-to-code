---
name: owner-gate
description: "Apply an owner gate to an OpenSpec change: the owner reviews the plan or the verified result. Use when propose has written a change folder, before the first slice of a build, after a passed verify, and before the first push of a change."
---

# Owner gate

An **owner gate** is a point where you decide, by the criteria below, whether the owner looks at the work before it goes on. It is soft: no hook and no script applies it. You apply it, and you record what you did. You never approve for the owner. While a review is open, the work on that change waits.

## The two gates

| Gate | When | The owner reviews | The owner looks when |
| --- | --- | --- | --- |
| **Plan gate** | Propose has written and validated the change folder. | The change folder. | `assumption`: the plan rests on an assumption. `contract`: the change touches a public contract or is breaking. |
| **Result gate** | Verify has passed. Nothing is pushed yet. | The diff of the working branch. | `fix-round`: verify needed a fix round. `report`: the build report, `build-report.md` in the change folder, names a disputed test, a bug or a stop. `open-finding`: a lead or an Owner finding is still in a report. |

- **Assumption:** a choice in the change folder that no answer of the owner and no checked fact settles. A checked fact comes from the repo, a tool, a doc, a research note or a prototype. A choice the owner delegated ("you decide") is settled.
- **Public contract:** an interface that another repo or a user consumes: a published schema or module, a CLI command or flag, an API, a CRD, a config key, a file format.
- **Breaking:** the pull request title will carry `!`.

A change with no change folder (work outside a change) has no owner gate.

## Apply a gate

1. **Is the gate on?** Both gates are on, unless a gate line turns one off: `Plan gate: off.` or `Result gate: off.` The line stands in the repo guide (`AGENTS.md`, else `CLAUDE.md`), or in the `context:` of `openspec/config.yaml`. A gate line may be a list item, and no other wording turns a gate off. A line that says in other words that a gate is off turns no gate off. Report that line, and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. The question offers two options: write the gate line in its place, so that the gate is off, or keep the gate on. Until the owner answers, the gate is on. A gate that its line turns off has the outcome `off`; the source is `guide` when the repo guide holds the line, else `config`. The owner's word for this change wins over both: "skip the plan gate" gives `skipped`, source `owner`; "show me the plan" or "show me the result" goes straight to step 3, source `owner`. For `off` and `skipped`, go to step 5.
2. **Check every criterion of the gate** against the files and the answers and reports of this conversation, never from memory of another session: the change folder at the plan gate; the build report, the verify report and the fix-round report at the result gate. At the result gate, start only when the verify report of the pass that passed (its `Verify rules:` line and its `Base:` line first) is written as text in this conversation. Then judge the `fix-round` and `open-finding` criteria first. The `fix-round` criterion holds when `build-report.md` in the change folder holds a `## Fix round` section, or when this session ran a fix round. When one of them holds and that file is missing or holds only a `## Fix round` section, ask no question on the `report` criterion: the owner reviews the result anyway. Write in the record's `reason` that the `report` criterion was not checked, because no build report was found. Otherwise: Read the build report, `build-report.md` in the change folder, for the `report` criterion. When that file does not exist, do not judge the `report` criterion from memory. Put it to the owner as one question in the form of the `idea-to-code:grilling` skill, unless the repo guide says what holds then. The question asks whether the build's final report named a disputed test, a bug or a stop. A file that holds only a `## Fix round` section holds no build report: ask as for a missing file. When none holds, the outcome is `passed`: go to step 5.
3. **Show the work.** State first which criteria held, and why, in one to three sentences. At the result gate, also list each answer of the owner in the build report (the `### Answers` list under `## Fix round`): each test-lock offence and each finding about a past commit, with its commit and its answer, so that the owner sees what the test lock and the flow let stand.
   - With a review tool such as Plannotator (an optional tool, not part of this plugin): open the change folder at the plan gate, and the diff of the working branch at the result gate. In Plannotator: at the plan gate, `annotate` with the change folder as `target` and `gate: true`; at the result gate, `review` with the repo as `target`, `options.base` set to the `Base:` branch of the verify report (the default branch that the build and verify found), and `gate: true`. Then end your turn and wait for the feedback message.
   - Without one: show a summary (what the change does, the criteria that held, where the files are) and ask one question in the form of the `idea-to-code:grilling` skill, with the three answers of step 4 as its options.
4. **Follow the owner's answer:**
   - **Approve:** the result is `approve`.
   - **Approve with changes** (comments, and a word to go on): make each change, then go on. The result is `approve-with-changes`.
   - **Change and show again** (comments with no word to go on): make each change, then run step 3 again.

   At the plan gate, you make each change in the change folder, and validate the change again as propose did. At the result gate, a change to code or tests is a finding: run it through After verify of the `idea-to-code:slice-build` skill, where fresh writers make it and verify runs once more. A comment that needs a decision is one question in the form of the `idea-to-code:grilling` skill.
5. **Record the outcome** (The record), and name it in your report to the owner: the gate, the outcome and each criterion that held.

Done when `gates.json` holds an outcome for the gate.

## The record

Write `gates.json` in the change folder, `openspec/changes/<change>/`, only when a gate ends. It is one of the change's files: it reaches the default branch in the change's pull request, and it is archived with the change. After the archive, read it in the change's folder under `openspec/changes/archive/`.

```json
{
  "plan": {
    "outcome": "reviewed",
    "source": "criteria",
    "criteria": ["assumption"],
    "reason": "The plan stores the error text in a new messages file. No explore answer covers where the text lives.",
    "result": "approve-with-changes",
    "comments": [
      {
        "comment": "Put the text in the handler, no new file.",
        "change": "design.md: the messages file is removed; S1 names the handler."
      }
    ],
    "datetime": "2026-11-23T08:14:00Z"
  },
  "result": { "outcome": "off", "source": "config" }
}
```

- `outcome`: `off`, `skipped`, `passed` or `reviewed`.
- `source`: what set the outcome: `guide`, `config`, `owner` or `criteria`.
- `criteria`: the keys of the criteria that held; empty for `passed`. Only with `passed` and `reviewed`.
- `reason`: your reasoning, in one to three sentences. For `passed`, why no criterion held. Never a transcript. For `skipped`, the owner's word, in one sentence. Only with `passed`, `reviewed` and `skipped`.
- `result`: the owner's last answer, `approve` or `approve-with-changes`. Only with `reviewed`.
- `comments`: each comment of the owner, with the change you made for it. Only with `reviewed`.
- `datetime`: when the gate ended, in UTC, as ISO 8601 with `Z` (`date -u +%Y-%m-%dT%H:%M:%SZ`). Only with `passed`, `reviewed` and `skipped`.

A record with the outcome `off` holds `outcome` and `source`, and no other field, as the `result` record of the example shows. A record with the outcome `skipped` holds `outcome`, `source`, `reason` and `datetime`.

Do not commit the plan record yourself. The build commits it with the other files of the change folder: the `idea-to-code:slice-build` skill says which commit carries them. After the result gate, load the `idea-to-code:commit` skill and commit `gates.json` on the working branch. That commit holds only `gates.json`. It is a commit of this skill and not of the build, so the rule of the `idea-to-code:slice-build` skill on the first commit does not cover it. The commit ships nothing, and its type follows the repo's commit rules.

## The build check

Before the first slice of a build, read `gates.json`. When the plan gate has no outcome there, apply the plan gate now. The build starts only when the plan gate has an outcome.

## The push check

Before the first push of a change, read `gates.json`. When the result gate has no outcome there, apply the result gate now. Nothing is pushed before the result gate has an outcome.
