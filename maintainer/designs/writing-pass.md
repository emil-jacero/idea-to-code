# The writing pass

A review of every skill of the plugin against one reference on how to write a document that an
agent reads. The reference is the skill `writing-for-agents` of Matt Pocock's skills
(`skills/productivity/`). The plugin does not ship it, and no text of it is copied. This file holds what the review found, the
four changes that follow from it, and one prediction per change. A trial checks each prediction.

## Why

No skill of the plugin was written with that reference. The review read all of them. Its levers:

- **Pointer:** a description is always loaded. It names the skill and the cases that reach it,
  and nothing that the body carries.
- **Hierarchy:** the steps come first. Reference that only some runs need sits in a sibling file,
  behind a pointer that names those runs.
- **Completion criterion:** every step ends on a condition that is checkable and demanding.
- **One home:** one meaning stands in one place.
- **Positive wording:** a text names the wanted behaviour. A ban stays only as a hard guard, and
  then with the wanted behaviour beside it.

## Findings

1. `skills/slice-build/SKILL.md` served four callers from one file of about 5,000 words: the
   build, the fix round, propose (for the form of a slice) and verify (for the test lock). Its
   steps (a) to (g) stood under four paragraphs of reference.
2. The form of a seam question stood in full in two commands. The words "as one question in the
   form of the grilling skill" stood at about 25 places of the build skill.
3. The description of the `pr` skill named only the body of a pull request, and the skill also
   holds the push rule and the merge rule.
4. The description of the build skill named the trigger words that it then refused. Four other
   descriptions repeated what their body does.
5. Explore and propose had no completion criterion per step.

## What stays as it is

- The fixed phrases of `check_tree.py`. A phrase that names a command of the config stands word
  for word at each place, and a short back-reference to it is a retired string. The review first
  read this as duplication. It is a recorded choice, so it stays.
- The paragraph of Project rules in the four skills that carry it. The check holds its one text.
- A long sentence that an earlier trial added. No record says which trial added which sentence,
  so the pass moves such a sentence and does not cut it.

## The four changes

Each change is one commit, and each has its own prediction.

| Change | What | Prediction |
| --- | --- | --- |
| 1. Descriptions | Nine descriptions name the skill and its cases only. The build skill is described as reference of the step commands. The `pr` skill names the push and the merge. | A request in words to build loads the build command first, as before. A push or a merge with no new body loads the `pr` skill. |
| 2. One home | The seam question has one home, a sibling file of the grilling skill. The build skill states once how a question to the owner is put. | Every seam question keeps its `Test seam` heading and its `Catches:` and `Misses:` lines. Every question of a build keeps the form of the grill. |
| 3. The split | The fix round, the failure rules and the rules of a repo without specs move to sibling files of the build skill. The read for a resume becomes a numbered step. | A build with no failure never reads the fix-round file. After a failed check, the session reads the failure rules before its next action. A resume is found before the first slice, as before. |
| 4. Criteria | Explore and propose end their steps on a completion criterion. The support skills get the smaller corrections of the review. | Explore ends with one ledger entry per question and per choice, and with no open entry. Propose reports the result of the validation. |

## How a prediction is checked

One change of a repo runs through the four steps on the branch of this pass. The session logs
show which files a session read and which form a question had. A prediction that fails is
recorded with its evidence, and the change that it belongs to is corrected or taken back alone.

## Left open

- The `pr` skill loads the commit skill first, so both paragraphs of Project rules are in one
  context. A cut needs a change of the check, and the owner has not asked for it.
- One finding on the diagnosis skill needs a full read of the briefs before a cut.
