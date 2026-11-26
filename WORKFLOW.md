# Idea to Code

Idea to Code is a way to take an idea to merged code with a coding agent. The owner decides, and
the agent does the work. The idea becomes an OpenSpec change, built in thin slices, one at a time.
Where a repo has specs, the tests are written from the spec first, and the code may not change
them. The flow follows Matt Pocock's method (grill, spec, vertical slices, tests first, review),
with OpenSpec changes in place of a spec and tickets. It is built on OpenSpec and on skills adapted
from Matt Pocock's AI Hero skills. The credit and the licence duties are in
[Credit and licence duties](#credit-and-licence-duties).

> **Status:** As of 2026-11-24, a toy trial ran the flow from explore to verify, end to end. No
> real change has gone through the flow yet. A project's profile says which parts it has built.

## 1. Start here

**What the flow is.** The flow takes one change from an idea to main in five steps:

1. [Explore](#step-1-explore): an idea goes in; decisions come out.
2. [Propose](#step-2-propose): the decisions go in; a change folder comes out.
3. [Build](#step-3-build): the change folder goes in; every slice comes out closed, with its
   commits, and nothing is pushed.
4. [Verify](#step-4-verify): the built change goes in; a verified change comes out.
5. [Pull request and archive](#step-5-pull-request-and-archive): the verified change goes in; it
   comes out squash-merged to main.

Explore may pause for a side step, which settles an open assumption. The side step is not a sixth
step. The build loops while slices are left. Verify loops once, for the fix round.

A *change* is one piece of work in one repo, kept as an OpenSpec change: a folder of files that
says what must be true. A *slice* is a thin, working piece of a change, built and closed on its
own. *Main* is the repo's main branch. A *road* is a way from an idea to main. The *path* is the
main road: five steps for one change in one repo with specs. The path is
[chapter 2](#2-the-path-five-steps-from-an-idea-to-main), the other roads are
[chapter 3](#3-other-roads), and the optional parts are [chapter 4](#4-optional-parts).

![The five steps of the path from an idea to main, who acts at each, the side step that
explore may pause for, and the loops of build and verify.](diagrams/the-path.svg)

*Figure:* The path from an idea to main: five steps, the side step that explore may pause for,
and the two loops.

In a repo with OpenSpec, feature work is always delivered as a change: never as a plan alone, and
never as direct code. A bug fix or a chore may be [work outside a change](#work-outside-a-change).

**What the flow assumes.** A project that uses the flow has:

- git;
- a host with pull requests that squash-merges them;
- OpenSpec 2.x in each repo;
- a coding agent that loads skills and starts fresh sub-agents;
- a test command in each repo.

**Who does what.** The owner decides. The agent finds the facts and does the work.

The *owner* is the person who decides: the owner answers every question, and approves what the
flow leaves to the owner. The *agent* is the coding agent that does the work.

The agent looks up every fact in the repo, the tools or the docs, and checks it at its source or
by running it. A code comment is not a source. The agent never asks the owner for a fact that it
can look up.

An *owner decision* is a choice of one of five kinds:

- scope;
- a public contract;
- a breaking change;
- a security trade-off;
- a new dependency.

The agent works as one session and many sub-agents. The *session* is the agent conversation that
the owner talks to. It runs the checks, makes every commit and asks the owner each question. A
*sub-agent* is a fresh agent with a clean context, which the session starts for one job. It gets
its whole task in one brief.

A sub-agent, or a run with nobody to answer, never asks the owner. For an owner decision, it stops
and hands the question back, drafted in the question form (below). The session asks the owner,
and a fresh sub-agent of the same role goes on with the answer. Every other choice the sub-agent
makes itself, and it lists the choice as an assumption, with the question it answered. It never
invents an owner answer.

![An owner decision goes from the sub-agent back to the session, which asks the owner, and every
other choice the sub-agent makes itself and lists as an assumption.](diagrams/owner-decision.svg)

*Figure:* A sub-agent stops for an owner decision, and makes every other choice itself.

A sub-agent commits nothing, ticks no task box and starts no other agent.

These rules hold at every step:

- **Commits.** Before every commit, the agent loads the `commit` skill, which picks the type, the
  scope and the message. When the owner staged changes himself and they hold more than one unrelated
  concern, the skill asks once: A two commits (the skill restages), or B one commit as staged. The
  owner's index changes only after that answer. The skill runs the repo's check command before every
  commit that is not a tests commit, and a failed check command stops the commit ([The repo's own
  files](#the-repos-own-files)). The agent runs each check alone, reads its exit status, and only
  then runs `git commit` in a separate call. It never chains a check and a commit in one call. The
  agent commits a change only on a branch other than the default branch: [Before the first
  slice](#before-the-first-slice) names it the working branch. The agent never amends a commit. It
  makes a new commit, because the branch tip may have moved.
- **Text.** Commit, pull request, issue, comment and release note text is permanent. So it never
  carries a session ID, a session link or a "Generated with" footer, and no attribution or signature
  line in it names a model. It never carries a bare `@name`, because the name can be a real account,
  and the mention cannot be undone. By default, it carries no attribution line, and no `@` stands
  before a word, code spans and fenced code included. The repo's `## Text rules` section sets the
  project's own rules: an exact attribution line on its `Attribution:` point, and a looser mention
  rule on its `Mentions:` point ([The repo's own files](#the-repos-own-files)).
- **Hooks.** When a hook blocks a command, the agent asks the owner. It never works around the
  hook.
- **The repo guide.** The *repo guide* is `AGENTS.md`, else `CLAUDE.md`. Before the agent works in
  a repo, it reads the repo guide, the files that it names and the repo's OpenSpec config, and it
  applies the strictest combination of their rules. It checks the branch before it edits.
- **Defaults.** A rule that this document calls a default holds until the owner sets another.

Apart from the moments that stop for the owner, the agent works alone. It finds the facts and
writes the change folder ([Step 2](#step-2-propose)). It builds ([Step 3](#step-3-build)) and
verifies ([Step 4](#step-4-verify)). It pushes the working branch and opens the pull request
([The pull request](#the-pull-request)). It merges when the merge rule lets it
([The merge](#the-merge)).

**How the agent asks a question.** Every question to the owner has one form, the *question form*.
The agent asks one question per message, never a batch. A question has these parts:

- a heading: `### <name>, Q<k> of about <m>: <question>`;
- a background in plain English: what exists now, and why the choice matters;
- two to four lettered options, each with what it means and a concrete example, a `Pro:` and a
  `Con:`;
- a recommendation that names its source (a file, a report, or a skill and its subject), or says
  "my judgement, not researched";
- a last line: "Next: answer A, B or C."

The background names a decision, a review or a change in words, never by an id. It names a file,
a field or a command only when the owner will touch it. The owner answers by letter, or in words.

An offer to write files is a question in this form too, and so is a pick among review findings.
The agent offers findings as classes of fixes, described in words. A request for an input that is
missing, such as the idea or what to build, is not a decision: the agent asks it in one
plain sentence. The `grilling` skill holds the exact form.

> **Example:** The running example is a made-up change in a small web service that stores
> uploaded files. Its first question, in the question form:
>
> ```text
> ### Error text, Q1 of about 3: What does the refusal tell the uploader?
>
> **Background:** Today the service stores a file with an empty name and answers
> 201. The change will refuse it. The uploader must see what was wrong.
>
> **Options:**
>
> **A. Name the field (recommended)**
> - A 400 error whose message names the field: `filename must not be empty`.
> - Pro: the uploader sees at once which field to fix.
> - Con: one more message in the messages file.
>
> **B. A plain refusal**
> - A 400 error with the generic text `bad request`.
> - Pro: no new message.
> - Con: the uploader must guess what was wrong.
>
> **Recommendation: A.** The service's other errors name their field (the error
> form in the upload handler).
>
> Next: answer A or B.
> ```

**How to read this document.** Each step of chapter 2 starts with six fields, in this order:

- *Goes in*: what the step starts from.
- *Who acts*: the owner, the agent, or both.
- *What happens*: the step's actions, in order.
- *Checks*: what is checked in the step.
- *Comes out*: what the step hands to the next step.
- *Stops for the owner when*: each moment the work waits for the owner.

Subsections with the detail follow the fields. Callouts mark what must stand out:

- *Example*: the running example at this point of the path.
- *Open*: a point that is not decided, and what a project does until it is decided.
- *Optional*: where an optional part joins the path, with a link to chapter 4, or the whole of a
  small optional part.
- *Owner*: a moment where the work stops for the owner.
- *Note*: anything else that must stand out.

The service of the running example has one repo, and the example uses no part of chapter 4. Of
the small optional parts, it uses one: check scripts.

Some words name things that each project fills in, such as "the test command". Each project names
these things in the repo's own files ([The repo's own files](#the-repos-own-files)). While it
builds the flow in, it plans them in its *profile*
([The project's profile](#the-projects-profile)). A *step command* is the command that starts a
step: the explore command, the propose command, the build command or the verify command. The step
commands come with the kit ([The kit](#the-kit)).

## 2. The path: five steps from an idea to main

The path takes one change in one repo with specs from an idea to main. Every part of the flow
shows on it. [Chapter 3](#3-other-roads) gives the roads that change it.

### Step 1: Explore

**Goes in:** an idea, in the owner's own words.

**Who acts:** both. The agent asks, and the owner decides.

**What happens:**
1. The explore command starts explore, with the grill added
   ([The explore command](#the-explore-command)).
2. The agent looks up the facts itself. First it brings the checkout up to date with the remote's
   default branch, or says that the checkout is behind (the fresh-base check, in
   [`CHECKS.md`, Fresh base](skills/slice-build/CHECKS.md#fresh-base)). It also searches every spec
   for the behaviour that the idea changes, not only the specs that the idea names. It reads them
   also for rules on how the work is done (a requirement with never, only, must, always or no).
   When the idea comes from an issue or a report, it checks each claim in it (the cause, the
   proposed fix and the result the fix should give) before the first question, and its first
   answer lists the checked claims as true, false or open.
3. The grill asks the owner questions, until no open decision is left
   ([The grill](#the-grill)).
4. When an assumption is open, a side step settles it (the side-step callout in
   [The grill](#the-grill)).
5. Where an optional part adds tracks, the agent asks the track question
   ([The track question](#the-track-question)).

**Checks:** no script check. The grill's stop rule ends the questions ([The grill](#the-grill)).

**Comes out:** decisions, and the work on a track. The only files so far are a new term or
decision record, and what a side step left as evidence.

**Stops for the owner when:**
- the grill asks a question;
- the grill asks which seam the tests go at: one question per distinct seam
  ([The grill](#the-grill));
- the agent asks the track question (only where an optional part adds tracks);
- the idea is a design question (the second Owner callout in
  [The track question](#the-track-question)).

#### The explore command

The explore command runs OpenSpec's explore skill, a *generated skill*: a skill that OpenSpec
writes into the repo. The command adds the grill, the question form, the record of decisions, and
the hand-offs to the side step and to the record files. It also states that explore writes no
change folder. It does this from outside the generated skill ([OpenSpec](#openspec) says why).

Explore is read-only. It reads and searches, and it never writes code or a change folder.

> **Note:** OpenSpec's generated explore skill lets explore write change files when the owner
> confirms (checked on OpenSpec 2.1.1). The flow does not use that permission.

`improve-codebase-architecture` is another way into the path. It is an
[upstream skill](https://github.com/mattpocock/skills/tree/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/improve-codebase-architecture)
that the plugin does not ship; a reader who wants it installs it from upstream. It scans the code
for modules to deepen, and writes a report of its candidates to the temporary directory, outside
the repo. It asks the owner which candidate to explore, and then runs the `grilling` skill on that
one. It may add or sharpen a term in the glossary as decisions settle. When the owner rejects a
candidate for a reason that lasts, it offers a decision record. The flow counts that grill as the
explore grill, and the next step is propose.

> **Optional:** With [tracker issues](#a-tracker-issue-for-several-repos), explore first lists the
> open ones. With [many repos](#many-repos-in-one-workspace), the session first names the repo it
> works in.

#### The grill

The *grill* is the run of questions in explore. Facts come first ([chapter 1](#1-start-here)).
Then the `grilling` skill asks the owner questions, in the question form:

- Of the questions whose prerequisites are already answered, it asks first the one that opens the
  most other questions. After each answer, it works out again which questions it can ask next.
- It asks one decision per question. Two decisions joined by "and" are two questions.
- It asks no question whose answer would not change the outcome.
- It asks the *seams* too. A seam is the public interface where a slice's tests go. It asks them
  after the decisions that fix what is built, because a seam depends on them. It asks one question
  per distinct seam, not one per slice, and each option says what the seam catches and what it
  misses. The heading of a seam question starts with `Test seam`, and its background says that
  the build writes the tests there first and then locks them. Every seam is agreed with the owner
  before the change is written.
- It keeps a running record of each decision, marked as the owner's answer or as the agent's
  assumption. An open assumption is never recorded as settled. "You decide" is an answer: the
  agent decides, and records the decision as delegated.
- When an answer contradicts an earlier one, the agent says so, and the owner says which one
  stands.
- A requirement that the owner states outright is the owner's answer. The agent records it, and
  adds the questions that it opens to those it can ask next. Only an answer that offers a new
  option in place of a choice becomes an option, and the question is asked again.

The grill stops when no open decision that the work needs is left. After two exchanges in which
nothing settled, the grill stops and says what blocks it:

- a missing fact: the agent finds it;
- an option nobody likes: the agent finds new ones;
- a decision that is not ready: the agent offers "decide later".

> **Optional:** The side step. An assumption is open when only running code or a wider search can
> settle it. Explore names it and pauses. The agent runs a *side step* apart from explore, never
> inside it: a prototype with the `prototype` skill, or a research run with the `research`
> skill. Explore resumes with the finding. A research run may read in the background while the
> grill goes on with other questions. A prototype is throwaway: it is built in a scratch folder
> outside any repo, and the side step commits nothing: its files reach git only inside the
> change's evidence folder. Research uses primary sources only.
>
> The side step's files are kept as evidence. Propose moves them into the change's *evidence
> folder*, `evidence/<nn>-<name>/`, with a short `README.md` note. The folder is archived with the
> change. Prototype files never become product code. The finding goes into the design, which
> points at the folder. Without a side step, the change has no evidence folder.

> **Optional:** Glossary and decision records. When the grill settles a new term, or a decision
> that may need a record, the `domain-modeling` skill asks the *capture question*. That is the
> offer to write the file, in the question form. On the owner's yes, it writes the file at once,
> in a pause of explore, one file at a time. The reason: every later agent (the test writer, the
> code writer and the reviewer) reads it. A term goes into the repo's *glossary*, its terms file.
> Where a repo's rules require a term to be backed by its spec or code, the term reaches main in
> the same pull request as its backing. A term whose backing the change dropped is removed before
> that pull request merges.
>
> A *decision record* (an ADR) is offered only when the decision is hard to reverse, surprising
> without context, and the result of a real trade-off. A repo without an ADR folder puts the
> decision in the *decision home* that its `## Decision records` section names, never only in the
> change's design. Where the repo names none, `domain-modeling` offers a new reference file of the
> repo, and writes its path as the `Decision home:` point of that section, so that the next decision
> finds it. Agents never create the ADR folder. A decision that binds several repos is not a
> decision record ([An enhancement store](#an-enhancement-store),
> [A tracker issue for several repos](#a-tracker-issue-for-several-repos)).
>
> The file stays uncommitted until the build's first commit carries it, on the owner's yes
> ([Before the first slice](#before-the-first-slice)). When explore ends with no change, the agent
> reports the file, and commits it only when the owner asks.

#### The track question

The *track question* ends explore: it puts the work on a *track*. Without an optional part that
adds tracks, there is one track, one change in one repo, which goes on to step 2. Then the agent
does not ask the track question, because its answer would not change the outcome
([The grill](#the-grill)).

> **Optional:** An [enhancement store](#an-enhancement-store) adds questions 1 and 2 here, and
> [tracker issues](#a-tracker-issue-for-several-repos) add question 3. A project asks only the
> questions of the parts it has, in this order:
>
> 1. Does the work deliver a line of a live entry? Yes: it goes through that entry
>    ([An enhancement store](#an-enhancement-store)).
> 2. Is it a major feature? Yes: it becomes an enhancement in the store (same part).
> 3. Does it touch several repos? Yes: one tracker issue ties one change per repo
>    ([A tracker issue for several repos](#a-tracker-issue-for-several-repos)).
>
> All no: one change in one repo.

> **Owner:** Where an optional part adds tracks, the owner answers the track question. The agent
> asks it in the question form, with the track it recommends.

> **Owner:** A design question is an idea of the form "how do we make X possible". For one, the
> agent presents the researched design with its recommendation, the open questions and one
> proposed next step, and stops. No change folder, enhancement entry
> ([An enhancement store](#an-enhancement-store)), branch or pull request comes before the owner
> approves the design.

> **Example:** The owner's idea: "An upload with an empty file name should be refused, so the
> uploader sees the mistake at once." The agent looks up two facts itself: the upload handler
> stores such a file and answers 201, and the service's other errors name their field. Then it
> asks three questions, one per message. The first, shown in full in [chapter 1](#1-start-here),
> asks what the refusal tells the uploader. The owner answers A: a 400 error whose message names
> the field, `filename must not be empty`. The second asks whether a file name of only spaces
> counts as empty. The owner answers A: yes. These two answers fix what is built, so the third
> asks where the tests go. Both behaviours show at one seam, so it is one question. Option A, the
> upload API, `POST /files` (recommended): its tests catch the 400 answer and whether a file is
> stored. Option B, the name check inside the handler: its tests run faster, and miss the 400
> answer and the stored file. The owner answers A. No optional part adds tracks, so the agent asks
> no track question: the work is one change in one repo, `upload-service`. Explore writes no file.

### Step 2: Propose

**Goes in:** the decisions from step 1. The owner starts propose in the session that ran explore,
because the record of decisions lives only in that conversation. A small change may start here
instead ([The fast path](#the-fast-path)).

**Who acts:** the agent alone.

**What happens:** the propose command runs OpenSpec's propose skill. It plans only, and writes no
code. It writes the change folder ([The change folder](#the-change-folder)). The repo's config
rules for each artifact apply ([OpenSpec](#openspec)). It starts with the fresh-base check, as
explore does. Before it writes the spec deltas, it searches every spec for the behaviour that the
change alters. Each requirement or scenario that the change makes false gets a delta, also in a
spec that the decisions do not name. So does a rule on how the work is done (a requirement with
never, only, must, always or no) that a choice of the design breaks.

**Checks:** the *slice check* checks the Slices section: its form, and that every slice it names
exists. After propose, it runs only as a script, where the project has check scripts (the
check-scripts callout in [Per slice](#per-slice)). The slice check has no by-hand form, and
OpenSpec's validate never reads `design.md` (OpenSpec 1.17.0 and 2.1.0). So without the scripts,
no form check runs in this step. On the fast path, propose first runs four read-only checks
([The fast path](#the-fast-path)). Propose runs OpenSpec's validate on the change folder before
the plan gate.

**Comes out:** a change folder that says what must be true, slice by slice.

**Stops for the owner when:**
- on the fast path, one of its checks fails ([The fast path](#the-fast-path));
- a change of the same name exists already;
- an owner decision is open: propose puts it to the owner as one question. On the fast path, an
  open owner decision fails the second check instead;
- a seam is still open: propose asks it before it writes, one question per distinct seam. On the
  fast path, with no explore, it asks each seam here ([The fast path](#the-fast-path)).

> **Optional:** With [owner gates](#owner-gates), propose ends with the plan gate, which may stop
> for the owner.

#### The change folder

The *change folder* holds the change's files, at `openspec/changes/<name>/`. Every word that the
build uses later is met here first.

- `proposal.md`: why the change exists, and what it changes.
- Delta specs, under `specs/<capability>/spec.md`. A *delta spec* adds, changes or removes
  requirements, in ADDED, MODIFIED or REMOVED sections. Each requirement states what must hold
  with SHALL or MUST, and has scenarios in WHEN and THEN form. The archive folds the delta specs
  into the *main specs*: the repo's living specs, which hold delivered behaviour only.
- `design.md`: the design, with the `## Slices` section ([The Slices section](#the-slices-section)).
- `tasks.md`: one task section per slice ([The task sections](#the-task-sections)).
- The evidence folder, when a side step ran (the side-step callout in [The grill](#the-grill)).

OpenSpec's new, continue and update skills (`openspec-new-change`, `openspec-continue-change`,
`openspec-update-change`) start a change part by part, or revise its planning files.

> **Optional:** User stories. `proposal.md` holds a `## User stories` list, at most about seven
> lines by default, one line per story: `As a <actor>, I want <feature>, so that <benefit>`. A
> change with no user-visible behaviour writes none. Verify then checks that a requirement covers
> each story: this is the *user-story check*.

> **Optional:** With an [enhancement store](#an-enhancement-store), a change that delivers a line
> of a live entry names the entry and the line in its proposal.

> **Open:** One split is tentative: OpenSpec's generated skills keep writing the change files, and
> the [kit](#the-kit) skills (the skills that each repo gets) give them input and check them.
> Until it is settled, a project works with that split.

#### The Slices section

The `## Slices` section of `design.md` holds one *slice block* per slice, headed
`### S<n>: <name>`. Each block has four fields:

- `Delivers`: what the slice delivers, such as the scenarios it makes true.
- `Seam`: the public interface where the slice's tests go. The owner agreed it in explore or in
  propose ([The grill](#the-grill), [Step 2](#step-2-propose)).
- `Depends on`: the slices it needs first, or "none".
- `Done when`: when the slice is done. This *Done when line* needs a test too. A Done when line
  that only says that the delivered scenarios pass is covered by their tests.

Every slice is a real slice. None is a try-out: that is the side step's job.

#### The task sections

A *task section* is one `## N.` section of `tasks.md`. Section N holds every task of slice SN and
nothing else. The slice's code commit ticks its boxes ([Per slice](#per-slice)).

> **Note:** Put any extra line of a task section directly under its `## N.` heading: a line there
> is safe (OpenSpec 1.17.0 and 2.1.0). A plain paragraph line right after a checkbox line is glued
> onto that task (OpenSpec 2.1.0). OpenSpec's validate warns, and with `--strict` fails, when a
> task id does not match its section number or when ids repeat (built-in schema `spec-driven`,
> OpenSpec 1.17.0 and 2.1.0).

> **Example:** Propose writes the change folder `openspec/changes/refuse-empty-file-name/`. It has
> no evidence folder, because no side step ran. The proposal says why: an upload with an empty
> file name is stored and answered 201, so the uploader does not see the mistake. It says what:
> the service refuses such an upload with a 400 error that names the field. The delta spec for the
> capability `upload` holds one requirement with two scenarios. The second scenario,
> `Blank file name`, has the same form, with the file name `"   "`. The slice check script passes:
> both slices have the right form, and S2 names S1, which exists. The requirement with its first
> scenario, the two slice blocks and the two task sections:
>
> ```text
> // specs/upload/spec.md
> ### Requirement: Refuse an empty file name
> The service SHALL refuse an upload whose file name is empty or holds only spaces.
>
> #### Scenario: Empty file name
> - WHEN a client uploads a file with the file name ""
> - THEN the service answers 400 with an error that names `filename`
> - AND it stores no file
>
> // design.md, section ## Slices
> ### S1: Refuse an empty file name
> Delivers: scenario Empty file name
> Seam: the upload API, POST /files
> Depends on: none
> Done when: scenario Empty file name passes
>
> ### S2: Refuse a file name of only spaces
> Delivers: scenario Blank file name
> Seam: the upload API, POST /files
> Depends on: S1
> Done when: scenario Blank file name passes
>
> // tasks.md
> ## 1. Refuse an empty file name
> - [ ] 1.1 Check the file name in the upload handler
> - [ ] 1.2 Answer 400 with an error that names `filename`
>
> ## 2. Refuse a file name of only spaces
> - [ ] 2.1 Treat a file name of only spaces as empty
> ```

### Step 3: Build

**Goes in:** the change folder, with its Slices section and its task sections. A change with no
Slices section builds each task section as a slice ([No Slices section](#no-slices-section)).

**Who acts:** both. The owner starts the build, then the agent works alone. The session writes no
test and no code. For each slice it starts a fresh test writer, then a fresh code writer (in a
[repo without specs](#a-repo-without-specs), only a code writer). A *writer* is a sub-agent of
the build or of the fix round: the test writer writes only tests, and the code writer writes only
code.

**What happens:** the owner starts the build with the build command, which loads the
`slice-build` skill. A request in words, or a yes after the session named the build command,
starts it too: the session then loads the build command
([Steering the build](#steering-the-build)). The build command runs no generated skill of OpenSpec.
One `slice-build` run builds every slice of the change, not one slice per run. Slices go in
order, one at a time, never in parallel. Before the first slice, the session sets up
([Before the first slice](#before-the-first-slice)). Then each slice runs seven parts, (a) to (g)
([Per slice](#per-slice)).

**Checks:** for each slice, the gate, the red check, the test-lock check, and the test command
before the code commit ([Per slice](#per-slice)).

**Comes out:** every slice closed on the working branch, each with its tests commits and its code
commit. Nothing is pushed. The owner gets the final report, and the change folder holds it as
`build-report.md` ([The final report](#the-final-report)).

**Stops for the owner when:**
- at the start, when no change is named and several changes are active: which change to build;
- before the first slice ([Before the first slice](#before-the-first-slice)):
    - none of the branches that the default branch rule names exists;
    - a change in the tree that is not part of the build;
    - whether the first commit carries a term or decision record from explore;
    - a clash with the repo's apply guidance;
    - a command that the build runs and that the config does not name;
- during the build:
    - a resumed build cannot tell from the `Tests-For` trailers which slice resumes
      ([Per slice](#per-slice));
    - the gate stops the build ([Per slice](#per-slice));
    - the trailer block of a tests commit fails its check, or git cannot write it
      ([Per slice](#per-slice));
    - a default for a failed part says stop ([When a part fails](#when-a-part-fails));
    - a writer hands back an owner decision ([chapter 1](#1-start-here));
    - the spec cannot settle a disputed test, or a test is disputed a second time
      ([A disputed test](#a-disputed-test));
    - the slice cannot be done without a fix to older code
      ([A bug found during the build](#a-bug-found-during-the-build));
- after the last slice: the check command fails at the commit of `build-report.md`
  ([The final report](#the-final-report)).

#### Before the first slice

The session sets up once:

1. It runs every git and file command from the repo's root.
2. It runs `git status`.
3. It finds the *default branch*, the branch that the change is compared against: the remote's
   default branch, else `main` when that branch exists, else `master` when that branch exists. It
   asks the owner only when none exists. It names the result on a line `Base: <branch>`, in
   `build-report.md`. `slice-build` holds the shell lines
   ([`CHECKS.md`, Default branch](skills/slice-build/CHECKS.md#default-branch)). In the same call
   it runs the fresh-base check: a clean default branch moves forward to the remote, and a
   default branch with local work that is behind stops the run
   ([`CHECKS.md`, Fresh base](skills/slice-build/CHECKS.md#fresh-base)).
4. It picks the working branch. The *working branch* is the branch that the build commits to: the
   branch the run started on, or, when the run started on the default branch, a branch named after
   the change. The repo's apply guidance may name another form for that branch. The session
   creates or switches to the branch before the first commit.
5. It reads the apply guidance: the apply entry under `operations` in `openspec/config.yaml`.

> **Optional:** With [many repos](#many-repos-in-one-workspace), the session first resolves which
> repo the work is about.

> **Optional:** With [owner gates](#owner-gates), the session reads `gates.json` before the first
> slice. It does not start while a plan gate that is on has no outcome.

> **Owner:** The session puts each of these to the owner as one question, in the question form:
>
> - the name of the default branch, when none of the branches that the rule names exists;
> - a change in the tree that is not part of this build;
> - whether the build's first commit carries a term or decision record that explore wrote, so
>   that it goes into the change's own pull request. The change folder goes into that commit with
>   no question;
> - a clash between the apply guidance and these steps, for example "one commit per section";
> - a command that the build runs and that the repo's OpenSpec config does not name, such as the
>   test command (the test-command note in [Per slice](#per-slice)).
>
> The set-up is done when the session works from the repo root on the working branch, the tree
> holds no unrelated change, and every question has the owner's answer.

#### Per slice

Each part starts only when the part before it is done.

![The seven parts of a slice, (a) to (g), each marked as the session, a sub-agent or a check,
and the two commits that close it: tests, then code.](diagrams/per-slice.svg)

*Figure:* The seven parts of a slice, which closes with two commits: tests first, then code.

- **(a) Gate.** The *gate* checks, at the start of a slice, that every task box of each slice in
  `Depends on` is ticked. If one is not, the build stops, with a message such as "S2 is blocked
  by S1".
- **(b) Test writer.** A fresh sub-agent loads the `tdd` skill and writes tests at the slice's Seam:
  one or more for each scenario the slice delivers, and for its Done when line. It takes expected
  values from the spec, never from running code. It may add compile-only stubs, and it writes no
  other production code. A *stub* is a signature that only makes the code build. A stub never
  returns a value: it raises the language's "not implemented" error, so a test that asserts a
  value cannot pass on a stub. Wiring that a test needs to reach the Seam (an export line, a
  registration) belongs to the stub. It may stand in the tests commit when it holds no behaviour.
  Where the language has no such error, the stub stops the program instead, with the message
  "not implemented" (a panic, an abort). A test that expects an error names the error of its
  scenario, by a type or a message that the stub's error does not match. A stub is not a test
  file, and the code writer replaces it. When the slice deepens a module, the test writer deletes
  the old tests that the new tests replace (the `codebase-design` skill).
- **(c) Red check.** Before any code for the slice exists, every new test must fail on the
  behaviour that its scenario names. The right reason is an assertion on that behaviour, or a
  stub's "not implemented" error. A wrong reason is a build or syntax error, a missing import
  or symbol, or a missing fixture. A test that passes fails the *red check*, and so does a report
  that leaves a scenario or the Done when line without a test. A *guard test* is the one
  exception: it covers a scenario that says a behaviour of the code before the change stays (a
  refusal that still holds), so it passes before the code by design. The test writer marks it,
  the build report lists it, and the owner gets no question for it. When a stub ends the test run at
  the first test, each new test runs alone.
- **(d) Tests commit.** The session commits only the test files, the stubs and the change-folder
  files named here. The title has the repo's tests commit title form, by default
  `test(<scope>): <what the tests cover>`. The message ends with the trailer line
  `Tests-For: <slice name>`, for example `Tests-For: S1`. So the failing tests are committed before
  any code, in a *tests commit*. The first commit that the build makes carries every file of the
  change folder that is not committed yet, `gates.json` included. It carries a term or decision
  record from explore on the owner's yes. On a resume, that is the next commit that the build
  makes. The build makes no commit that holds only `gates.json`. A fix slice's tests commit also
  carries its new slice block and task section. The session lets git write the trailer block, and
  reads the block after the commit. When the block is wrong, the build stops for the owner,
  because the flow never amends. The owner's question offers a new, empty tests commit with the
  right block, or a stop. The build also stops before the commit when git cannot write the block:
  the git is too old, or the attribution line does not have the form `<key>: <value>`. The
  session keeps the commit's hash in its own notes, never in a file that a sub-agent writes.
- **(e) Code writer.** A second fresh sub-agent writes code until the tests pass. It may not
  edit, add, delete or rename a test file or a test fixture. It replaces each stub, and does every
  task of the section and nothing beyond. For a failure it cannot explain, it may load the
  `diagnosing-bugs` skill. A special case for a test input is never the fix.
- **(f) Test-lock check.** A test file that was changed, added, deleted or renamed since the
  slice's newest tests commit, committed or not, fails the *test-lock check*. Nobody weakens a
  test. No hook blocks the edits: this check is the guard.
- **(g) Code commit.** The test command passes first. The session ticks every box of the slice's
  task section, and commits the code and `tasks.md`. The `commit` skill runs the check command
  before that commit. This *code commit* closes the slice. The next slice starts at (a).

Each test correction adds one more tests commit before the code commit. A build can resume: a slice
whose boxes are all ticked is skipped, and a branch that ends in tests commits resumes at the code
writer of the slice that their trailer names. The build knows a tests commit by its `Tests-For`
trailer, never by its title. The build stops for the owner when those trailers carry different
values, or name no slice with an unticked box. It stops too when an older tests commit on the
branch names another slice with an unticked box. `slice-build` holds the exact rule.

> **Note:** OpenSpec's apply output is a flat task list, with no sections and no dependencies
> (OpenSpec 1.17.0 and 2.1.0). So the gate reads `design.md` and `tasks.md` itself.

> **Optional:** Check scripts in place of checks by hand. A project may run the slice check and the
> gate as one script: the slice check after propose and again at verify, the gate at each slice. At
> the gate, a non-zero exit of that script stops the build. It may run the red check and the
> test-lock check as a second script at each slice. Verify and its fix round do not run that
> script: verify checks the test lock in a form of its own ([Step 4](#step-4-verify)), and the fix
> round runs the red check and the test-lock check by hand. A failure of the second script
> is a failed red check or a failed test-lock check, and the defaults
> of [When a part fails](#when-a-part-fails) apply. Without the scripts, the session runs the gate,
> the red check and the test-lock check by hand, as `slice-build` describes. The repo's OpenSpec
> config names each script in its `context:` block: the first after `Slice check:`, the second after
> `Test check:`. No check script ships with the kit skills: a repo writes its own.

> **Note:** The *test command* is the command after `Tests:` in the `context:` block of the repo's
> OpenSpec config. The [check command](#the-repos-own-files) is the command after `Checks before a
> commit:` there. The `commit` skill runs the check command before every commit except a tests
> commit, so the build does not run it a second time. When the config does not name the test
> command, the session asks the owner one question before the first slice, with the command it found
> in the repo's build files as its recommendation. It never guesses. A repo with no `Checks before a
> commit:` line has no check command. In a repo without specs, the check command takes the place of
> the test command, and the build asks for it the same way.

> **Example:** The owner asks in words for the build, and the session loads the build command. It
> finds the default branch `main`, and names it on the line `Base: main`. The session works on the
> branch `refuse-empty-file-name`, named after the change. Before the first slice, it asks no
> question: the tree holds only the change folder, and the first tests commit carries it. In S1, the
> gate passes, because S1 depends on none. The test writer writes `test_empty_file_name_is_refused`
> at the upload API. The red check reads `test_empty_file_name_is_refused FAILED: expected 400, got
> 201`. That is an assertion on the behaviour, so the reason is right. The session makes tests
> commit 1, with `tests/test_upload.py` and the change folder. Its message ends with the trailer
> `Tests-For: S1`. The code writer adds the check in `upload/handler.py`, and the test passes. The
> test-lock check finds no changed test file. `pytest` passes, the session ticks tasks 1.1 and 1.2,
> and it makes code commit 2, with `upload/handler.py` and `tasks.md`.
>
> S2 runs the same way. Its gate passes, because every box of section 1 is ticked. With one box
> left open, it would stop with "S2 is blocked by S1". The final report lists four commits and one
> assumption (the code writer kept the service's existing error form). It lists no failed check,
> no bug and no disputed test. The four commit titles:
>
> ```text
> test(upload): cover the empty file name refusal
> feat(upload): refuse an empty file name
> test(upload): cover a file name of only spaces
> feat(upload): refuse a file name of only spaces
> ```
>
> The session writes the same report to `build-report.md`, and commits that file alone, as
> commit 5.

#### When a part fails

These defaults ([chapter 1](#1-start-here)) hold when a part fails:

- After a failed red check, a fresh test writer gets the evidence: each failing test and its
  output. At most three fresh test writers follow the first.
- After a failed test-lock check, the session restores the test files from the newest tests
  commit, and removes each test file added after it. Then one fresh code writer gets the finding.
- When the test command fails at the code commit on a test that the slice did not change, the
  session first runs that test on a clean checkout of the default branch. When it fails the same
  way there, it is a *base failure*: the owner answers once, keep it out of the change or fix it
  here. The answer keep it out is a record in `build-report.md`, and later verify runs read it
  ([`CHECKS.md`, A failure that the default branch has too](skills/slice-build/CHECKS.md#a-failure-that-the-default-branch-has-too)).
- When the slice's tests fail after the code writer, or the test command or the check command
  fails at the code commit, one fresh code writer gets the output. After a failed check command,
  the session first unticks the boxes of the slice.

> **Owner:** When the last retry still fails, the build stops. The session puts the failure to the
> owner as one question, with the evidence.

#### A disputed test

A *disputed test* is a committed test that the code writer says is wrong. The spec rules on it,
never the code writer. That the spec rules is the owner's decision. The steps below are defaults
([chapter 1](#1-start-here)).

![A fresh test writer rules on a disputed test by the spec, the owner answers when the spec
cannot settle it or the test is disputed a second time, and the work then comes
back.](diagrams/disputed-test.svg)

*Figure:* A disputed test, from the dispute to the work coming back: two rulings by the spec,
and one answer by the owner.

The session sets the code writer's work aside: it restores the test files, and stashes every
other file that the writer changed or added. A fresh test writer that has never seen the code
reads the test, the spec and the evidence, and rules on each disputed test:

- The spec backs the code writer: the test writer corrects the test.
- The spec backs the test: the test stays as committed.

After a correction, the red check runs on the corrected tests while the work stays aside. The
corrections become one more tests commit. In every case, also when every test stays as committed,
the work then comes back, and a fresh code writer runs part (e) again with the rulings.

> **Owner:** When the spec is silent or unclear, or the same test is disputed a second time, the
> session puts it to the owner as one question. The question carries the test, the spec text and
> the evidence of both writers. The owner's answer takes the place of the ruling. When the answer
> asks for a correction, a fresh test writer makes it.

> **Optional:** A [repo without specs](#a-repo-without-specs) has no spec to rule by, and its own
> rule for a disputed test.

#### A bug found during the build

The code writer reports each bug it finds. Where the bug sits decides what happens. These routes
are defaults ([chapter 1](#1-start-here)):

- **A test reaches it, or the code is new.** A failing test of the slice or the test command
  reaches the bug, or the bug sits in code not yet committed. The code writer fixes it, and lists
  it under Bugs fixed, with a minimised repro, its seam and the confirmed hypothesis. The slice
  goes on, and the bug goes into the final report.
- **No test reaches it, in code of this change.** The bug sits in code that an earlier slice of
  this change committed. The code writer leaves it, and lists it under Bugs left. It becomes a
  *fix slice*: a new slice, added after the current slice's code commit, at the next free number,
  and built next. The session writes its slice block in `design.md`, beside a new task section
  with one task box for the fix. Its fields: `Delivers` the corrected behaviour; `Seam` the
  reported seam; `Depends on` the slice with the bug; `Done when` the minimised repro, written out
  in full, passes.
- **The code is older than the change.** The bug is a *lead*: a bug or a finding that is only
  listed in a report. It goes into the final report.

> **Owner:** A bug in code from before the change goes to the owner, as a scope question, only
> when the slice cannot be done without the fix.

#### The final report

After the last slice, the owner gets one report:

- the default branch of the build, on a line `Base: <branch>`;
- each slice with its commits (hash and title);
- every assumption, with the question it answered;
- every bug fixed, every fix slice and every lead;
- every disputed test, with its ruling and its correction commit;
- every guard test, and every base failure with the owner's answer;
- every failed check, with its slice, its round and what was restored or retried;
- every stop of the build, with its cause and the owner's answer. A resume counts as a stop: the
  report names the slice and the part that the run resumed at, and says that it does not hold
  what the earlier run reported;
- the `Project rules:` line of the `commit` skill, once for the build: it names each rules section
  that the skill read, or it says `defaults` ([The repo's own files](#the-repos-own-files));
- the `Check command:` line of the `commit` skill at the code commits, once for the build: it
  names the check command and its result, or it says `none`.

The session writes the same report to `build-report.md` in the change folder, and commits that
file alone, after the last code commit: the report names every commit, and a commit cannot hold
its own hash. A build that ends at a stop before its last slice is closed writes no
`build-report.md`: the run that resumes it writes the file. The result gate reads the file there
([Owner gates](#owner-gates)), because verify runs in a fresh session. When the check command fails
at that commit, no code changes, and the session asks the owner one question: correct the report
and commit it again, or stop.

The item on failed checks shows the owner when the test-lock check fires, so that the owner can
add a hook then. The next step is [verify](#step-4-verify). The session names the verify command,
and the owner runs it in a fresh session. The build session does not start verify, so that verify
reads the work without the context that wrote it.

### Step 4: Verify

**Goes in:** every slice closed on the working branch, nothing pushed, and the final report in
`build-report.md`.

**Who acts:** the agent: the session that runs verify, and fresh writers in the fix round. The
owner starts verify in a fresh session, not in the session that built the change.

**What happens:**
1. The verify command starts verify. It runs parts 2 and 3 itself, and it runs OpenSpec's
   generated `openspec-verify-change` skill for part 4.
2. Verify finds the default branch by the rule of [Before the first slice](#before-the-first-slice).
   The test command and the check command run once. With check scripts, the slice check runs
   again (the check-scripts callout in [Per slice](#per-slice)). In a repo with specs, the
   test-lock check then runs once over the working branch (the Note below).
3. Verify follows the repo's verify rules file: the repo's own rules, and the verify checks
   ([The verify rules file](#the-verify-rules-file)).
4. OpenSpec's own comparison checks the code against the specs, the design and the tasks.
5. Verify writes its report as text to the owner, on every pass, the second pass of the fix round
   included. The report names the default branch on a line `Base: <branch>`, and lists each answered
   offence and each answered finding about a past commit. The fix round and the result gate start
   only after the report.
6. With no finding, verify has passed. With findings, one fix round follows
   ([The fix round](#the-fix-round)). Each later verify run starts a round of its own, which
   appends its own `## Fix round` section to `build-report.md`.

**Checks:** parts 2 to 4 above.

**Comes out:** a verified change, or a finding that is still open, with the owner
([The fix round](#the-fix-round)).

**Stops for the owner when:**
- at the start, when no change is named and several changes are active: which change to verify;
- none of the branches that the default branch rule names exists
  ([Before the first slice](#before-the-first-slice));
- in a repo with specs, the config names no test command;
- in a [repo without specs](#a-repo-without-specs), the config names no check command;
- in the fix round, for each offending commit that no answer in `build-report.md` covers: keep the
  edit, or restore the test (the Note below);
- in the fix round, for each finding about a past commit that no answer in `build-report.md`
  covers: keep the commit, or stop ([The fix round](#the-fix-round));
- in the fix round (its Owner callout in [The fix round](#the-fix-round)).

> **Optional:** With [owner gates](#owner-gates), the result gate follows a passed verify, and may
> stop for the owner.

> **Note:** At verify, the test lock is one check over the whole working branch, with or without
> check scripts. It holds when no commit in `<default branch>..HEAD` without a `Tests-For`
> trailer adds, changes, deletes or renames a test file, and the tree holds no uncommitted
> test-file change. A `Tests-For` trailer whose value is not one slice name or `verify` counts as
> missing. So a tests commit whose trailer check failed in the build shows as an offence here (for
> the owner's veto). `slice-build` holds the commands
> ([`CHECKS.md`, Test lock at verify](skills/slice-build/CHECKS.md#test-lock-at-verify)). Each
> failure of the test command or the check command, each offending commit that no answer covers
> and each uncommitted test-file change is a finding for the fix round. A base failure that a
> record in `build-report.md` answers is no finding, as long as it still fails on the default
> branch: verify runs that check again on each pass.
>
> An offending commit stays on the branch, because the flow never amends. Only the owner's answer
> clears it. Verify puts one question per offending commit to the owner: keep the edit, or restore
> the test. The session writes the answer into `build-report.md` with the commit's full hash. A
> later verify reports that offence as answered, and it is no finding. A test-file change that is
> not committed is never answered away: it stays a finding until it is committed in a tests commit
> or the owner removes it.

#### The verify rules file

The *verify rules file* is a file that the repo keeps beside its OpenSpec config. OpenSpec never
writes it. It holds the repo's own verify rules and the verify checks:

- **The code review.** The `code-review` skill reviews the change once in each verify run, against
  the repo's written standards and a smell baseline (the skill's fixed list of code smells) only.
  The *written standards* are the repo's written rules for code, in its guide or in a standards
  file. The repo's `## Written standards` section may list further files. OpenSpec's comparison
  (part 4 of verify) checks the specs, so the review has no spec part. The skill stays callable by
  hand on any branch. The verify rules file names the skill by its full name,
  `idea-to-code:code-review`.
- **The check for unasked work.** Each behaviour that the diff adds must be asked for by a
  requirement, a scenario, a task or a Done when line. Each miss is a finding.

> **Optional:** With user stories, the user-story check is a verify check too (the user-stories
> callout in [The change folder](#the-change-folder)).

The verify command applies the verify rules file, where the repo has one
([Steering verify](#steering-verify)). In a repo with no verify rules file, the verify command
loads `code-review` once, and runs the check for unasked work by hand.

> **Open:** A repo whose verify rules file does not call the code review gets no code review at
> verify. The load by hand holds only in a repo with no verify rules file. Until this is decided,
> the profile records which repos have a verify rules file without the code review.

#### The fix round

The *fix round* is the one round after verify that fixes the findings. The session that ran
verify loads `slice-build` for it. The round runs like a slice: fresh writers do the work, the
session commits, and the defaults of [When a part fails](#when-a-part-fails) apply. One
exception: in this round, no bug becomes a fix slice.

A *finding* is a result of verify that points at something to fix or to list. The session sorts
each finding into one route:

- **Fix.** The finding cites something written: an unticked task, a requirement or scenario not
  met, a behaviour nobody asked for, or a breach of a written standard.
- **Test first.** A Fix finding that needs a test changed or added before the code.
- **Owner.** The finding needs a spec change, or it is unasked behaviour that is worth keeping,
  or it is a base failure that no record answers: keep it out of the change, or fix it here.
- **Lead.** A smell with no cited rule. It is a [lead](#a-bug-found-during-the-build), and the
  report only lists it.
- **Past commit.** A finding about a commit already made, which no code can fix, because the flow
  never amends: its message breaks a commit rule of the repo. It goes to the owner, one question per commit: keep it as it is, or stop, which leaves
  the finding open. No option offers a fix.

A failure of the test command or of the check command at verify is a Fix finding. A test-lock
finding of verify is an Owner finding: its commit stays on the working branch, because the flow
never amends, so no route of the round removes it. Only the owner's answer clears it (the Note on
the test lock in [Step 4](#step-4-verify)). The answer to restore the test brings the test back in
a tests commit with `Tests-For: verify`. The offending commit stays in the history, and its record
in `build-report.md` answers it.

A finding of the route Past commit works the same way. The answer to keep closes the finding. The
answer to stop writes no record, and a later verify asks the question again. The session writes
each keep answer into `build-report.md` with the commit's full hash, and commits that file. A later verify lists the
finding as answered, and it is no finding. Both kinds of answer have one record form: one line
with a kind field (`lock`, `past` or `base`), under `### Answers` in the part `## Fix round` of the file
([`CHECKS.md`, Answers in the build report](skills/slice-build/CHECKS.md#answers-in-the-build-report)).

> **Note:** A lead that the report lists does not keep verify from passing. This is a default
> ([chapter 1](#1-start-here)): a rule of the repo guide may say that a listed lead is an open
> finding.

Inside a change, refactoring happens only as a Fix finding that cites a written standard.

![The fix round sorts each finding into one route, puts each Owner finding and each Past commit
finding to the owner, and runs the Fix and Test first findings in five parts.](diagrams/fix-round.svg)

*Figure:* The fix round sorts each finding into one route, and runs the Fix and Test first
findings in its five parts.

The round runs five parts, in this order:

1. One fresh test writer writes the tests for the Test first findings. The red check runs on
   them, and the session makes a tests commit. That commit belongs to no slice, so its trailer is
   `Tests-For: verify`.
2. One fresh code writer gets every Fix and Test first finding, and the diff of the change. It
   fixes each finding at every place of the diff that breaks the same rule, not only at the place
   that the finding names. The test files are locked at the commit it starts from.
3. The test-lock check runs against that commit.
4. The test command passes. The session ticks each task box that the fix completes, and commits
   the fix.
5. Verify runs once more.

An owner's answer that asks for a fix moves the finding to Fix. An answer that keeps unasked
behaviour writes the behaviour into the change's delta spec, and closes the finding. An answer
that changes the spec writes the change the same way, and the finding goes to Test first. The
round's first commit carries each spec edit.

There is one round only, apart from a round that the owner's answer at the result gate starts
([Owner gates](#owner-gates)). The round's report lists each finding with its route and outcome, the
round's commits, every question put to the owner, every lead, the `Project rules:` line and the
`Check command:` line ([The final report](#the-final-report)). Before verify runs once more, the
session appends that report to `build-report.md`, with the record of each owner's answer on a
test-lock offence or on a past commit, and commits that file alone.

> **Owner:** The session puts each of these to the owner as one question:
>
> - a tests commit of an earlier fix round at the end of the working branch, before the round
>   sorts a finding;
> - each Owner finding other than a test-lock offence or a finding about a past commit (the stops
>   of [Step 4](#step-4-verify) cover those), before the code writer starts;
> - every bug on a Bugs left line;
> - a finding still open after the second verify ([The pull request](#the-pull-request) says what
>   this blocks);
> - every stop of a default of [When a part fails](#when-a-part-fails);
> - a failed check command at the commit of `build-report.md`;
> - every hand-back of an owner decision.

> **Optional:** A [repo without specs](#a-repo-without-specs) changes verify and the fix round.

> **Example:** The test command and the check command pass, and so does the slice check script.
> The test-lock check finds no commit without a `Tests-For` trailer that touched a test file. The
> code review finds one breach of a written standard. The handler
> writes `filename must not be empty` inline, but the repo guide says that every message a client
> sees comes from `upload/messages.py`. The review also notes a smell with no cited rule: the file
> name is a plain string in four functions (Primitive Obsession). The check for unasked work finds
> nothing, and so does OpenSpec's comparison.
>
> In the fix round, the breach is a Fix finding, and the smell is a lead. One fresh code writer
> moves the text into `upload/messages.py`, with the test files locked. The test-lock check
> passes, and `pytest` passes. The session makes commit 6,
> `refactor(upload): take the empty-name message from the messages file`, with
> `upload/handler.py` and `upload/messages.py`. It appends the round's report to
> `build-report.md`, and commits it as commit 7. Verify runs once more. It finds only the lead
> again. A listed lead does not keep verify from passing, so verify has passed. The lead stays in
> the fix round's report.

### Step 5: Pull request and archive

**Goes in:** a verified change.

**Who acts:** both. The agent pushes the working branch and opens the pull request. The merge
rule says who merges. Who starts the archive is open ([The archive](#the-archive)).

**What happens:** three parts, one subsection each: [the pull request](#the-pull-request),
[the archive](#the-archive) and [the merge](#the-merge). The order of the subsections is not a
time order: when the archive runs is open.

**Checks:** before the pull request opens, the `pr` skill checks the body. It refuses a body over
its word cap, and a bare `@` in the title or the body. It also refuses a body under a `!` title
that does not end with its footer block ([The pull request](#the-pull-request)). An agent merge
has its own conditions ([The merge](#the-merge)).

**Comes out:** the change squash-merged to main: its requirements in the main specs, and its change
folder in the archive.

**Stops for the owner when:**
- the pull request is breaking ([The merge](#the-merge));
- the merge rule makes the merge wait for the owner ([The merge](#the-merge));
- a review finding on the pull request is still open ([The merge](#the-merge)).

#### The pull request

Nothing is pushed while verify has not passed. After a passed verify, the agent pushes the
change's working branch on its own, with a lease push (`--force-with-lease`), and opens the pull
request on its own. It never pushes to main. It never pushes with `--force` or `-f`: every push of
the working branch is a lease push. This holds only for a change built through the flow. Any
other push needs the owner's ask.

The title of the pull request has the form of a commit title, by the repo's commit rules. The `pr`
skill writes the body in the project's text rules. The body is short, and says only what the diff
and the title cannot. It links the change folder in the archive, instead of restating the change.
Then the agent gives the owner the link to the pull request. Under the default merge rule, it says
that the owner merges.

A *breaking pull request* has `!` in its title. The `pr` skill ends its body with the
*breaking-change footer*, in a fenced block. The footer says what broke, and how a consumer
migrates.

> **Optional:** With [tracker issues](#while-the-changes-run), the body ends with a
> `Part of <issue URL>` line. With an [enhancement store](#from-draft-to-delivered), the body
> names the entry line that the change delivers.

> **Optional:** With [owner gates](#owner-gates), nothing is pushed before the result gate ends.

> **Note:** The `pr` skill states defaults, such as its word cap. A point of the repo's
> `## Pull request rules` or `## Text rules` section (a line that starts with a fixed label, such
> as `Word cap:`) replaces the default of its own label. A plain line of a section wins only over a
> default that has no label. A rule that this document states for every project, such as the ban on
> a bare `@name`, wins over the repo's rules and over the defaults.

#### The archive

Archiving moves the change folder into the archive, and folds its delta specs into the repo's
main specs. OpenSpec's `openspec-archive-change` skill does the archive. The archive commit goes
into the change's own pull request.

> **Open:** Who starts the archive, and whether it runs before or after the pull request opens, is
> not decided. No step command starts it. Until this is decided, the profile names who starts
> OpenSpec's archive skill, and when.

> **Optional:** A [repo without specs](#a-repo-without-specs) changes the archive.

#### The merge

The project's *merge rule* says who merges a pull request. By default, the owner merges, and the
agent merges no pull request. A repo sets another rule in its `## Merge rule` section, and the `pr`
skill applies that section as its last step. Without release rules, one rule holds for every pull
request. For example, the agent merges on green checks and a passed verify.

When the agent merges, it merges only a pull request that it opened. It merges only after every
required check is green, verify has passed, every review finding on the pull request is closed,
and the text keeps the project's text rules. It uses a plain squash merge, never a merge that
bypasses the host's branch protection.

By default, whoever merges a breaking pull request gives the footer's text, without the fence
lines, as the squash commit message. A repo's `## Release rules` section may name another way.

Pull requests are squash-merged, so main never sees a failing tests commit.

> **Owner:** A breaking pull request waits for the owner's approval. Another pull request waits
> for the owner when the merge rule says so.

> **Optional:** With [release rules](#release-rules-tied-to-commit-types), the merge rule may let
> the type in the title decide who merges.

> **Example:** The service's profile says that the agent runs the archive before it pushes. The
> archive moves the change folder into the archive, and folds the requirement into
> `openspec/specs/upload/spec.md`. The archive commit goes into the pull request. The agent
> pushes `refuse-empty-file-name` with a lease push, and opens the pull request
> `feat(upload): refuse an upload with an empty file name`. The `pr` skill writes the body, which
> links the archived change folder. The owner gets the link. The service's repo has no
> `## Merge rule` section, so the default holds: the owner merges the pull request. It is
> squash-merged: main gets one commit, and the failing tests commits never reach main.

### After main

Releases follow the project's release process, with its rules for tags and for publishing. The
repo's `## Release rules` section holds them. Where a release tool cuts releases, nobody tags or
publishes by hand.

> **Optional:** With [release rules](#release-rules-tied-to-commit-types), the release tool reads
> the merged titles, and opens a release pull request only for a commit whose type cuts a release.

## 3. Other roads

Three kinds of work change the path. Each road says which steps it changes. The tracks that need
an enhancement store or a tracker issue are in [chapter 4](#4-optional-parts).

### A small change

A small change may take two shortcuts: the fast path skips step 1, and the form with no Slices
section changes steps 2 to 4. A *small change* is a change in one repo, with at most two task
sections by default.

#### The fast path

The fast path skips step 1 and starts at step 2: the owner types the propose command. Before
anything is written, propose checks four things, read-only:

- the outcome and the done-test each fit in one sentence;
- no owner decision is open;
- the change has at most two task sections;
- no assumption is open.

When one check fails, step 2 writes nothing, and points to the explore command. An open assumption
is then settled in the side step (the side-step callout in [The grill](#the-grill)).

With no explore, no seam is agreed yet. When the four checks pass, propose asks each seam before
it writes, one question per distinct seam ([Step 2](#step-2-propose)). An open seam fails none of
the four checks.

#### No Slices section

A small change needs no Slices section, and it may have no `design.md` at all. `slice-build`
treats any change without a Slices section as a small change. Each task section is then one slice,
built in order, with no Done when line. By default, each slice depends on the section before it,
and the gate checks that section's boxes. Propose writes the slice's agreed seam on a `Seam:` line
directly under the `## N.` heading of its task section, where a line is safe
([The task sections](#the-task-sections)). Where a task section has no such line, as in a change
written by hand, the test writer picks the seam closest to the public interface, and lists it as
an assumption. The slice delivers the scenarios whose behaviour its tasks add.

A fix slice in a small change writes its four fields as the first lines of its new task section.
It depends only on the slice that its `Depends on` line names.
[A bug found during the build](#a-bug-found-during-the-build) has the base rule. The check scripts
and verify must handle a change with no Slices section too.

### A bug

Where a bug is found decides its road. This road changes step 3 or step 4, or it runs outside the
steps.

- A bug found during a build: [A bug found during the build](#a-bug-found-during-the-build).
- A bug found in the fix round: [The fix round](#the-fix-round).
- A reported bug: the `diagnosing-bugs` skill, below.

For a reported bug, `diagnosing-bugs` runs a diagnosis loop:

1. It redacts every secret first.
2. It builds a loop that goes red on the bug.
3. It minimises the repro.
4. It ranks its hypotheses, and shows them to the owner, without waiting when the owner is away.
5. It tags its debug logs, so that the cleanup is one search.
6. It writes a regression test where a correct seam exists, then the fix. When no correct seam
   exists, it reports that as a finding.
7. It checks the cleanup.

The skill writes loop code, so it never runs inside a read-only step such as explore. Explore
names the bug and pauses, the skill runs, and explore resumes with the finding. A bug fix may be
[work outside a change](#work-outside-a-change).

As a last resort, for a loop where a person must act, the agent writes a script. The owner runs
it in their own terminal, and pastes the captured block back.

> **Owner:** When no loop can be built, the agent asks the owner one question with three options:
>
> - access to an environment that reproduces the bug;
> - a captured artifact, with its secrets redacted;
> - temporary instrumentation in production, named as a security trade-off.
>
> The agent forms no hypothesis without a loop. When the redacted output is not enough to
> diagnose the bug, the agent says so, and asks the owner for the missing signal as one question.

### Work outside a change

Some work never becomes a change. This road uses none of the five steps.

For a bug fix or a chore, one agent may write both the test that shows the bug and the fix. The
split into two writers, and the test-lock check, hold inside a change only.

The `tdd` skill covers test-first work here: one seam, one test and one minimal implementation per
cycle. Each new test is red for the right reason (the red check in [Per slice](#per-slice)).

> **Owner:** The agent proposes the seams, and puts each seam to the owner as one question, one per
> seam. Each option says what that seam catches and what it misses.

Refactoring outside a change belongs to the `code-review` skill. The commit rules of
[chapter 1](#1-start-here) still hold, and a push needs the owner's ask
([The pull request](#the-pull-request)).

## 4. Optional parts

Each part below says when a project needs it, where it joins the path, and how the flow reads
without it. A project skips what it does not use. Four smaller optional parts sit in Optional
callouts at their steps:

- the side step and the evidence folder ([The grill](#the-grill));
- glossary and decision records ([The grill](#the-grill));
- user stories ([The change folder](#the-change-folder));
- check scripts in place of checks by hand ([Per slice](#per-slice)).

### An enhancement store

**When a project needs it.** A project needs a store when it designs major features that span
repos before any repo change. Only a major feature becomes an enhancement. Work is not an
enhancement only because it spans repos: the size of the feature decides. A breaking change to a
public contract is not an enhancement by that fact alone. The reason: the store is the design
record of major features, and an entry for every change across repos dilutes it.

An *enhancement* is a major feature that spans repos, designed in the store before any repo
change. The *store* is the repo where enhancements are designed, registered as an OpenSpec store.
An *entry* is one enhancement in the store, kept as an OpenSpec change.

**Where it joins the path.**

- the first two questions of [the track question](#the-track-question);
- the entry line, named in the proposal ([The change folder](#the-change-folder)) and in the pull
  request body ([The pull request](#the-pull-request));
- the repo list of a tracker issue, taken from the store's list of repos
  ([Opening the issue](#opening-the-issue));
- the store correction line of a tracker issue ([Closing the issue](#closing-the-issue)).

**Without it.** The track question loses its first two questions, and every feature is one change
per repo. A proposal names no entry line. A tracker issue has no store correction line, and its
repo list comes from the project's own list of repos.

The store is one repo, registered as an OpenSpec store on each machine that uses it, and each repo
lists it under `references:` in its OpenSpec config (checked on OpenSpec 2.1.1). When the store is
not registered, the agent reports it and goes on. A person registers the store; an agent never does.

#### An entry

One entry is one OpenSpec change in the store, with an id that is never reused or renumbered. A
text that cites an entry gives the reason in words, beside the id. It never gives the id alone,
and never a decision number.

- Its design holds themes, not numbered decisions. Entries stay short and high level.
- Its delta specs hold the requirements until delivery. Each requirement must be observable from
  outside one repo, and must carry SHALL or MUST and at least one scenario.
- Its tasks list which repos still have work. That list is advice on order, not a schedule.
- Its evidence folder holds cited, dated notes.

By default, a store proposal has no user stories, because an agent that works in one repo cannot
read the store.

> **Note:** The *proposer*, the person who proposes the entry, owns the proposal word for word. An
> agent drafts it only from what the proposer said, and changes it only on the proposer's
> instruction.

#### From draft to delivered

An open entry is a draft: a *live entry*. The accept step refuses the entry while its open
questions still list a blocking question or an answered one. Repo changes deliver its task lines.
Each such change names the entry and its line, the *entry line*, in its proposal and in its pull
request body. A proposal that delivers no line says so, in the same place. A later pull request on
the store ticks the line. A delivered entry is archived.

The store's main specs hold delivered behaviour only. They change only on delivery, by a seed or a
store correction (store changes that are not entries), or by a fix to a spec's purpose.

The flow names no command that makes or changes an entry. Each project builds that part its own
way, and its profile says how.

> **Open:** Whether the track question's test of what makes work an enhancement needs more than
> the size of the feature is not decided. Nothing on the store's side checks that a line of a
> live entry was delivered. Until these are decided, the track question stays as step 1 gives it,
> and the profile says how the project checks a delivered line.

#### Corrections

A *store correction* brings delivered requirements in line with behaviour that has already
shipped. It never carries new behaviour, and it may cite only merged changes.

### A tracker issue for several repos

**When a project needs it.** A project needs it for work over several repos that is not a major
feature. Where the project has no store, it needs it for all work over several repos. Each repo
gets one ordinary change, and one issue ties the changes together: a *tracker issue*, in a repo
that hosts such issues. That repo does not become a store. The reason: the failure this part
prevents is a forgotten repo, not a wrong order.

**Where it joins the path.**

- the start of explore, which lists the open tracker issues
  ([The explore command](#the-explore-command));
- the third question of [the track question](#the-track-question), and the repo list at the end
  of explore ([Opening the issue](#opening-the-issue));
- the pull request body ([The pull request](#the-pull-request));
- step 5 of each change: a link when its pull request opens, a tick when it merges, and the close
  ([While the changes run](#while-the-changes-run), [Closing the issue](#closing-the-issue));
- the store correction, where the project has a store ([Corrections](#corrections)).

**Without it.** Each repo's change stands alone. The track question loses its third question.
Explore ends with no repo list, pull request bodies have no "Part of" line, and nothing checks that
every repo was done. A one-repo project drops this part entirely.

![The track question, which the owner answers: its three questions in their order, the optional
part that adds each, the track that each yes leads to, and one change in one repo when all are
no.](diagrams/track-question.svg)

*Figure:* The track question with both parts: the questions in their order, and the track that
each yes leads to.

#### Opening the issue

At the end of explore, the agent shows the *repo list*: each affected repo, and each unaffected
repo with a reason. The list comes from the project's list of repos, or from the store's list
where there is a store.

> **Owner:** The owner approves the repo list. Without that approval, the agent opens no issue.

On the owner's approval, the agent opens one issue, with the project's label and no code. The
body holds:

- an intro sentence;
- one unticked line per repo, in merge order;
- a "Not affected" section;
- a "Store correction" section, where the project has a store.

A line that names N repos needs N pull request links. A public tracker never names a private
repo. The issue's text keeps the same rules as a pull request's ([chapter 1](#1-start-here),
[The pull request](#the-pull-request)).

#### While the changes run

Each repo gets its own change and its own pull request. The body of each pull request ends with a
`Part of <issue URL>` line. "Part of" closes nothing. A pull request with no change carries the
link in its body only.

The issue gets three kinds of write: a link when a pull request opens, a tick when it merges, and
one close. Each write reads the body first, and changes only one repo's line. Sending the saved
body back undoes a wrong tick or link, but only while no later edit followed.

#### Closing the issue

The session that merges the last pull request closes the issue, once every repo line is ticked.
When the work made a store spec wrong, a [store correction](#corrections) is the issue's last
line. The session that merges the last code pull request starts the correction at once, because
a correction may cite only merged changes. Then the issue closes only when the correction is
delivered.

### Many repos in one workspace

**When a project needs it.** A project keeps several independent repos side by side in one
workspace, and wants the same flow in each. Each repo must still work in a lone clone
([What a repo needs before its first change](#what-a-repo-needs-before-its-first-change)).

**Where it joins the path.**

- before step 1: the session names the repo it works in
  ([The explore command](#the-explore-command));
- step 3: the session resolves the repo root ([Before the first slice](#before-the-first-slice));
- every step: a root command may pick the repo first ([The kit](#the-kit)).

**Without it.** In a one-repo project, the kit is the repo's own files and scripts, with the
skills and the step commands from the plugin ([The kit in every repo](#the-kit-in-every-repo)).
There is no shared rules file and no root command.

Nothing that the flow needs may live only at the workspace root. A project with many repos may
keep routing commands of its own: such a command picks the repo, and then starts the plugin's step
command there. Where only a person can start a step command, the routing command names it, and
the owner types it. No step command is locked, so a routing command may start the build command
too ([Steering the build](#steering-the-build)). A routing command at the workspace root is a *root
command*. Everything else is in the repo, or the repo names where it comes from
([The kit in every repo](#the-kit-in-every-repo)). When the target repo is unclear, or the work
spans repos, the agent asks one question. The agent names the repo before it edits, and commits to
a repo from inside it.

#### The kit in every repo

Each repo gets the [kit](#the-kit), with one shared rules file and the settings file of the
[text hook](#the-kit). The skills and the four step commands reach every repo through one plugin,
`idea-to-code`: each person installs it, and each repo names it in its settings. A clone then
holds the pointer to them, and no command file. The profile says which parts of the kit stay as
files in each repo.

The plugin keeps the [credit and licence duties](#credit-and-licence-duties). The *shared rules
file* holds the rules sections for every repo. Each repo keeps its own copy inside the repo, and
its repo guide names the copy on a `Rules file:` line
([The repo's own files](#the-repos-own-files)). An import line (a line of the repo guide that
loads another file) may also load the copy, but no skill relies on it.

### Release rules tied to commit types

**When a project needs it.** A release tool versions from the titles of squash-merged pull
requests.

**Where it joins the path.**

- step 5, [the merge](#the-merge);
- [after main](#after-main).

**Without it.** One merge rule holds for every pull request ([The merge](#the-merge)), and commit
types carry no release meaning. The rules of step 5 for a breaking pull request still hold
([The pull request](#the-pull-request), [The merge](#the-merge)).

The type at the start of a pull request's title says whether the pull request cuts a release. For
example, `feat` and `fix` do, and `chore` and `test` do not. The repo's `## Release rules` section
holds the full list. Where the repo's `## Merge rule` section says so, the agent merges a pull
request whose title cuts no release, under the conditions of [The merge](#the-merge).

> **Owner:** A pull request whose title cuts a release waits for the owner's approval. The owner
> can override this rule. By default, an override works either way, for one pull request at a
> time.

### A repo without specs

**When a project needs it.** A project needs it when a repo's OpenSpec schema has no specs
artifact, for example a repo of docs, configuration, or content with few or no tests. Such a repo
is a *repo without specs*.

**Where it joins the path.** Steps 2 to 5, as listed below. Detection is automatic.

**Without it.** Every repo has a specs artifact and tests written from specs, or such repos stay
outside the flow.

When the repo's schema has no specs artifact, the build skips four parts for every slice: the
test writer, the red check, the tests commit and the test-lock check. The gate, the code writer
and the commit still run. Each step changes like this:

- **Step 2.** The change has no delta specs. A Done when line covers each user story (the
  user-stories callout in [The change folder](#the-change-folder)).
- **Step 3.** One fresh code writer builds each slice from its `Delivers` and `Done when` lines.
  Its report says how it showed that each Done when line holds. The check command must pass. One
  commit closes the slice. It carries the files that a tests commit would add, and never the
  `Tests-For` trailer. By default, a bug in this change's code is fixed in that slice's commit,
  and listed. By default, the code writer leaves the existing tests as committed.
- **Step 4.** Verify runs the check command once, as its test command, and skips the red check
  and the test-lock check. When the config names no check command, verify asks the owner for it,
  as the build does. The user-story check reads the Done when lines. In the fix round, the test
  writer, the red check, the tests commit and the test-lock check are skipped. An owner's answer
  that keeps unasked behaviour, or that changes the spec, is written into `design.md`, and a
  spec-change finding goes to Fix, not to Test first.
- **Step 5.** The archive only moves the change folder, because the repo has no main specs.

![The seven parts of a slice in a repo without specs: the gate, the code writer and one commit
run, and the other four parts are skipped.](diagrams/slice-without-specs.svg)

*Figure:* A slice in a repo without specs skips four of its seven parts, and one commit closes it.

`openspec update` puts the sync skill back whenever archive or bulk-archive is in the workflow
list (OpenSpec 2.1.0). In a repo without specs, following the sync skill changes no file.

> **Owner:** By default, a disputed test, or a needed test change, goes straight to the owner,
> because there is no spec to rule by.

> **Open:** A small change in a repo without specs has no Done when line, although this build
> relies on it. Until this is decided, the profile says how the project builds such a change.

### Owner gates

**When a project needs it.** The owner wants to see the plan before the build, or the verified
change before the pull request, but only on the changes where a look matters.

**Where it joins the path.**

- step 2, [propose](#step-2-propose): the *plan gate*, after the change folder is written;
- step 3, [before the first slice](#before-the-first-slice): the build reads the outcome;
- step 4, [verify](#step-4-verify): the *result gate*, after a passed verify;
- step 5, [the pull request](#the-pull-request): nothing is pushed before the result gate ends.

**Without it.** No owner gate runs. The owner still decides at every stop of the path.

An *owner gate* is a point where the agent decides whether the owner looks at the work before the
work goes on. An owner gate is soft: no hook and no script enforces it. The agent applies it, and
records what it did. There are two owner gates, and each is optional on its own. Both are on, unless
a gate line turns one off: `Plan gate: off.` or `Result gate: off.` The line stands in the repo
guide, or in the `context:` block of the OpenSpec config. A line that says in other words that a
gate is off turns no gate off: the agent reports it, and asks the owner one question. The owner
can turn one on or off for a single change, with a word.

For an owner gate that is on, the agent checks the gate's criteria. When no criterion holds, the
gate passes and the work goes on. When one holds, the agent stops and shows the work to the owner.
By default, the criteria are these, and a rule of the repo guide may add others:

| Owner gate | The owner looks when |
| --- | --- |
| The plan gate | the plan rests on an assumption; or the change touches a public contract or is breaking |
| The result gate | verify needed a fix round; or the final report names a disputed test, a bug or a stop; or a lead or an Owner finding is still in the report |

The result gate reads the build's final report from `build-report.md` in the change folder ([The
final report](#the-final-report)). Where that file is missing, as after a build by hand, the agent
asks the owner one question about the report. This is a default: a rule of the repo guide may say
what holds then. Where another criterion already holds, the agent asks no question about the report:
the owner looks at the result anyway, and the `reason` in `gates.json` says that the report was not
checked. At the result gate, the agent also lists each answer in the build report (each test-lock
offence and each finding about a past commit that the owner answered), so that the owner sees what
the test lock and the flow let stand.

With a *review tool*, the agent opens the real files in the tool and waits: the change folder at the
plan gate, and the diff of the working branch at the result gate. The tool is optional: the flow
needs none. Without one, the agent shows a summary and asks one question, in the question form.

> **Owner:** The owner answers the review with one of three: approve; approve with changes (the
> agent makes them and goes on; a change to code or tests runs one more fix round, and verify
> runs once more); or change and show again (the agent makes them and runs the review again).
> The agent never approves for the owner. While the owner is away, the work waits.

The agent writes the outcome of each owner gate to `gates.json` in the change folder. The file is
one of the change's files: it reaches main in the change's own pull request, and it is archived
with the change. OpenSpec's validate and archive accept it (checked on OpenSpec 2.1.1). The build
reads it before the first slice, and does not start while a plan gate that is on has no outcome.
The first commit that the build makes carries the file. The build makes no commit that holds only
`gates.json`. After the result gate, the agent commits the file once more. That commit holds only
`gates.json`: it is the gate's commit, not a commit of the build.

```json
{
  "plan": {
    "outcome": "reviewed",
    "source": "criteria",
    "criteria": ["assumption"],
    "reason": "The plan stores the error text in a new messages file. No explore answer covers where the text lives.",
    "result": "approve-with-changes",
    "comments": [
      {
        "comment": "Put the text in the handler, no new file.",
        "change": "design.md: the messages file is removed; S1 names the handler."
      }
    ],
    "datetime": "2026-11-23T08:14:00Z"
  },
  "result": { "outcome": "off", "source": "config" }
}
```

- `outcome`: `off` (a gate line), `skipped` (the owner's word), `passed` (no criterion held) or
  `reviewed`.
- `source`: what set the outcome: `guide`, `config`, `owner` or `criteria`.
- `criteria`: the criteria that held. Only with `passed` and `reviewed`.
- `reason`: the agent's reasoning, in one to three sentences. It is not a transcript. For
  `skipped`, it is the owner's word. Only with `passed`, `reviewed` and `skipped`.
- `result`: the owner's last answer: `approve` or `approve-with-changes`. Only with `reviewed`.
- `comments`: each comment of the owner, with the change that the agent made for it. Only with
  `reviewed`.
- `datetime`: when the gate ended, in UTC, as ISO 8601 with `Z`. Only with `passed`, `reviewed` and
  `skipped`.

A record with the outcome `off` holds `outcome` and `source`, and no other field. A record with
the outcome `skipped` holds `outcome`, `source`, `reason` and `datetime`.

## 5. Setting up a project

A project sets up each repo once, before the repo's first change, and answers its profile.

### What a repo needs before its first change

The repo's own files must be enough to run the whole flow in a lone clone. A *lone clone* is the
repo cloned on its own, outside any workspace.

#### OpenSpec

The repo pins one OpenSpec version, and a check fails when the installed version is not the pin.
A project may install the pinned version per repo from a saved lockfile. Outside CI, a plain
`openspec update` checks for a newer version and prints an upgrade command (OpenSpec 2.1.0). An
agent never runs that command, because it moves the installed version off the pin.

The repo's `openspec/config.yaml` holds the schema, `references:` (where the project has an
[enhancement store](#an-enhancement-store)), a `context:` block, a `rules:` block per artifact,
and `operations:` guidance. Config text points only at files inside the repo. An example config,
with the flow's lines marked, is [`examples/openspec-config.yaml`](examples/openspec-config.yaml).

The `rules:` block carries the flow's lines. The `design` rule asks for the `## Slices` section
([The Slices section](#the-slices-section)), and the `tasks` rule asks for one task section per
slice ([The task sections](#the-task-sections)). Where the project uses user stories, the
`proposal` rule asks for the `## User stories` list. A rule that clashes with the build, such as
"one commit per section", is reworded to fit it.

A *config check*, run by the repo's [check command](#the-repos-own-files), refuses three things:

- a config that does not parse;
- a key under `rules` that names no artifact of the schema;
- a rule that is not plain text.

No `openspec validate` step stands in for it.

Three tool facts decide what a repo may change:

- `operations` accepts only `apply` and `archive`. An `operations.verify` key is dropped with
  "Unknown operation ID" (OpenSpec 1.17.0 and 2.1.0).
- `openspec instructions apply --json` carries the config `context` and the apply guidance. The
  `rules` reach only each artifact's own instructions, from `openspec instructions <artifact>`.
  The generated verify skill runs the same apply command (OpenSpec 1.17.0 and 2.1.0).
- `openspec update` writes each generated skill as a real file under `.agents/skills/`, and makes
  each generated skill's folder in the agent's skill folder a link to it. It compares each skill
  with the generated text, so every plain update wipes any hand edit (OpenSpec 2.1.0).

Because an update wipes every hand edit, nobody edits a [generated skill](#the-explore-command) by
hand. The repo commits the generated skills: the files under `.agents/skills/` and the links in the
agent's skill folder. A lone clone then holds them.

#### Steering verify

The repo owns the verify rules file, which OpenSpec never writes
([The verify rules file](#the-verify-rules-file) says what it holds). An example is
[`examples/verify.md`](examples/verify.md). The verify command applies the file on every run: it
tests whether the file exists, runs the checks of the repo ([Step 4](#step-4-verify)), and then
follows the file, before OpenSpec's comparison.

OpenSpec's generated verify skill does not name the verify rules file, so a run of that skill
alone skips it. As the guard, the repo guide holds one fixed line:

```text
A verify run on an OpenSpec change also applies `openspec/verify.md`, because the generated verify skill does not name that file.
```

A pointer in the `context:` block of the OpenSpec config is not a safe carrier, because a long
instructions output can be cut before the agent reads it. A line of the repo guide is always read.
Nothing writes into a generated skill.

> **Open:** OpenSpec's workflow list is set per machine. On a machine whose list lacks verify,
> `openspec update` deletes the verify skill (OpenSpec 2.1.0). The verify command then says so and
> stops. What a project does about the workflow list is not decided. Until it is, the profile says
> what the project does.

OpenSpec's default init profile, `core`, writes six skills. It does not write
`openspec-new-change`, `openspec-continue-change` or `openspec-verify-change`. The README's
setup steps set the custom profile with the full workflow list before init, and that init writes
twelve skills, with all the generated skills that this document names (checked on OpenSpec 2.1.1).

#### Steering the build

The owner starts a build with the build command, `/idea-to-code:build <change>`, typed or loaded
by the session. A request in words to build, apply or implement a change, or to work through its
tasks, may start a build. So may a yes or a go-ahead in words, after the agent named the build
command. The session then loads `idea-to-code:build`, never `slice-build` alone. The build command
runs its own first steps: it picks the change, then the plan gate, then the branch check. No step
command is locked. The plan gate, tests first, the test lock and the rule that the build never
starts verify stay.

OpenSpec's generated apply skill, `openspec-apply-change`, runs a task loop of its own, with no
tests first. The build command never loads it, and a request in words must not load it either. As
the guard, the repo guide holds one fixed line:

```text
A request in words to build, apply or implement an OpenSpec change, or to work through its tasks, loads `idea-to-code:build` and never `openspec-apply-change`.
```

The apply guidance of the OpenSpec config says the same for a run of the apply skill. It is no
safe carrier, for the reason that [Steering verify](#steering-verify) gives.

#### The repo's own files

The repo also has these files and commands:

- the repo guide, which the agent reads first ([chapter 1](#1-start-here));
- the *rules sections*: the project's own rules, under seven fixed headings (`## Commit rules`,
  `## Release rules`, `## Text rules`, `## Pull request rules`, `## Merge rule`,
  `## Decision records`, `## Written standards`). A section sits in the repo guide, or in one
  *rules file* inside the repo, which the guide names on a `Rules file:` line. A repo with no rules
  of its own writes none, and each skill then uses its defaults. The value `none` is refused on
  the three labels whose default is a ban, `Tags:`, `Publishing:` and `Mentions:`: the agent asks
  the owner one question with three options (write the rule in words, remove the point, or stop);
  until then the default ban holds. A template with every heading,
  label and default is [`examples/project-rules.md`](examples/project-rules.md);
- the written standards ([The verify rules file](#the-verify-rules-file));
- a *check command*: the repo's one command that runs its checks, named after
  `Checks before a commit:` in the `context:` block of the OpenSpec config. The `commit` skill
  runs it before every commit that is not a tests commit, after its own checks of the message, and
  a failure stops the commit. A repo with no such line has no check command;
- a test command, named after `Tests:` in the same block (the test-command note in
  [Per slice](#per-slice));
- where the project uses them, a glossary and a place for decision records: an ADR folder that a
  person makes, or a decision home that the `## Decision records` section names
  ([The grill](#the-grill)).

#### The kit

The *kit* is what a repo carries, or names, so that the whole flow runs in a lone clone:

- the kit skills ([The skills](#the-skills)) and the four step commands: the explore command
  ([The explore command](#the-explore-command)), the propose command ([Step 2](#step-2-propose),
  [The fast path](#the-fast-path)), the build command ([Step 3](#step-3-build)) and the verify
  command ([Step 4](#step-4-verify)). They come from the plugin, which the repo's settings
  name ([The kit in every repo](#the-kit-in-every-repo));
- the verify rules file, with the verify line in the repo guide
  ([Steering verify](#steering-verify));
- the build line in the repo guide ([Steering the build](#steering-the-build));
- the config check script, which the check command runs ([OpenSpec](#openspec));
- where the project uses them, the check scripts (the check-scripts callout in
  [Per slice](#per-slice));
- where the project uses one, a *text hook*: a hook that blocks a commit or pull request command
  whose text breaks the project's text rules. [Chapter 1](#1-start-here) says what the agent does
  then.

Each step command adds what the flow needs at its step. The four step commands ship in the
plugin: `/idea-to-code:explore`, `/idea-to-code:propose`,
`/idea-to-code:build` and `/idea-to-code:verify`. A repo carries no command file. A step command
is always written in full, because Claude Code has a command of its own named `verify`.

### The skills

The skills hold the exact rules that agents run. This document names each skill, and says what it
does. A skill holds the method and its defaults. The project's own rules sit in the repo ([The
repo's own files](#the-repos-own-files)). In the Origin column, *adapted* means that the skill comes
from Matt Pocock's AI Hero skills, with local changes. *Own* means that the skill was written for
this flow. *OpenSpec* means that OpenSpec generates the skill. *Upstream, not shipped* means that
the skill is upstream's own, the plugin ships no copy of it, and the reader installs it from
[upstream](https://github.com/mattpocock/skills/tree/abeeaf95660ba9e8b7c753eb38f441ca707a8823/skills/engineering/improve-codebase-architecture).

| Skill | Job | Step | Origin |
| --- | --- | --- | --- |
| `grilling` | Runs the grill; holds the question form. | 1, every stop | adapted |
| `research` | Settles a fact from primary sources, in a cited note. | 1, side step | adapted |
| `prototype` | Settles a design question with throwaway code. | 1, side step | adapted |
| `domain-modeling` | Writes a term or a decision record, on the owner's yes. | 1 | adapted |
| `codebase-design` | A reference: the words for deep modules and seams. | 1, 3 | adapted |
| `slice-build` | Builds a change slice by slice, tests first; runs the fix round. | 3, 4 | own |
| `tdd` | The rules for good tests and the red-green loop. | 3, outside a change | adapted |
| `diagnosing-bugs` | A diagnosis loop for hard bugs and performance regressions. | 3, a bug | adapted |
| `commit` | The rules for every commit. | every commit | own |
| `code-review` | Reviews the diff against written standards and smells. | 4, outside a change | adapted |
| `pr` | Writes the pull request body and the breaking footer. | 5 | adapted |
| `owner-gate` | Applies the two owner gates, and records the outcome. | 2 to 5, with owner gates | own |
| `improve-codebase-architecture` | Finds modules to deepen. | before 2 | upstream, not shipped |
| The four step commands | Start explore, propose, build and verify. | 1 to 4 | own |
| OpenSpec's generated skills | Explore; write, check and archive the change files. | 1, 2, 4, 5 | OpenSpec |

OpenSpec's generated skills on the path are `openspec-explore`, `openspec-propose`,
`openspec-new-change`, `openspec-continue-change`, `openspec-update-change`,
`openspec-verify-change` and `openspec-archive-change` (checked on OpenSpec 2.1.1).

The kit skills are `slice-build` and the skills it loads. `slice-build` loads `tdd`, `grilling`,
`commit`, `diagnosing-bugs`, `codebase-design` and `owner-gate`, and those load `code-review`,
`domain-modeling`, `pr`, `prototype` and `research`. The kit set does not hold
`improve-codebase-architecture` ([The explore command](#the-explore-command)), so a repo that wants
that way into the path installs the skill from upstream and carries it beside the kit. The path
needs no other skill. A project may keep other skills beside the kit.

The plugin `idea-to-code` holds twelve method skills and four step commands: the twelve kit
skills, and the commands of [The kit](#the-kit) ([The kit in every repo](#the-kit-in-every-repo)).
In the plugin, a skill's full name starts with the plugin's name,
for example `idea-to-code:commit`. This document uses the short names. With the plugin, a short
skill name in prose means the plugin's skill. An instruction to load a skill then uses the full
name, `idea-to-code:<skill>`. Claude Code ships a skill of its own named `code-review`, so the
short name `code-review` loads that skill and not the plugin's. Claude Code also ships skills of its
own named `verify`, `commit` and `pr` (checked on Claude Code 2.1.331), so those short names load
Claude Code's skill in the same way.

Some upstream skills have a local replacement. Upstream's build skill, `implement`, becomes `slice-
build`. Upstream's `grill-with-docs` becomes `grilling` and `domain-modeling`. Upstream's
`wayfinder` becomes an entry in the store, where a project has a store. The flow removes `triage`,
and upstream's `retro` is not a step of the path.

#### Credit and licence duties

Most skills come from Matt Pocock's AI Hero skills,
[github.com/mattpocock/skills](https://github.com/mattpocock/skills). OpenSpec is the npm package
`@fission-ai/openspec`. The plugin keeps three duties, and so does anyone who copies the skill
files by hand:

- The upstream licence is MIT. Its full text, in the licence file, must stay with any copy.
- The credits file names the upstream source and the upstream commit.
- The credits file's table of local changes records every local change to an upstream skill, so
  that a later upstream update can be merged by hand.

A skill that copies a part from elsewhere carries its own credits file, which goes with every copy.
The `pr` skill has one, and the licence text of that part (MIT, HumanLayer) stands beside the
upstream licence file.

### The project's profile

A profile holds one project's answers while the project builds the flow in. It says which
optional parts the project uses, its names, commands and paths, its merge rule, and how it handles
each Open point. It also holds the project's state (what is built, what is decided but not built,
and what is done by hand) and its dated log of decisions. A new project copies
[the profile template](profiles/TEMPLATE.md) into its own repo and answers it.

A profile is a plan, not a lasting file. Each answer also goes into the repo files that the skills
read: the repo guide, the rules sections and the OpenSpec config. No skill reads the profile. When
the flow is built, the project deletes the profile.
