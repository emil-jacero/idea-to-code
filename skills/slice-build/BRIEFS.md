# Briefs

The two briefs you send in a slice build and in its fix round after verify, one per writer. Send each one as the fresh sub-agent's whole prompt: fill every `<placeholder>`, leave out each input line and paragraph that does not fit the repo or the round (a repeat-round line in a first round, the tests commit in a repo without specs, the glossary or the ADR folder in a repo that has none), and append [Rules for both writers](#rules-for-both-writers). Each input carries a "why" line: with the reason in hand, the writer can handle a case the brief did not foresee.

## Test writer

You write the tests for `<slice S<n>, or the verify findings below>` of the OpenSpec change `<change>`, before the code that makes them pass is written.

Inputs:

- The change folder `openspec/changes/<change>/`: proposal, delta specs, design, tasks. Why: the spec is the source of every expected value.
- The repo at HEAD, with its root at `<repo root>`. Why: your tests follow its test layout and conventions, and build against the code that exists now; run every command from the root.
- The repo's test command, `<command>`, and its test-file patterns, `<test-file patterns>`. Why: you run the new tests with the command, and only a file that matches a pattern counts as a test file, in the tests commit and in the test lock.
- The slice block: `<Delivers, Seam and Done when of S<n>>`. Why: Delivers bounds what you test, Seam is where every test goes, and the Done when line needs a test too.
- The scenarios the slice delivers: `<the full text of each>`. Why: each one needs at least one test.
- In a repeat round, the evidence of the failed red check: `<each failing test and its output, or each item left without a test>`. Why: it names each test that passed or was red for a wrong reason, and each scenario left without a test.
- In a dispute round, the disputed tests and the code writer's evidence: `<test file and test name, for each>`, `<evidence>`. Why: you rule on each of these tests from the spec alone; the code writer's code is set aside, so you judge each test by what the spec says, not by what the code does.
- In the fix round after verify, the findings that need a test changed or added, each with the slice block it falls in: `<finding, what it cites, slice block>`. Why: write or change only the tests these findings need, at that slice's Seam.
- After a hand-back, the question, the owner's answer and the files the last writer left in the tree: `<question>`, `<answer>`, `<paths>`. Why: the answer settles the decision that stopped the last writer; build on its files or replace them.

In a small change (no `design.md`, or one with no `## Slices` section), the slice block is the text of the `tasks.md` section `## <n>.`, and the slice delivers the scenarios whose behaviour its tasks add.

In a dispute round, this replaces the steps and the report below. Read each disputed test, the spec and the evidence, and rule on each: the spec backs the code writer, the spec backs the test, or the spec is silent or unclear. When the spec backs the code writer on a test, load the `idea-to-code:tdd` skill and correct that test (and its fixture) to what the spec says. Change no test that is not disputed. Run each corrected test and keep its red output. Report each ruling, the spec text it rests on, and each corrected test with its red output.

Steps:

1. Load the `idea-to-code:tdd` skill for the test-quality rules.
2. Write tests at the slice's Seam: one or more for each delivered scenario (in the fix round, for each finding), and for the Done when line where the slice has one. A Done when line that only says that the delivered scenarios pass is covered by their tests: map it to them in your report, and write no extra test. Take expected values from the spec or its worked examples, never from running code.
3. Where a test needs it to build, add a compile-only stub: a signature that builds. A stub never returns a value: it raises the language's "not implemented" error, so a test that asserts a value cannot pass on a stub. Wiring that a test needs to reach the Seam (an export line, a registration) belongs to the stub. It may stand in the tests commit when it holds no behaviour. Write the least of it. Where the language has no such error, the stub stops the program instead, with the message "not implemented" (a panic, an abort). List each stub and each wiring line. Write no other production code. A test that expects an error names the error of its scenario, by a type or a message that the stub's error does not match. Otherwise that test passes on the stub.
4. When the slice deepens a module, delete the old tests that the new tests at its interface replace (the `idea-to-code:codebase-design` skill, DEEPENING.md).
5. Run the new tests with the test command, and keep the red output of each. Every new test must be red. When a stub ends the test run at the first test, run each new test alone and keep the output of each.

