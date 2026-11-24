# Credits

The **Summary** section's menu of visuals (pseudocode, call trees, component trees, file trees, Mermaid, diffs) and its placement guidance come from [Dex Horthy](https://github.com/dexhorthy)'s [`show-me`](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md) skill, reproduced almost word for word and aimed at a diff instead of a live conversation. `idea-to-code:pr` does not depend on `show-me` as a skill (it isn't part of this repo, and a hard dependency would break standalone installs), so the content is copied in rather than pointed at; this file is the attribution a dependency would otherwise have carried.

## Licence of the copied text

- Source: `plugins/show-me/skills/show-me/SKILL.md` in `github.com/humanlayer/skills`. Commit: `bba9d13ab34f0a87f1cc33df4dd196372393ddfc` (2026-09-12). The text came to this repo through the upstream `skills/engineering/pr` of Matt Pocock's skills, at `abeeaf95660ba9e8b7c753eb38f441ca707a8823`, which carried it without the HumanLayer licence.
- Licence: MIT, Copyright (c) 2026 HumanLayer. The full text is in `LICENSE-humanlayer-skills.txt`, in the `skills/` folder, one level up. It must stay with any copy of this part of the skill.
- This licence covers the show-me part of `SKILL.md` only: the **Summary** section's menu of visuals and its guidance. It is not the licence of the other upstream, Matt Pocock's skills, and it is not the licence of the rest of this skill.

## Local changes

| Place | Change |
| --- | --- |
| Introduction | The upstream opening, aimed at a live conversation, is replaced by text aimed at a pull request diff. |
| Component tree | The code fence is `text`, not `tsx`. |
| Whole-block example | The two statements end in a semicolon. |
| HTML file | The upstream bullet that writes and opens an HTML file is removed. |
| Guidance | The heading is one level lower, with a capital letter. |
| Front matter | The upstream front matter is replaced by the `credits` block of this skill. Its `url` points to the source file at the head of the upstream default branch. |
