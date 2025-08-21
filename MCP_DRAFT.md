# Multi-Agent Communication Protocol (MCP) - Draft

**Version:** 0.1.0 (Draft for Proof of Concept)

## 1. Introduction

This document outlines a draft for a Multi-Agent Communication Protocol (MCP) for ElizaOS. The primary goal of this MCP is to enable effective, structured communication and collaboration between different AI agents within the ElizaOS ecosystem and potentially with external tools.

This initial draft is inspired by established Agent Communication Languages (ACLs) like FIPA ACL and KQML but aims for simplicity suitable for a Proof of Concept (PoC) and future iterative development.

## 2. Core Principles

- **Interoperability:** Allow diverse agents with different specializations to exchange information and requests.
- **Clarity:** Messages should have clear intent and content.
- **Extensibility:** The protocol should be adaptable to new message types and capabilities as ElizaOS evolves.
- **Simplicity (for PoC):** Start with a minimal set of essential message types and structures.

## 3. Message Structure

All MCP messages will share a common wrapper structure, with variations in the `payload` based on the `performative`.

```json
{
  "mcp_version": "0.1.0",
  "message_id": "unique_message_identifier_uuid",
  "performative": "PERFORMATIVE_TYPE",
  "sender": {
    "agent_id": "sending_agent_name_or_id"
  },
  "receiver": {
    "agent_id": "receiving_agent_name_or_id"
  },
  "in_reply_to": "optional_message_id_being_replied_to",
  "reply_with": "optional_identifier_expected_in_reply",
  "language": "content_language_of_payload", // e.g., "en", "application/json"
  "ontology": "ontology_identifier_for_payload_context", // e.g., "elizaos:coding", "elizaos:general_query"
  "timestamp": "ISO_8601_datetime_utc",
  "payload": {
    // Performative-specific content
  }
}
```

**Key Fields:**

- `mcp_version`: Version of the MCP this message adheres to.
- `message_id`: A unique UUID for this message.
- `performative`: The communicative act of the message (see Section 4).
- `sender`: Identifier of the sending agent.
- `receiver`: Identifier of the intended receiving agent.
- `in_reply_to`: `message_id` of a previous message if this is a reply.
- `reply_with`: An identifier that the sender expects the receiver to use in their `in_reply_to` field when replying. Useful for correlating requests and responses, especially for tasks.
- `language`: Specifies the language or format of the `payload` (e.g., "en" for natural language, "application/json" for structured data).
- `ontology`: A string or URI identifying the domain of knowledge or context for interpreting the `payload` (e.g., "elizaos:code_debugging", "elizaos:user_sentiment_analysis").
- `timestamp`: ISO 8601 UTC timestamp of when the message was created.
- `payload`: The actual content of the message, structured according to the `performative`.

## 4. Core Performatives (Message Types)

Inspired by FIPA ACL and KQML, the initial set of performatives for the PoC and near-future development includes:

### 4.1. `TASK_REQUEST` (Refined from `REQUEST`)

- **Purpose:** The sender requests the receiver to perform a specific, typically asynchronous, task.
- **Expected `payload` structure for a debugging task (Eddy to Jules):**
  ```json
  {
    "task_type": "debug_code", // Specific identifier for the kind of task
    "task_description": "A human-readable description of the task.", // e.g., "Debug the provided Python script to fix the 'IndexError'."
    "task_parameters": {
      "code_to_debug": "...", // The actual code snippet or path to code
      "programming_language": "python", // Language of the code
      "error_log": "...", // Optional: any error logs or symptoms observed
      "desired_outcome": "Identify and fix the bug, or provide analysis if not fixable."
    },
    "priority": "medium" // Optional: e.g., "low", "medium", "high"
  }
  ```
- **Example Use:** Eddy requests Jules to debug a piece of Python code.
- **Ontology Example:** `elizaos:ontology:code/python/debug_request`

### 4.2. `TASK_ACCEPT` (Refined from `ACCEPT`)

