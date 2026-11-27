---
name: slice-build
description: "Reference for the `idea-to-code:build` and `idea-to-code:verify` commands: the steps of a slice, its checks and the fix round after verify. The step commands load it. A request of the user for a build goes to `idea-to-code:build`."
---

# Slice Build

## Who does what

Go on to build only when the `/idea-to-code:build` command loaded this skill. The owner may have typed the command, or it may have loaded on a request in words, or on a yes in words after you named it. A fix round may also run when the fix round of the `/idea-to-code:verify` command loaded it, or when the owner's answer at the result gate of `idea-to-code:owner-gate` starts it. When the `/idea-to-code:propose` command loaded it for the form only, or the `/idea-to-code:verify` command loaded it for the test lock only, do that one job and build nothing. When a request in words loaded this skill directly, with no build command before it, do not build from here: load `idea-to-code:build` and follow its steps from the first one (it picks the change, applies the plan gate and checks the branch, then loads this skill again). Never load OpenSpec's `openspec-apply-change` skill for a build.

You, the session, orchestrate. You write no test and no code: each writer is a **fresh** sub-agent (the Agent tool) with a clean context, a test writer and then a code writer per slice (only a code writer in a repo without specs, see The input). Start each writer in the foreground, and wait for its report before the next step. Slices run one at a time, in order (a fix slice added during the build runs next), never in parallel. The build command started the build, so you make all its commits; you push nothing and open no pull request. A slice closes with its code commit. Before it come its tests commits: one, and one more for each test correction (When a step fails). A repo without specs has none.

## The input

The change folder, `openspec/changes/<change>/`:

- `design.md` has a `## Slices` section with one block `### S<n>: <name>` per slice, each with the fields Delivers, Seam, Depends on and Done when.
- `tasks.md` has one `## <n>.` section per slice: S<n> is the section `## <n>.`.

A small change is exempt: with no `design.md`, or a `design.md` with no `## Slices` section, each `## <n>.` section of `tasks.md` is a slice, built in order, and each depends on the section before it. Its sections have no Done when line, except a fix slice's section, which carries all four fields and depends only on the slice its Depends on line names (When a step fails). A section may hold a `Seam:` line directly under its heading: the seam that the owner agreed, which propose wrote there. A section without that line has no Seam.

The repo names the commands of the build: the test command (the command after `Tests:` in the `context:` of `openspec/config.yaml`), the check command (the command after `Checks before a commit:` in the `context:` of `openspec/config.yaml`), and the repo's test-file patterns (after `Test files:` in the `context:` of `openspec/config.yaml`, else the patterns of the repo's language and test runner). When the config does not name a command this build runs, then before the first slice put it to the owner as one question in the form of the `idea-to-code:grilling` skill, with the command you found in the repo's build files as the recommended option. The `idea-to-code:commit` skill runs the check command before every commit that is not a tests commit. Do not run it a second time yourself. A repo with no `Checks before a commit:` line has no check command: ask nothing for it, except in a repo without specs. Fill the placeholders of both briefs with the repo root, the test command and the test-file patterns. For the code-writer brief, also find the repo's glossary (`GLOSSARY.md`, or the glossary file the repo guide names) and the repo's ADR folder, the `ADR folder:` of the repo's `## Decision records` (the `idea-to-code:domain-modeling` skill says where the section sits; default: `adr/` where it exists). The repo guide is `AGENTS.md`, else `CLAUDE.md`.

A repo without specs builds without the test steps. When the schema named in `openspec/config.yaml` has no `specs` artifact, read [NO-SPECS.md](NO-SPECS.md) before the first slice: it says which steps fall away and what takes their place.

## Before the first slice

1. First resolve the repo the work is about, and run every git and file command from its root. In a lone clone, that is the current repo.
2. Run `git status`. When the tree holds a change unrelated to this build, put it to the owner as one question in the form of the `idea-to-code:grilling` skill. An uncommitted change folder is part of this build, and its first commit carries it, with no question ((d)). An uncommitted glossary, ADR or decision-record file written for this change in explore is part of this build too: put it to the owner the same way, in one question, asking whether the build's first commit carries it.
3. Commit only on the working branch: the branch the run started on, never the default branch. Find the default branch as [CHECKS.md](CHECKS.md), Default branch, gives it, once, and run the lines of Fresh base in the same shell call, and act on the result as that section says. Keep the name in your notes: it is `<default branch>` in every text of this skill, and the build report names it. When the run started on the default branch, create or switch to a branch named after the change before the first commit, unless the repo's apply guidance in `openspec/config.yaml` names another form.
4. Read that apply guidance. When it contradicts these steps (for example "Section 1 is a spike" or "one commit per section"), put the clash to the owner as one question in the form of the `idea-to-code:grilling` skill, naming it, before the first slice.
5. Load the `idea-to-code:owner-gate` skill and run its build check. A `gates.json` that this check writes goes into the first commit that this build makes, with no question ((d)).
6. Read the tests commits of the working branch, with the command of [CHECKS.md](CHECKS.md), Resume. Act as that section says: build from (a), resume one slice at (e), or stop.

