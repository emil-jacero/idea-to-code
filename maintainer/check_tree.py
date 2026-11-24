#!/usr/bin/env python3
"""Check the tree of the `idea-to-code` plugin repo.

Run:  python3 -I -B maintainer/check_tree.py [--tree DIR]

The script reads and never writes. It runs ten checks of the plugin's text
rules, and three more checks:

  a  the leak grep, with an allow list of hits that were read
  b  both JSON manifests parse, hold no placeholder and hold the expected values
  c  every relative link of WORKFLOW.md, README.md and profiles/TEMPLATE.md resolves

Without `--tree` the script reads the repo root, the parent of `maintainer/`.
With `--tree DIR` it reads another copy of the tree. The `maintainer/` folder
and the `.git` folder are never part of the tree that is read.

An optional file, `maintainer/private-words.txt` (git-ignored), adds a
maintainer's own search words to the leak checks. One line per word:
`<label><TAB><regex>`. A line that starts with `#` is a comment. A label that
starts with `page:` is for the page checker only. The label `allow` marks a
hit that is fine: its regex matches the line with the hit marked as `<<hit>>`.

Output: one line per check that passes, one line per failure of a check that
fails. Exit code 1 when a check fails, else 0.
"""

import json
import posixpath
import re
import sys
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PRIVATE = HERE / "private-words.txt"

SKILLS = [
    "code-review", "codebase-design", "commit", "diagnosing-bugs", "domain-modeling",
    "grilling", "owner-gate", "pr", "prototype", "research", "slice-build", "tdd",
]

# The four step commands. Each one is a skill folder with no `name:` field.
COMMANDS = ["build", "explore", "propose", "verify"]

# THE LOCK. The commands whose frontmatter carries `disable-model-invocation: true`.
# To change the lock, change this list and the frontmatter of the command file
# together. Check 10 reads this list and nothing else.
LOCKED = []

# ---------------------------------------------------------------------------
# The fixed phrases. Each one stands word for word in the files that carry it.
# ---------------------------------------------------------------------------

