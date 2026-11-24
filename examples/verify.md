# Verify rules

<!-- Copy this file to openspec/verify.md, and edit it to fit the repo. Delete this comment. -->

The `/idea-to-code:verify` command applies this file on every verify run, before OpenSpec's comparison. Each breach of a rule here, and each failed check, is a finding that cites its rule.

## Checks

1. **The code review.** Load the `idea-to-code:code-review` skill once in each verify run. It reviews the diff against the repo's written standards and a smell baseline. A breach of a written standard is a finding. A smell that cites no written rule is a lead.
2. **The check for unasked work.** Read the diff that the code review read. A requirement, a scenario, a task or a Done when line must ask for each behaviour that the diff adds. Each miss is a finding.

<!-- Optional (user stories). Keep this check only when the proposals of the project hold a `## User stories` list: remove the comment marks. Delete it otherwise.
3. **The user-story check.** A requirement must cover each story of the proposal. In a repo without specs, a Done when line covers each story. Each story that nothing covers is a finding.
-->

## Rules of the repo

<!-- Write the repo's own verify rules here, one per line. Delete this heading when the repo has none. -->