Report:

- A table with one row per scenario, finding or Done when line: the test that covers it, its seam and its red output line.
- The test files you added, changed or deleted, and the stub files, with each wiring line.
- Your assumptions, each with the question it answered.
- Every point where the spec was too vague to test.

## Code writer

You write the production code for `<slice S<n>, or the verify findings below>` of the OpenSpec change `<change>`.

Inputs:

- The change folder `openspec/changes/<change>/`. Why: it says what the code must do.
- The tests commit `<hash>` (the slice's newest; in the fix round, the commit you start from) and the test paths: `<paths>`. Why: the slice's tests are committed there, red until your code exists; these files are locked, and when you finish, a check compares them with that commit.
- The repo, with its root at `<repo root>`, and its test command, `<command>`. Why: the whole suite must pass, not only the new tests; run every command from the root.
- The repo's glossary, `<glossary file>`. Why: name new code with the glossary's words; a term this change needs was written before the build.
- The repo's ADR folder, `<ADR folder>`. Why: follow the ADRs for the area you touch; an ADR this change needs was written before the build.
- The slice's `tasks.md` section `## <n>.`: `<its text>`. Why: the session ticks every box in it at the code commit, so each task must be done.
- In a repeat round, the finding of the failed check: `<finding>`. Why: the last round changed a test file, which is now restored, left the test command red, or failed the check command.
- In a repeat round after a failed check command, that command: `<check command>`. Why: the commit runs it, and it failed on the last round's code; run it too before you report.
- In the fix round after verify, the findings: `<each finding and what it cites>`. Why: each cites a task, a requirement, a scenario or a repo standard the change does not meet yet; fix each one at what it cites, and nothing more.
- After a hand-back or a dispute ruling, the question, the answer (the owner's, or the rulings on the disputed tests) and the files the last writer left in the tree: `<question>`, `<answer>`, `<paths>`. Why: the answer settles what stopped the last writer; build on its files or replace them.

In a repo without specs, no tests are written first: you have no tests commit and no new tests to pass. Your inputs also hold the slice block, `<Delivers and Done when of S<n>>`, where the change has one. Why: its Done when line says what must hold when you finish. Your report says how you showed each Done when line holds.

Steps:

1. Write production code until the repo's test command passes, with the tests of your tests commit in that run. Replace each stub with real code. A task that the wiring of a stub already completes is done at the tests commit: report it so. Do every task and fix every finding in your inputs that is not a test or a commit, and add nothing beyond them: nothing for a later slice.
2. Leave every test file and test fixture exactly as committed: edit, add, delete or rename none of them.
3. For a failure you cannot explain, you may load the `idea-to-code:diagnosing-bugs` skill; under this brief it fixes only code. Fix a bug when a failing test of the slice or the repo's test command reaches it, or when it sits in code not yet committed; in a repo without specs, also when it sits in code this change committed. Leave every other bug as it is.
4. Make the code right for every input the change's spec or design allows. When a test looks wrong, stop and report it as a disputed test, with the evidence: a special case for a test input is never the fix.

Report:

- What changed.
- Each task or finding you were given, and where it is done.
- The test result.
- Your assumptions, each with the question it answered.
- Disputed tests: each committed test you believe is wrong, with the evidence: the test, the spec text it contradicts and the test output.
- Bugs fixed: each bug you diagnosed and fixed in code, with its minimised repro, its seam and the confirmed hypothesis.
- Bugs left: each bug you left as it is, with the minimised repro and the seam.

## Rules for both writers

Append this text to each brief.

- Owner decisions: apart from a disputed test (code writer, step 4), stop and hand back only for a decision of these five kinds: scope, a public contract, a breaking change, a security trade-off, a new dependency. Hand it back with the question drafted in the form of the `idea-to-code:grilling` skill. Decide every other open choice yourself and list it as an assumption. The session asks the owner; you ask nobody.
- You commit nothing, tick no task box, and start no other agent.
