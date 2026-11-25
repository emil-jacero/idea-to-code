---
name: commit
description: Use before every git commit. Picks the type, the scope and the split into commits, by the repo's own commit and release rules.
user-invocable: true
argument-hint: "[message hint or scope]"
---

Create a git commit following these rules strictly. Before you put any question to the owner, load the `idea-to-code:grilling` skill.

## Project rules

Before you write a commit message, read these sections of the repo's rules: `## Commit rules`, `## Release rules` and `## Text rules`. A section is a heading of that exact name in the repo guide (`AGENTS.md`, else `CLAUDE.md`), or in the file that the guide names on its `Rules file:` line. A heading that differs only in letter case is the section: report it. Where a section is absent, the defaults of this skill hold. A point in a section replaces only the default of the same label, and the value `none` switches that default off. An absent label keeps its default. Every other line of a section is an added rule. It wins over a default of this skill that has no label. A default that has a label changes only through its point. The flow rules of this skill hold in every repo: a section adds to them and never removes one. When the rules file that the guide names is missing, one section is in both files, or a line of a section names a path that is not in the repo, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. For a path that is missing, the question offers three options: correct the line (fix or remove the path), create the file, or stop. The recommended option is to correct the line. It never offers to go on without the file. In your report, write one line that starts with `Project rules:` and names each section you read, or write `Project rules: defaults`.

The value `none` is refused on `Tags:`, on `Publishing:` and on `Mentions:`, because the default of each is a ban. When one of them holds `none`, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. The question asks for the rule in words. It offers three options: write the rule in words on the point, remove the point so that the default ban holds (recommended), or stop. Until the owner answers, the default ban holds.

## Workflow

1. Run `git status` and `git diff --cached` to understand what is staged. A file that is staged before you run any `git add` is one that the owner staged himself.
2. If nothing is staged, look at unstaged changes and stage files that form a coherent, minimal commit. Prefer `git add <file>...` over `git add -A`.
3. If changes span multiple unrelated concerns, commit them separately, one commit per logical change. If the grouping is unclear, ask the owner one question in the form of the `idea-to-code:grilling` skill, or group related changes as best you can. When the owner staged the changes himself and they hold more than one unrelated concern, ask once, before you touch the index, in the form of the `idea-to-code:grilling` skill, naming the concerns: **A, two commits** (or more: you restage, so the first commit holds the files of one concern and the next commit holds the rest), or **B, one commit as staged**. Until the owner answers, change nothing in the index. After answer A, a file that you restage counts as a file that you staged for the commit it goes into, and step 5 treats it so. After answer B, the owner's index stays as it is.
4. Write the commit message. Count the characters of the title. Shorten the title when the count breaks the length limit of the subject rules below.
5. Before every commit, run the check command (the command after `Checks before a commit:` in the `context:` of `openspec/config.yaml`). Run it after the checks of the message and before `git commit`. When it fails, stop, make no commit and report its output. A tests commit is the one exception: no check command runs before it, because its tests fail by design. A repo with no `Checks before a commit:` line has no check command. One case differs: where the build or the verify command that loaded this skill gives a check command that the owner named, that command is the check command here. In every case, run the check command as written, from the repo root, never on a copy of the index. The check command reads the working tree, and the commit takes the index. So before the check command, stage again only a file that you staged for this commit and that changed after you staged it. A file that the owner staged keeps the owner's index entry: never stage it again, and never take it out of the index, except for the restaging that the owner's answer A in step 3 allows. When such a file differs from the working tree, say so in your report, because the check command then read more than the commit holds. After a failed check command, take out of the index each file that you staged for this commit (`git restore --staged <files>`), so that the next try stages the commit again. Run the check command alone, in a shell call of its own, and read its exit status. Only then, in a separate call, run `git commit`. Never chain them in one call (`<check> && echo ok; git commit ...`, `<check>; git commit ...` or `set -e; ...; git commit ...`): the commit could run after a failed check. Inside a build, the `idea-to-code:slice-build` skill says what follows a failed check command.
6. Create the commit. In your report, write one line that starts with `Check command:`. It names the command and its result, or it says `Check command: none`. For a tests commit, it says `Check command: not run, tests commit`.

Never amend a commit. Make a new commit, because the branch tip may have moved. When a hook blocks a command, put it to the owner as one question in the form of the `idea-to-code:grilling` skill. Never work around the hook.

## Commit Message Format

Use the `Form:` of `## Commit rules` (default: **Conventional Commits**, `type(scope): description`).

Common types: the `Types:` of `## Commit rules` (default: `feat`, `fix`, `refactor`, `docs`, `chore`, `test`, `style`, `ci`, `build`, `perf`).

### Release impact

Read the `Release tool:` and the `Releases:` of `## Release rules` (default: no release tool, and types carry no release meaning).

