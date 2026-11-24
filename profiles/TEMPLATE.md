# Profile template

A profile holds one project's answers to the flow in
[Idea to Code](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md):
the optional parts it uses, its names, commands and paths, its rules for merge and text, its
state, its open points and its decisions. To adopt the flow, copy this file into the project's
own repo and write each answer after `Answer:` under its question. Keep the questions, so that
each answer stays next to its question. A question about a part the project does not use gets the
answer "not used". Where the project keeps a default of the skills, the answer is "default".

A profile is a plan, and no skill reads it. Each answer also goes into the repo files that the
skills read: the repo guide, the rules sections and the OpenSpec config. Where a question names
such a file, a section or a label, the answer goes there too. When the flow is built, the project
deletes the profile
([The project's profile](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-projects-profile)).

> **Status:** These questions follow `WORKFLOW.md` as written on 2026-11-24.

## 1. The project

Who the project is, and where its shared files live.

**What is the project called?**
Names the profile.

Answer:

**Which git host and which coding agent does the project use?**
Configures [Start here](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#1-start-here).

Answer:

**Which repos make up the project?**
Configures [Many repos in one workspace](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#many-repos-in-one-workspace).

Answer:

**Where do the files that several repos share live, if anywhere?**
Configures [Many repos in one workspace](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#many-repos-in-one-workspace).

Answer:

**Who is the owner, named as a role?**
Configures [Start here](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#1-start-here).

Answer:

## 2. Optional parts

Which optional parts the project uses, and why.

### Parts with a section in chapter 4

**Does the project use an enhancement store, and why?**
Configures [An enhancement store](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#an-enhancement-store).

Answer:

**Does the project use tracker issues for work over several repos, and why?**
Configures [A tracker issue for several repos](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#a-tracker-issue-for-several-repos).

Answer:

**Does the project keep many repos in one workspace, and why?**
Configures [Many repos in one workspace](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#many-repos-in-one-workspace).

Answer:

**Does the project release from commit types, and why?**
Configures [Release rules tied to commit types](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#release-rules-tied-to-commit-types).

Answer:

**Which repos, if any, have no specs, and why?**
Configures [A repo without specs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#a-repo-without-specs).

Answer:

**Does the project use owner gates: which of the two does a gate line (`Plan gate: off.`, `Result gate: off.`) in the repo guide or in the OpenSpec config turn off, which criteria does the repo guide add, and which review tool does it use?**
Configures [Owner gates](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#owner-gates).

Answer:

### Small parts at their steps

**Does the project use the side step and its evidence folder, and why?**
Configures [Step 1: Explore](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-1-explore).

Answer:

**Does the project keep a glossary and decision records, and why?**
Configures [Step 1: Explore](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-1-explore).

Answer:

**Does each proposal carry user stories, and why?**
Configures [Step 2: Propose](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-2-propose).

Answer:

**Does the project run check scripts, or the checks by hand, and why?**
Configures [Step 3: Build](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-3-build).

Answer:

## 3. OpenSpec

How the project installs OpenSpec and sets it up in each repo.

**Which OpenSpec version does the project pin, and what fails when the installed one differs?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

**How is the pinned version installed: once per machine, or per repo from a saved lockfile?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

**Which schema does each repo use, and does it have a specs artifact?**
Configures [A repo without specs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#a-repo-without-specs).

Answer:

**Where do the rules for each artifact live?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

**Does every machine that runs `openspec update` keep verify in its workflow list?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

**Which script is the config check, and where does it live?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

**Does any repo's OpenSpec config point at files outside the repo?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

## 4. Commands and skills

The commands that start each step and check each repo, and how the skills reach a repo.

### Commands

**Which commands of its own does the project keep beside the plugin's step commands (`/idea-to-code:explore`, `/idea-to-code:propose`, `/idea-to-code:build`, `/idea-to-code:verify`), such as a root command that picks the repo: what are they called, and where do they live?**
Configures [What a repo needs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#what-a-repo-needs-before-its-first-change).

Answer:

**Which command is the test command of each repo (the OpenSpec config names it after `Tests:`)?**
Configures [Per slice](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#per-slice).

Answer:

**Which command is the check command of each repo (the OpenSpec config names it after `Checks before a commit:`, and the `commit` skill runs it before every commit that is not a tests commit)?**
Configures [The repo's own files](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-repos-own-files).

Answer:

### Skills

**How does each person install the `idea-to-code` plugin: for every project, or for each repo?**
Configures [The kit in every repo](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-kit-in-every-repo).

Answer:

**The plugin holds the skills and the four step commands. Which parts of the kit stay as files in each repo?**
Configures [The kit](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-kit).

Answer:

**Which skills beside the kit skills does each repo carry?**
Configures [The skills](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-skills).

Answer:

## 5. Files

Where each file that the flow reads lives. Where the kit skills have a default, the question gives
it.

### Guides and records

**Which file is the repo guide (`AGENTS.md`, else `CLAUDE.md`), and which files does it name?**
Configures [Start here](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#1-start-here).

Answer:

**Which files hold the written standards, and which of them does the `## Written standards` section list?**
Configures [The verify rules file](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-verify-rules-file).

Answer:

**Which file is the glossary (the kit skills read `GLOSSARY.md`, or the file that the repo guide names)?**
Configures [Step 1: Explore](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-1-explore).

Answer:

**Where do decision records go: an ADR folder (the kit skills use `adr/`, or the folder that the `## Decision records` section names), or a decision home that the section names?**
Configures [The grill](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-grill).

Answer:

**Must a new term reach main in the same pull request as the spec or code that backs it?**
Configures [Step 1: Explore](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-1-explore).

Answer:

### The rules sections

The project's own rules sit under seven fixed headings: `## Commit rules`, `## Release rules`,
`## Text rules`, `## Pull request rules`, `## Merge rule`, `## Decision records` and
`## Written standards`. A repo with no rules of its own writes none, and each skill then uses its
defaults.

**Which of the seven sections does each repo write?**
Configures [The repo's own files](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-repos-own-files).

Answer:

**Where does each section sit: in the repo guide, or in one rules file that the guide names on a `Rules file:` line?**
Configures [The repo's own files](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-repos-own-files).

Answer:

**With several repos: how does each repo get its own copy of the shared rules file?**
Configures [The kit in every repo](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-kit-in-every-repo).

Answer:

### Verify and checks

**Which repos have a verify rules file (the verify command reads `openspec/verify.md`), and does each of their repo guides hold the verify line?**
Configures [Step 4: Verify](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-4-verify).

Answer:

**Where the repo has check scripts: which commands does the OpenSpec config name after `Slice check:` and `Test check:`?**
Configures [Per slice](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#per-slice).

Answer:

## 6. Merge, push and archive

Who merges, what may be pushed, and who starts the archive.

**What is the merge rule: does the default hold (the owner merges, and the agent merges no pull request), or does the repo's `## Merge rule` section say who merges, and when?**
Configures [The merge](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-merge).

Answer:

**Which pushes does the owner allow outside the flow?**
Configures [Step 5: Pull request and archive](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-5-pull-request-and-archive).

Answer:

**Which merge settings does the host enforce, such as squash only and branch protection?**
Configures [Step 5: Pull request and archive](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-5-pull-request-and-archive).

Answer:

**Who starts the archive, when (before or after the pull request opens), and how?**
Configures [Step 5: Pull request and archive](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-5-pull-request-and-archive).

Answer:

## 7. Text rules

The rules that the project sets for commit, pull request, issue and comment text. Each rule has a
default in the skills. A rule of the project goes into the repo's `## Text rules` or
`## Pull request rules` section.

**Which attribution line, if any, ends a commit message (by default none; the `Attribution:` point names the exact line)?**
Configures [Start here](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#1-start-here).

Answer:

**Which words of the project look like a mention, and how are they written safely (by default no `@` stands before a word, code spans and fenced code included; the `Mentions:` point loosens it)?**
Configures [Start here](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#1-start-here).

Answer:

**What is the word cap and the language of a pull request body, where the project changes the defaults of the `pr` skill?**
Configures [The pull request](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-pull-request).

Answer:

**Where do the text rules live: the `## Text rules` section of the repo guide, a rules file, a text hook?**
Configures [The repo's own files](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#the-repos-own-files).

Answer:

## 8. Releases

How releases are cut once a change is on main. The repo's `## Release rules` section holds these
rules, and its `## Merge rule` section says who merges.

**Which release tool cuts releases?**
Configures [After main](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#after-main).

Answer:

**May a tag be moved, deleted or re-created?**
Configures [After main](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#after-main).

Answer:

**Which commit types cut a release?**
Configures [Release rules tied to commit types](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#release-rules-tied-to-commit-types).

Answer:

**What does the host write into the squash commit?**
Configures [Release rules tied to commit types](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#release-rules-tied-to-commit-types).

Answer:

**How does a breaking change's footer reach main?**
Configures [Release rules tied to commit types](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#release-rules-tied-to-commit-types).

Answer:

**Who merges a release pull request?**
Configures [After main](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#after-main).

Answer:

## 9. Store and tracker

Where the store and the tracker issues live.

**Which repo is the store?**
Configures [An enhancement store](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#an-enhancement-store).

Answer:

**Who registers the store, and how?**
Configures [An enhancement store](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#an-enhancement-store).

Answer:

**How does the project make and change an entry?**
Configures [An enhancement store](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#an-enhancement-store).

Answer:

**Which repo hosts tracker issues, and which label marks them?**
Configures [A tracker issue for several repos](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#a-tracker-issue-for-several-repos).

Answer:

**Where does the list of repos come from, and which repos are private?**
Configures [A tracker issue for several repos](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#a-tracker-issue-for-several-repos).

Answer:

## 10. The flow's open points

What the project does about each point that the flow leaves open. Two of them are asked above:
the workflow list in [section 3](#3-openspec) and the archive in
[section 6](#6-merge-push-and-archive). One question below is on a default that a repo guide
can change.

### On the path

**How does the project split the work between OpenSpec's generated skills and the kit skills?**
Configures [Step 2: Propose](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-2-propose).

Answer:

**Which repos have a verify rules file that does not call the code review?**
Configures [Step 4: Verify](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-4-verify).

Answer:

**A listed lead does not keep verify from passing (the default). Does a repo guide say that a listed lead is an open finding?**
Configures [Step 4: Verify](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#step-4-verify).

Answer:

### In the optional parts

**What decides that work goes to the store, and what checks a delivered entry line?**
Configures [An enhancement store](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#an-enhancement-store).

Answer:

**How is a small change built in a repo without specs, where it has no Done when line?**
Configures [A repo without specs](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#a-repo-without-specs).

Answer:

## 11. State

Three lists: what is built and in use, what is decided but not built, and what is done by hand
today. The project's state lives here, because the flow names none
([Idea to Code](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#idea-to-code)).

## 12. Open points of this project

The points that only this project has and that are not decided. Write each as one sentence that
says what waits on it.

## 13. Decision log

The project's decisions, oldest first, one dated line each. Mark each line owner (the owner
decided), delegated (the owner said "you decide") or agent default (an agent's choice that holds
until the owner sets another; see
[Start here](https://github.com/emil-jacero/idea-to-code/blob/main/WORKFLOW.md#1-start-here)).
A line that a later decision replaced keeps its mark and names the date of the line that replaced
it.
