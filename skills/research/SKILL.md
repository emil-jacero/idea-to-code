---
name: research
description: "Research a question against primary sources and write a cited Markdown note. Use when the user asks for research, or when a fact that a design rests on needs a source."
---

Spin up a **background agent** to do the research, so you keep working while it reads. Start it with a fresh context window. Brief it with the question, the repo it serves, and the change name or "no change yet". If you are already a sub-agent, do the research yourself and start no other agent.

Its job:

1. Investigate the question against **primary sources** (official docs, source code, specs, first-party APIs), not a secondary write-up of them. Follow every claim back to the source that owns it.
2. Write the findings to a single Markdown file, citing each claim's source.
3. Save it as `README.md` in a folder `<nn>-<name>/` (`<nn>` is the next free two-digit number in the change's `evidence/`, `01` in a scratch folder):
   - **The change already exists:** write the folder straight into its `evidence/`.
   - **No OpenSpec change exists yet** (explore paused for this question): put that folder in a scratch folder outside any repo, made with `mktemp -d` under `$TMPDIR` (else `/tmp`). Propose moves it to `openspec/changes/<change>/evidence/<nn>-<name>/`; the change's `design.md` points at the folder.
   - **The question serves no change:** save it where the repo the question serves already keeps such notes, or else in the scratch folder.
4. Report the full path and a one-line answer, so the paused step resumes with it and the design can cite it. **Done when** every claim in the note cites its primary source or is marked `not settled`. Commit nothing.
