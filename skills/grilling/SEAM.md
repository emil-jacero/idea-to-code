# The seam question

A **seam** is the public interface where the tests of a part of the work go. Every seam is agreed with the owner before the change is written. So a seam is always a question to the owner, and never a choice of your own. In the ledger, a seam has the scope `program-design`.

- Ask a seam after the decisions that fix what is built, because a seam depends on them.
- Ask one question per distinct seam, not one per slice.
- Start the name in its heading with `Test seam`.
- Say in its background that the build writes the tests there before the code, and then locks them. Name the parts of the work whose tests go there: the slices, where they are known.
- Each option keeps the form of the grill: its example line, then `Catches:` as its pro and `Misses:` as its con, in place of `Pro:` and `Con:`. The recommended option shows its `Misses:` line too.
- "You decide" is an answer: pick the seam, and record it as delegated.

Example:

```text
### Test seam of the refusal, Q4 of about 4: Where do the tests of the refusal go?

**Background:** An upload with an empty file name is refused. The build writes the
tests at this seam before the code, and then locks them. The tests of the refusal
and of the name of only spaces go there.

**Options:**

**A. The upload API (recommended)**
- A request to `POST /files` with an empty `filename`.
- Catches: the 400 answer, and that no file is stored.
- Misses: which check inside the handler refused.

**B. The name check inside the handler**
- A call of the check with `""` and with `"  "`.
- Catches: every form of an empty name, in a fast test.
- Misses: that the API answers 400 and stores nothing.

**Recommendation: A.** Only the API shows the answer that the uploader gets.
My judgement, not researched.

Next: answer A or B.
```