P = {
    "GUIDE": "the repo guide (`AGENTS.md`, else `CLAUDE.md`)",
    "GUIDE-DEF": "The repo guide is `AGENTS.md`, else `CLAUDE.md`.",
    "GLOSSARY": "the repo's glossary (`GLOSSARY.md`, or the glossary file the repo guide names)",
    "TESTS-COMMIT": "the `Tests commit:` title form of the repo's `## Commit rules` (the "
                    "`idea-to-code:commit` skill says where the section sits; default: "
                    "`test(<scope>): <what the tests cover>`)",
    "TESTS-TRAILER": "The message of every tests commit ends with a trailer block: one empty "
                     "line, then the line `Tests-For: <slice name>`. Any other trailer line "
                     "follows it with no empty line between them, and the attribution line "
                     "stays last.",
    "SLICE-NAME": "The slice name is `S<n>` and nothing more, where `<n>` is the number of the "
                  "slice's section `## <n>.` in `tasks.md`. A fix slice uses the number of its "
                  "own section. In the fix round after verify, the value is the word `verify`.",
    "TESTS-KNOWN": "A commit whose message carries a `Tests-For` trailer is a tests commit, and "
                   "a commit without one is not. The title decides nothing.",
    "TESTS-WRITE": "Make the tests commit with plain git, and write no message file: "
                   "`git commit -m \"<title>\" --trailer \"Tests-For: <slice name>\"`. Where "
                   "the repo has an attribution line, add `--trailer \"<the attribution "
                   "line>\"` as the last option.",
    "TESTS-CHECK": "After the commit, read the trailer block as git reads it: "
                   "`git log -1 --format='%(trailers)'`. Its first line must be "
                   "`Tests-For: <slice name>`, and its last line must be the attribution line "
                   "where the repo has one. When it is not so, stop and make no further commit. "
                   "Put it to the owner as one question in the form of the "
                   "`idea-to-code:grilling` skill.",
    "TESTS-REDO": "The question offers two options: a new tests commit with the right trailer "
                  "block (recommended), or a stop. For the new commit, remove the cause first, "
                  "then run the same command with `--allow-empty`. The wrong commit stays, "
                  "because the flow never amends.",
    "FIRST-COMMIT": "The first commit that this build makes carries every file of the change "
                    "folder that is not committed yet, `gates.json` included. On a resume, that "
                    "is the next commit that this build makes. The build makes no commit that "
                    "holds only `gates.json`.",
    "STUB": "A stub never returns a value: it raises the language's \"not implemented\" error, "
            "so a test that asserts a value cannot pass on a stub. Wiring that a test needs to "
            "reach the Seam (an export line, a registration) belongs to the stub. It may stand "
            "in the tests commit when it holds no behaviour.",
    "NONE": "The value `none` switches the default off and nothing more. So `Scope: none` means "
            "that a scope is not required, and a scope is still allowed. A repo that forbids a "
            "scope also writes an added rule.",
    "NONE-BAN": "The value `none` is refused on `Tags:`, on `Publishing:` and on `Mentions:`, "
                "because the default of each is a ban.",
    "CHECK-RUN": "Before every commit, run the check command (the command after `Checks before "
                 "a commit:` in the `context:` of `openspec/config.yaml`). Run it after the "
                 "checks of the message and before `git commit`. When it fails, stop, make no "
                 "commit and report its output. A tests commit is the one exception: no check "
                 "command runs before it, because its tests fail by design. A repo with no "
                 "`Checks before a commit:` line has no check command.",
    "CHECK-LINE": "In your report, write one line that starts with `Check command:`. It names "
                  "the command and its result, or it says `Check command: none`. For a tests "
                  "commit, it says `Check command: not run, tests commit`.",
    "PR-TITLE": "The title of the pull request takes the title form of the repo's "
                "`## Commit rules`. The `idea-to-code:commit` skill holds that form: load it, "
                "and write the title by its rules for the title of a commit.",
    "HAND-OVER": "Then give the owner the link to the pull request. Under the default merge "
                 "rule, say that the owner merges.",
    "RULES-LINE": "the `Project rules:` line that the `idea-to-code:commit` skill gave, once "
                  "for the build",
    "NAMES": "With the plugin, a short skill name in prose means the plugin's skill. An "
             "instruction to load a skill then uses the full name, `idea-to-code:<skill>`. "
             "Claude Code ships a skill of its own named `code-review`, so the short name "
             "`code-review` loads that skill and not the plugin's.",
    "CMD-NAMES": "The four step commands ship in the plugin: `/idea-to-code:explore`, "
                 "`/idea-to-code:propose`, `/idea-to-code:build` and `/idea-to-code:verify`. A "
                 "repo carries no command file. A step command is always written in full, "
                 "because Claude Code has a command of its own named `verify`.",
    "ROUTING": "A project with many repos may keep routing commands of its own: such a command "
               "picks the repo, and then starts the plugin's step command there. Where only a "
               "person can start a step command, the routing command names it, and the owner "
               "types it.",
    "COUNT": "twelve method skills and four step commands",
    "VERIFY-LINE": "A verify run on an OpenSpec change also applies `openspec/verify.md`, "
                   "because the generated verify skill does not name that file.",
    "CLAUDE-MD": "Claude Code loads `CLAUDE.md` at session start. Where the repo guide is "
                 "`AGENTS.md`, add a `CLAUDE.md` that holds the one line `@AGENTS.md`, so that "
                 "the guide binds a session that loaded no skill.",
    "BUILD-LINE": "A request in words to build, apply or implement an OpenSpec change, or to "
                  "work through its tasks, loads `idea-to-code:build` and never "
                  "`openspec-apply-change`.",
    "BUILD-REPORT": "Write the same report to `build-report.md` in the change folder, and "
                    "commit that file alone, after the last code commit.",
    "LOCK-VERIFY": "At verify, the test lock holds when no commit in `<default branch>..HEAD` "
                   "without a `Tests-For` trailer adds, changes, deletes or renames a test "
                   "file, and the tree holds no uncommitted test-file change.",
    "NEXT-VERIFY": "The next step is verify: name `/idea-to-code:verify <change>`, and tell the "
                   "owner to run it in a fresh session. Do not start verify in this session, so "
                   "that verify reads the work without the context that wrote it.",
    "LEAD-PASS": "A lead stays in the report and does not keep verify from passing, unless the "
                 "repo guide says that a listed lead is an open finding.",
    "ADR": "the repo's ADR folder, the `ADR folder:` of the repo's `## Decision records` (the "
           "`idea-to-code:domain-modeling` skill says where the section sits; default: `adr/` "
           "where it exists)",
    "TEST-CMD": "the test command (the command after `Tests:` in the `context:` of "
                "`openspec/config.yaml`)",
    "CHECK-CMD": "the check command (the command after `Checks before a commit:` in the "
                 "`context:` of `openspec/config.yaml`)",
    "TEST-FILES": "the repo's test-file patterns (after `Test files:` in the `context:` of "
                  "`openspec/config.yaml`, else the patterns of the repo's language and test "
                  "runner)",
    "SLICE-SCRIPT": "the slice check script (the command after `Slice check:` in the `context:` "
                    "of `openspec/config.yaml`)",
    "TEST-SCRIPT": "the test check script (the command after `Test check:` in the `context:` of "
                   "`openspec/config.yaml`)",
    "NO-CMD": "When the config does not name a command this build runs, then before the first "
              "slice put it to the owner as one question in the form of the "
              "`idea-to-code:grilling` skill, with the command you found in the repo's build "
              "files as the recommended option.",
    "GATES": "Both gates are on, unless a gate line turns one off: `Plan gate: off.` or "
             "`Result gate: off.` The line stands in the repo guide (`AGENTS.md`, else "
             "`CLAUDE.md`), or in the `context:` of `openspec/config.yaml`.",
    "GATE-WORDS": "A line that says in other words that a gate is off turns no gate off. Report "
                  "that line, and put it to the owner as one question in the form of the "
                  "`idea-to-code:grilling` skill.",
    "NO-REPORT": "Read the build report, `build-report.md` in the change folder, for the "
                 "`report` criterion. When that file does not exist, do not judge the `report` "
                 "criterion from memory. Put it to the owner as one question in the form of the "
                 "`idea-to-code:grilling` skill, unless the repo guide says what holds then.",
    "AMEND": "Never amend a commit. Make a new commit, because the branch tip may have moved.",
    "PUSH": "Push the working branch only with a lease push (`git push --force-with-lease "
            "origin <branch>`), never with `--force` or `-f`. Never push to the default branch.",
    "HOOK": "When a hook blocks a command, put it to the owner as one question in the form of "
            "the `idea-to-code:grilling` skill. Never work around the hook.",
    "BAN-END": "These bans hold against any default of the agent tool that asks for such a "
               "line. Only the owner, in this session, lifts one.",
    # Strings of check 1 that are not fixed phrases.
    "the test command placeholder": "its test command, `<command>`",
    "the repo root placeholder": "<repo root>",
    "the test-file patterns placeholder": "<test-file patterns>",
    "the glossary placeholder": "<glossary file>",
    "the ADR placeholder": "<ADR folder>",
    "the code span `guide`": "`guide`",
    "the code span `config`": "`config`",
    "the code span `owner`": "`owner`",
    "the code span `criteria`": "`criteria`",
}

# The two gate lines. They are fixed lines, not phrases.
GATE_LINES = ["Plan gate: off.", "Result gate: off."]

BLOCK = (
    "Before you <act>, read these sections of the repo's rules: <sections>. A section is a "
    "heading of that exact name in the repo guide (`AGENTS.md`, else `CLAUDE.md`), or in the "
    "file that the guide names on its `Rules file:` line. A heading that differs only in "
    "letter case is the section: report it. Where a section is absent, the defaults of this "
    "skill hold. A point in a section replaces only the default of the same label, and the "
    "value `none` switches that default off. An absent label keeps its default. Every other "
    "line of a section is an added rule. It wins over a default of this skill that has no "
    "label. A default that has a label changes only through its point. The flow rules of this "
    "skill hold in every repo: a section adds to them and never removes one. When the rules "
    "file that the guide names is missing, one section is in both files, or a line of a "
    "section names a path that is not in the repo, stop and put it to the owner as one "
    "question in the form of the `idea-to-code:grilling` skill. For a path that is missing, "
    "the question offers three options: correct the line (fix or remove the path), create the "
    "file, or stop. The recommended option is to correct the line. It never offers to go on "
    "without the file. In your report, write one line that starts with `Project rules:` and "
    "names each section you read, or write `Project rules: defaults`."
)

