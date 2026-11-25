# Idea to Code

Idea to Code is a way to take an idea to merged code with a coding agent. This repo holds the flow
as one Markdown document, the same flow as a page, the skills and the step commands that run it,
and the template of a project's profile. The skills and the four step commands ship as one Claude
Code plugin, `idea-to-code`.

> **Status:** no version number: each commit on `main` is a new version, and an update
> installs it. The flow is new. It was tried only in toy repos: a toy trial ran
> explore to verify, end to end, on 2026-11-24. No real change has gone through it yet.
> [WORKFLOW.md](WORKFLOW.md) has an "as of" line that says how far it was used.

**What it needs.** Claude Code with plugin support (checked on Claude Code 2.1.331), OpenSpec 2.x
(checked on OpenSpec 2.1.1) and git (checked on git 2.56.0).

**Open the page.** GitHub shows `workflow.html` as source. To read it as a page, download the file
or clone this repo, and open the file in a browser.
The page loads its fonts from Google Fonts, and it falls back to system fonts when offline.

**Words used here.**

- The *owner* is the person who runs the flow and answers its questions.
- An *owner gate* is a stop where the owner reviews the work: the plan gate after propose, and the
  result gate after a passed verify.
- The *test lock* is the check at verify that only a tests commit changes a test file: no other
  commit on the branch, and no uncommitted change, adds, changes, deletes or renames one.
- A *profile* is one project's answers to the questions in `profiles/TEMPLATE.md`, a plan for
  building the flow into that project.
- The *repo guide* is the file with a repo's rules for an agent: `AGENTS.md`, else `CLAUDE.md`.

| File | What it is |
| --- | --- |
| `WORKFLOW.md` | The flow, in full. Every rule lives here. |
| `workflow.html` | The page: the same flow as a picture, written by hand. |
| `diagrams/` | The figures of the flow, one hand-written SVG file each. |
| `skills/` | The skills and the four step commands that run the flow, with their credits and licence. |
| `examples/` | Example files for a new repo. `openspec-config.yaml` is an OpenSpec config with the flow's lines marked. `project-rules.md` is the template of a repo's rules sections. `verify.md` is an example of a repo's verify rules file. |
| `profiles/TEMPLATE.md` | The questions that a project answers to adopt the flow. |
| `.claude-plugin/` | The plugin manifest and the marketplace file. |
| `LICENSE` | The MIT licence. The adapted skills keep their upstream MIT licence, in `skills/LICENSE-mattpocock-skills.txt`. The show-me part of the `pr` skill keeps its own MIT licence, in `skills/LICENSE-humanlayer-skills.txt`. |

**Start a new project.** Set up each repo in this order:

1. Install OpenSpec 2.x, the npm package `@fission-ai/openspec`:

   ```bash
   npm install -g @fission-ai/openspec
   ```

   OpenSpec prints a note that it collects anonymous usage stats. To opt out, set
   `OPENSPEC_TELEMETRY=0`.
2. In the repo root, run the init command for Claude Code:

   ```bash
   openspec config set profile custom
   openspec config set workflows '["propose","explore","new","continue","apply","update","verify","archive","sync","ff","bulk-archive","onboard"]'
   openspec init --tools claude --scope project --no-animation .
   ```

   The first two lines are needed because OpenSpec's default profile writes only six skills. It
   leaves out `openspec-new-change`, `openspec-continue-change` and `openspec-verify-change`, and
   verify stops without the last one. The two `config` lines change the global config of OpenSpec on
   this machine, not only this repo. They are set once, and they apply to every repo you init
   there. The init writes twelve generated skills under
   `.agents/skills/`, with links under `.claude/skills/`, and a first `openspec/config.yaml`
   (checked on OpenSpec 2.1.1). Everyone who runs `openspec init` or `openspec update` in the repo
   sets the same two `config` lines first: a machine whose profile is `core` deletes the verify
   skill on `openspec update` (checked on OpenSpec 2.1.1). Without `--no-copilot-cloud`, the init is
   the same: that flag only prints a warning when `--tools` is `claude`.
3. Copy `examples/openspec-config.yaml` over that `openspec/config.yaml`. Read its header comment,
   then replace the placeholders of the `context:` block, of the Optional parts above `rules:` and
   of the example design rule. Every other form in angle brackets under `rules:`, such as `S<n>`,
   `<name>`, `<actor>` and `<entry>`, stays: the flow fills it. Fill the lines after
   `Checks before a commit:`, `Tests:` and `Test files:`. Delete each part marked Optional that the
   repo does not use. To turn an owner gate off, add its gate line (`Plan gate: off.` or
   `Result gate: off.`) at the end of the `context:` block, indented as the lines above it, or put
   the line in the repo guide. Last, delete the header comment, every line above `schema:`.
