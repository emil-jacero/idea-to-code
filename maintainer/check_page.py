"""Check workflow.html against WORKFLOW.md and diagrams/. Reads only; writes nothing.

Usage: python3 -I maintainer/check_page.py [page]

By default the script reads workflow.html, WORKFLOW.md and diagrams/ at the repo
root, the parent of `maintainer/`. An optional path names another page.

An optional file, `maintainer/private-words.txt` (git-ignored), adds a
maintainer's own search words to the leak check. One line per word:
`<label><TAB><regex>`. A line that starts with `#` is a comment. A label that
starts with `tree:` is for the tree checker only. The label `allow` marks a hit
that is fine: its regex matches the page text around the hit marked `<<hit>>`.

Prints one line per check (PASS or FAIL with the details) and exits 1 if any
check fails.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PAGE = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "workflow.html"
PRIVATE = HERE / "private-words.txt"
LIMIT = 4900
STYLE = re.compile(r"<style>.*?</style>", re.S)

SKIP = {"svg", "style", "script", "title"}


class Counter(HTMLParser):
    """Count the words outside SVG, style, script and title; inside <main> when it exists."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.in_main = 0
        self.saw_main = False
        self.all_text = []
        self.main_text = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        if tag == "main":
            self.in_main += 1
            self.saw_main = True

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag == "main" and self.in_main:
            self.in_main -= 1

    def handle_data(self, data):
        if self.skip:
            return
        self.all_text.append(data)
        if self.in_main:
            self.main_text.append(data)


def count_words(path):
    parser = Counter()
    with open(path, encoding="utf-8") as handle:
        parser.feed(handle.read())
    text = parser.main_text if parser.saw_main else parser.all_text
    return len(" ".join(text).split())


