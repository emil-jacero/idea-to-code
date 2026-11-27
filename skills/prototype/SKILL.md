---
name: prototype
description: Build a throwaway prototype or a small runnable check that settles a design question before the change is planned. Use when a design rests on an assumption that only running code can settle (how a language evaluates a construct, what a library or a tool does), when the user wants to sanity-check whether a state model or logic feels right, or to explore what a UI should look like.
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

It runs before the OpenSpec change exists, as its own step: when explore meets an open assumption, explore names it and pauses, this skill answers it, and explore resumes with the finding. It is never a slice of a change.

## Pick a branch

Identify which question is being answered, using the user's prompt, the surrounding code, or, when the owner is present, by one question in the form of the `idea-to-code:grilling` skill:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a single shareable HTML file (free-play buttons plus tabbed guided walkthroughs) that pushes the state machine through cases that are hard to reason about on paper, and that a non-developer can drive.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.
- **"Does this behave as we assume?"** (how a language evaluates a pattern, what a library or a service does, how a tool or an API answers). Build the smallest runnable check in the language that owns the behaviour: a file run by the tool under test, a small program, or a shell script, in the scratch folder of rule 1. Copy what it needs, and import nothing from a live repo. Beside it, write a `README.md` with four headings: Hypothesis (one sentence), Setup (what you copied, from which repo and commit), Run (the exact command), Outcome (the output that decides it, ending "Hypothesis held." or "Hypothesis refuted." and one sentence of evidence). Keep every file the Run command needs: the check stays runnable as evidence.

The branches produce very different artifacts, so getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the owner isn't present, default to whichever branch better matches the surrounding code (a claim about how a language, a library or a tool behaves → check; a state model → logic; a page → UI) and state the assumption at the top of the prototype.

## Rules that apply to every branch

1. **Throwaway from day one, clearly marked, never committed.** Every branch works in a scratch folder outside any repo, made with `mktemp -d` under `$TMPDIR` (else `/tmp`), and keeps its `README.md` there; report its full path. No file in the repo's own checkout is edited.
2. **Trivial to run.** A UI prototype starts from one command in the project's task runner: `pnpm <name>`, `python <path>`, `bun <path>`, etc. A logic demo is a single HTML file the user double-clicks. A check runs with the one command its `README.md` names. In every branch, no thinking required to start it.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE, wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Capture the answer, never fold the code.** Write the question, the verdict and its evidence (the command and its output, or what the owner saw and said) into the `README.md` in the scratch folder. When the change is proposed, its files move to `openspec/changes/<change>/evidence/<nn>-<name>/` (`<nn>` is the next free two-digit number in the change's `evidence/`), which holds the runnable files and a short note, `README.md` (for a UI prototype: the patch and the screenshots); the change's `design.md` points at the folder. The repo's build, lint and test commands must not load an evidence file, also after archive. Where the repo guide (`AGENTS.md`, else `CLAUDE.md`) states how a check stays out of them, follow that rule. Where it states none, give the check what its language needs to stand apart in that folder (its own module or package file, for example). Never fold prototype code into product code: the change's slice build writes the code and its tests from the spec. Never commit, push or write to an issue.

## Done

Done when the `README.md` in the scratch folder holds the question, the verdict and its evidence, and you have handed back the one-line answer and the folder path: to the paused explore, else to the user.
