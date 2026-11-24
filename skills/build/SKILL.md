---
description: "Build an OpenSpec change slice by slice, tests first, in the current repo. Use it when propose has written the change folder, or to resume a build that stopped. It commits on the working branch and pushes nothing. Load it also when the user asks in words to build, apply or implement an OpenSpec change, or to work through its tasks, or says yes after you named this command."
argument-hint: "[change-name]"
---

Run the build step of the Idea to Code flow in the current repo.

Change: $ARGUMENTS

Select the change first. When the `Change:` line holds a name after the colon, use it. When it holds no text, use the change that this conversation names. With none named, run `openspec list --json` and use the only active change. With several active changes, ask the owner which one, as one question in the form of the `idea-to-code:grilling` skill. With no active change, say so, name `/idea-to-code:propose`, and stop. Say which change you use.

1. Work from the repo root. Read the repo guide (`AGENTS.md`, else `CLAUDE.md`), the files it names and `openspec/config.yaml`.
2. Read the state of the change: `openspec status --change <name> --json` and `openspec instructions apply --change <name> --json`. When the state is blocked, show what is missing and stop. When every task is complete and `openspec/changes/<name>/build-report.md` is committed, the change is built: report that, name `/idea-to-code:verify <name>`, and stop. When every task is complete and that file is missing or not committed, load the `idea-to-code:slice-build` skill and run only its After the last slice: the report counts this run as a resume.
3. Load the `idea-to-code:slice-build` skill and follow it, from Before the first slice to After the last slice. One run builds every slice. The skill says who writes the tests and the code, which checks run, and when each commit is made.
4. Never load the repo's `openspec-apply-change` skill, also not on a request in words to apply the change. Its task loop lets the session write the code and tick a box after each task, and the steps of the `idea-to-code:slice-build` skill take the place of that loop. The two commands of step 2 give all that the build needs from OpenSpec.
5. Give the final report as that skill describes it. Push nothing and open no pull request.
6. End as that skill says in After the last slice: name `/idea-to-code:verify <name>` for a fresh session, and do not start verify in this session.