def load_private():
    """Read the private file. Returns (patterns, allow rules, info line)."""
    if not PRIVATE.is_file():
        return [], [], ("# private words: none (%s is absent), only the generic checks run"
                        % PRIVATE.name)
    patterns, allow = [], []
    for number, line in enumerate(PRIVATE.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        label, _, regex = line.partition("\t")
        if not regex:
            print(f"FAIL  private  {PRIVATE.name}:{number} is not `<label><TAB><regex>`")
            sys.exit(1)
        try:
            re.compile(regex, re.I)
        except re.error as error:
            print(f"FAIL  private  {PRIVATE.name}:{number} bad regex: {error}")
            sys.exit(1)
        if label == "allow":
            allow.append(regex)
        elif not label.startswith("tree:"):
            patterns.append((label.removeprefix("page:"), regex))
    return patterns, allow, f"# private words: {len(patterns)} patterns, {len(allow)} allow rules from {PRIVATE.name}"


PRIVATE_PATTERNS, PRIVATE_ALLOW, PRIVATE_INFO = load_private()
print(PRIVATE_INFO)

page = PAGE.read_text(encoding="utf-8")
md = (REPO / "WORKFLOW.md").read_text(encoding="utf-8")
results = []


def report(name, problems, info=""):
    results.append(not problems)
    head = "PASS" if not problems else "FAIL"
    print(f"{head}  {name}" + (f"  ({info})" if info else ""))
    for p in problems[:40]:
        print("      -", p)


def anchor(title):
    """GitHub's rule for the anchor of a heading."""
    t = title.strip().lower().replace(" ", "-")
    return re.sub(r"[^\w-]", "", t)


def headings():
    out, seen, fence = [], {}, False
    for line in md.splitlines():
        if line.startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        m = re.match(r"^(#{1,6}) (.+?)\s*$", line)
        if not m:
            continue
        a = anchor(m.group(2))
        if a in seen:
            seen[a] += 1
            a = f"{a}-{seen[a]}"
        else:
            seen[a] = 0
        out.append((a, m.group(2)))
    return out


class Walker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.hrefs, self.srcs, self.tags = [], [], [], []
        self.svg_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "svg":
            self.svg_depth += 1
        if "id" in a:
            self.ids.append((a["id"], self.svg_depth > 0))
        if a.get("href", "").startswith("#"):
            self.hrefs.append(a["href"][1:])
        if "data-src" in a:
            self.srcs.extend(a["data-src"].split())

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "svg":
            self.svg_depth -= 1

    def handle_endtag(self, tag):
        if tag == "svg" and self.svg_depth:
            self.svg_depth -= 1


w = Walker()
w.feed(page)
heads = headings()
anchors = [a for a, _ in heads]
ids = [i for i, _ in w.ids]

# 1. words outside SVG
words = count_words(str(PAGE))
report("words outside SVG", [] if words <= LIMIT else [f"{words} > {LIMIT}"], f"{words} of {LIMIT}")

# 2. each heading anchor is an id exactly once
probs = [f"{a}: {ids.count(a)} times" for a in anchors if ids.count(a) != 1]
report("heading anchors as ids, once each", probs, f"{len(anchors)} anchors")

# 2b. no id twice anywhere (page and figures)
dup = sorted({i for i in ids if ids.count(i) > 1})
report("no id used twice", [f"{i}: {ids.count(i)} times" for i in dup], f"{len(ids)} ids")

# 3. every in-page link resolves
idset = set(ids)
report("every href=\"#...\" resolves", sorted({h for h in w.hrefs if h not in idset}), f"{len(w.hrefs)} links")

# 4. every data-src names a heading anchor
aset = set(anchors)
report("every data-src names a heading", sorted({s for s in w.srcs if s not in aset}), f"{len(w.srcs)} anchors in data-src")

# 5. no details element
report("no details element", ["details found"] if re.search(r"<details\b", page, re.I) else [])

# 6. no colour outside the token blocks
styles = re.findall(r"<style>(.*?)</style>", page, re.S)
probs = []
if len(styles) != 1:
    probs.append(f"{len(styles)} style elements")
css = styles[0] if styles else ""
css_wo = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
blocks = [
    re.compile(r"^:root \{[^}]*\}", re.M),
    re.compile(r"@media \(prefers-color-scheme: dark\) \{\s*:root:not\(\[data-theme=\"light\"\]\) \{[^}]*\}\s*\}"),
    re.compile(r":root\[data-theme=\"dark\"\] \{[^}]*\}"),
]
rest = css_wo
for b in blocks:
    found = b.findall(rest)
    if len(found) != 1:
        probs.append(f"token block {b.pattern[:40]!r} found {len(found)} times")
    rest = b.sub("", rest)
NAMED = ("white black red green blue gray grey silver maroon purple fuchsia lime olive yellow navy "
         "teal aqua orange pink brown gold beige ivory tan crimson coral salmon khaki violet indigo "
         "plum orchid lavender cyan magenta").split()
colour = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\(|(?<![-\w])(?:" +
                    "|".join(NAMED) + r")(?![-\w])", re.I)
for m in colour.finditer(rest):
    line = rest[:m.start()].count("\n")
    probs.append(f"style: {m.group(0)!r} near {rest[max(0, m.start() - 40):m.end() + 10]!r}")
body = STYLE.sub("", page)
for m in re.finditer(r"\b(fill|stroke|color|stop-color|bgcolor)=\"([^\"]*)\"", body):
    if m.group(2) not in ("none", "currentColor"):
        probs.append(f"attribute {m.group(0)}")
if re.search(r"\sstyle=", body):
    probs.append("a style attribute")
report("no colour outside the token blocks", probs)

# 7. no em-dash or en-dash
probs = []
for ch, name in (("\u2014", "em-dash"), ("\u2013", "en-dash")):
    if ch in page:
        probs.append(f"{name} x{page.count(ch)}")
for ent in ("&mdash;", "&ndash;", "&#8212;", "&#8211;", "&#x2014;", "&#x2013;"):
    if ent in page.lower():
        probs.append(ent)
report("no em-dash or en-dash", probs)

# 8. no private word: local paths, email addresses, and the words of the private file
LOCAL_PATH = r"/var/home|/home/|(?-i:/Users/)|(?<![\w.])~/|file://|\b[A-Za-z]:\\"
EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"
scan = re.sub(r"/\*.*?\*/", " ", page, flags=re.S)
probs = []
for label, source in [("local path", LOCAL_PATH), ("email address", EMAIL)] + PRIVATE_PATTERNS:
    for m in re.finditer(source, scan, re.I):
        marked = f"{scan[max(0, m.start() - 40):m.start()]}<<{m.group(0)}>>{scan[m.end():m.end() + 40]}"
        if any(re.search(rule, marked, re.I) for rule in PRIVATE_ALLOW):
            continue
        probs.append(f"{label}: {m.group(0)!r}")
report("no private word", sorted(set(probs)))

# 8b. no version number outside SVG except the date of the status line and OpenSpec 2.x
outside = re.sub(r"<svg\b.*?</svg>", " ", body, flags=re.S)
outside_text = re.sub(r"<[^>]+>", " ", outside)
vers = [v for v in re.findall(r"\b\d+\.\d+(?:\.\d+)?\b", outside_text)]
report("no version number", vers, "OpenSpec 2.x allowed")

# 9. the page frame: a full document, and one small script last inside the body
probs = []
if not page.startswith("<!doctype html>\n"):
    probs.append("does not start with <!doctype html>")
for t in ("html", "head", "body"):
    n = len(re.findall(r"<\s*" + t + r"\b", page, re.I))
    c = len(re.findall(r"<\s*/\s*" + t + r"\s*>", page, re.I))
    if n != 1 or c != 1:
        probs.append(f"<{t}> opens {n} times and closes {c} times, once each is required")
if len(re.findall(r"<!doctype", page, re.I)) != 1:
    probs.append("not exactly one doctype")
if not re.search(r'<html lang="[a-z-]+">', page):
    probs.append("<html> has no lang")
m_head = re.search(r"<head>(.*?)</head>", page, re.S)
head = m_head.group(1) if m_head else ""
if not re.search(r'<meta charset="utf-8">', head):
    probs.append('head has no <meta charset="utf-8">')
if not re.search(r'<meta name="viewport" content="width=device-width, initial-scale=1">', head):
    probs.append("head has no viewport meta")
if len(re.findall(r"<title>[^<]+</title>", head)) != 1:
    probs.append("head does not hold exactly one title")
if re.search(r"<meta\b[^>]*\bclaude:", page, re.I):
    probs.append("a claude: meta tag")
if not re.match(r'<!doctype html>\n<html lang="[a-z-]+">\n<head>\n', page):
    probs.append("the page does not start with the doctype, <html lang> and <head> on lines of their own")
if "</head>\n<body>\n" not in page:
    probs.append("</head> is not followed directly by <body>")
# one small inline script is allowed (for views and marks): it is the last
# thing inside the body, has no attribute, is under 80 lines and uses no network or storage
scripts = re.findall(r"<script\b([^>]*)>(.*?)</script>", page, re.S | re.I)
if len(scripts) != 1 or len(re.findall(r"<script\b", page, re.I)) != len(scripts):
    probs.append(f"{len(re.findall(r'<script\b', page, re.I))} script elements, exactly one required")
if not re.search(r"</script>\n</body>\n</html>\n?$", page):
    probs.append("the script is not the last thing inside the body")
for attrs, code in scripts:
    if attrs.strip():
        probs.append(f"script with attributes {attrs.strip()!r}")
    if len(code.strip().splitlines()) >= 80:
        probs.append(f"script of {len(code.strip().splitlines())} lines, under 80 allowed")
    for api in ("fetch(", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon", "import(",
                "localStorage", "sessionStorage", "indexedDB", "document.cookie", "src="):
        if api in code:
            probs.append(f"script uses {api}")
for m in re.finditer(r"\b(?:href|src)=\"(https?:[^\"]+)\"", page):
    u = m.group(1)
    if not (u.startswith("https://fonts.googleapis.com/") or u == "https://github.com/mattpocock/skills"):
        probs.append(f"external {u}")
report("page frame: doctype, html lang, head with charset, viewport and title, body, one small script last", probs)

# 10. every inline figure equals its file but for the style element; seven, once each
fig_names = sorted(p.stem for p in (REPO / "diagrams").glob("*.svg"))
inline = re.findall(r"(<svg xmlns=\"http://www.w3.org/2000/svg\" class=\"dg\".*?</svg>\n)", page, re.S)
probs, seen = [], []
for s in inline:
    m = re.search(r'aria-labelledby="([a-z0-9-]+)-title', s)
    name = m.group(1) if m else "?"
    seen.append(name)
    want = STYLE.sub("", (REPO / "diagrams" / f"{name}.svg").read_text(encoding="utf-8"))
    if s != want:
        probs.append(f"{name}: differs from diagrams/{name}.svg")
for n in fig_names:
    if seen.count(n) != 1:
        probs.append(f"{n}: {seen.count(n)} copies")
for n in seen:
    if n not in fig_names:
        probs.append(f"{n}: no file")
if "<!-- figure:" in page:
    probs.append("a figure placeholder is left")
report("inline figures equal their files (style element removed)", probs, f"{len(inline)} figures")

# 10b. each figcaption is the caption of WORKFLOW.md, word for word
paras = re.split(r"\n\s*\n", md)
caps = {}
for i, para in enumerate(paras):
    m = re.fullmatch(r"!\[[^\]]*\]\(diagrams/([a-z0-9-]+)\.svg\)", para.strip(), re.S)
    if m:
        caps[m.group(1)] = " ".join(paras[i + 1].split())[len("*Figure:* "):]
probs = []
for fig in re.findall(r"<figure class=\"figure\".*?</figure>", page, re.S):
    m = re.search(r'aria-labelledby="([a-z0-9-]+)-title', fig)
    c = re.search(r"<figcaption>(.*?)</figcaption>", fig, re.S)
    if not m or not c:
        probs.append("a figure without an inline svg or a caption")
        continue
    if c.group(1) != caps.get(m.group(1)):
        probs.append(f"{m.group(1)}: caption {c.group(1)!r}")
report("captions word for word", probs, f"{len(caps)} in WORKFLOW.md")

ok = all(results)
print("ALL PASS" if ok else "SOME CHECKS FAIL")
sys.exit(0 if ok else 1)
