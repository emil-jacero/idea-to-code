# Checks by hand

A repo can name two check scripts in its config: the slice check script (the command after `Slice check:` in the `context:` of `openspec/config.yaml`) for the gate, and the test check script (the command after `Test check:` in the `context:` of `openspec/config.yaml`) for the red check and the test lock. It also holds the fresh-base check that explore, propose and the build run first. This file holds the same checks, done by hand, for a repo without them, and for the fix round after verify, which runs them by hand in every repo. It also holds the test lock at verify, which verify runs by hand in every repo with specs, the check for a failure that the default branch has too, the check for a failure of the checkout, the rule that the commands run as written, and the form of the owner's answers in `build-report.md`.

## Default branch

`<default branch>` in these texts is the branch that this rule finds. It is the remote's default branch (`git symbolic-ref --short refs/remotes/origin/HEAD` prints it as `origin/<name>`). The lines cut `origin/` off when a local branch of that name exists, and they keep `origin/<name>` when only the remote branch exists (a local branch that was renamed or deleted). A clone made with `--single-branch --branch <name>` has no `origin/HEAD`; there the lines fall back to `main`, `master` or the owner's answer. Else the default branch is `main` when that branch exists, else `master` when that branch exists. The lines test `refs/heads/main` and `refs/heads/master`, so a tag of that name does not count. The owner is asked only when none exists. The rule asks nothing else, and the session never takes a name without testing that it resolves. Run the lines in one shell call, from the repo root:

```sh
B=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null)
[ -n "$B" ] && git rev-parse --verify --quiet "refs/heads/${B#origin/}" >/dev/null && B=${B#origin/}
[ -n "$B" ] && { git rev-parse --verify --quiet "$B^{commit}" >/dev/null || B=; }
[ -n "$B" ] || { git rev-parse --verify --quiet refs/heads/main >/dev/null && B=main; }
[ -n "$B" ] || { git rev-parse --verify --quiet refs/heads/master >/dev/null && B=master; }
[ -n "$B" ] && echo "Base: $B" || echo 'NO DEFAULT BRANCH: ask the owner'
```

The last line prints `Base: <branch>`, or `NO DEFAULT BRANCH: ask the owner`. In that case put one question to the owner, in the form of the `idea-to-code:grilling` skill, that asks for the name of the branch the work is compared against, with the branches that `git branch --list` shows as the options. The build names the result in `build-report.md`, and verify names it in its report, each on a line `Base: <branch>`. The fix round uses the branch that the verify report names. In a repo with no remote the lines find a local `main` or `master`. A `main` that is the working branch itself leaves nothing to compare: the check below ends with `SETUP FAILED`.

## Fresh base

Explore, propose and the build read the repo's rules, config and specs from the checkout. A checkout that misses commits of the remote's default branch gives them old rules. Run these lines once, after the lines of Default branch, in the same shell call, so that `B` is set:

```sh
git fetch -q origin 2>/dev/null || echo 'NO FETCH: the remote was not read'
case "$B" in origin/*) R=$B ;; *) R=origin/$B ;; esac
if git rev-parse --verify --quiet "$R^{commit}" >/dev/null; then
  n=$(git rev-list --count "HEAD..$R")
  if [ "$n" = 0 ]; then echo 'FRESH'
  elif [ "$(git branch --show-current)" = "${B#origin/}" ] && [ -z "$(git status --porcelain --untracked-files=no)" ] && git merge --ff-only -q "$R" 2>/dev/null; then echo "UPDATED: $n commits"
  else echo "BEHIND: $n commits of $R are missing"; fi
else echo 'NO REMOTE BASE'; fi
```

- `FRESH` or `NO REMOTE BASE`: go on.
- `UPDATED: <n> commits`: the checkout was on the default branch with no local change, and it moved forward to the remote. Name the line in your first answer, and go on.
- `NO FETCH`: name it in your first answer, and go on with what the checkout holds.
- `BEHIND: <n> commits`: on the default branch, the checkout holds a local change or a local commit, so it cannot move forward. Stop, and ask the owner to bring it up to date. On another branch, name the line in your first answer, and go on: the rules and specs you read may be older than the remote's.

## Resume

A build can resume an earlier build. So before the first slice, whether you build it or skip it, read only the commits that are on the working branch and not on the default branch, with git's trailer format and never with a search of the message text:

```bash
git log --format='%h %(trailers:key=Tests-For,valueonly,separator=%x2C)' <default branch>..HEAD
```