Done when you work from the repo root on the working branch, the tree holds no unrelated change, every question above has the owner's answer, the plan gate has an outcome, and the read of step 6 says where the build starts.

## Per slice

Start (a) of the first slice only when Before the first slice is done. Run steps (a) to (g) for each slice, in order. A step starts only when the step before it is done.

Skip a slice whose `tasks.md` boxes are all ticked: it is built.

Run each check on its own. Run the test command, the test-lock check (f) and the check command alone, one shell call each, and read the exit status of each before you go on. Only then, in a separate shell call, tick the boxes and run `git commit`. Never chain a check and a commit in one call (`<check> && echo ok; git commit ...`, `<check>; git commit ...` or `set -e; ...; git commit ...`): the commit could run after a failed check.


### (a) Gate

When the config names the slice check script (the command after `Slice check:` in the `context:` of `openspec/config.yaml`), run it as its `--help` says; a non-zero exit stops the build. Otherwise check by hand ([CHECKS.md](CHECKS.md), Gate). While any task box in the `tasks.md` section of a slice it depends on (The input) is unticked, stop with a message in this form: "S2 is blocked by S1".

Done when every dependency's boxes are ticked.

### (b) Test writer

Start a fresh sub-agent with the test-writer brief in [BRIEFS.md](BRIEFS.md).

Done when its report maps each scenario the slice delivers, and the Done when line where the slice has one, to at least one test, and lists the test files, any stubs and its assumptions.

### (c) Red check

When the config names the test check script (the command after `Test check:` in the `context:` of `openspec/config.yaml`), run it as its `--help` says; otherwise check by hand ([CHECKS.md](CHECKS.md), Red check). Before any code for the slice exists, every new test must be **red** for the right reason: it fails on the behaviour its scenario names. A test that passes, or fails on a build error, a syntax error or a missing import, fails the check. A guard test is the one exception ([CHECKS.md](CHECKS.md), Red check): a test that the test writer's report marks as a guard of a behaviour that stays. It passes the check, with no question to the owner.

Done when every new test is red for the right reason or is a guard test, and at least one new test is red. In a tests-only slice ([CHECKS.md](CHECKS.md), Red check), done when every new test is a guard test that passed the break check.

### (d) Tests commit

Load the `idea-to-code:commit` skill. Commit only the test files, the stubs and the change-folder files named here. The first commit that this build makes carries every file of the change folder that is not committed yet, `gates.json` included. On a resume, that is the next commit that this build makes. The build makes no commit that holds only `gates.json`. The same commit carries a glossary, ADR or decision-record file from explore only when the owner chose that in Before the first slice. A fix slice's tests commit also carries its new `design.md` block and `tasks.md` section.

The title of a tests commit has the `Tests commit:` title form of the repo's `## Commit rules` (the `idea-to-code:commit` skill says where the section sits; default: `test(<scope>): <what the tests cover>`). The message of every tests commit ends with a trailer block: one empty line, then the line `Tests-For: <slice name>`. Any other trailer line follows it with no empty line between them, and the attribution line stays last. The slice name is `S<n>` and nothing more, where `<n>` is the number of the slice's section `## <n>.` in `tasks.md`. A fix slice uses the number of its own section. In the fix round after verify, the value is the word `verify`. Every tests commit of one slice carries the same value: the first one, and each correction. A commit whose message carries a `Tests-For` trailer is a tests commit, and a commit without one is not. The title decides nothing.

The message has a title in the `Tests commit:` title form and the trailer `Tests-For: <slice name>`. An example, for slice S1:

```text
test(upload): cover the empty file name refusal

Tests-For: S1
<the attribution line, where the repo has one>
```

Make the tests commit with plain git, and write no message file: `git commit -m "<title>" --trailer "Tests-For: <slice name>"`. Where the repo has an attribution line, add `--trailer "<the attribution line>"` as the last option. Git writes the trailer block itself, in the order of the options. The option needs git 2.32 or newer. Stop before the commit, with one question to the owner in the form of the `idea-to-code:grilling` skill, in two cases: git refuses `--trailer`, or the attribution line does not have the form `<key>: <value>`.

After the commit, read the trailer block as git reads it: `git log -1 --format='%(trailers)'`. Its first line must be `Tests-For: <slice name>`, and its last line must be the attribution line where the repo has one. When it is not so, stop and make no further commit. Put it to the owner as one question in the form of the `idea-to-code:grilling` skill. The question offers two options: a new tests commit with the right trailer block (recommended), or a stop. For the new commit, remove the cause first, then run the same command with `--allow-empty`. The wrong commit stays, because the flow never amends. When the trailer read of the wrong commit does not give `Tests-For` the value `<slice name>` alone, the background of the question says that the test lock at verify will report the wrong commit, and that only the owner's answer at verify clears it. Check the new commit the same way, and stop when it fails too. Keep the commit hash in your own notes, never in a file a sub-agent writes.