- **Purpose:** The sender confirms acceptance of a previously received `TASK_REQUEST`.
- **Must include `in_reply_to` field referencing the original `TASK_REQUEST` message_id.**
- **Expected `payload` structure:**
  ```json
  {
    "status": "accepted",
    "task_id_assigned": "optional_receiver_internal_task_id", // Jules might assign its own ID to track the task
    "estimated_completion_time": "optional_time_estimate_in_seconds_or_ISO_duration", // e.g., 300 or "PT5M"
    "comments": "Optional comments, e.g., 'Starting task now.'"
  }
  ```
- **Example Use:** Jules accepts a debugging task requested by Eddy.
- **Ontology Example:** `elizaos:ontology:general/task_acceptance`

### 4.3. `INFORM_RESULT` (Refined from `INFORM` for task outcomes)

- **Purpose:** The sender informs the receiver of the outcome of a previously accepted task.
- **Must include `in_reply_to` field referencing the original `TASK_REQUEST` message_id or the `reply_with` identifier from it.**
- **Expected `payload` structure for a debugging task result (Jules to Eddy):**
  ```json
  {
    "task_status": "success | failure | partial_success",
    "result_summary": "A human-readable summary of the outcome.", // e.g., "Bug fixed and tested." or "Analysis complete, bug identified but not fixed."
    "result_details": {
      // Content varies based on task_status and ontology
      // For a successful debug:
      "original_code": "...",
      "fixed_code": "...",
      "diff": "...", // Optional: a diff of changes
      "explanation": "Description of the bug and the fix.",
      "tests_passed": true // Optional
      // For a failed debug:
      // "error_encountered": "Details of why it failed",
      // "analysis": "Any insights gained despite failure"
    },
    "artifacts": [ // Optional: list of paths or references to created/modified files or resources
      // {"type": "file", "path": "/path/to/fixed_script.py"},
      // {"type": "log", "content": "..."}
    ]
  }
  ```
- **Example Use:** Jules informs Eddy of the result of the debugging task.
- **Ontology Example (Success):** `elizaos:ontology:code/python/solution_provided`
- **Ontology Example (Failure/Analysis):** `elizaos:ontology:code/python/debug_analysis`


### 4.4. `QUERY_IF` / `QUERY_REF`

- **Purpose:**
  - `QUERY_IF`: Sender asks the receiver if a statement is true.
  - `QUERY_REF`: Sender asks the receiver for the value of some reference.
- **Expected `payload` structure for `QUERY_IF`:**
  ```json
  {
    "condition": {
      /* a statement or condition to verify */
    }
  }
  ```
- **Expected `payload` structure for `QUERY_REF`:**
  ```json
  {
    "reference": "identifier_of_the_information_sought" // e.g., "latest_commit_hash", "user_preferences.theme"
  }
  ```
- **Example Use:** Eddy queries Jules if it has capacity for a new task.

### 4.5. `TASK_REJECT` (Refined from `REJECT`)

- **Purpose:** The sender refuses a previous `TASK_REQUEST` from the receiver.
- **Must include `in_reply_to` field referencing the original `TASK_REQUEST` message_id.**
- **Expected `payload` structure:**
  ```json
  {
    "status": "rejected",
    "reason_code": "optional_rejection_code", // e.g., "busy", "incapable", "unauthorized"
    "reason_text": "optional_human_readable_explanation"
  }
  ```
- **Example Use:** Jules rejects a task from Eddy because it's currently overloaded.
- **Ontology Example:** `elizaos:ontology:general/task_rejection`

### 4.6. `FAILURE` (General Action Failure)

- **Purpose:** The sender informs the receiver that an action, previously agreed to (e.g., via `TASK_ACCEPT` or other agreement), could not be completed successfully due to an unexpected error in carrying out the action itself, rather than a "negative" result of the action's logical goal.
- **Must include `in_reply_to` field referencing the `message_id` of the message that initiated the action (e.g., the `TASK_REQUEST` or a `reply_with` identifier from it).**
- **Expected `payload` structure:**
  ```json
  {
    "status": "failure",
    "error_code": "optional_error_code",
    "error_text": "description_of_the_failure"
  }
  ```