BLOCK_ROWS = {
    "commit": ("write a commit message",
               "`## Commit rules`, `## Release rules` and `## Text rules`"),
    "pr": ("write a pull request body",
           "`## Pull request rules`, `## Text rules`, `## Release rules` and `## Merge rule`"),
    "code-review": ("list the standards sources",
                    "`## Written standards` and `## Decision records`"),
    "domain-modeling": ("write a term or a decision record", "`## Decision records`"),
}

CHECK1 = [
    ("skills/slice-build/SKILL.md",
     ["TEST-CMD", "CHECK-CMD", "TEST-FILES", "NO-CMD", "TESTS-COMMIT", "TESTS-TRAILER",
      "SLICE-NAME", "TESTS-KNOWN", "TESTS-WRITE", "TESTS-CHECK", "TESTS-REDO", "FIRST-COMMIT",
      "RULES-LINE", "NEXT-VERIFY", "BUILD-REPORT", "SLICE-SCRIPT", "TEST-SCRIPT", "GLOSSARY", "ADR",
      "GUIDE-DEF"]),
    ("skills/slice-build/CHECKS.md",
     ["SLICE-SCRIPT", "TEST-SCRIPT", "TEST-CMD", "TEST-FILES", "LOCK-VERIFY"]),
    ("skills/slice-build/BRIEFS.md",
     ["STUB", "the test command placeholder", "the repo root placeholder",
      "the test-file patterns placeholder", "the glossary placeholder", "the ADR placeholder"]),
    ("skills/tdd/SKILL.md", ["GLOSSARY", "GUIDE-DEF", "ADR"]),
    ("skills/diagnosing-bugs/SKILL.md", ["GLOSSARY", "GUIDE-DEF", "ADR"]),
    ("skills/codebase-design/SKILL.md", ["GLOSSARY", "GUIDE-DEF"]),
    ("skills/codebase-design/DESIGN-IT-TWICE.md", ["GLOSSARY", "GUIDE-DEF"]),
    ("skills/commit/SKILL.md",
     ["AMEND", "HOOK", "BAN-END", "TESTS-TRAILER", "NONE", "NONE-BAN", "CHECK-RUN",
      "CHECK-LINE"]),
    ("skills/pr/SKILL.md", ["GLOSSARY", "PUSH", "HOOK", "BAN-END", "PR-TITLE", "HAND-OVER"]),
    ("skills/code-review/SKILL.md", ["GLOSSARY"]),
    ("skills/domain-modeling/SKILL.md", ["GLOSSARY"]),
    ("skills/owner-gate/SKILL.md",
     ["GATES", "GATE-WORDS", "NO-REPORT", "the code span `guide`", "the code span `config`",
      "the code span `owner`", "the code span `criteria`"]),
    ("skills/prototype/SKILL.md", ["GUIDE"]),
]

NO_LOOKUP = [
    "the repo guide", "AGENTS.md", "CLAUDE.md", "Rules file:", "openspec/config.yaml",
    "context:", "GLOSSARY.md", "## Project rules", "## Commit rules", "## Release rules",
    "## Text rules", "## Pull request rules", "## Merge rule", "## Decision records",
    "## Written standards",
]

RETIRED = ["scripts/kit", "in the same `context:`", "`profile`", '"profile"',
           "text before the first `<`", "the `Tests commit:` form",
           "a temporary file outside the repo", "git commit -F", "returns a zero value",
           "or `openspec/config.yaml` turns one off", "so no test passes on a stub",
           "has the right scope", "run no test-lock check by hand",
           "When this session holds no final report of the build",
           "the user asks to build a change's slices",
           "Say that the result gate will ask about this report"]

# Check 4, the second part: strings that no file of the public tree holds.
RETIRED_TREE = ["/opsx:", "verify block", "verify-block", "Verify follows `openspec/verify.md`",
                "refused on `Tags:` and on `Publishing:`", "master copy", "copy task",
                "one shared package"]

# Check 10, the strings. An entry that is a key of P stands for that phrase. Every
# other entry is the string itself.
CHECK10 = {
    "explore": ["openspec-explore", "idea-to-code:grilling", "/idea-to-code:propose"],
    "propose": ["openspec-propose", "SLICE-SCRIPT", "idea-to-code:owner-gate",
                "/idea-to-code:explore", "/idea-to-code:build"],
    "build": ["idea-to-code:slice-build", "/idea-to-code:verify"],
    "verify": ["openspec/verify.md", "openspec-verify-change", "idea-to-code:code-review",
               "idea-to-code:slice-build", "idea-to-code:owner-gate", "CHECK-CMD", "SLICE-SCRIPT",
               "TEST-SCRIPT", "TEST-CMD", "LEAD-PASS", "Test lock at verify", "Verify rules: openspec/verify.md",
               "Verify rules: none, by hand"],
}

PREFIX = "idea-to-code:"
NAMES_LONG = ["slice-build", "tdd", "diagnosing-bugs", "codebase-design", "code-review",
              "owner-gate", "grilling", "domain-modeling"]
NAMES_SPAN = ["commit", "pr", "research", "prototype"]

EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"

# Check 9, the search: the generic patterns. A maintainer's own words come from
# the private file and join this list.
LOCAL_PATH = (r"/var/home|/home/|(?-i:/Users/)|(?<![\w.])~/|file://|\b[A-Za-z]:\\")
DASH = "\u2014|&mdash;|&#8212;|&#x2014;|\u2013|&ndash;|&#8211;|&#x2013;"

PRIVATE_PATTERNS, PRIVATE_ALLOW = [], []

LEAK9 = [LOCAL_PATH, EMAIL]

# Check a. Wider than check 9: the dash also as an HTML entity.
# `/Users/` keeps its letter case: `/users/` is a route in an upstream code example.
LEAK_A = [
    ("local path", LOCAL_PATH),
    ("email address", EMAIL),
    ("dash", DASH),
]


