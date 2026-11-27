---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first outside an OpenSpec change, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read the repo's glossary (`GLOSSARY.md`, or the glossary file the repo guide names) where it has one, so test names and interface vocabulary match the project's domain language. The repo guide is `AGENTS.md`, else `CLAUDE.md`. Respect the ADRs in the repo's ADR folder, the `ADR folder:` of the repo's `## Decision records` (the `idea-to-code:domain-modeling` skill says where the section sits; default: `adr/` where it exists), where it has one, for the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

Before you write a test, read [tests.md](tests.md). Before you add a mock or a test double, read [mocking.md](mocking.md).

## Seams: where tests go

A **seam** is the place you test at: the public interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

**Test only at pre-agreed seams.** No test is written at an unconfirmed seam, except the seam picks below. You can't test everything, so agreeing the seams up front is how testing effort lands on the critical paths and complex logic instead of every edge case.

- In an OpenSpec change, the seam is the Seam field of the slice block your `idea-to-code:slice-build` brief hands you: use it and ask nothing. When the slice block has no Seam field, pick the seam closest to the public interface that reaches the behavior and list it as an assumption, with the same hand-back rule as below. When the agreed seam cannot reach the behavior, use the nearest seam that can and list it as an assumption; stop and hand back only when that pick is an owner decision of the five kinds your brief's rules list.
- Outside a change, propose seams and put each seam choice to the owner as one question in the form of the `idea-to-code:grilling` skill: one question per seam, each option saying what the seam catches and what it misses.

When the shape of that interface is itself in question (how deep the module is, where the seam belongs, what the interface should expose), call the Skill tool with `idea-to-code:codebase-design` for the vocabulary. It is the shared source of the module, interface, depth, seam, adapter, leverage and locality terms, and it is a reference to consult, not a session to run.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies through a side channel (querying the database instead of using the interface). The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing the tests for several slices, or for a whole change, before any code. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: inside a change, one slice's tests, then that slice's code, then the next slice; outside a change, one test, then its code, then the next. Each slice is a **tracer bullet** that responds to what the last one taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features. A new test is red for the reason its scenario gives: an assertion on the missing behavior, not a build error or a missing import.
- **One slice at a time.** Outside a change, one seam, one test, one minimal implementation per cycle.
- **Inside an OpenSpec change**, the `idea-to-code:slice-build` skill runs the loop: its test writer writes a slice's tests with these rules, and its code writer never touches a test. Follow its order, not this loop.
- **Refactoring is not part of the loop.** It belongs to review. Inside a change, a refactor is made only as a fix-round finding that cites a written standard (the `idea-to-code:slice-build` skill, After verify), and a smell with no cited rule is a lead for the owner. Outside a change, it belongs to the `idea-to-code:code-review` skill.
