---
name: slice-build
description: "Build an OpenSpec change slice by slice, tests first, each slice by fresh sub-agents, then run its one fix round after verify. Use when the `/idea-to-code:build` command builds a change (typed by the owner, or loaded on a request in words), or when verify reported findings on a change. Never load this skill directly on a request in words to build, apply or implement a change, or to work through its tasks: load `idea-to-code:build` first, and it loads this skill. A yes in words after you named the build command is such a request."
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

A repo without specs builds without the test steps. When the schema named in `openspec/config.yaml` has no `specs` artifact, skip (b), (c), (d) and (f) for every slice. In (e), one fresh code writer builds the slice with the code-writer brief in its form for a repo without specs ([BRIEFS.md](BRIEFS.md)), which also says which bugs it fixes; (e) is done when its report also says how it showed each Done when line holds. In the code-writer brief, the test command is the check command. In (g) and in step 5 of After verify, run no command yourself: the `idea-to-code:commit` skill runs the check command before the commit, and a failure there counts as a failed test command. When the config holds no `Checks before a commit:` line, the command that the owner named is the check command of this build and of its fix round: give it to the `idea-to-code:commit` skill at each commit. The one commit of (g) closes the slice; it also carries the files that (d) would add to a tests commit, and never the `Tests-For` trailer. A repo without specs has no tests commit, so no commit of its build carries the trailer.

## Before the first slice

1. First resolve the repo the work is about, and run every git and file command from its root. In a lone clone, that is the current repo.
2. Run `git status`. When the tree holds a change unrelated to this build, put it to the owner as one question in the form of the `idea-to-code:grilling` skill. An uncommitted change folder is part of this build, and its first commit carries it, with no question ((d)). An uncommitted glossary, ADR or decision-record file written for this change in explore is part of this build too: put it to the owner the same way, in one question, asking whether the build's first commit carries it.
3. Commit only on the working branch: the branch the run started on, never the default branch. Find the default branch as [CHECKS.md](CHECKS.md), Default branch, gives it, once, and keep the name in your notes: it is `<default branch>` in every text of this skill, and the build report names it. When the run started on the default branch, create or switch to a branch named after the change before the first commit, unless the repo's apply guidance in `openspec/config.yaml` names another form.
4. Read that apply guidance. When it contradicts these steps (for example "Section 1 is a spike" or "one commit per section"), put the clash to the owner as one question in the form of the `idea-to-code:grilling` skill, naming it, before the first slice.
5. Load the `idea-to-code:owner-gate` skill and run its build check. A `gates.json` that this check writes goes into the first commit that this build makes, with no question ((d)).

Done when you work from the repo root on the working branch, the tree holds no unrelated change, every question above has the owner's answer, and the plan gate has an outcome.

## Per slice

Start (a) of the first slice only when Before the first slice is done. Run steps (a) to (g) for each slice, in order. A step starts only when the step before it is done.

Skip a slice whose `tasks.md` boxes are all ticked: it is built.

Run each check on its own. Run the test command, the test-lock check (f) and the check command alone, one shell call each, and read the exit status of each before you go on. Only then, in a separate shell call, tick the boxes and run `git commit`. Never chain a check and a commit in one call (`<check> && echo ok; git commit ...`, `<check>; git commit ...` or `set -e; ...; git commit ...`): the commit could run after a failed check.

The title of a tests commit has the `Tests commit:` title form of the repo's `## Commit rules` (the `idea-to-code:commit` skill says where the section sits; default: `test(<scope>): <what the tests cover>`). The message of every tests commit ends with a trailer block: one empty line, then the line `Tests-For: <slice name>`. Any other trailer line follows it with no empty line between them, and the attribution line stays last. The slice name is `S<n>` and nothing more, where `<n>` is the number of the slice's section `## <n>.` in `tasks.md`. A fix slice uses the number of its own section. In the fix round after verify, the value is the word `verify`. Every tests commit of one slice carries the same value: the first one, and each correction. A commit whose message carries a `Tests-For` trailer is a tests commit, and a commit without one is not. The title decides nothing.