Each line is one commit, newest first: its hash and its trailer value, or the hash alone for a commit that is not a tests commit. The tests commits that the working branch ends in are the lines above the first line with a hash alone. When the working branch ends in one or more tests commits, their trailer value names the slice that resumes at (e). The newest of them is the slice's newest tests commit. The test paths are the files that match the repo's test-file patterns in every tests commit of that slice: every commit on the working branch whose `Tests-For` value is the slice name (a stub is not a test file). Build that slice first, from (e), then go on with the other slices in order.

When the tests commits that the working branch ends in carry different values, or their value is not the name of a slice of `tasks.md` whose boxes are not all ticked, stop and put it to the owner as one question in the form of the `idea-to-code:grilling` skill. The value `verify` names no slice, so it stops the build the same way: the findings of the fix round are not in the repo. A tests commit can also stand lower on the working branch, below a commit without the trailer (a merge of the default branch, or a commit made by hand). When such a tests commit names a slice whose boxes are not all ticked, and that slice is not the one the branch ends in, stop and put it to the owner the same way. A start at (a) would run a second test writer over red tests that are already committed.

## Gate

1. In `design.md`, find the block `### S<n>:` and read its Depends on line: "none", or slice names such as "S1, S2".
2. For each S<m> named there, read `tasks.md` from `## <m>.` to the next `## ` heading. Any line with `- [ ]` there means S<n> is blocked: stop with "S<n> is blocked by S<m>".

In a small change (no `design.md`, or no `## Slices` section in it), read the section before `## <n>.` the same way; for a fix slice (its `tasks.md` section has a Depends on line), read only the section that line names.

## Red check

Run the test command (the command after `Tests:` in the `context:` of `openspec/config.yaml`) on the new or corrected tests, and read the result of each. When a stub ends the test run at the first test, run each new test alone and keep the output of each.

- Right reason: an assertion on the scenario's behaviour, or a stub's "not implemented" error.
- Wrong reason: a build or syntax error, a missing import or symbol, a missing fixture.

A new or corrected test that passes, or fails for a wrong reason, fails the check. A guard test is the one exception. A *guard test* covers a scenario that says a behaviour of the code before the change stays as it is (a refusal that still holds, an output that does not change), so it passes before any code exists, by design. It passes the check when the test writer's report marks it as a guard and names that scenario, and the code before the change already shows that behaviour. Ask the owner nothing for it. At least one new test of the slice must still be red for the right reason, except in a tests-only slice. A *tests-only slice* adds tests for behaviour that exists and changes no behaviour: its Delivers line starts with `Tests only:`. Each of its new tests is a guard test, and the break check below takes the place of the red one. The build report lists each guard test.

**Break check.** A guard test must be able to fail. For each guard test, the test writer breaks the production code that the test covers for one run only (a one-line change that removes the behaviour), runs the test, keeps its failing output, and restores the file with `git checkout -- <file>`. The test must fail on an assertion on its scenario's behaviour, as in the red check. Then check yourself that the tree holds no production change (`git status --porcelain` lists only test files and stubs), and run the guard tests once: they pass. A guard test that does not fail on its break fails the check. When the test check script fails only because guard tests pass, apply this rule to its output by hand.

## Test lock