def load_private():
    """Read the private file. Returns (patterns, allow, info line).

    `patterns` is a list of (label, regex source) for the tree checks. `allow` is a
    list of context regexes: a hit is fine when the regex matches the line with the
    hit marked as `<<hit>>`.
    """
    if not PRIVATE.is_file():
        return [], [], ("# private words: none (%s is absent), only the generic leak "
                        "checks run" % PRIVATE.name)
    patterns, allow = [], []
    for number, line in enumerate(PRIVATE.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        label, _, regex = line.partition("\t")
        if not regex:
            print("FAIL  private  %s:%d is not `<label><TAB><regex>`" % (PRIVATE.name, number))
            sys.exit(1)
        try:
            re.compile(regex, re.IGNORECASE)
        except re.error as error:
            print("FAIL  private  %s:%d bad regex: %s" % (PRIVATE.name, number, error))
            sys.exit(1)
        if label == "allow":
            allow.append(regex)
        elif not label.startswith("page:"):
            patterns.append((label.removeprefix("tree:"), regex))
    return patterns, allow, "# private words: %d patterns, %d allow rules from %s" % (
        len(patterns), len(allow), PRIVATE.name)


def handles(tree):
    """The GitHub handles that the manifests name: the author and the owner."""
    found = set()
    for rel, keys in ((".claude-plugin/plugin.json", ("author", "name")),
                      (".claude-plugin/marketplace.json", ("owner", "name"))):
        doc = tree.get(rel)
        if doc is None:
            continue
        try:
            value = json.loads(doc.text)
            for key in keys:
                value = value[key]
        except (ValueError, KeyError, TypeError):
            continue
        if isinstance(value, str) and value:
            found.add(value.lower())
    return found


def allowed(line, start, end, names, allow):
    """A hit is fine when it lies inside a handle that the manifests name, or when a
    private allow rule matches the line with the hit marked."""
    low = line.lower()
    for name in names:
        at = low.find(name)
        while at >= 0:
            if at <= start and end <= at + len(name):
                return True
            at = low.find(name, at + 1)
    marked = "%s<<%s>>%s" % (line[:start], line[start:end], line[end:])
    return any(re.search(rule, marked, re.IGNORECASE) for rule in allow)


PLACEHOLDER = re.compile(
    r"\b(todo|tbd|fixme|xxx+|changeme|placeholder|lorem|example\.(com|org|net)|"
    r"your[-_ ]?(name|org|repo|email|handle|plugin)|owner[-_ ]?name|user[-_ ]?name)\b"
    r"|<[^>]*>|\{\{|\$\{|\[[A-Z_ ]{3,}\]",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Reading
# ---------------------------------------------------------------------------


def squeeze(numbered):
    """Count each run of white space as one space.

    `numbered` yields (line number, text of the line). Returns the text and,
    for each of its characters, the line that the character comes from.
    """
    out, where = [], []
    for number, line in numbered:
        for char in line:
            if char.isspace():
                if out and out[-1] != " ":
                    out.append(" ")
                    where.append(number)
            else:
                out.append(char)
                where.append(number)
        if out and out[-1] != " ":
            out.append(" ")
            where.append(number)
    while out and out[-1] == " ":
        out.pop()
        where.pop()
    return "".join(out), where


class Para:
    def __init__(self, numbered):
        self.first = numbered[0][0]
        self.last = numbered[-1][0]
        self.text, self.where = squeeze(numbered)

    def line_at(self, pos):
        if not self.where:
            return self.first
        return self.where[min(max(pos, 0), len(self.where) - 1)]

    def sentence_at(self, pos):
        """The sentence that holds `pos`. A sentence ends at . ? or ! before a space."""
        start = 0
        for match in re.finditer(r"[.?!] ", self.text):
            if match.end() <= pos:
                start = match.end()
            else:
                return self.text[start:match.start() + 1]
        return self.text[start:]


class Doc:
    def __init__(self, rel, path):
        self.rel = rel
        self.path = path
        self.raw = path.read_bytes()
        self.text = self.raw.decode("utf-8", "replace")
        self.lines = [line.rstrip("\r") for line in self.text.split("\n")]
        if self.lines and self.lines[-1] == "":
            self.lines.pop()
        self._norm = None
        self._paras = None

    @property
    def shown(self):
        try:
            return str(self.path.relative_to(ROOT))
        except ValueError:
            return str(self.path)

    @property
    def norm(self):
        if self._norm is None:
            self._norm = squeeze(enumerate(self.lines, 1))
        return self._norm[0]

    def line_at(self, pos):
        where = self._norm[1] if self._norm else squeeze(enumerate(self.lines, 1))[1]
        if not where:
            return 1
        return where[min(max(pos, 0), len(where) - 1)]

    @property
    def paras(self):
        if self._paras is None:
            self._paras, current = [], []
            for number, line in enumerate(self.lines, 1):
                if line.strip() == "":
                    if current:
                        self._paras.append(Para(current))
                        current = []
                else:
                    current.append((number, line))
            if current:
                self._paras.append(Para(current))
        return self._paras

    def frontmatter_end(self):
        """The index (0-based) of the line after the frontmatter, or 0."""
        if self.lines and self.lines[0].strip() == "---":
            for index in range(1, len(self.lines)):
                if self.lines[index].strip() == "---":
                    return index + 1
        return 0

    def fenced(self):
        """The numbers of the lines inside a fenced code block, fence lines included."""
        inside, marker, result = False, "", set()
        for number, line in enumerate(self.lines, 1):
            stripped = line.lstrip()
            match = re.match(r"(`{3,}|~{3,})", stripped)
            if not inside and match:
                inside, marker = True, match.group(1)[0] * 3
                result.add(number)
            elif inside:
                result.add(number)
                if stripped.startswith(marker) and stripped.strip(marker[0] + " \t") == "":
                    inside = False
        return result


def build_tree(tree_dir):
    """Return ({path in the tree: Doc}, [problems], the skills folder)."""
    base = tree_dir if tree_dir is not None else ROOT
    files, problems = {}, []
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if rel.parts[0] in (".git", "maintainer") or "__pycache__" in rel.parts:
            continue
        if path.is_file():
            files[rel.as_posix()] = path
    return {rel: Doc(rel, path) for rel, path in files.items()}, problems, base / "skills"


def variants(phrase):
    """A phrase matches exactly. Only its first letter may be a capital."""
    capital = phrase[:1].upper() + phrase[1:]
    return [phrase] if capital == phrase else [phrase, capital]


def find_all(hay, phrase):
    hits = []
    for form in variants(phrase):
        start = hay.find(form)
        while start >= 0:
            hits.append(start)
            start = hay.find(form, start + 1)
    return sorted(set(hits))


def find_all_any_case(hay, phrase):
    hay, phrase = hay.lower(), phrase.lower()
    hits, start = [], hay.find(phrase)
    while start >= 0:
        hits.append(start)
        start = hay.find(phrase, start + 1)
    return hits


def nearest(doc, phrase):
    """Where an absent phrase nearly stands: (line, note)."""
    best, low, high = 0, 1, len(phrase)
    while low <= high:
        middle = (low + high) // 2
        if find_all(doc.norm, phrase[:middle]):
            best, low = middle, middle + 1
        else:
            high = middle - 1
    if best < 12:
        return 1, "no part of it stands in the file"
    pos = find_all(doc.norm, phrase[:best])[0]
    got = doc.norm[pos + best:pos + best + 40]
    want = phrase[best:best + 40]
    return doc.line_at(pos), 'nearest text: after "...%s" the file has "%s", the phrase has "%s"' % (
        phrase[max(0, best - 30):best], got, want)


def group_of(rel):
    parts = rel.split("/")
    if parts[0] == "skills" and len(parts) > 2:
        return parts[1]
    if parts[0] == "examples":
        return "examples"
    if rel in ("WORKFLOW.md", "workflow.html") or parts[0] == "diagrams":
        return "doc"
    if parts[0] == "profiles":
        return "template"
    return "root-files"


class Run:
    def __init__(self, tree, problems, skills_dir):
        self.tree = tree
        self.problems = problems
        self.skills_dir = skills_dir
        self.fails = []

    def fail(self, rel, line, text):
        """Record one failure. `rel` is a path of the public tree, or a Doc, or None."""
        if isinstance(rel, Doc):
            doc = rel
            self.fails.append((group_of(doc.rel), "%s:%d" % (doc.shown, line), text))
        elif rel in self.tree:
            doc = self.tree[rel]
            self.fails.append((group_of(rel), "%s:%d" % (doc.shown, line), text))
        else:
            self.fails.append((group_of(rel) if rel else "root-files", "%s:%d" % (rel, line), text))

    def need(self, rel):
        """The Doc of a file that must exist, or None with a failure."""
        doc = self.tree.get(rel)
        if doc is None:
            self.fails.append((group_of(rel), "%s:0" % rel, "the file is not in the public tree"))
        return doc

    def under(self, prefix, suffix=""):
        return [doc for rel, doc in sorted(self.tree.items())
                if rel.startswith(prefix) and rel.endswith(suffix)]


# ---------------------------------------------------------------------------
# The ten checks
# ---------------------------------------------------------------------------


def check_1(run):
    """The fixed phrases."""
    for rel, names in CHECK1:
        doc = run.need(rel)
        if doc is None:
            continue
        for name in names:
            if not find_all(doc.norm, P[name]):
                line, note = nearest(doc, P[name])
                run.fail(doc, line, "%s is absent; %s" % (name, note))
    doc = run.tree.get("skills/prototype/SKILL.md")
    if doc is None:
        return
    for string in NO_LOOKUP:
        hits = find_all_any_case(doc.norm, string)
        if string in ("the repo guide", "AGENTS.md", "CLAUDE.md"):
            if len(hits) != 1:
                lines = ", ".join(str(doc.line_at(pos)) for pos in hits) or "none"
                run.fail(doc, doc.line_at(hits[-1]) if hits else 1,
                         '"%s" stands %d times, not once (lines: %s)' % (string, len(hits), lines))
        else:
            for pos in hits:
                run.fail(doc, doc.line_at(pos), 'the lookup string "%s" stands here' % string)


def check_2(run):
    """The block."""
    for skill, (act, sections) in BLOCK_ROWS.items():
        doc = run.need("skills/%s/SKILL.md" % skill)
        if doc is None:
            continue
        want = BLOCK.replace("<act>", act).replace("<sections>", sections)
        start = doc.frontmatter_end()
        heading = next((index for index in range(start, len(doc.lines))
                        if doc.lines[index].startswith("## ")), None)
        if heading is None:
            run.fail(doc, 1, "no line starts with `## ` after the frontmatter")
            continue
        if doc.lines[heading] != "## Project rules":
            run.fail(doc, heading + 1, "the first `## ` line is %r, not `## Project rules`"
                     % doc.lines[heading])
            continue
        index = heading + 1
        while index < len(doc.lines) and doc.lines[index].strip() == "":
            index += 1
        numbered = []
        while index < len(doc.lines) and doc.lines[index].strip() != "":
            numbered.append((index + 1, doc.lines[index]))
            index += 1
        if not numbered:
            run.fail(doc, heading + 1, "no paragraph stands under `## Project rules`")
            continue
        para = Para(numbered)
        if para.text != want:
            same = 0
            while same < min(len(para.text), len(want)) and para.text[same] == want[same]:
                same += 1
            run.fail(doc, para.line_at(same),
                     'the block differs after "...%s": the file has "%s", the fixed text has "%s"'
                     % (want[max(0, same - 30):same], para.text[same:same + 40],
                        want[same:same + 40]))


def check_3(run):
    """The repo guide is defined."""
    for doc in run.under("skills/", ".md"):
        for para in doc.paras:
            hits = find_all_any_case(para.text, "the repo guide")
            if not hits:
                continue
            if "`AGENTS.md`, else `CLAUDE.md`" not in para.text:
                run.fail(doc, para.line_at(hits[0]),
                         "the paragraph of the first `the repo guide` holds no "
                         "`` `AGENTS.md`, else `CLAUDE.md` ``")
            break


def check_4(run):
    """Retired strings."""
    for doc in run.under("skills/"):
        for string in RETIRED:
            for pos in find_all_exact(doc.norm, string):
                run.fail(doc, doc.line_at(pos), "the retired string %s stands here" % string)
    for doc in run.under(""):
        for string in RETIRED_TREE:
            for pos in find_all(doc.norm, string):
                run.fail(doc, doc.line_at(pos), "the retired string %s stands here" % string)


def find_all_exact(hay, string):
    hits, start = [], hay.find(string)
    while start >= 0:
        hits.append(start)
        start = hay.find(string, start + 1)
    return hits


def check_5(run):
    """`adr/`."""
    domain = "skills/domain-modeling/SKILL.md"
    for doc in run.under("skills/", ".md"):
        if doc.rel.count("/") < 2 or doc.rel == "skills/pr/CREDITS.md":
            continue
        fenced = doc.fenced() if doc.rel == domain else set()
        for para in doc.paras:
            for pos in find_all_exact(para.text, "adr/"):
                before, after = para.text[:pos], para.text[pos + 4:]
                if before.endswith("default: `") and after.startswith("` where it exists"):
                    continue
                line = para.line_at(pos)
                if doc.rel == domain:
                    sentence = para.sentence_at(pos)
                    if (line in fenced or sentence.startswith("Never create the ADR folder")
                            or "no point and no" in sentence):
                        continue
                run.fail(doc, line, "`adr/` stands here, and it is not one of the four allowed cases")


def check_6(run):
    """No lookup."""
    docs = [run.need(rel) for rel in ("skills/slice-build/BRIEFS.md", "skills/prototype/LOGIC.md",
                                      "skills/prototype/UI.md")]
    docs += run.under("skills/grilling/") + run.under("skills/research/")
    for doc in docs:
        if doc is None:
            continue
        for string in NO_LOOKUP:
            for pos in find_all_any_case(doc.norm, string):
                run.fail(doc, doc.line_at(pos), 'the lookup string "%s" stands here' % string)


def check_7(run):
    """Names, branches, dashes."""
    long_names = re.compile(r"(?<![\w\-/])(%s)(?![\w\-/])" % "|".join(map(re.escape, NAMES_LONG)))
    span_names = re.compile(r"(?<!`)(`+)(/?)(%s)\1(?!`)" % "|".join(NAMES_SPAN))
    name_line = re.compile(r"name:\s*(%s)\s*$" % "|".join(map(re.escape, SKILLS)))
    docs = run.under("skills/")
    examples = [run.need(rel) for rel in ("examples/openspec-config.yaml", "examples/verify.md")]
    for doc in docs + [doc for doc in examples if doc]:
        front = doc.frontmatter_end()
        for index, line in enumerate(doc.lines):
            if index < front and name_line.match(line):
                continue
            for match in long_names.finditer(line):
                if not line[:match.start()].endswith(PREFIX):
                    run.fail(doc, index + 1,
                             "the skill name `%s` stands without `%s`" % (match.group(1), PREFIX))
            for match in span_names.finditer(line):
                if (doc.rel == "skills/prototype/UI.md" and match.group(2) == ""
                        and match.group(3) == "prototype"):
                    continue
                run.fail(doc, index + 1, "the code span %s is a bare skill name" % match.group(0))
    url = re.compile(r"https?://[^\s)\]\"'>]*")
    branch = re.compile(r"\b(?:[Mm]ain|[Mm]aster)\b")
    for doc in docs:
        # The one place that may name `main` and `master`: the section of CHECKS.md that
        # finds the default branch.
        skip_from = skip_to = -1
        if doc.rel == "skills/slice-build/CHECKS.md":
            skip_from = next((i for i, l in enumerate(doc.lines) if l == "## Default branch"), -1)
            skip_to = next((i for i, l in enumerate(doc.lines)
                            if i > skip_from >= 0 and l.startswith("## ")), len(doc.lines))
        for index, line in enumerate(doc.lines):
            if skip_from <= index < skip_to:
                continue
            for match in branch.finditer(url.sub("", line)):
                run.fail(doc, index + 1, "the branch name `%s` stands here" % match.group(0))
    for doc in run.under(""):
        for index, line in enumerate(doc.lines):
            if "\u2014" in line:
                run.fail(doc, index + 1, "U+2014 (em-dash) stands here")


def exact_line(doc, text):
    return next((index + 1 for index, line in enumerate(doc.lines) if line == text), None)


def md_links(doc):
    """The link targets of a Markdown file: (line, target). Code is left out.

    A link text may wrap over lines, so the search reads the whole file.
    """
    fenced = doc.fenced()
    masked = []
    for number, line in enumerate(doc.lines, 1):
        if number in fenced:
            masked.append("")
        else:
            masked.append(re.sub(r"`+[^`]*`+", lambda m: " " * len(m.group(0)), line))
    text = "\n".join(masked)
    patterns = (
        re.compile(r"\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)"),
        re.compile(r"^ {0,3}\[[^\]]+\]:\s*<?([^\s>]+)>?", re.MULTILINE),
        re.compile(r"\b(?:src|href)=\"([^\"]+)\""),
    )
    found = []
    for pattern in patterns:
        for match in pattern.finditer(text):
            found.append((text.count("\n", 0, match.start(1)) + 1, match.group(1)))
    return sorted(found)


def resolve(doc, target):
    """The path in the public tree that a relative link target names, and its anchor."""
    path, _, anchor = target.partition("#")
    path = unquote(path)
    if path == "":
        return doc.rel, anchor
    return posixpath.normpath(posixpath.join(posixpath.dirname(doc.rel), path)), anchor


def check_8(run):
    """What another file names exists."""
    doc = run.need("skills/slice-build/SKILL.md")
    if doc:
        for heading in ("## Before the first slice", "## After the last slice",
                        "## After verify"):
            if exact_line(doc, heading) is None:
                run.fail(doc, 1, "no line is exactly `%s`" % heading)
    run.need("skills/codebase-design/DEEPENING.md")
    doc = run.need("skills/slice-build/CHECKS.md")
    if doc and exact_line(doc, "## Test lock at verify") is None:
        run.fail(doc, 1, "no line is exactly `## Test lock at verify`")
    doc = run.need("skills/slice-build/BRIEFS.md")
    if doc:
        for string in ("Bugs fixed", "Bugs left"):
            if string not in doc.norm:
                run.fail(doc, 1, "`%s` is absent" % string)
    doc = run.need("skills/pr/SKILL.md")
    if doc:
        for heading in ("## Squash footer", "## The body", "## Merge"):
            if exact_line(doc, heading) is None:
                run.fail(doc, 1, "no line is exactly `%s`" % heading)
        if "gh pr merge <n> --squash --body-file <file>" not in doc.norm:
            run.fail(doc, 1, "`gh pr merge <n> --squash --body-file <file>` is absent")
    targets = ("examples/project-rules.md", "examples/verify.md", "profiles/TEMPLATE.md")
    for rel in targets:
        run.need(rel)
    doc = run.need("WORKFLOW.md")
    if doc:
        linked = {resolve(doc, target)[0] for _, target in md_links(doc)
                  if not re.match(r"[a-z][a-z0-9+.-]*:", target)}
        for rel in targets:
            if rel not in linked:
                run.fail(doc, 1, "no link points at `%s`" % rel)
    doc = run.need("examples/openspec-config.yaml")
    if doc:
        for string in ["Test files:", "Slice check:", "Test check:", "idea-to-code:slice-build",
                       "idea-to-code:owner-gate"] + GATE_LINES:
            if string not in doc.norm:
                run.fail(doc, 1, "`%s` is absent" % string)
    doc = run.tree.get("examples/verify.md")
    if doc:
        for string in ("idea-to-code:code-review", "/idea-to-code:verify"):
            if string not in doc.norm:
                run.fail(doc, 1, "`%s` is absent" % string)
    for rel, names in (
            ("examples/project-rules.md", ["NONE", "NONE-BAN"]),
            ("WORKFLOW.md", ["NAMES", "CMD-NAMES", "VERIFY-LINE", "COUNT", "ROUTING", "BUILD-LINE"]),
            ("README.md", ["NAMES", "CMD-NAMES", "VERIFY-LINE", "COUNT", "CLAUDE-MD", "BUILD-LINE"]),
            ("skills/CREDITS.md", ["COUNT"])):
        # The lines above report the first two files when they are absent.
        doc = run.need(rel) if rel in ("README.md", "skills/CREDITS.md") else run.tree.get(rel)
        if doc is None:
            continue
        for name in names:
            if not find_all(doc.norm, P[name]):
                line, note = nearest(doc, P[name])
                run.fail(doc, line, "%s is absent; %s" % (name, note))
    # Check b reports a manifest that is absent or is not JSON.
    doc = run.tree.get(".claude-plugin/plugin.json")
    if doc:
        try:
            description = json.loads(doc.text).get("description")
        except (ValueError, AttributeError):
            description = None
        if isinstance(description, str) and not find_all(description, P["COUNT"]):
            line = next((index + 1 for index, text in enumerate(doc.lines)
                         if '"description"' in text), 1)
            run.fail(doc, line, "COUNT is absent from the `description`")


def check_9(run):
    """No leak."""
    patterns = [re.compile(source, re.IGNORECASE)
                for source in LEAK9 + [regex for _, regex in PRIVATE_PATTERNS]]
    names = handles(run.tree)
    for doc in run.under(""):
        for index, line in enumerate(doc.lines):
            hits = []
            for pattern in patterns:
                for match in pattern.finditer(line):
                    if allowed(line, match.start(), match.end(), names, PRIVATE_ALLOW):
                        continue
                    hits.append(match.group(0))
            if hits:
                run.fail(doc, index + 1, "the leak pattern finds: %s" % ", ".join(sorted(set(hits))))
    names = set(run.tree)
    for rel in sorted(names):
        parts = rel.split("/")
        if parts[-1] == "PLUGIN.md":
            run.fail(rel, 0, "the public tree holds a `PLUGIN.md`")
        if parts[0] == "profiles" and rel != "profiles/TEMPLATE.md":
            run.fail(rel, 0, "`profiles/` holds a file other than `TEMPLATE.md`")
        if "commands" in parts[1:-1]:
            run.fail(rel, 0, "the public tree holds a `commands/` folder")
    for folder in ("commands",):
        if run.skills_dir.parent.joinpath(folder).exists():
            run.fail(folder + "/", 0, "the public tree holds a `%s/` folder" % folder)
    found = sorted(path.name for path in run.skills_dir.iterdir() if path.is_dir()) \
        if run.skills_dir.is_dir() else []
    wanted = sorted(SKILLS + COMMANDS)
    if found != wanted:
        extra = sorted(set(found) - set(wanted))
        missing = sorted(set(wanted) - set(found))
        run.fail("skills/", 0, "`skills/` does not hold exactly the sixteen folders (extra: %s; "
                 "missing: %s)" % (", ".join(extra) or "none", ", ".join(missing) or "none"))
    for problem in run.problems:
        run.fail(None, 0, problem)


def check_10(run):
    """The step commands."""
    for command in COMMANDS:
        folder = "skills/%s/" % command
        rel = folder + "SKILL.md"
        for other in sorted(run.tree):
            if other.startswith(folder) and other != rel:
                run.fail(other, 0,
                         "the folder of a step command holds a file other than `SKILL.md`")
        on_disk = run.skills_dir / command
        if on_disk.is_dir():
            for path in sorted(on_disk.iterdir()):
                if path.is_dir():
                    run.fail(folder + path.name + "/", 0,
                             "the folder of a step command holds a folder")
        doc = run.need(rel)
        if doc is None:
            continue
        # The frontmatter.
        end = doc.frontmatter_end()
        if end == 0:
            run.fail(doc, 1, "the file does not start with a frontmatter")
        front = [(index + 1, doc.lines[index]) for index in range(1, max(end - 1, 1))]
        if end:
            for field in ("description:", "argument-hint:"):
                if not any(line.startswith(field) for _, line in front):
                    run.fail(doc, 1, "the frontmatter holds no `%s` line" % field)
            for number, line in front:
                if line.startswith("name:"):
                    run.fail(doc, number, "the frontmatter holds a `name:` line")
        # The lock.
        lock = [(number, line) for number, line in front
                if line.startswith("disable-model-invocation")]
        if command in LOCKED:
            if end and not any(line.rstrip() == "disable-model-invocation: true"
                               for _, line in lock):
                run.fail(doc, 1, "the frontmatter does not hold the line "
                         "`disable-model-invocation: true`, and the LOCKED list locks this command")
        else:
            for number, _ in lock:
                run.fail(doc, number, "a line starts with `disable-model-invocation`, and the "
                         "LOCKED list does not lock this command")
        # The body.
        body = squeeze((index + 1, doc.lines[index]) for index in range(end, len(doc.lines)))[0]
        if "$ARGUMENTS" not in body:
            run.fail(doc, end + 1, "`$ARGUMENTS` is absent from the body")
        if not find_all(body, P["GUIDE"]):
            line, note = nearest(doc, P["GUIDE"])
            run.fail(doc, line, "GUIDE is absent from the body; %s" % note)
        for pos in find_all_exact(doc.norm, "## Project rules"):
            run.fail(doc, doc.line_at(pos), "`## Project rules` stands here")
        # The strings.
        for name in CHECK10[command]:
            if name in P:
                if not find_all(doc.norm, P[name]):
                    line, note = nearest(doc, P[name])
                    run.fail(doc, line, "%s is absent; %s" % (name, note))
            elif name not in doc.norm:
                run.fail(doc, 1, "`%s` is absent" % name)


# ---------------------------------------------------------------------------
# The three more checks
# ---------------------------------------------------------------------------


def check_a(run):
    """The wide leak grep, with its allow list."""
    patterns = [(label, re.compile(source, re.IGNORECASE))
                for label, source in LEAK_A + PRIVATE_PATTERNS]
    names = handles(run.tree)
    for doc in run.under(""):
        for index, line in enumerate(doc.lines):
            hits = []
            for label, pattern in patterns:
                for match in pattern.finditer(line):
                    if allowed(line, match.start(), match.end(), names, PRIVATE_ALLOW):
                        continue
                    hits.append("%s `%s`" % (label, match.group(0)))
            if hits:
                run.fail(doc, index + 1, "leak: %s" % ", ".join(sorted(set(hits))))


def check_b(run):
    """The JSON manifests."""
    wanted = {
        ".claude-plugin/plugin.json": [
            (("name",), "idea-to-code"), (("version",), "0.1.0"), (("license",), "MIT"),
            (("author", "name"), None), (("description",), None),
        ],
        ".claude-plugin/marketplace.json": [
            (("name",), "idea-to-code"), (("owner", "name"), None),
            (("plugins", 0, "name"), "idea-to-code"), (("plugins", 0, "source"), None),
        ],
    }

    def line_of(doc, needle):
        return next((index + 1 for index, line in enumerate(doc.lines) if needle in line), 1)

    def strings(value, key="(root)"):
        if isinstance(value, dict):
            for name, item in value.items():
                yield "key", name
                yield from strings(item, name)
        elif isinstance(value, list):
            for item in value:
                yield from strings(item, key)
        elif isinstance(value, str):
            yield key, value

    for rel, fields in wanted.items():
        doc = run.need(rel)
        if doc is None:
            continue
        try:
            data = json.loads(doc.text)
        except ValueError as error:
            run.fail(doc, getattr(error, "lineno", 1), "the file is not JSON: %s" % error)
            continue
        for key, string in strings(data):
            if string.strip() == "":
                run.fail(doc, line_of(doc, '"%s"' % key), "the value of `%s` is empty" % key)
            elif PLACEHOLDER.search(string):
                run.fail(doc, line_of(doc, string[:20]),
                         "a placeholder stands in `%s`: %s" % (key, string[:60]))
        for path, want in fields:
            value = data
            try:
                for step in path:
                    value = value[step]
            except (KeyError, IndexError, TypeError):
                run.fail(doc, 1, "the field `%s` is absent" % ".".join(map(str, path)))
                continue
            if want is not None and value != want:
                run.fail(doc, line_of(doc, '"%s"' % path[-1]),
                         "the field `%s` is %r, not %r" % (".".join(map(str, path)), value, want))
    pair = [handles({rel: run.tree[rel]}) for rel in wanted if rel in run.tree]
    if len(pair) == 2 and pair[0] != pair[1]:
        run.fail(".claude-plugin/plugin.json", 1, "the author of plugin.json and the owner of "
                 "marketplace.json are not the same name")


def slug(heading):
    """The anchor that GitHub gives a Markdown heading."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    text = re.sub(r"[`*]", "", text).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(doc):
    found = set()
    if doc.rel.endswith(".md"):
        fenced, seen = doc.fenced(), {}
        for number, line in enumerate(doc.lines, 1):
            match = re.match(r" {0,3}#{1,6}\s+(.*?)\s*#*\s*$", line)
            if number in fenced or not match:
                continue
            base = slug(match.group(1))
            count = seen.get(base, 0)
            seen[base] = count + 1
            found.add(base if count == 0 else "%s-%d" % (base, count))
    found.update(re.findall(r"\b(?:id|name)=\"([^\"]+)\"", doc.text))
    return found


def check_c(run):
    """Relative links resolve in the public tree."""
    folders = {posixpath.dirname(rel) for rel in run.tree}
    folders |= {folder[:end] for folder in folders for end in range(len(folder)) if folder[end] == "/"}
    cache = {}
    for rel in ("WORKFLOW.md", "README.md", "profiles/TEMPLATE.md"):
        doc = run.need(rel)
        if doc is None:
            continue
        for number, target in md_links(doc):
            if re.match(r"[a-z][a-z0-9+.-]*:", target, re.IGNORECASE) or target.startswith("//"):
                continue
            path, anchor = resolve(doc, target)
            if path.startswith("..") or path.startswith("/"):
                run.fail(doc, number, "the link `%s` points outside the public tree" % target)
                continue
            if path not in run.tree:
                if path.rstrip("/") not in folders:
                    run.fail(doc, number, "the link `%s` points at `%s`, which is not in the "
                             "public tree" % (target, path))
                continue
            if anchor and (path.endswith(".md") or path.endswith(".html")):
                if path not in cache:
                    cache[path] = anchors(run.tree[path])
                if unquote(anchor) not in cache[path]:
                    run.fail(doc, number, "the link `%s` names an anchor that `%s` does not have"
                             % (target, path))


CHECKS = [
    ("check 1", check_1), ("check 2", check_2), ("check 3", check_3), ("check 4", check_4),
    ("check 5", check_5), ("check 6", check_6), ("check 7", check_7), ("check 8", check_8),
    ("check 9", check_9), ("check 10", check_10),
    ("check a", check_a), ("check b", check_b), ("check c", check_c),
]


def main(argv):
    global PRIVATE_PATTERNS, PRIVATE_ALLOW
    tree_dir = None
    if len(argv) == 3 and argv[1] == "--tree":
        tree_dir = Path(argv[2]).resolve()
        if not tree_dir.is_dir():
            print("FAIL  args     %s is not a folder" % tree_dir)
            return 1
    elif len(argv) != 1:
        print("usage: python3 -I -B maintainer/check_tree.py [--tree DIR]")
        return 2
    PRIVATE_PATTERNS, PRIVATE_ALLOW, info = load_private()
    tree, problems, skills_dir = build_tree(tree_dir)
    print("# tree: %s, %d files" % (tree_dir or "the repo root", len(tree)))
    print(info)
    failed = total = 0
    for name, function in CHECKS:
        run = Run(tree, problems, skills_dir)
        function(run)
        title = function.__doc__.strip().splitlines()[0].rstrip(".")
        if not run.fails:
            print("PASS  %-8s %s" % (name, title))
            continue
        failed += 1
        total += len(run.fails)
        for group, place, text in run.fails:
            print("FAIL  %-8s [%s] %s  %s" % (name, group, place, text))
    print("# %d checks, %d failed, %d failures" % (len(CHECKS), failed, total))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