A build can resume an earlier build. So before the first slice, whether you build it or skip it, read only the commits that are on the working branch and not on the default branch, with git's trailer format and never with a search of the message text:

```bash
git log --format='%h %(trailers:key=Tests-For,valueonly,separator=%x2C)' <default branch>..HEAD
```

Each line is one commit, newest first: its hash and its trailer value, or the hash alone for a commit that is not a tests commit. The tests commits that the working branch ends in are the lines above the first line with a hash alone. When the working branch ends in one or more tests commits, their trailer value names the slice that resumes at (e). The newest of them is the slice's newest tests commit. The test paths are the files that match the repo's test-file patterns in every tests commit of that slice: every commit on the working branch whose `Tests-For` value is the slice name (a stub is not a test file). Build that slice first, from (e), then go on with the other slices in order.

When the tests commits that the working branch ends in carry different values, or their value is not the name of a slice of `tasks.md` whose boxes are not all ticked, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. The value `verify` names no slice, so it stops the build the same way: the findings of the fix round are not in the repo. A tests commit can also stand lower on the working branch, below a commit without the trailer (a merge of the default branch, or a commit made by hand). When such a tests commit names a slice whose boxes are not all ticked, and that slice is not the one the branch ends in, stop and put it to the owner the same way. A start at (a) would run a second test writer over red tests that are already committed.

### (a) Gate

When the config names the slice check script (the command after `Slice check:` in the `context:` of `openspec/config.yaml`), run it as its `--help` says; a non-zero exit stops the build. Otherwise check by hand ([CHECKS.md](CHECKS.md), Gate). While any task box in the `tasks.md` section of a slice it depends on (The input) is unticked, stop with a message in this form: "S2 is blocked by S1".

Done when every dependency's boxes are ticked.

### (b) Test writer

Start a fresh sub-agent with the test-writer brief in [BRIEFS.md](BRIEFS.md).

Done when its report maps each scenario the slice delivers, and the Done when line where the slice has one, to at least one test, and lists the test files, any stubs and its assumptions.

### (c) Red check

When the config names the test check script (the command after `Test check:` in the `context:` of `openspec/config.yaml`), run it as its `--help` says; otherwise check by hand ([CHECKS.md](CHECKS.md), Red check). Before any code for the slice exists, every new test must be **red** for the right reason: it fails on the behaviour its scenario names. A test that passes, or fails on a build error, a syntax error or a missing import, fails the check.

Done when every new test is red for the right reason.

### (d) Tests commit

Load the `idea-to-code:commit` skill. Commit only the test files, the stubs and the change-folder files named here. The first commit that this build makes carries every file of the change folder that is not committed yet, `gates.json` included. On a resume, that is the next commit that this build makes. The build makes no commit that holds only `gates.json`. The same commit carries a glossary, ADR or decision-record file from explore only when the owner chose that in Before the first slice. A fix slice's tests commit also carries its new `design.md` block and `tasks.md` section.

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

Start a fresh sub-agent with the code-writer brief in [BRIEFS.md](BRIEFS.md). It writes code until the slice's tests pass, and leaves every test file as committed.

Done when its report says the tests pass, says where each task of the slice's section is done, and lists what changed and its assumptions.

### (f) Test-lock check

When the config names the test check script, run it as its `--help` says; otherwise check by hand ([CHECKS.md](CHECKS.md), Test lock). Compare every test file with the slice's newest tests commit: a test file changed, added, deleted or renamed since that commit, committed or not, fails the check. The slice's newest tests commit is the newest commit on the working branch whose `Tests-For` trailer carries the slice name. Your notes hold its hash, and [CHECKS.md](CHECKS.md), Test lock, gives the command that finds it again.

Done when no test file differs.

### (g) Code commit

Run the repo's full test command; it passes. Tick every box of the slice's `tasks.md` section. Load the `idea-to-code:commit` skill and commit the code and `tasks.md`. That skill runs the check command before the commit. Do not run it yourself. When this is the first commit that this build makes (a resume at (e)), it also carries the files that (d) names for that commit. This commit closes the slice.