4. Add the build line to the repo guide (`AGENTS.md`, else `CLAUDE.md`):

   ```text
   A request in words to build, apply or implement an OpenSpec change, or to work through its tasks, loads `idea-to-code:build` and never `openspec-apply-change`.
   ```

   Then copy `examples/verify.md` to `openspec/verify.md`, edit it to fit the repo, and delete its
   comments. Add the verify line to the repo guide too:

   ```text
   A verify run on an OpenSpec change also applies `openspec/verify.md`, because the generated verify skill does not name that file.
   ```

   A repo that wants no verify rules of its own skips the copy and the verify line. The verify
   command then checks by hand. Every repo adds the build line.
5. Claude Code loads `CLAUDE.md` at session start. Where the repo guide is `AGENTS.md`, add a
   `CLAUDE.md` that holds the one line `@AGENTS.md`, so that the guide binds a session that loaded
   no skill.
6. Name the plugin in `.claude/settings.json`, as [Name the plugin in a repo](#name-the-plugin-in-a-repo)
   shows. Commit that file, the config, all of `.agents/skills/` with the links under
   `.claude/skills/`, and the files of steps 4 and 5, so that a lone clone works.
7. Add a rules section only where the repo differs from a default. `examples/project-rules.md` is
   the template. A repo with no rules of its own adds none.
8. Read [chapter 5](WORKFLOW.md#5-setting-up-a-project) of the flow for the other parts of the kit.
   Then copy `profiles/TEMPLATE.md` into the project's own repo, and write each answer under its
   question.

Start each step with its command: `/idea-to-code:explore`, `/idea-to-code:propose`,
`/idea-to-code:build`, `/idea-to-code:verify`. [The step commands](#the-step-commands) says what
each one does.

[The plugin](#the-plugin) says how the project's repos get the skills and the step commands.

## The plugin

The skills and the step commands of the flow ship as one Claude Code plugin named `idea-to-code`.
This repo is also the marketplace that lists the plugin, under the same name.

The plugin holds twelve method skills and four step commands. It has no agent, no hook and no MCP
server. A skill holds the method and no rule of one project. It reads the project's rules from the
repo: the repo guide (`AGENTS.md`, else `CLAUDE.md`), `openspec/config.yaml`, or the rules file
that the guide names.

### The skills

Every skill of the plugin has the plugin name as a prefix: `idea-to-code:<skill>`. A person types
`/idea-to-code:grilling`. With the plugin, a short skill name in prose means the plugin's skill. An
instruction to load a skill then uses the full name, `idea-to-code:<skill>`. Claude Code ships a
skill of its own named `code-review`, so the short name `code-review` loads that skill and not the
plugin's. Claude Code also ships skills of its own named `verify`, `commit` and `pr` (checked on
Claude Code 2.1.331), so those short names load Claude Code's skill in the same way.

| Skill | Job |
| --- | --- |
| `idea-to-code:grilling` | Runs the grill; holds the question form. |
| `idea-to-code:research` | Settles a fact from primary sources, in a cited note. |
| `idea-to-code:prototype` | Settles a design question with throwaway code. |
| `idea-to-code:domain-modeling` | Writes a term or a decision record, on the owner's yes. |
| `idea-to-code:codebase-design` | A reference: the words for deep modules and seams. |
| `idea-to-code:slice-build` | Builds a change slice by slice, tests first; runs the fix round. |
| `idea-to-code:tdd` | The rules for good tests and the red-green loop. |
| `idea-to-code:diagnosing-bugs` | A diagnosis loop for hard bugs and performance regressions. |
| `idea-to-code:commit` | The rules for every commit. |
| `idea-to-code:code-review` | Reviews the diff against written standards and smells. |
| `idea-to-code:pr` | Writes the pull request body and the breaking footer. |
| `idea-to-code:owner-gate` | Applies the two owner gates, and records the outcome. |

### The step commands

The four step commands ship in the plugin: `/idea-to-code:explore`, `/idea-to-code:propose`,
`/idea-to-code:build` and `/idea-to-code:verify`. A repo carries no command file. A step command is
always written in full, because Claude Code has a command of its own named `verify`.

| Command | Argument | What it does |
| --- | --- | --- |
| `/idea-to-code:explore` | `[idea]` | Looks up the facts, then asks the owner one question per message. It writes no change. |
| `/idea-to-code:propose` | `[change-name or description]` | Writes the change folder, and ends with the plan gate. |
| `/idea-to-code:build` | `[change-name]` | Builds the change slice by slice, tests first. It pushes nothing. |
| `/idea-to-code:verify` | `[change-name]` | Runs the test command, the check command and the test lock, applies `openspec/verify.md`, runs OpenSpec's comparison and one fix round, and ends with the result gate. |

Type a command to start its step. A request in words to build a change, or a yes after the session
named the build command, also starts the build: it loads the build command. The build ends by naming
`/idea-to-code:verify`: run it in a fresh session, so that verify reads the work without the context
that wrote it.

### Install the plugin

Each person installs the plugin by hand, once. In a Claude Code session, add the marketplace, then
install the plugin:

```text
/plugin marketplace add emil-jacero/idea-to-code
/plugin install idea-to-code@idea-to-code
```

The second command opens the details of the plugin. Read what the plugin adds, then choose a
scope: for you in every project, for this repo, or for you in this repo only.

The same two steps work from a shell, with no session open:

```bash
claude plugin marketplace add emil-jacero/idea-to-code
claude plugin install idea-to-code@idea-to-code
```

From a shell, the install is for you in every project, unless you pass `--scope project` or
`--scope local`. After the install, start a new session or run `/reload-plugins`.

### Name the plugin in a repo

Each repo names the marketplace and the plugin in its `.claude/settings.json`, and commits that
file:

```json
{
  "extraKnownMarketplaces": {
    "idea-to-code": {
      "source": { "source": "github", "repo": "emil-jacero/idea-to-code" }
    }
  },
  "enabledPlugins": {
    "idea-to-code@idea-to-code": true
  }
}
```

Claude Code registers the marketplace for a person after that person trusts the repo folder. The
file turns the plugin on, but it does not install it. Each person still installs the plugin by
hand, once in each clone:

```bash
claude plugin install idea-to-code@idea-to-code --scope project
```

With `--scope user`, one install covers all the projects of that person.

The files of the repo that tell an agent to load a skill (the OpenSpec config and the verify rules
file) use the full name of the skill.

### Update the plugin

Claude Code does not update the plugin on its own. Auto-update is off for this marketplace until a
person turns it on. To get a new version, run one of these two commands. The first is for a
session, the second is for a shell:

```text
/plugin marketplace update idea-to-code
claude plugin update idea-to-code@idea-to-code
```

Then start a new session or run `/reload-plugins`. To turn auto-update on, run `/plugin`, go to the
Marketplaces tab, select `idea-to-code` and turn auto-update on.

A person gets a new copy only when the `version` in `.claude-plugin/plugin.json` changes. So each
release of this repo changes that string.

### What stays in the repo

The plugin holds the skills and the four step commands of the [kit](WORKFLOW.md#the-kit): what a
repo carries, or names, so that the whole flow runs in a lone clone. A repo carries no command
file. The other parts of the kit stay as files in the repo:

- the build line in the repo guide;
- the verify rules file, `openspec/verify.md`, with the verify line in the repo guide;
- the config check script;
- where the project uses them, the check scripts and the text hook.

The plugin ships no check script. A repo that uses check scripts writes its own, and names each
one in the `context:` block of its `openspec/config.yaml`: the slice check script after
`Slice check:`, and the test check script after `Test check:`.

The plugin ships no config check script either. A repo writes its own and runs it from its check
command: it refuses the three things that [OpenSpec](WORKFLOW.md#openspec) names.

The repo's own rules stay in the repo too. `examples/project-rules.md` is the template of the
rules sections.

## Edit this repo

**Edit the flow.** Change `WORKFLOW.md` first. Each rule has one home: other sections link to it.
Never write an em-dash or an en-dash. Then make the same change by hand in `workflow.html`, and
commit both together.
The scripts `maintainer/check_tree.py` and `maintainer/check_page.py` check the repo and the page.

The page has five tabs: Flow, Who and how, Roads, Parts, Set up. It orders its
sections by its tabs; `WORKFLOW.md` keeps its chapter order.

The page follows four rules:

- It says nothing that `WORKFLOW.md` does not say.
- It stays under 4,900 words outside its figures.
- Each section names the heading of `WORKFLOW.md` that holds the full text, and the anchor of
  every heading is an id on the page.
- It works without its script. The script shows one tab at a time and marks where you read.
  Without it the page is one scroll, in the order of the tabs.

**Edit a figure.** Change the SVG file in `diagrams/`. `WORKFLOW.md` places each figure once, as an
image with a `*Figure:*` caption under it. The page holds a copy of the file's text without its
`<style>` element. After a change, copy the file's text into the page again; never edit the copy.

## Credits

The flow is built on OpenSpec and on skills adapted from Matt Pocock's AI Hero skills
([github.com/mattpocock/skills](https://github.com/mattpocock/skills), MIT licence). The `pr` skill also carries text from the `show-me` skill by Dex Horthy
([github.com/humanlayer/skills](https://github.com/humanlayer/skills), MIT licence, Copyright (c) 2026 HumanLayer). The flow's
[Credit and licence duties](WORKFLOW.md#credit-and-licence-duties) name both, and say what a copy
must keep. `skills/CREDITS.md` records every local change to an upstream skill.

The figures follow the method of the diagram-design skills
([github.com/cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design), MIT
licence). They are drawn for this flow, and nothing is copied from that repo.
