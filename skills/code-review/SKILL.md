---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag or merge-base) against this repo's written standards and a code-smell baseline, in a fresh sub-agent. Use once in each verify run, when the user wants a branch, a PR or work in progress reviewed, or asks to \"review since X\"."
---

One-axis review of the diff between `HEAD` and a fixed point: does the code follow this repo's written standards? It runs in one sub-agent with a fresh context window, so the diff is read without the context that wrote it. During verify it runs once in each verify run: the repo's `openspec/verify.md` calls it, and in a repo without that file the verify command, `/idea-to-code:verify`, loads it. Outside verify, it runs on any branch. Whether the code matches its spec, and whether it adds behaviour the spec and tasks did not ask for, is verify's check, not this skill's.

## Project rules

Before you list the standards sources, read these sections of the repo's rules: `## Written standards` and `## Decision records`. A section is a heading of that exact name in the repo guide (`AGENTS.md`, else `CLAUDE.md`), or in the file that the guide names on its `Rules file:` line. A heading that differs only in letter case is the section: report it. Where a section is absent, the defaults of this skill hold. A point in a section replaces only the default of the same label, and the value `none` switches that default off. An absent label keeps its default. Every other line of a section is an added rule. It wins over a default of this skill that has no label. A default that has a label changes only through its point. The flow rules of this skill hold in every repo: a section adds to them and never removes one. When the rules file that the guide names is missing, one section is in both files, or a line of a section names a path that is not in the repo, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. For a path that is missing, the question offers three options: correct the line (fix or remove the path), create the file, or stop. The recommended option is to correct the line. It never offers to go on without the file. In your report, write one line that starts with `Project rules:` and names each section you read, or write `Project rules: defaults`.

## Process

### 1. Resolve the repo

First resolve the repo the work is about, and run every git and file command from its root. In a lone clone, that is the current repo.

### 2. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag, the default branch, `HEAD~5`, etc.). When verify called you without one, use the merge-base with the branch the work merges into (the default branch, unless the branch was cut from another long-lived branch such as a maintenance branch) and ask nothing. Otherwise, with none given, put it to the owner as one question in the form of the `idea-to-code:grilling` skill, with that merge-base as the recommended option.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves (`git rev-parse <fixed-point>`) and the diff is non-empty. A bad ref or empty diff should fail here, not inside the sub-agent.

### 3. Identify the standards sources

Search the repo for every file that documents how code should be written. When the repo guide, `openspec/config.yaml`, `CODING_STANDARDS.md` or `CONTRIBUTING.md` exists in the repo, it must be on the list, and so must the repo's glossary (`GLOSSARY.md`, or the glossary file the repo guide names) and the ADRs in the `ADR folder:` of `## Decision records` (default: `adr/` where it exists) that cover the area the diff touches, where they exist. Every file that the repo's `## Written standards` section lists must be on the list too: that section adds to this default list and never shortens it. Read only files inside the repo.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs no caller in the diff or the repo has yet. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

### 4. Start the sub-agent

Start one sub-agent in the foreground and wait for its report. If you are already a sub-agent, apply the brief below yourself instead.

**Standards sub-agent prompt** should include:

- The full diff command and commit list.
- The list of standards-source files you found in step 3, **plus the smell baseline from step 3** pasted in full (the sub-agent has no other access to it).
- The brief: "Report, per file/hunk where relevant, (a) every place the diff violates a documented standard: cite the standard (file + the rule). When the diff breaks one rule in several places, list each place, not only the first; (b) any baseline smell you spot: name it and quote the hunk; and (c) each commit message of the listed commits that breaks the commit rules of the repo (its `## Commit rules` section, else the defaults of the `idea-to-code:commit` skill): name the commit, quote its title and cite the rule. Report such a breach as a Past commit finding. Distinguish hard violations from judgement calls: documented-standard breaches can be hard, but baseline smells are always judgement calls, and a documented repo standard overrides the baseline. Skip anything tooling enforces. This review has one axis: breaches of the listed files, and baseline smells. Do not report whether the code matches a spec, or whether it adds behaviour the spec and tasks did not ask for. Another check does that. A breach of a rule in a listed file stays a finding. A step that the flow itself skips by its own rule is no breach: the check command does not run before a tests commit (a commit with a `Tests-For` trailer), so the line `Checks before a commit:` of the config is no standard that such a commit breaks. Under 400 words. Do not invoke the `idea-to-code:code-review` skill or start more agents: do this review yourself."

### 5. Report

Present the report under a `## Standards` heading, verbatim or lightly cleaned. Put the `Project rules:` line directly under that heading. End with a one-line summary: the number of findings and the worst one, if any. When verify called you, hand the report back to verify.
