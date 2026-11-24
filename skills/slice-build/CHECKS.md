# Checks by hand

A repo can name two check scripts in its config: the slice check script (the command after `Slice check:` in the `context:` of `openspec/config.yaml`) for the gate, and the test check script (the command after `Test check:` in the `context:` of `openspec/config.yaml`) for the red check and the test lock. This file holds the same checks, done by hand, for a repo without them, and for the fix round after verify, which runs them by hand in every repo. It also holds the test lock at verify, which verify runs by hand in every repo with specs.

## Gate

1. In `design.md`, find the block `### S<n>:` and read its Depends on line: "none", or slice names such as "S1, S2".
2. For each S<m> named there, read `tasks.md` from `## <m>.` to the next `## ` heading. Any line with `- [ ]` there means S<n> is blocked: stop with "S<n> is blocked by S<m>".

In a small change (no `design.md`, or no `## Slices` section in it), read the section before `## <n>.` the same way; for a fix slice (its `tasks.md` section has a Depends on line), read only the section that line names.

## Red check

Run the test command (the command after `Tests:` in the `context:` of `openspec/config.yaml`) on the new or corrected tests, and read the result of each. When a stub ends the test run at the first test, run each new test alone and keep the output of each.

- Right reason: an assertion on the scenario's behaviour, or a stub's "not implemented" error.
- Wrong reason: a build or syntax error, a missing import or symbol, a missing fixture.

A new or corrected test that passes, or fails for a wrong reason, fails the check.

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

Set `B` to the default branch. `git symbolic-ref --short refs/remotes/origin/HEAD` prints it as `origin/<name>`. When it prints no name or fails (git prints `fatal: ref refs/remotes/origin/HEAD is not a symbolic ref` and exits 128 in a repo with no remote), ask the owner for the name in one plain sentence. After `set --`, give each of the repo's test-file patterns (after `Test files:` in the `context:` of `openspec/config.yaml`, else the patterns of the repo's language and test runner) as one argument in single quotes, with `:(glob)` before it. A pattern with no slash, such as a test runner's `test_*.py`, becomes `:(glob)**/test_*.py`. Git's glob knows `*`, `?`, `[...]` and `**` as a whole path part, and nothing more. Give a pattern with braces, or with `?(...)`, `+(...)` or `@(...)`, as one argument per form that it stands for: `**/*.{test,spec}.ts` becomes `':(glob)**/*.test.ts' ':(glob)**/*.spec.ts'`. Remove a slash at the end of a pattern. Remove a slash at the start of a pattern. No pattern may match a path under `openspec/`: the code commits and the report commits change files of the change folder, and they carry no trailer. Narrow such a pattern, for example `**/test/**` and `**/tests/**` in place of `**/test*/**`. For example, with the patterns `tests/test_*.py` and `**/*_test.go`: `set -- ':(glob)tests/test_*.py' ':(glob)**/*_test.go'`. Replace `<change>` in the line `R=` with the name of the change. Then run the whole block in one shell call, from the repo root. The Bash tool runs it as written: it is safe in bash and in zsh, and prints the same lines under both. `B` and the patterns do not carry over to another shell call. Claude Code's permission check may ask the owner before it runs the block (a nested trial with a narrow allow list refused it with "Contains brace with quote character (expansion obfuscation)"). That is expected, and the owner allows it once.

