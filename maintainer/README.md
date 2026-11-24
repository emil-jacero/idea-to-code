# Maintainer scripts

Two scripts check this repo. They read and never write. Run them from the repo root.

- `check_tree.py` checks the plugin tree: the fixed phrases of the skills, the names and
  branches in them, the links, the two JSON manifests, and the leak grep.
  Run `python3 -I -B maintainer/check_tree.py`. Add `--tree DIR` to check another copy.
- `check_page.py` checks `workflow.html` against `WORKFLOW.md` and `diagrams/`: word limit,
  anchors and links, colours, dashes, the page frame, and the figures and captions.
  Run `python3 -I maintainer/check_page.py`. An optional path argument names another page.

An optional file, `maintainer/private-words.txt`, adds a maintainer's own search words to the
leak checks. Git ignores it. Each line is `<label>`, a tab, then `<regex>`. A line that starts
with `#` is a comment. Without the file, both scripts say so in one line and run the generic checks.