Done when the commit exists and no file this slice changed is left uncommitted. Then go to the next slice.

## When a step fails

These defaults hold until the owner sets others. When a default below says stop, put it to the owner as one question in the form of the `idea-to-code:grilling` skill, with the evidence.

- **Red check fails:** start a fresh test writer with the evidence (each failing test and its output), at most three fresh test writers after the first. When the third still fails the check, stop. A test-writer report that leaves a scenario or the Done when line without a test fails the check too, with each item left without a test as the evidence.
- **Test-lock check fails:** restore the test files from the newest tests commit. A tests commit can delete a test file, so the commit does not hold every test path, and `git checkout` fails as a whole on a path that its commit does not hold. So `git ls-tree -r --name-only <tests-commit> -- <paths>` lists the test paths that the commit holds: restore those with `git checkout <tests-commit> -- <those paths>`, and remove each test file that the commit does not hold (one added after it, or a deleted one that came back). When the list is empty, run no checkout: with no path, that command leaves the working branch. Then start one fresh code writer with the finding. A second failure stops the build.
- **The slice's tests fail after the code writer, or the full test command or the check command fails at the code commit:** when the check command failed, first untick the boxes that (g), or step 5 of After verify, ticked. Then start one fresh code writer with the output, and after a failed check command also with that command. A second failure stops the build. When the check command failed again, untick those boxes again before you stop.
- **A code writer lists a bug under Bugs fixed:** the slice goes on; carry it into the final report.
- **A code writer lists a bug under Bugs left:** when it is in code an earlier slice of this change committed, add a fix slice after this slice's code commit, at the next free number, with the fields Delivers: the corrected behaviour; Seam: the reported seam; Depends on: the slice with the bug; Done when: the minimised repro from the Bugs left line, written out in full, passes. Write them as a `design.md` block beside a new `tasks.md` section, or in a small change as the first lines of the new `tasks.md` section, and give that section one task box for the fix. Build it next with steps (a) to (g). In code from before the change, list it in the final report as a lead; put it to the owner as a scope question only when the slice cannot be done without the fix.
- **A code writer reports disputed tests** (committed tests it believes are wrong): in a repo without specs there is no spec to rule by, so put each to the owner as one question in the form of the `idea-to-code:grilling` skill, with the evidence; the answers say how the slice goes on. Otherwise, set the code writer's unfinished work aside: restore the test files from the newest tests commit, as for a failed test-lock check, then stash every other file it changed or added (`git stash push --include-untracked -m "set aside: <slice name>" -- <paths>`). When it changed or added no other file, run no stash, and later run no `git stash pop`. With nothing to save, git makes no entry, and a pop then brings back an older stash, such as one of the owner. After a stash, check that `git stash list` shows your entry. Start a fresh test writer with the dispute-round inputs of its brief: it has never seen the code, and it rules on each disputed test from the spec. Then follow the ruling for each test:
  - **The spec backs the code writer:** the test writer corrects the test.
  - **The spec backs the test:** the test stays as committed.
  - **The spec is silent or unclear, or the test is disputed a second time:** put it to the owner as one question in the form of the `idea-to-code:grilling` skill, with the test, the spec text and the evidence of both writers. The owner's answer takes the place of the ruling. When it asks for a correction, a fresh test writer makes it, with the hand-back inputs of its brief.

  When any test was corrected, run the red check (c) on the corrected tests while the set-aside work stays stashed, so no code for the slice exists. Load the `idea-to-code:commit` skill and commit the corrections as one further tests commit, in the `Tests commit:` title form, with the slice's `Tests-For` trailer, by the command and the check of (d); keep its hash in your notes as the slice's newest tests commit. To go on, bring the set-aside work back, only when you made that stash: find your entry in `git stash list` and pop it by its index (`git stash pop stash@{<n>}`). Then run (e) again with a fresh code writer and the rulings.

## Owner decisions in a build

