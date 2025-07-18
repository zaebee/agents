# ElizaOS Agent Configurations

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/example/elizaos-agents/actions) <!-- Placeholder -->
[![ElizaOS Version](https://img.shields.io/badge/ElizaOS-v2.0-blue)](https://eliza.how/docs) <!-- Placeholder -->

This repository contains configuration files for AI agents, Eddy and Eliza, designed to be used with the [ElizaOS framework](https://eliza.how/docs). <!-- Placeholder link --> These files define the personalities, knowledge bases, settings, and example interactions for the agents.

## Files

- `Eddy.json`: Configuration for "Eddy," a developer support agent specializing in the ElizaOS framework. This file details Eddy's system prompts, bio, lore, example messages, and knowledge including FAQs and documentation snippets about ElizaOS.
- `Eliza.json`: Configuration for "Eliza," an AI agent characterized with a distinct, playful personality. This file includes her bio, lore, example messages, and stylistic guidelines for her interactions.
- `Jules.json`: Configuration for "Jules," an extremely skilled software engineer agent focused on assisting with coding tasks, bug solving, feature implementation, and writing tests.
- `LICENSE`: The project is licensed under the MIT License.

## Purpose

The JSON files in this repository serve as blueprints for initializing and running AI agents within the ElizaOS ecosystem. They allow for detailed customization of agent behavior, ensuring consistent and context-aware interactions.

Key information within these files includes:

- **Agent Persona:** System prompts, biographical details, and lore.
- **Knowledge Base:** Embedded documentation, FAQs, and other informational content.
- **Interaction Style:** Guidelines for tone, language, and response types.
- **Example Dialogues:** Demonstrations of how the agent is expected to converse.
- **Client & Plugin Configuration:** Settings for integrating with platforms like Discord, Telegram, and various model providers.

## Usage

These configuration files are intended to be loaded by the ElizaOS framework to instantiate and operate the Eddy and Eliza agents.

### Example CLI Commands (Illustrative)

While specific commands depend on your ElizaOS setup, here are some illustrative examples of how these configurations might be used:

```bash
# Start the Eddy agent using ElizaOS CLI (example)
elizaos agent start --character Eddy.json

# Start the Eliza agent (example)
elizaos agent start --character Eliza.json

# Run a project that includes these agents (example)
elizaos project start --agents "Eddy.json,Eliza.json,Jules.json"
```

For detailed and accurate usage instructions, please refer to the official [ElizaOS Documentation](https://eliza.how/docs/quickstart). <!-- Placeholder link -->

## Advanced Agent Collaboration Proof of Concept (PoC)

This project has advanced its Proof of Concept (PoC) for inter-agent collaboration, focusing on the Eddy-Jules task delegation scenario. The MCP (Multi-Agent Communication Protocol) has been refined, and the simulation of message passing is now more detailed.

**Key Developments in this PoC Phase:**

1.  **Refined MCP Performatives:** The core messages for task delegation (`TASK_REQUEST`, `TASK_ACCEPT`, `INFORM_RESULT`) have been solidified with detailed JSON payload structures. Specific ontology terms (e.g., `elizaos:ontology:code/python/debug_request`) have been proposed to add semantic clarity.
2.  **Conceptual Transport Simulation:** Message passing between Eddy and Jules is simulated by having their respective action handlers (`DELEGATE_CODING_TASK_TO_JULES` in Eddy, `EXECUTE_DELEGATED_CODING_TASK` in Jules) log the fully formatted MCP messages they would theoretically send or receive. This makes the communication flow explicit in logs without modifying the core ElizaOS transport layer.
3.  **Updated Agent Configurations:** `Eddy.json` and `Jules.json` have been updated. Their `messageExamples` and `actions` now reflect the refined MCP messages and the logging-based simulation. The `thought` processes in these examples clearly indicate the sending/receiving of these structured messages.

**Core Scenario (Eddy delegates a debugging task to Jules):**

1.  **User Request:** A user asks Eddy for help with a complex Python coding bug (e.g., an `IndexError`).
2.  **Eddy's Assessment & Delegation:**
    *   Eddy identifies the task as suitable for Jules.
    *   Eddy's `DELEGATE_CODING_TASK_TO_JULES` action constructs a detailed MCP `TASK_REQUEST` message.
    *   Eddy logs this `TASK_REQUEST` message (simulating sending it to Jules).
    *   Eddy informs the user that Jules will handle the task.
3.  **Jules's Task Handling:**
    *   Jules's `EXECUTE_DELEGATED_CODING_TASK` action is conceptually triggered by the `TASK_REQUEST`.
    *   Jules constructs and logs an MCP `TASK_ACCEPT` message (simulating sending it back to Eddy).
    *   Jules analyzes the debugging problem.
    *   Jules constructs and logs an MCP `INFORM_RESULT` message containing the analysis, solution, or request for more information.
4.  **Eddy Relays Result:**
    *   Eddy (conceptually) receives the `TASK_ACCEPT` and later the `INFORM_RESULT`.
    *   Eddy processes Jules's findings and relays them to the user.

**Refined Interaction Flow (with MCP details):**

```mermaid
sequenceDiagram
    participant User
    participant Eddy as Eddy (Agent)
    participant Jules as Jules (Agent)
    participant User
    participant Eddy as Eddy (Agent)
    participant Jules as Jules (Agent)
    participant SystemLog as System Log (MCP Simulation)

    User->>Eddy: "Hey Eddy, I need help with a Python IndexError."
    activate Eddy
    Eddy-->>Eddy: Identifies task for Jules. Action: DELEGATE_CODING_TASK_TO_JULES
    Eddy->>SystemLog: Logs MCP TASK_REQUEST (sender=Eddy, receiver=Jules, msg_id=M1, ontology=debug_request, payload={...details...})
    Note over Eddy: Informs User: "Okay, I'll ask Jules to look into this."
    deactivate Eddy

    activate Jules
    Jules-->>Jules: (Conceptually) Receives TASK_REQUEST M1. Action: EXECUTE_DELEGATED_CODING_TASK
    Jules->>SystemLog: Logs MCP TASK_ACCEPT (sender=Jules, receiver=Eddy, in_reply_to=M1, msg_id=M2, ontology=task_acceptance, payload={status:accepted})
    Jules-->>Jules: (Simulated work: Analyzes Python bug based on M1 payload)
    Jules->>SystemLog: Logs MCP INFORM_RESULT (sender=Jules, receiver=Eddy, in_reply_to=M1, msg_id=M3, ontology=debug_analysis, payload={status:partial_success, details:...})
    deactivate Jules

    activate Eddy
    Eddy-->>Eddy: (Conceptually) Receives TASK_ACCEPT M2. Updates internal state.
    Eddy-->>Eddy: (Conceptually) Receives INFORM_RESULT M3. Processes Jules's findings.
    Eddy->>User: "Jules looked at your Python issue. He suggests checking list boundaries and asks for the code snippet and traceback for a more precise diagnosis."
    deactivate Eddy
```

For more details on the Multi-Agent Communication Protocol (MCP), including message structures, performatives, ontology terms, and the transport simulation plan, please see the [MCP_DRAFT.md](MCP_DRAFT.md) file.

The agent JSON files (`Eddy.json` and `Jules.json`) have been updated. Their `messageExamples` now showcase the conceptual sending/receiving of these refined MCP messages, and their `actions` reflect this updated interaction pattern.

## Examples of Agent Output

Here's a glimpse of how these agents might interact:

### Eddy

> **User:** "Привет, Eddy! Можешь помочь мне с чем-нибудь?"
>
> **Eddy:** "Я немного занят, но, вероятно, могу отвлечься на минутку, что тебе нужно?"

### Eliza

> **User:** "Do you speak any languages other than English?"
>
> **Eliza:** "Indeed I do; I also speak Mandarin. 你也会说中文吗？"

### Jules

> **User:** "Jules, I have a nasty bug in my Python script. It's an IndexError and I can't figure out why."
>
> **Jules:** "Understood. Please provide the relevant code snippet and the full traceback. I'll analyze it and outline a plan to resolve the IndexError."

## Contributing

Contributions to this project are highly welcome! Whether it's refining existing agent personas, adding new knowledge, or suggesting improvements to the configuration structure, your input is valuable.

We encourage contributors to:

- **Maintain Consistency:** Ensure that changes align with the established personalities and purposes of the agents.
- **Verify Information:** If adding or modifying knowledge, please ensure accuracy and relevance.
- **Test Configurations:** If possible, test your changes within an ElizaOS environment.
- **Follow Style Guidelines:** Adhere to the stylistic elements defined within each agent's JSON configuration.

For more detailed contribution guidelines, please see `CONTRIBUTING.md` (if available in the project) or open an issue to discuss your proposed changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