- **Example Use:** Jules informs Eddy that it failed to process the debugging task request due to an internal system crash (distinct from `INFORM_RESULT` with `task_status: "failure"` which would mean Jules *tried* to debug but couldn't find a solution).
- **Ontology Example:** `elizaos:ontology:general/action_execution_failure`

### 4.7. `NOT_UNDERSTOOD`

- **Purpose:** The sender informs the receiver that it could not understand a previous message.
- **Must include `in_reply_to` field referencing the `message_id` of the misunderstood message.**
- **Expected `payload` structure:**
  ```json
  {
    "reason_code": "e.g., 'unknown_performative', 'parsing_error', 'unknown_ontology', 'invalid_payload_structure'",
    "reason_text": "optional_explanation"
  }
  ```
- **Ontology Example:** `elizaos:ontology:general/message_not_understood`

### 4.8. `QUERY_CAPABILITIES`

- **Purpose:** The sender asks the receiver to describe its capabilities or skills. This is used for service discovery.
- **Expected `payload` structure:**
  ```json
  {
    "query_type": "summary | specific | action_details",
    "query_parameters": {
      // Optional, depends on query_type. See mcp/PATTERNS.md for details.
    }
  }
  ```
- **Example Use:** Eddy asks Jules what topics it is skilled in before delegating a task.
- **Ontology Example:** `elizaos:ontology:agent/capability_query`

### 4.9. `INFORM_CAPABILITIES`

- **Purpose:** The sender responds to a `QUERY_CAPABILITIES` message, providing information about its skills and actions.
- **Must include `in_reply_to` field referencing the original `QUERY_CAPABILITIES` message_id.**
- **Expected `payload` structure:**
  ```json
  {
    "status": "success",
    "capabilities": {
      // Structure depends on the original query_type. See mcp/PATTERNS.md for details.
    }
  }
  ```
- **Example Use:** Jules informs Eddy that it is proficient in Python and Debugging.
- **Ontology Example:** `elizaos:ontology:agent/capability_information`

## 5. Content Language and Ontology

- **Content Language (`language` field):**
  - For structured data, `application/json` is recommended for the PoC.
  - For natural language content within payloads, standard language codes (e.g., "en", "es") can be used.
- **Ontology (`ontology` field):**
  - The `ontology` field provides semantic context for the `payload`. It helps the receiving agent correctly interpret the content.
  - For the PoC, URN-like string identifiers will be used. The proposed structure is `elizaos:ontology:<domain>/<subdomain>/<concept>`.
  - **Initial Ontology Terms for PoC (Coding Domain):**
    - `elizaos:ontology:code/python/debug_request`: Used in `TASK_REQUEST` when Eddy asks Jules to debug Python code.
    - `elizaos:ontology:code/python/solution_provided`: Used in `INFORM_RESULT` when Jules provides a successful debugging solution for Python code.
    - `elizaos:ontology:code/python/debug_analysis`: Used in `INFORM_RESULT` when Jules provides an analysis of Python code, even if a full solution isn't found (e.g., error identification, partial fix).
    - `elizaos:ontology:code/general/refactor_request`: For requesting general code refactoring.
    - `elizaos:ontology:code/general/refactor_suggestion`: For providing refactoring suggestions.
  - **Initial Ontology Terms for PoC (General Task Management):**
    - `elizaos:ontology:general/task_acceptance`: Used in `TASK_ACCEPT` to acknowledge a task.
    - `elizaos:ontology:general/task_rejection`: Used in `TASK_REJECT` to decline a task.
    - `elizaos:ontology:general/action_execution_failure`: Used in `FAILURE` when the execution of an agreed-upon action fails at a system level.
    - `elizaos:ontology:general/message_not_understood`: Used in `NOT_UNDERSTOOD`.
  - Future versions may adopt or define more formal ontologies (e.g., using RDF, OWL, or custom ElizaOS schemas) to ensure semantic interoperability. This is where Eddy's "Digital Ontology" ideas could be heavily influential.

## 6. Integration with External Tools (e.g., IDEs)

The MCP is envisioned to facilitate integration with developer tools like VS Code or Vim.

**Scenario: IDE-Agent Interaction**

1.  **Developer in IDE:** Highlights a code snippet and requests refactoring suggestions.
2.  **IDE Plugin:** Constructs an MCP `TASK_REQUEST` message:
    - `performative`: `TASK_REQUEST`
    - `receiver`: { "agent_id": "Jules" } // Or a general coding assistant agent group
    - `language`: `application/json`
    - `ontology`: `elizaos:ontology:code/general/refactor_request`
    - `payload`:
      ```json
      {
        "task_type": "refactor_code_snippet",
        "task_description": "Request for refactoring suggestions for the selected code.",
        "task_parameters": {
          "code_snippet": "...",
          "programming_language": "python",
          "desired_outcome": "improve readability and performance"
        }
      }
      ```
3.  **ElizaOS Gateway/Service:** Receives the MCP message and routes it to the appropriate agent (Jules).
4.  **Jules:** Processes the request.
    - Sends `TASK_ACCEPT` back to the IDE Plugin (via Gateway).
    - Performs refactoring analysis.
    - Sends an `INFORM_RESULT` message with the refactoring suggestions.
      - `performative`: `INFORM_RESULT`
      - `in_reply_to`: (original `TASK_REQUEST` message_id or `reply_with` id)
      - `language`: `application/json`
      - `ontology`: `elizaos:ontology:code/general/refactor_suggestion`
      - `payload`:
        ```json
        {
          "task_status": "success",
          "result_summary": "Refactoring suggestions provided.",
          "result_details": {
            "original_snippet": "...",
            "suggestions": [
              {
                "change_type": "rename_variable",
                "description": "Rename variable 'x' to 'index' for clarity.",
                "suggested_code_diff": "...", // Or full suggested code
                "confidence": 0.9
              },
              {
                "change_type": "extract_method",
                "description": "Extract the selected block into a new method 'calculate_value'.",
                "suggested_code_diff": "...",
                "confidence": 0.85
              }
            ]
          }
        }
        ```
5.  **IDE Plugin:** Receives the `INFORM_RESULT` message and displays the suggestions to the developer within the IDE.

**Considerations for Tool Integration:**

- **Transport Layer:** How MCP messages are sent between the tool and ElizaOS (e.g., HTTP, WebSockets, local IPC).
- **Authentication/Authorization:** Securing the communication channel.
- **Service Discovery:** How does the IDE plugin discover available ElizaOS agents and their capabilities?
- **Ontology Alignment:** Ensuring the IDE plugin and agents share a common understanding of terms used in `ontology` and `payload` structures.

## 7. PoC Simplification (Eddy & Jules Delegation) and Transport Simulation

For the initial PoC involving Eddy delegating a debugging task to Jules, the focus will be on demonstrating the MCP message exchange conceptually through logging.

### 7.1. Performatives and Message Flow

- **Performatives to be used:**
  - `TASK_REQUEST`: Eddy sends this to Jules to request debugging.
  - `TASK_ACCEPT`: Jules sends this to Eddy to confirm it will take the task.
  - `INFORM_RESULT`: Jules sends this to Eddy with the outcome (success or failure analysis).
- **Key Fields for PoC:**
  - `mcp_version`, `message_id`, `performative`, `sender`, `receiver`, `in_reply_to`, `reply_with`, `language`, `ontology`, `timestamp`, `payload`.
- **`language`:** Will be `application/json` for the payload.
- **`ontology`:**
  - Eddy to Jules `TASK_REQUEST`: `elizaos:ontology:code/python/debug_request`
  - Jules to Eddy `TASK_ACCEPT`: `elizaos:ontology:general/task_acceptance`
  - Jules to Eddy `INFORM_RESULT` (success): `elizaos:ontology:code/python/solution_provided`
  - Jules to Eddy `INFORM_RESULT` (failure/analysis): `elizaos:ontology:code/python/debug_analysis`
- **Payloads:** Will follow the detailed structures defined in Section 4 for `TASK_REQUEST`, `TASK_ACCEPT`, and `INFORM_RESULT` tailored for the debugging scenario.

### 7.2. MCP Transport Simulation via Logging (Conceptual Plan)

Given that direct ElizaOS runtime modification for a message bus is out of scope for this PoC, the inter-agent communication will be simulated by enhancing agent action handlers to log the exact MCP messages they *would* send or *have conceptually received*.

**Logging Mechanism:**
- Agents will use their standard logging capabilities.
- MCP messages will be logged as structured JSON strings, prefixed with a clear indicator like `MCP_MESSAGE_SENT:` or `MCP_MESSAGE_RECEIVED:`.

**Eddy's `DELEGATE_CODING_TASK_TO_JULES` Action Handler:**
1.  When triggered, this action will construct a full MCP `TASK_REQUEST` message destined for Jules.
    - This includes generating a unique `message_id`, setting `sender` to "Eddy", `receiver` to "Jules", appropriate `ontology`, and the detailed `payload` as defined in Section 4.1.
2.  Instead of sending this message over a transport layer, Eddy's handler will log:
    `MCP_MESSAGE_SENT: [JSON string of the TASK_REQUEST message]`
3.  Eddy's `thought` process (as seen in `Eddy.json` message examples) will be updated to reflect that it has "sent" this message and is now awaiting a `TASK_ACCEPT` and subsequently an `INFORM_RESULT` from Jules, referencing the `message_id` or `reply_with` of the sent `TASK_REQUEST`.

**Jules's `EXECUTE_DELEGATED_CODING_TASK` Action Handler:**
1.  Conceptually, this action is triggered upon "receiving" a `TASK_REQUEST` from Eddy. For the PoC, this will be simulated by having an example in `Jules.json` that shows an incoming `TASK_REQUEST` (as if logged by a transport layer).
2.  Upon activation (conceptually, after parsing the incoming `TASK_REQUEST`):
    - Jules's handler will first construct an MCP `TASK_ACCEPT` message.
        - This message will reference the `in_reply_to` field with the `message_id` from Eddy's `TASK_REQUEST`.
    - Jules will log:
        `MCP_MESSAGE_SENT: [JSON string of the TASK_ACCEPT message to Eddy]`
3.  Jules will then proceed with the core logic of the task (analyzing the coding problem).
4.  After completing the analysis/work, Jules's handler will construct an MCP `INFORM_RESULT` message.
    - This message will also reference the `in_reply_to` field with the `message_id` from Eddy's original `TASK_REQUEST`.
    - The `payload` will contain the results of the debugging task.
5.  Jules will log:
    `MCP_MESSAGE_SENT: [JSON string of the INFORM_RESULT message to Eddy]`

**Simulated Reception at Eddy:**
- While Jules logs sent messages, Eddy won't automatically pick them up.
- The PoC will demonstrate the *expected* reception by updating Eddy's `messageExamples` to show how Eddy would react *if* it received the `TASK_ACCEPT` and `INFORM_RESULT` messages from Jules. This part remains conceptual in terms of actual message handling but will be clear in the JSON examples. For instance, Eddy's subsequent turn might show a `thought` like: "Received TASK_ACCEPT from Jules for message_id X. Now awaiting INFORM_RESULT." and later "Received INFORM_RESULT from Jules for message_id X. Forwarding result to user."

This logging approach will make the intended MCP flow visible and verifiable through agent logs, achieving the PoC's goal of demonstrating structured inter-agent communication without deep OS modifications.

## 8. Future Considerations

- Actual implementation of a message bus or event emitter within ElizaOS.
- More complex performatives (e.g., `SUBSCRIBE`, `CANCEL`, `PROPOSE`, `TASK_REJECT`, `FAILURE`).
- Negotiation of language and ontology.
- Directory services for agent discovery (Yellow Pages).
- Error handling and exception propagation.
- Security: message signing, encryption.
- Conversation management protocols (managing sequences of related messages).

This draft provides a starting point. It will be refined based on the PoC implementation and further requirements.Tool output for `create_file_with_block`:

## 9. Architectural Patterns (Codons)

While performatives are the basic communicative acts, they can be combined into higher-level conversational patterns, or "codons," to achieve more complex goals.

For a detailed description of these patterns, such as the "Whispering Wind" codon for capability discovery, please see the `mcp/PATTERNS.md` document.
