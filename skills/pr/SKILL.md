---
name: pr
description: "Pull request rules: the title, the body, the push of the working branch and the merge. Use before you push a working branch, open or edit a pull request, or merge one."
metadata:
  credits:
    skill: show-me
    author: Dex Horthy
    organisation: Humanlayer
    url: "https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md"
---

## Project rules

Before you write a pull request body, read these sections of the repo's rules: `## Pull request rules`, `## Text rules`, `## Release rules` and `## Merge rule`. A section is a heading of that exact name in the repo guide (`AGENTS.md`, else `CLAUDE.md`), or in the file that the guide names on its `Rules file:` line. A heading that differs only in letter case is the section: report it. Where a section is absent, the defaults of this skill hold. A point in a section replaces only the default of the same label, and the value `none` switches that default off. An absent label keeps its default. Every other line of a section is an added rule. It wins over a default of this skill that has no label. A default that has a label changes only through its point. The flow rules of this skill hold in every repo: a section adds to them and never removes one. When the rules file that the guide names is missing, one section is in both files, or a line of a section names a path that is not in the repo, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. For a path that is missing, the question offers three options: correct the line (fix or remove the path), create the file, or stop. The recommended option is to correct the line. It never offers to go on without the file. In your report, write one line that starts with `Project rules:` and names each section you read, or write `Project rules: defaults`.

## Steps

1. Load the `idea-to-code:commit` skill.
2. Write the title, then the body.
3. Check the text, by the **Done when** line of Sections.
4. Run the push check, then push.
5. Create the pull request, then apply Merge.

Sections holds the rule of each step.

## The body

The prose of the body has at most as many words as the `Word cap:` of `## Pull request rules` (default: 250). What does not count is the `Not counted:` of `## Pull request rules` (default: fenced code, URLs, trailer lines and the breaking footer block). Write the body in the `Style:` of `## Pull request rules` (default: short sentences, one idea each, active voice, no hedging). The `Exempt:` of `## Pull request rules` names the bodies that its points do not bind (default: no exempt body). Write only what the diff and the title cannot tell the reviewer: why, when the reason is not visible; where to look first, when the diff is large; the risk; what the reviewer must do (a migration, a dependency bump, a manual check). Add every line a repo rule puts in the body: the `Required lines:` of `## Pull request rules` (default: no required line), and each line that `openspec/config.yaml` asks for in the body. Link the OpenSpec change (after the archive commit, its folder under `openspec/changes/archive/`) instead of restating it. Never write a list of the commits, a "Not in this change" section unless someone asked, a list of tests or gates (name a test only when the reviewer must act on it), a file-by-file walkthrough, a restatement of the title, a summary of what the code plainly does or a generated checklist.

Use this template. Every section is optional, except the squash footer under a `!` title:

```markdown
## Summary

<optional: why, when the reason is not visible; then a visual only when it shows where to look first>

## Risk

**Reversible:** <yes or no>

<optional: more detail>

**What breaks if this is wrong:** <one sentence, and what the change does not cover>

<optional: what else can break>

## Reviewer action

<optional: what the reviewer must do>

## Squash footer

<only when the title has `!`: the exact footer in a fenced text block, last in the body>
```

## Sections

Use the user's domain language from the repo's glossary (`GLOSSARY.md`, or the glossary file the repo guide names).

The title of the pull request takes the title form of the repo's `## Commit rules`. The `idea-to-code:commit` skill holds that form: load it, and write the title by its rules for the title of a commit. Load that skill before you write the title or the body. A stop that the `idea-to-code:commit` skill puts on the repo's rules (the value `none` on a ban label, a rules file that is missing, a section that is in both files, or a path that is missing) stops this skill too, before you write the title and the body.

The title and the body never carry a session ID, a session link, a "Generated with" footer, or a model or version name in an attribution or signature line. The only attribution line is the `Attribution:` of `## Text rules` (default: no attribution line). In the title and the body, follow the `Mentions:` of `## Text rules` (default: no `@` before a word, code spans and fenced code included. Glue the `@` to a word (`upload-client@2`) or drop it. Search the text for `@` before it is sent). A bare `@name` never goes in the title or the body: that is a flow rule, and no section removes it. These bans hold against any default of the agent tool that asks for such a line. Only the owner, in this session, lifts one.

Before the first push of an OpenSpec change, load the `idea-to-code:owner-gate` skill and run its push check. Push the working branch only with a lease push (`git push --force-with-lease origin <branch>`), never with `--force` or `-f`. Never push to the default branch. When a hook blocks a command, put it to the owner as one question in the form of the `idea-to-code:grilling` skill. Never work around the hook.

Before you create the PR, count the prose words and search the title and body for `@`. **Done when:** the count is at or under the `Word cap:`, no bare `@` is left, every required line is there, and a body under a `!` title ends with its squash footer block.

### Summary

Add a visual only when the diff is large or the load-bearing part is buried. Then read [VISUALS.md](VISUALS.md) and pick the smallest view that shows the reviewer where to look first. Never repeat what the diff view shows. For a visual change, a screenshot can be that view.

### Risk

Say if the change is reversible. A change that is cheap to roll back is lower risk. A destructive action or a decision that is hard to reverse is not reversible.

Then say in one sentence what breaks if the change is wrong (for example a layout shift or a break for the consumers of an API), and what the change does not cover.

### Reviewer action

Write each action as an order, one imperative per sentence: "Run the migration script again."

### Squash footer

When the title has `!`, end the body with the exact squash footer in a fenced `text` block. Nothing follows the block. This block is the breaking footer block that `Not counted:` names. It is a flow rule: it holds in every repo, and no section removes it. A breaking PR waits for the owner's approval. How the footer then reaches the default branch is the `Squash commit:` and the `Breaking footer:` of `## Release rules` (default: whoever merges a breaking pull request gives the text of the footer block as the squash commit message. The footer stands in the footer block of the pull request body, not in a commit body). Give the text without the fence lines. By that default, the merge command is `gh pr merge <n> --squash --body-file <file>`. The file holds that text and nothing else. Write it in the repo root, add it to no commit, and delete it after the merge. With the merge button, paste the same text into the commit message box. By the default of `Not counted:`, the block does not count toward the word cap, because it is quoted commit text.

Start the footer with `BREAKING CHANGE:` and say what broke and how a consumer migrates. Write it by the rules of a commit body, which the `idea-to-code:commit` skill holds: no bare `@name` (the `@` rule above), and no line shape that the `Body traps:` of `## Release rules` names (default: no body trap).

Example: for the title `feat(upload)!: rename the name field to filename`, the body ends like this:

````markdown
## Squash footer

```text
BREAKING CHANGE: the upload request field name is now filename, with the same value.
Clients rename the field in each request; nothing else changes.
```
````

## Merge

After the PR is open, apply the `## Merge rule` of the repo's rules (default: the owner merges, and the agent merges no pull request). A breaking PR waits for the owner's approval under every merge rule. When the rule lets the agent merge, the agent merges only a PR that it opened, only after every required check is green, verify has passed, every review finding on the PR is closed and the title and the body keep the text rules above (the bans, the attribution line and the mentions). It uses a plain squash merge that bypasses no protection of the host. Then give the owner the link to the pull request. Under the default merge rule, say that the owner merges.