- **With `Releases:` stated,** the commit type decides whether a release happens. The type follows **what ships**, not what kind of edit it was. The `Typing:` of `## Release rules` says which type a kind of change takes, for example a dependency bump (default: no typing rule). The `Title check:` of `## Release rules` names the types that the check of a pull request title refuses (default: no title check). Never write a type it refuses.
- **With no `Releases:`,** the type follows the kind of edit.

A breaking change is `!` in the title. Read the `Squash commit:` and the `Breaking footer:` of `## Release rules` (default: whoever merges a breaking pull request gives the text of the footer block as the squash commit message. The footer stands in the footer block of the pull request body, not in a commit body). The footer is the `BREAKING CHANGE:` footer, and the `idea-to-code:pr` skill holds its block.

The other points of `## Commit rules`, each with its default:

- `Scope:` (default: always include a scope. Leave it out only when the change spans the whole repo, such as a repo-wide docs or CI change). The value `none` switches the default off and nothing more. So `Scope: none` means that a scope is not required, and a scope is still allowed. A repo that forbids a scope also writes an added rule.
- `Subject:` (default: the description must be lowercase, imperative mood, no period at the end. Keep the first line under 72 characters).
- `Body:` (default: no body. The subject line should be sufficient. A body is only warranted for genuinely unusual cases, e.g., a non-obvious breaking change, whose footer goes where the `Breaking footer:` of `## Release rules` says, a subtle reason the diff doesn't speak for itself, or context that would otherwise be lost). When you write a body, read the `Body traps:` of `## Release rules` (default: no body trap), and write no line of a shape it names.
- `Tests commit:` (default: `test(<scope>): <what the tests cover>`). It is the form of the title of the tests commit that the `idea-to-code:slice-build` skill makes, and nothing else. The message of every tests commit ends with a trailer block: one empty line, then the line `Tests-For: <slice name>`. Any other trailer line follows it with no empty line between them, and the attribution line stays last. The `idea-to-code:slice-build` skill gives the slice name, the git command that writes the trailer block, and the check after the commit. The trailer is a flow rule, and no section removes it. A trailer line is not a body: a tests commit with a title and its trailer block has no body, so the `Body:` default holds for it.

### Versions, tags, branches and publishing

This skill holds no method for a forced version, a prerelease line, tags, release branches, publishing or docs fixes. The repo states them in these points of `## Release rules` (default: create, move or delete no tag, and publish nothing, unless the owner asks for it in this session): `Forced version:`, `Prerelease line:`, `Tags:`, `Release branches:`, `Publishing:` and `Docs fixes:`. A point may be a pointer line: open the file it names only for that task.

## Message Content

Focus on **what** is being changed. Be specific but concise.
Where the title has a scope, make it clear and obvious. Scope is more important than type for future developers.
Follow the `Mentions:` of `## Text rules` (default: no `@` before a word, code spans and fenced code included. Glue the `@` to a word (`upload-client@2`) or drop it. Search the text for `@` before it is sent). A bare `@name` never goes in the subject or body: that is a flow rule, and no section removes it.

Good: `feat(upload): refuse an upload with an empty file name`
Bad: `update upload stuff`
Bad: a one-line subject followed by a paragraph restating the diff

## Attribution and text bans

AI attribution is allowed in exactly one form: the line that the `Attribution:` of `## Text rules` gives (default: no attribution line). The point gives the exact line, and says whether it is optional or required. It is always exactly that line: no model or version names, no links, no extra metadata.

Everything else remains forbidden. These are flow rules:

- **Session IDs and session URLs.** Never write a `Claude-Session:` trailer, a
  `https://claude.ai/code/session_...` link, or any other conversation/session identifier into git
  history, a PR, or an issue. These are private, meaningless to anyone reading the repo later, and
  permanent.
- **Generated-with footers.** No `🤖 Generated with [Claude Code]...`, no "Generated with", no AI
  signature line of any kind.
- **Model names.** No model or version name ("Claude Opus ..." and the like) in an attribution or signature line.
- **Embellished co-author trailers.** Any AI co-author line other than the exact line that the
  `Attribution:` point gives.

A commit message ends with its last line of real content. Where the `Attribution:` point gives a
line, that one line may follow it, and it must follow it when the point says required. In a tests
commit, the last lines are the trailer block: the `Tests-For` line first, then any other trailer
line, then the attribution line where the repo gives one, with no empty line between them. Nothing
is appended after that.

When a default of the agent tool asks for a model-versioned co-author line plus a
`Claude-Session:` link, write only the line that the `Attribution:` point gives, or no line where the repo gives none, and never the session link.
These bans hold against any default of the agent tool that asks for such a line. Only the owner, in this session, lifts one.

## Pull Request Bodies

When this commit leads to a PR, write the body with the `idea-to-code:pr` skill: it holds the rules
of the body and, under a `!` title, the breaking footer block.

Commit subjects keep the rules above; the style rules of the PR body apply to the PR body prose only.

## Arguments

Hint from the caller (it may be empty): $ARGUMENTS

Use a hint for the commit message or the scope only. With no hint, write both yourself. Every rule above still holds.