Apart from a disputed test (When a step fails), a writer stops and hands back only for a decision of the five owner kinds ([BRIEFS.md](BRIEFS.md), Rules for both writers). You then put that one question to the owner in the form of the `idea-to-code:grilling` skill, and a fresh sub-agent of the same role continues with the answer. A writer never asks the owner anything itself: it decides every other open choice and lists it as an assumption in its report. Collect all assumptions for the final report.

## After the last slice

Report to the owner:

- the default branch of the build, as the line `Base: <branch>`;
- each slice with its commits (hash and title);
- every assumption the writers listed, with the question it answered;
- every bug fixed, every fix slice and every lead;
- every disputed test, with its ruling (by the spec or by the owner) and its correction commit, if any;
- every check that failed (red check, test lock, test command, check command), with its slice, its round and what was restored or retried;
- every stop of the build, with its cause and the owner's answer. A resume counts as a stop: name the slice and the step that this run resumed at, take the earlier slices and their commits from git, and say that this report does not hold the assumptions, bugs and failed checks of the earlier run;
- the `Project rules:` line that the `idea-to-code:commit` skill gave, once for the build;
- the `Check command:` line that the `idea-to-code:commit` skill gave at the code commits, once for the build.

Write the same report to `build-report.md` in the change folder, and commit that file alone, after the last code commit. The path is `openspec/changes/<change>/build-report.md`. Load the `idea-to-code:commit` skill for that commit. The report gets a commit of its own because it names every commit of the build, and a commit cannot hold its own hash. When the check command fails at that commit, change no code and untick no box: the `idea-to-code:commit` skill has taken the file out of the index, and the file stays in the change folder. Put the failure to the owner as one question in the form of the `idea-to-code:grilling` skill, with the output of the check command. The question offers two options: correct the report so that the check command passes, and commit it again (recommended), or stop.

A run that ends at a stop before the last slice is closed writes no `build-report.md` and makes no commit for it: give the owner the report items so far in the chat. The run that resumes the build writes the file, and counts the resume as a stop.

The next step is verify: name `/idea-to-code:verify <change>`, and tell the owner to run it in a fresh session. Do not start verify in this session, so that verify reads the work without the context that wrote it. That command holds every step of verify, and it applies the result gate, which reads `build-report.md`.

Done when the report is shown and `build-report.md` is committed.

## After verify

When verify reports findings, the session that ran verify loads this skill for one fix round. You orchestrate it as you do a slice: fresh writers do the work, you make the commits, and When a step fails applies, except for Bugs left: in this round every bug on that line goes to the owner (below), never to a fix slice.

`<default branch>` in this round is the `Base:` branch of the verify report that started it. First read the trailers as Per slice says. When the working branch ends in a tests commit with the value `verify`, an earlier fix round stopped after its tests commit: put it to the owner as one question in the form of the `idea-to-code:grilling` skill, before you sort a finding.

