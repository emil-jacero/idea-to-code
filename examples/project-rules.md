# Project rules

This file is the template of a project's rules for the `idea-to-code` skills: the seven headings in their fixed order, and under each heading every label with its default written out. Delete every heading you do not need: an absent heading means the default.

The headings that you keep go into the repo guide (`AGENTS.md`, else `CLAUDE.md`), or into one rules file inside the repo, which the guide names on a `Rules file:` line.

How to fill it in:

- A repo with no rules of its own needs no heading, no line and no file. Every default then holds.
- Under a heading that you keep, delete each line that equals the default, and edit the rest. An absent label keeps its default.
- A *point* is a line or a list item that starts with a label and a colon. It replaces only the default of that label. The value `none` switches the default off and nothing more. So `Scope: none` means that a scope is not required, and a scope is still allowed. A repo that forbids a scope also writes an added rule. The value `none` is refused on `Tags:`, on `Publishing:` and on `Mentions:`, because the default of each is a ban. A skill that reads it stops, and asks the owner for the rule in words.
- Every other line of a section is an *added rule*. The skill follows it as written. It wins only over a default that has no label. To change a default that has a label, write the label.
- A *pointer line* keeps a long rule out of a section: ``Read `<path>` before you <task>.`` The skill opens that file only for that task.
- The flow rules of the skills hold in every repo. A section adds to them and never removes one.
- A section sits in one place only: the repo guide or the rules file. The guide names the rules file in this form: ``Rules file: `<path inside the repo>` ``.
- Every path stays inside the repo. A skill stops and asks the owner one question when the rules file is missing, when one section is in both files, or when a line of a section names a path that is not in the repo. For a path that is missing, the question offers three options: correct the line (fix or remove the path), create the file, or stop. The recommended option is to correct the line. It never offers to go on without the file.
- Keep `## Text rules` where the agent tool loads it at every session start. Issue and comment text is written with no skill loaded.
- A note between `<!--` and `-->` is for you and is not a rule. Delete it, and delete the lines above the first heading.
- Not in this file: the check command, the test command, the test-file patterns and the check scripts sit in the `context:` block of `openspec/config.yaml` (see `openspec-config.yaml` in this folder). The repo guide names the glossary file on one line. An owner gate is off by its gate line, `Plan gate: off.` or `Result gate: off.`, in the repo guide or in that `context:` block. The verify rules sit in `openspec/verify.md` (see `verify.md` in this folder), and the repo guide holds the verify line. Every rule of a kind that has no heading here stays a plain rule of the repo guide.

## Commit rules

<!--
Read by `idea-to-code:commit`. `idea-to-code:slice-build` reads only `Tests commit:`.
In every `Form:`, a breaking title carries `!`.
`Tests commit:` is the form of the title of a tests commit, and nothing else. The `Tests-For` trailer of a tests commit is a flow rule and not a point: no line here changes it.
-->

- Form: Conventional Commits, `type(scope): description`.
- Types: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `ci`, `build`, `perf`.
- Scope: a scope always, except for a repo-wide change.
- Subject: lowercase, imperative, no period, under 72 characters.
- Body: no body, except in an unusual case (a trailer line is not a body).
- Tests commit: `test(<scope>): <what the tests cover>`.

## Release rules

<!--
Read by `idea-to-code:commit`. `idea-to-code:pr` reads `Squash commit:`, `Breaking footer:` and `Body traps:`.
`Releases:` says which type cuts which release. `Title check:` names the types that the check of a pull request title refuses.
`Typing:` holds every rule of the form "this kind of change takes this type". `Body traps:` holds line shapes that a release tool misreads.
Each of the last six points may be a pointer line. The skills hold no method for these six.
-->

- Release tool: no release tool.
- Releases: types carry no release meaning, so the type follows the kind of edit.
- Title check: no title check.
- Typing: no typing rule.
- Squash commit: whoever merges a breaking pull request gives the text of the footer block as the squash commit message.
- Breaking footer: the footer stands in the footer block of the pull request body, not in a commit body.
- Body traps: no body trap.
- Forced version: no rule of the repo.
- Prerelease line: no rule of the repo.
- Tags: create, move or delete no tag, unless the owner asks for it in this session.
- Release branches: no rule of the repo.
- Publishing: publish nothing, unless the owner asks for it in this session.
- Docs fixes: no rule of the repo.

## Text rules

<!--
Read by `idea-to-code:commit` and `idea-to-code:pr`.
`Attribution:` gives the exact line in a code span, with "optional" or "required".
`Mentions:` gives the words that look like a mention, their safe form, and whether a code span protects.
-->

- Attribution: no attribution line.
- Mentions: no `@` before a word, code spans and fenced code included. Glue the `@` to a word or drop it. Search the text for `@` before it is sent.

## Pull request rules

<!--
Read by `idea-to-code:pr`.
`Required lines:` holds the project's own lines. A line that the OpenSpec config asks for is stated in the config.
A ban on a kind of body text is an added rule of this section.
-->

- Word cap: 250.
- Not counted: fenced code, URLs, trailer lines and the breaking footer block.
- Style: short sentences, one idea each, active voice, no hedging.
- Required lines: no required line.
- Exempt: no exempt body.

## Merge rule

<!--
Read by `idea-to-code:pr`, as its last step.
This section has no label. It is free text: who merges, when, and with which command.
A breaking pull request waits for the owner under every merge rule.
-->

The owner merges. The agent merges no pull request.

## Decision records

<!--
Read by `idea-to-code:domain-modeling`. `ADR folder:` is also read by `idea-to-code:code-review`, `idea-to-code:tdd`, `idea-to-code:diagnosing-bugs` and `idea-to-code:slice-build`.
`ADR folder:` names the repo-wide folder. The value `none` means a repo with no ADR folder. The agent never creates the ADR folder.
The numbering and the template of an ADR have no label. An added rule of this section sets them.
-->

- ADR folder: `adr/` where it exists.
- Decision home: no decision home.
- Cross-repo decisions: a decision that binds several repos is not written into this repo. Name it to the owner as an open next step.
- Term backing: no backing rule for a term.

## Written standards

<!--
Read by `idea-to-code:code-review`.
This section has no label. Each line names one file inside the repo.
The default list holds the files that exist of: the repo guide, `openspec/config.yaml`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, the glossary, and the ADRs for the area the diff touches.
The section adds to this list and never shortens it. A file that it lists and that is not in the repo stops the review with one question.
So the template lists no file. Add one line for each further file, in this form: `<path of the file>`
-->