Done when the commit exists, its trailer block passed that check, and no test file is left uncommitted.

### (e) Code writer

Start a fresh sub-agent with the code-writer brief in [BRIEFS.md](BRIEFS.md). It writes code until the slice's tests pass, and leaves every test file as committed. A tests-only slice skips (e) and (f) when each task of its section is done by its tests commit: its code commit (g) then holds `tasks.md` alone.

Done when its report says the tests pass, says where each task of the slice's section is done, and lists what changed and its assumptions.

### (f) Test-lock check

When the config names the test check script, run it as its `--help` says; otherwise check by hand ([CHECKS.md](CHECKS.md), Test lock). Compare every test file with the slice's newest tests commit: a test file changed, added, deleted or renamed since that commit, committed or not, fails the check. The slice's newest tests commit is the newest commit on the working branch whose `Tests-For` trailer carries the slice name. Your notes hold its hash, and [CHECKS.md](CHECKS.md), Test lock, gives the command that finds it again.

Done when no test file differs.

### (g) Code commit

Run the repo's full test command; it passes. A base failure that the owner answered with Keep it out does not count (When a step fails). Tick every box of the slice's `tasks.md` section. Load the `idea-to-code:commit` skill and commit the code and `tasks.md`. That skill runs the check command before the commit. Do not run it yourself. When this is the first commit that this build makes (a resume at (e)), it also carries the files that (d) names for that commit. This commit closes the slice.

Done when the commit exists and no file this slice changed is left uncommitted. Then go to the next slice.

## When a step fails

The default for each failure is in [FAILURES.md](FAILURES.md). Read that file before your next action in each of these cases:

- the red check, the test-lock check, the full test command or the check command fails;
- the tests of a slice fail after the code writer;
- a report of a test writer leaves a scenario or the Done when line without a test;
- a report of a code writer lists a bug under Bugs fixed or under Bugs left, or reports disputed tests.

Then act as the point for that case says.

## Owner decisions in a build

Apart from a disputed test (When a step fails), a writer stops and hands back only for a decision of the five owner kinds ([BRIEFS.md](BRIEFS.md), Rules for both writers). You then put that one question to the owner in the form of the `idea-to-code:grilling` skill, and a fresh sub-agent of the same role continues with the answer. A writer never asks the owner anything itself: it decides every other open choice and lists it as an assumption in its report. Collect all assumptions for the final report.

## After the last slice

Report to the owner:

- the default branch of the build, as the line `Base: <branch>`;
- each slice with its commits (hash and title);
- every assumption the writers listed, with the question it answered;
- every bug fixed, every fix slice and every lead;
- every disputed test, with its ruling (by the spec or by the owner) and its correction commit, if any;
- every guard test, with the scenario that it guards;
- every base failure, with the owner's answer;
- every check that failed (red check, test lock, test command, check command), with its slice, its round and what was restored or retried;
- every stop of the build, with its cause and the owner's answer. A resume counts as a stop: name the slice and the step that this run resumed at, take the earlier slices and their commits from git, and say that this report does not hold the assumptions, bugs and failed checks of the earlier run;
- the `Project rules:` line that the `idea-to-code:commit` skill gave, once for the build;
- the `Check command:` line that the `idea-to-code:commit` skill gave at the code commits, once for the build.

Write the same report to `build-report.md` in the change folder, and commit that file alone, after the last code commit. Put the record line of each answer Keep it out on a base failure under the heading `### Answers` at the end of the report, in the form that [CHECKS.md](CHECKS.md) gives under Answers in the build report. The path is `openspec/changes/<change>/build-report.md`. Load the `idea-to-code:commit` skill for that commit. The report gets a commit of its own because it names every commit of the build, and a commit cannot hold its own hash. When the check command fails at that commit, change no code and untick no box: the `idea-to-code:commit` skill has taken the file out of the index, and the file stays in the change folder. Put the failure to the owner as one question in the form of the `idea-to-code:grilling` skill, with the output of the check command. The question offers two options: correct the report so that the check command passes, and commit it again (recommended), or stop.

A run that ends at a stop before the last slice is closed writes no `build-report.md` and makes no commit for it: give the owner the report items so far in the chat. The run that resumes the build writes the file, and counts the resume as a stop.

The next step is verify: name `/idea-to-code:verify <change>`, and tell the owner to run it in a fresh session. Do not start verify in this session, so that verify reads the work without the context that wrote it. That command holds every step of verify, and it applies the result gate, which reads `build-report.md`.

Done when the report is shown and `build-report.md` is committed.

## After verify

When verify reports findings, the session that ran verify loads this skill for one fix round. Read [FIX-ROUND.md](FIX-ROUND.md), and run the round as that file says. Only a fix round reads that file.