```sh
B=<default branch>
set -- <test-file patterns>
[ -n "$B" ] && [ "$#" -gt 0 ] && git rev-parse --verify --quiet "$B^{commit}" >/dev/null && [ -n "$(git rev-list -1 "$B..HEAD")" ] || echo 'SETUP FAILED: set B and the patterns'
for p; do case "$p" in ':(glob)'*) case "${p#':(glob)'}" in *'{'*|*'('*|*'/'|'/'*) echo "SETUP FAILED: pattern git cannot read: $p";; esac;; *) echo "SETUP FAILED: no :(glob) before: $p";; esac; done
R=openspec/changes/<change>/build-report.md
case "$R" in openspec/changes/?*/build-report.md) ;; *) echo 'SETUP FAILED: set the change name in R';; esac
[ -d "${R%/*}" ] || echo "SETUP FAILED: no change folder: ${R%/*}"
rec=$(git show "HEAD:$R" 2>/dev/null | grep -E '^[[:space:]]*[-*+][[:space:]]*Lock answer:')
ans=$(printf '%s\n' "$rec" | sed -n 's/^- Lock answer: \([0-9a-f]\{40,64\}\) | .*/\1/p')
printf '%s\n' "$rec" | grep -v -E '^- Lock answer: [0-9a-f]{40,64} \| ' | grep . | sed 's/^/IGNORED RECORD, bad form: /'
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

An offence stays on the branch, because the flow never amends. The owner's answer is the only thing that clears it. The block reads the answers from `build-report.md` as committed at `HEAD`: a line `- Lock answer: <full hash> | <keep or restore> | <test files> | <date and time>`. An offence whose full hash has such a line prints as `ANSWERED <full hash> <title>` in place of the `OFFENCE` line and its files, and it is no finding. List each `ANSWERED` line in the verify report. A record line that is not of that form prints `IGNORED RECORD, bad form: <line>`. A record whose hash is not a commit of `<default branch>..HEAD` prints `IGNORED RECORD, not on the branch: <hash>`. An `IGNORED RECORD` line is no finding. List it in the verify report. An `UNCOMMITTED` line is never answered: it stays a finding until it is committed in a tests commit with `Tests-For: verify`, or the owner removes it. A record that is written but not yet committed answers nothing.

An `OFFENCE` line that no record answers is an Owner finding of the fix round (SKILL.md, After verify, step 1). There, put one question per offending commit to the owner, in the form of the `idea-to-code:grilling` skill: what the commit changed in which test file, and two options. **Keep the edit** (the commit stays as it is). **Restore the test** (a tests commit with `Tests-For: verify` brings the test files back as SKILL.md, After verify, step 1, says, and then the code goes green again). Recommend one option, and give the basis. When the offending commit carries a `Tests-For` trailer with a wrong value (a tests commit of the build whose trailer check failed), say in the background that its test files are the slice's tests, and recommend Keep the edit. Otherwise recommend Restore the test, because the lock keeps the committed tests. With `OFFENCE` lines from several commits, ask one question after the other, and never in one message. Write each answer as a record line under `### Test-lock answers` in the `## Fix round` section of `build-report.md`, with the hash from `git rev-parse <hash>`, the test files that the commit touched, separated by commas, and the date and time from `date -u +%Y-%m-%dT%H:%MZ`. Write a record line only for the owner's answer to that question in this session. Never write one by your own choice, from a repo rule, or from an answer to another question, such as the question on a failed trailer check in the build: the block cannot tell who wrote a record. The record rides the commit of the round's report (After verify, step 6).

A `SETUP FAILED` line is no pass and no finding: `B` is empty, names no commit, or has no commit of the working branch after it (as when `B` is the working branch), or no pattern is set, or the line `R=` holds no change name, or the folder of `R` does not exist (a wrong or missing change name), or a pattern has no `:(glob)` prefix, or holds braces, `(` or a slash at its start or end, which git's glob cannot read. Correct it, and run the whole block again. Never replace the loop with `git log <range> -- <patterns>`: after a merge, that form can hide a commit.

Limits:

- `B` must hold every commit that the working branch merged from the default branch. Use the newest ref of the default branch, such as `origin/<default branch>` when it is ahead of the local branch. With an older ref, a commit of the default branch shows as an offence.
- A merge commit is not read, so a test edit made inside a merge is not caught.
- A commit whose trailer value is `S<n>` or `verify` passes whole. The check compares no test file with a lock commit.
- A rename out of the test paths or into them shows as D or A, not as R.
- The trailer options need git 2.32 or newer.