1. Sort every finding into one route:
   - **Fix:** it cites something written: an unticked task, a requirement or scenario not met, a behaviour nobody asked for, or a breach of a written repo standard. A failure of the test command or of the check command at verify is a Fix finding.
   - **Test first:** a Fix finding that needs a test changed or added before the code.
   - **Owner:** it needs a spec change, or it is unasked behaviour you judge worth keeping. Put each to the owner as one question in the form of the `idea-to-code:grilling` skill before the code writer starts; an answer that asks for a fix moves the finding to Fix. An answer that keeps unasked behaviour: write the behaviour into the change's delta spec (in a repo without specs, into `design.md`), so the second verify finds it asked for, and close the finding. An answer that changes the spec: write the change the same way, then route the finding to Test first (to Fix in a repo without specs). The round's first commit (step 2, else step 5) carries each spec edit. A test-lock finding of verify is an Owner finding, and no route of this round removes its commit: it stays on the working branch, because the flow never amends. Only the owner's answer clears it. Put one question per offending commit to the owner, as [CHECKS.md](CHECKS.md) says under Test lock at verify, and write each answer as a record line in `build-report.md` (step 6), with the kind `lock`. The answer to keep the edit closes the finding. The answer to restore the test needs no writer: you bring back each test file of the commit, one path at a time: `git checkout <hash>^ -- <path>` for an M or D line and for the first path of an R line, and `git rm <path>` for an A line and for the second path of an R line. First run `git log --format=%h <hash>..HEAD -- <paths>`. When it prints a line, a later commit changed one of those files, and the checkout would undo that change too: restore nothing, and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. Otherwise commit the restored files as a tests commit with `Tests-For: verify`, by the command of (d), with no red check. Then run the test command. When a restored test fails, it goes to step 3 as a Fix finding, and steps 3 to 5 run. An uncommitted test-file change is never answered away: put it to the owner as one question: you commit it as a tests commit with `Tests-For: verify`, by the command of (d), or the owner removes it. Discard nothing yourself, and start no code writer while it is in the tree: a failed check (f) would remove it. The round's report names each commit, the answer and the record.
   - **Past commit:** it is about a commit already made, and no code can fix it, because the flow never amends: the commit message breaks a commit rule of the repo (verify finds it, see its step 5). Put one question per commit to the owner, in the form of the `idea-to-code:grilling` skill, before the code writer starts: the finding, the commit (hash and title), and two options. **Keep it as it is** (the commit stays). **Stop** (the finding stays open and the round writes no record for it). No option offers a fix, because the flow never amends. The question is still asked: the session never records Keep by its own choice. Recommend one option, and give the basis. With findings on several commits, ask one question after the other, never in one message. The answer to keep closes the finding. Write each answer as a record line in `build-report.md` (step 6), in the form that [CHECKS.md](CHECKS.md) gives under Answers in the build report. Write it only for the owner's answer to this question, never before it and never in its place. A later verify lists that commit as answered, and it is no finding.
   - **Lead:** a smell with no cited rule. It is a lead for the owner, not a fix: list it in the report.

   When no finding is routed to Fix or Test first, skip steps 2 to 4. In step 5, commit only the spec edits of the Owner answers, and skip the step when there are none.
2. For the Test first findings, start one fresh test writer with them ([BRIEFS.md](BRIEFS.md)). Run the red check (c) on its tests by hand ([CHECKS.md](CHECKS.md), Red check) and commit them as in (d), with the trailer `Tests-For: verify`.
3. Start one fresh code writer with every Fix and Test first finding ([BRIEFS.md](BRIEFS.md)). The test files are locked at the commit it starts from.
4. Run the test-file check (f) against that commit, by hand ([CHECKS.md](CHECKS.md), Test lock). The test check script does not run in this round: it compares the tests with one slice's tests commit.
5. Run the repo's full test command; it passes. Tick each task box the fix completes. Load the `idea-to-code:commit` skill and commit the fix.
6. Append the round's report (below) to `build-report.md` in the change folder, under the heading `## Fix round`. Create the file when it is missing. Put each record line of an owner's answer on an offending commit or on a past commit under `### Answers` in that section, in the form that [CHECKS.md](CHECKS.md) gives. Write the record line even when the round has no other finding, and only for the owner's answer to that question: never before it, and never in its place. Commit that file alone, as After the last slice says for the build report, a failed check command included. Then run verify once more, as the `/idea-to-code:verify` command says: steps 3 to 7, and write that pass's report as text (its `Verify rules:` line and its `Base:` line first) before the result gate.

In a repo without specs, skip steps 2 and 4, and put a finding that needs a test change to the owner.

One round per verify run, apart from a round that the owner's answer at the result gate starts (`idea-to-code:owner-gate`). A later verify run starts a round of its own, which appends its own `## Fix round` section to `build-report.md`; the records of every section count. A finding that the owner answered with Stop has no record, so it is asked again. A finding still open after it goes to the owner as one question in the form of the `idea-to-code:grilling` skill, and so does a bug the code writer listed under Bugs left. A finding still open means verify has not passed.

Report to the owner: each finding with its route and outcome, each offending commit and each past commit with the owner's answer, the round's commits, every question put to the owner, every lead, and the `Project rules:` line and the `Check command:` line that the `idea-to-code:commit` skill gave at the commit of step 5.

Done when the second verify passes, or every finding still open is with the owner.