This form runs in the build and in the fix round after verify. Verify runs [Test lock at verify](#test-lock-at-verify) instead.

Take the lock commit: the slice's newest tests commit, or in the fix round after verify, the commit its code writer started from. Your notes hold its hash.

The slice's newest tests commit is the newest commit on the working branch whose `Tests-For` trailer carries the slice name (SKILL.md, Per slice). Never find it by its title. When your notes do not hold the hash, or on a resume, read the trailers:

```bash
git log --format='%h %(trailers:key=Tests-For,valueonly,separator=%x2C)' <default branch>..HEAD
```

Each line is one commit, newest first: its hash and its trailer value, or the hash alone for a commit that is not a tests commit. The first line whose value is the slice name (for example `S2`) is the slice's newest tests commit. Every line with that value is a tests commit of the slice.

Take the test paths from the test writers' reports. On a resume, take them from the tests commits of the slice, as the resume rule in SKILL.md, Per slice, gives them. For each of those commits, run the command below, with the repo's test-file patterns (after `Test files:` in the `context:` of `openspec/config.yaml`, else the patterns of the repo's language and test runner) as pathspecs, in the form that [Test lock at verify](#test-lock-at-verify) gives them:

```bash
git show --name-only --format= <tests commit> -- <patterns>
```

Then run:

```bash
git diff --name-status <lock-commit> -- <test paths>
git status --porcelain -- <test paths>
git diff --name-status <lock-commit>
git status --porcelain --untracked-files=all
```

Give the last two commands the repo's test-file patterns as pathspecs, in the form that Test lock at verify gives them (`:(glob)` before each pattern, `**/` before a pattern with no slash, one argument per brace form): `git diff --name-status <lock-commit> -- <patterns>` and `git status --porcelain --untracked-files=all -- <patterns>`. They catch a test file added outside the listed paths. With no test paths (a fix round with no test writer), run only those two. Any line they print fails the check.

## Test lock at verify

At verify, the test lock holds when no commit in `<default branch>..HEAD` without a `Tests-For` trailer adds, changes, deletes or renames a test file, and the tree holds no uncommitted test-file change. The test check script does not run at verify.

Set `B` to the default branch that [Default branch](#default-branch) finds. It is the branch that the verify report names on its `Base:` line. After `set --`, give each of the repo's test-file patterns (after `Test files:` in the `context:` of `openspec/config.yaml`, else the patterns of the repo's language and test runner) as one argument in single quotes, with `:(glob)` before it. A pattern with no slash, such as a test runner's `test_*.py`, becomes `:(glob)**/test_*.py`. Git's glob knows `*`, `?`, `[...]` and `**` as a whole path part, and nothing more. Give a pattern with braces, or with `?(...)`, `+(...)` or `@(...)`, as one argument per form that it stands for: `**/*.{test,spec}.ts` becomes `':(glob)**/*.test.ts' ':(glob)**/*.spec.ts'`. Remove a slash at the end of a pattern. Remove a slash at the start of a pattern. No pattern may match a path under `openspec/`: the code commits and the report commits change files of the change folder, and they carry no trailer. Narrow such a pattern, for example `**/test/**` and `**/tests/**` in place of `**/test*/**`. For example, with the patterns `tests/test_*.py` and `**/*_test.go`: `set -- ':(glob)tests/test_*.py' ':(glob)**/*_test.go'`. Replace `<change>` in the line `R=` with the name of the change. Then run the whole block in one shell call, from the repo root. The Bash tool runs it as written: it is safe in bash and in zsh, and prints the same lines under both. `B` and the patterns do not carry over to another shell call. Claude Code's permission check may ask the owner before it runs the block (a nested trial with a narrow allow list refused it with "Contains brace with quote character (expansion obfuscation)"). That is expected, and the owner allows it once.

```sh
B=<default branch>
set -- <test-file patterns>
[ -n "$B" ] && [ "$#" -gt 0 ] && git rev-parse --verify --quiet "$B^{commit}" >/dev/null && [ -n "$(git rev-list -1 "$B..HEAD")" ] || echo 'SETUP FAILED: set B and the patterns'
for p; do case "$p" in ':(glob)'*) case "${p#':(glob)'}" in *'{'*|*'('*|*'/'|'/'*) echo "SETUP FAILED: pattern git cannot read: $p";; esac;; *) echo "SETUP FAILED: no :(glob) before: $p";; esac; done
R=openspec/changes/<change>/build-report.md
case "$R" in openspec/changes/?*/build-report.md) ;; *) echo 'SETUP FAILED: set the change name in R';; esac
[ -d "${R%/*}" ] || echo "SETUP FAILED: no change folder: ${R%/*}"
rec=$(git show "HEAD:$R" 2>/dev/null | grep -E '^[[:space:]]*[-*+][[:space:]]*Answer:')
ans=$(printf '%s\n' "$rec" | sed -n 's/^- Answer: lock | \([0-9a-f]\{40,64\}\) | .*/\1/p')
printf '%s\n' "$rec" | grep -v -E '^- Answer: (lock|past|base) \| [0-9a-f]{40,64} \| ' | grep . | sed 's/^/IGNORED RECORD, bad form: /'
for h in $ans; do git rev-list --no-merges "$B..HEAD" | grep -qx "$h" || echo "IGNORED RECORD, not on the branch: $h"; done
{
for c in $(git rev-list --no-merges $B..HEAD); do
  git log -1 --format='%(trailers:key=Tests-For,valueonly,separator=%x2C)' $c | grep -Eq '^(S[0-9]+|verify)$' && continue
  f=$(git diff-tree -r -M --no-commit-id --name-status $c -- "$@")
  [ -n "$f" ] && { git log -1 --format='OFFENCE %h %s' $c; echo "$f"; }
done
git status --porcelain --untracked-files=all -- "$@" | sed 's/^/UNCOMMITTED /'
} | while IFS= read -r l; do
  case "$l" in
    'OFFENCE '*) s=${l#OFFENCE }; s=${s%% *}; h=$(git rev-parse --verify --quiet "$s^{commit}")
      if [ -n "$h" ] && printf '%s\n' "$ans" | grep -qx "$h"; then echo "ANSWERED $h ${l#OFFENCE $s }"; skip=1; else echo "$l"; skip=0; fi;;
    'UNCOMMITTED '*) echo "$l"; skip=0;;
    *) [ "$skip" = 1 ] || echo "$l";;
  esac
done
```

The test lock gives no finding when the commands print no `OFFENCE` line and no `UNCOMMITTED` line: an offence that the owner answered prints as `ANSWERED` (below). An `OFFENCE <hash> <title>` line, with the test files under it, is a commit whose `Tests-For` trailer is missing, or holds a value other than one `S<n>` or `verify`, and that added (A), changed (M), deleted (D) or renamed (R) a test file. An `UNCOMMITTED` line is a test file that is changed, staged or untracked. Each is a finding.

An offence stays on the branch, because the flow never amends. The owner's answer is the only thing that clears it. The block reads the answers from `build-report.md` as committed at `HEAD`: a line of the form that [Answers in the build report](#answers-in-the-build-report) gives, with the kind `lock`. An offence whose full hash has such a line prints as `ANSWERED <full hash> <title>` in place of the `OFFENCE` line and its files, and it is no finding. List each `ANSWERED` line in the verify report. A record line of the kind `past` or `base` is no concern of the test lock: the block reads no more of it than its form. A record line that is of neither form prints `IGNORED RECORD, bad form: <line>`. A record whose hash is not a commit of `<default branch>..HEAD` prints `IGNORED RECORD, not on the branch: <hash>`. An `IGNORED RECORD` line is no finding. List it in the verify report. An `UNCOMMITTED` line is never answered: it stays a finding until it is committed in a tests commit with `Tests-For: verify`, or the owner removes it. A record that is written but not yet committed answers nothing.

An `OFFENCE` line that no record answers is an Owner finding of the fix round (SKILL.md, After verify, step 1). There, put one question per offending commit to the owner, in the form of the `idea-to-code:grilling` skill: what the commit changed in which test file, and two options. **Keep the edit** (the commit stays as it is). **Restore the test** (a tests commit with `Tests-For: verify` brings the test files back as SKILL.md, After verify, step 1, says, and then the code goes green again). Recommend one option, and give the basis. When the offending commit carries a `Tests-For` trailer with a wrong value (a tests commit of the build whose trailer check failed), say in the background that its test files are the slice's tests, and recommend Keep the edit. Otherwise recommend Restore the test, because the lock keeps the committed tests. With `OFFENCE` lines from several commits, ask one question after the other, and never in one message. Write each answer as a record line, kind `lock`, as Answers in the build report says. Write a record line only for the owner's answer to that question in this session. Never write one by your own choice, from a repo rule, or from an answer to another question, such as the question on a failed trailer check in the build: the block cannot tell who wrote a record. The record rides the commit of the round's report (After verify, step 6).

A `SETUP FAILED` line is no pass and no finding: `B` is empty, names no commit, or has no commit of the working branch after it (as when `B` is the working branch), or no pattern is set, or the line `R=` holds no change name, or the folder of `R` does not exist (a wrong or missing change name), or a pattern has no `:(glob)` prefix, or holds braces, `(` or a slash at its start or end, which git's glob cannot read. Correct it, and run the whole block again. Never replace the loop with `git log <range> -- <patterns>`: after a merge, that form can hide a commit.

Limits:

- `B` must hold every commit that the working branch merged from the default branch. Use the newest ref of the default branch, such as `origin/<default branch>` when it is ahead of the local branch (the lines of Default branch print the bare name when a local branch exists, and `origin/<name>` when only the remote branch exists). With an older ref, a commit of the default branch shows as an offence.
- A merge commit is not read, so a test edit made inside a merge is not caught.
- A commit whose trailer value is `S<n>` or `verify` passes whole. The check compares no test file with a lock commit.
- A rename out of the test paths or into them shows as D or A, not as R.
- The trailer options need git 2.32 or newer.

## A failure that the default branch has too

A failure of the test command or of the check command can come from the default branch and not from the change: a test or a program that fails the same way on a clean checkout of `<default branch>`. Check that before you treat the failure as the change's. Run the failing test or program alone on a detached worktree of the default branch, in a scratch folder outside the repo, and remove the worktree after the run:

```sh
W=<scratch folder>/base-check
git worktree add -q --detach "$W" <default branch>
( cd "$W" && <the command of the failing test or program> ); echo "exit $?"
git worktree remove "$W" || { rm -rf "$W"; git worktree prune; }
```

The failure is the same when the run exits non-zero with the same error line. It is then a *base failure*. When the command stopped at the failure (a task runner ends at its first failed part), run each part that it did not reach, one by one, and read the result of each, so that a base failure hides no other failure.

A base failure goes to the owner once, as one question in the form of the `idea-to-code:grilling` skill: the test, its error line, and the run on the default branch. Two options: **Keep it out** (the change goes on with this failure, and a separate change fixes it), or **Fix it in this change**. When a changed form of the command passes (The commands run as written, below), add a third option, **Run it changed**: the failure stays out of the change, and the build and every later verify run the command in that form. Recommend Keep it out, or Run it changed where that option exists, when the diff of the change touches none of the files of the failing test or program. Each of the answers Keep it out and Run it changed is a record line of the kind `base` (below), and it answers that failure in the rest of the build and in every later verify. Each verify runs the check above again: a failure that no longer fails on the default branch is the change's, whatever the records say.

## A failure of the checkout

A command can fail in this checkout and pass on the same commit in a clean worktree. The cause is then outside the commits: a file or a folder that git does not track (a second worktree inside the repo, a build output, a local config file). It is a *checkout failure*: neither the change nor the default branch has it.

Run this check when the check above shows no base failure, and only while the work tree holds no uncommitted work of a writer: before the first slice, after a code commit, and in verify. Run the failing command on a detached worktree of `HEAD`, by the lines above with `HEAD` in place of `<default branch>`. When `HEAD` is the commit of the default branch, the run of the check above serves. A clean run that fails the same way is the change's failure. When the clean run passes, find the cause in the checkout. Done when you can name the path that makes the command fail.

A checkout failure goes to the owner once, as one question in the form of the `idea-to-code:grilling` skill: the command, its error line, the clean run and the path. Two options: **Clear the checkout** (the owner moves or removes that path, and you run the command again), or **Stop**. Recommend Clear the checkout. What git does not track in the checkout is the owner's: move, remove or replace none of it yourself. A checkout failure writes no record line, because it is gone when the work goes on.

## The commands run as written

Run the test command and the check command as the config gives them, at every step. A changed form (a variable set before the command, a part left out, a tool that you build by hand) is evidence about a failure, and no way past it: name it in the background of the question, with its result. Run a command in a changed form only after the owner answered Run it changed (A failure that the default branch has too), and name that form in the report at each run.

## Answers in the build report

The fix round writes each owner's answer on a commit that the flow cannot change, and on a base failure, as one record line in `build-report.md`, under the heading `### Answers` in the `## Fix round` section of that round (SKILL.md, After verify, step 6). The build writes an answer on a base failure under the heading `### Answers` of the build report itself (SKILL.md, After the last slice). Each round appends its own section, and the records of every section count. One form serves every kind of answer:

```text
- Answer: <kind> | <full hash> | <choice> | <detail> | <UTC time>
```

- `<kind>` is `lock` for a test-lock offence (above), `past` for a finding about a past commit (SKILL.md, After verify, step 1), or `base` for a base failure (A failure that the default branch has too). The test-lock block reads only the lines of the kind `lock`.
- `<full hash>` is the output of `git rev-parse <hash>` for the commit that the question named. For `base`, it is the commit of the default branch that the check ran on: `git rev-parse <default branch>`.
- `<choice>` is `keep` or `restore` for `lock`, `keep` for `past`, and `keep` or `changed` for `base` (the answers Stop and Fix it in this change write no record).
- `<detail>` is the test files that the commit touched, separated by commas, for `lock`. For `past` it is the finding in a few words. For `base` it is the failing test or program, then its error line in a few words. After the choice `changed`, the changed form of the command follows, after the words `run as`. It holds no `|`.
- `<UTC time>` comes from `date -u +%Y-%m-%dT%H:%MZ`.

A record holds the owner's answer to the question of this session, and nothing else. The round's report commit carries it (SKILL.md, After verify, step 6), or in the build, the commit of `build-report.md`. A record that is written but not committed answers nothing. For `past`, the later verify (the verify command, step 4) reads the committed records of the kind `past` with `git show HEAD:openspec/changes/<change>/build-report.md | grep -E '^- Answer: past \| '`, and a finding about the commit of a record, for the breach that its detail names, is listed as answered and is no finding. For `base`, it reads the records with `grep -E '^- Answer: base \| '` in place of that pattern. A failure of the test command or of the check command whose test or program a `base` record names, and that the check of A failure that the default branch has too still shows as a base failure, is listed as answered and is no finding. After a record with the choice `changed`, run the command once more in the form that the record holds: the result of that run is the result of the command.
