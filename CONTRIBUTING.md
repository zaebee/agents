# Contributing to the Hive: A Developer's Guide

Welcome, builder! This guide explains the practical philosophy of how we write code in our Hive. Our goal is not just to write functional code, but to grow a healthy, resilient, and understandable digital Organism. Our core architectural principles are defined in `HIVE_CONSTITUTION.md`. This document explains how to apply them.

## The Ontological Manifest

When you create a new component (a "Cell"), you will start with a declarative manifest (`manifest.yaml`). This file is more than just configuration; it is an **ontological declaration**.

*   It asserts the **existence and essence** of your new component.
*   It defines your component's **identity** (`name`), its **purpose** (`description`), and its **relationships** with the rest of the Organism (`listens_to`, `produces`, `connectors`).

This manifest is the source of truth for your component's role in the greater system. Treat it as the primary blueprint for your Cell.

## Writing Codeons

We do not write large, monolithic functions. We compose small, pure, testable functions called **`Codeons`**.

A `Codeon` is a **design principle**, not a specific class. When writing code, strive to make your `Codeons` (your functions and methods) adhere to these rules:

1.  **Small:** A `Codeon` should do one thing and do it well. Aim for functions with very few lines of code.
2.  **Readable:** The name of the function should make its purpose immediately clear.
3.  **Pure (when possible):** The best `Codeons` are pure functions. They take input, return output, and have no side effects (like writing to a database or a file). This makes them trivial to test and reason about.
4.  **Composed:** Build complex logic by chaining these small `Codeons` together. The `process_order` example from our discussions is a perfect model for this.

## Mutations and Evolution

Change is how our system evolves. We think of changes to the codebase as "mutations."

*   **Beneficial Mutations (Refactoring):** These are encouraged. Leave the code better than you found it. Improve the fitness of your Cell.
*   **Neutral Mutations (Styling):** Permitted, but should be handled by automated formatters where possible.
*   **Harmful Mutations (Bugs):** These are failures in our quality control process.

## The Pipeline as Quality Control (Epigenetics and Environment)

The CI/CD pipeline is the Cell's internal machinery that prevents harmful mutations from reaching production. Your responsibility as a developer is to provide it with the right tests.

A note on the environment:
The environment (e.g., environment variables, feature flags) can be used as a **SWITCH** to influence which `Codeons` are expressed. For example, a feature flag can enable or disable a chain of `Codeons`. This is a safe and powerful way to manage features.

However, the environment must **NEVER** be the **SOURCE** of a `Codeon's` logic. We do not use `eval()` or similar constructs on environment variables. All logic must be committed, version-controlled, and tested code. Allowing the environment to define logic is a forbidden practice that leads to chaos and insecurity.

By following these principles, you will not just be a builder of code; you will be a Beekeeper, a cultivator of a healthy and thriving digital ecosystem.
