# Multi-Agent Communication Protocol (MCP) - Draft

**Version:** 0.1.0 (Draft for Proof of Concept)

## 1. Introduction

This document outlines a draft for a Multi-Agent Communication Protocol (MCP) for ElizaOS. The primary goal of this MCP is to enable effective, structured communication and collaboration between different AI agents within the ElizaOS ecosystem and potentially with external tools.

This initial draft is inspired by established Agent Communication Languages (ACLs) like FIPA ACL and KQML but aims for simplicity suitable for a Proof of Concept (PoC) and future iterative development.

## 2. Core Principles

*   **Interoperability:** Allow diverse agents with different specializations to exchange information and requests.
*   **Clarity:** Messages should have clear intent and content.
*   **Extensibility:** The protocol should be adaptable to new message types and capabilities as ElizaOS evolves.
*   **Simplicity (for PoC):** Start with a minimal set of essential message types and structures.

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

*   `mcp_version`: Version of the MCP this message adheres to.
*   `message_id`: A unique UUID for this message.
*   `performative`: The communicative act of the message (see Section 4).
*   `sender`: Identifier of the sending agent.
*   `receiver`: Identifier of the intended receiving agent.
*   `in_reply_to`: `message_id` of a previous message if this is a reply.
*   `reply_with`: An identifier that the sender expects the receiver to use in their `in_reply_to` field when replying. Useful for correlating requests and responses, especially for tasks.
*   `language`: Specifies the language or format of the `payload` (e.g., "en" for natural language, "application/json" for structured data).
*   `ontology`: A string or URI identifying the domain of knowledge or context for interpreting the `payload` (e.g., "elizaos:code_debugging", "elizaos:user_sentiment_analysis").
*   `timestamp`: ISO 8601 UTC timestamp of when the message was created.
*   `payload`: The actual content of the message, structured according to the `performative`.

## 4. Core Performatives (Message Types)

Inspired by FIPA ACL and KQML, the initial set of performatives for the PoC and near-future development includes:

### 4.1. `REQUEST`
*   **Purpose:** The sender requests the receiver to perform some action.
*   **Expected `payload` structure:**
    ```json
    {
      "action_name": "name_of_the_action_to_perform", // e.g., "debug_code", "generate_report"
      "action_params": { /* parameters for the action */ }
    }
    ```
*   **Example Use:** Eddy requests Jules to debug a piece of code.

### 4.2. `INFORM`
*   **Purpose:** The sender is informing the receiver of a statement, fact, or result.
*   **Expected `payload` structure:**
    ```json
    {
      "statement_type": "fact | result | event | status_update",
      "data": { /* the information being conveyed */ }
    }
    ```
*   **Example Use:** Jules informs Eddy of the result of a debugging task.

### 4.3. `QUERY_IF` / `QUERY_REF`
*   **Purpose:**
    *   `QUERY_IF`: Sender asks the receiver if a statement is true.
    *   `QUERY_REF`: Sender asks the receiver for the value of some reference.
*   **Expected `payload` structure for `QUERY_IF`:**
    ```json
    {
      "condition": { /* a statement or condition to verify */ }
    }
    ```
*   **Expected `payload` structure for `QUERY_REF`:**
    ```json
    {
      "reference": "identifier_of_the_information_sought" // e.g., "latest_commit_hash", "user_preferences.theme"
    }
    ```
*   **Example Use:** Eddy queries Jules if it has capacity for a new task.

### 4.4. `ACCEPT`
*   **Purpose:** The sender agrees to a previous `REQUEST` from the receiver.
*   **Must include `in_reply_to` field referencing the original `REQUEST` message_id.**
*   **Expected `payload` structure:**
    ```json
    {
      "status": "accepted",
      "estimated_completion_time": "optional_time_estimate"
    }
    ```
*   **Example Use:** Jules accepts a debugging task requested by Eddy.

### 4.5. `REJECT`
*   **Purpose:** The sender refuses a previous `REQUEST` from the receiver.
*   **Must include `in_reply_to` field referencing the original `REQUEST` message_id.**
*   **Expected `payload` structure:**
    ```json
    {
      "status": "rejected",
      "reason_code": "optional_rejection_code", // e.g., "busy", "incapable", "unauthorized"
      "reason_text": "optional_human_readable_explanation"
    }
    ```
*   **Example Use:** Jules rejects a task from Eddy because it's currently overloaded.

### 4.6. `FAILURE`
*   **Purpose:** The sender informs the receiver that an action, previously agreed to (e.g., via `ACCEPT`), could not be completed successfully.
*   **Must include `in_reply_to` field referencing the `message_id` of the message that initiated the action (e.g., the `REQUEST` or a `reply_with` identifier from it).**
*   **Expected `payload` structure:**
    ```json
    {
      "status": "failure",
      "error_code": "optional_error_code",
      "error_text": "description_of_the_failure"
    }
    ```
*   **Example Use:** Jules informs Eddy that it failed to debug a piece of code due to missing dependencies.

### 4.7. `NOT_UNDERSTOOD`
*   **Purpose:** The sender informs the receiver that it could not understand a previous message.
*   **Must include `in_reply_to` field referencing the `message_id` of the misunderstood message.**
*   **Expected `payload` structure:**
    ```json
    {
      "reason_code": "e.g., 'unknown_performative', 'parsing_error', 'unknown_ontology'",
      "reason_text": "optional_explanation"
    }
    ```

## 5. Content Language and Ontology

*   **Content Language (`language` field):**
    *   For structured data, `application/json` is recommended for the PoC.
    *   For natural language content within payloads, standard language codes (e.g., "en", "es") can be used.
*   **Ontology (`ontology` field):**
    *   For the PoC, simple string tags will be used (e.g., `elizaos:coding_task`, `elizaos:documentation_query`).
    *   Future versions may adopt or define more formal ontologies (e.g., using RDF, OWL, or custom ElizaOS schemas) to ensure semantic interoperability. This is where Eddy's "Digital Ontology" ideas could be heavily influential.

## 6. Integration with External Tools (e.g., IDEs)

The MCP is envisioned to facilitate integration with developer tools like VS Code or Vim.

**Scenario: IDE-Agent Interaction**

1.  **Developer in IDE:** Highlights a code snippet and requests refactoring suggestions.
2.  **IDE Plugin:** Constructs an MCP `REQUEST` message:
    *   `performative`: `REQUEST`
    *   `receiver`: `Jules` (or a general "coding assistant" agent group)
    *   `language`: `application/json`
    *   `ontology`: `elizaos:code_refactor_request`
    *   `payload`:
        ```json
        {
          "action_name": "refactor_code_snippet",
          "action_params": {
            "code_snippet": "...",
            "programming_language": "python",
            "desired_outcome": "improve readability and performance"
          }
        }
        ```
3.  **ElizaOS Gateway/Service:** Receives the MCP message and routes it to the appropriate agent (Jules).
4.  **Jules:** Processes the request.
    *   Sends `ACCEPT` back to the IDE Plugin (via Gateway).
    *   Performs refactoring analysis.
    *   Sends an `INFORM` message with the `result` containing refactoring suggestions.
        *   `performative`: `INFORM`
        *   `in_reply_to`: (original `REQUEST` message_id or `reply_with` id)
        *   `language`: `application/json`
        *   `ontology`: `elizaos:code_refactor_suggestions`
        *   `payload`:
            ```json
            {
              "statement_type": "result",
              "data": {
                "original_snippet": "...",
                "suggestions": [
                  { "change_type": "rename_variable", "details": "...", "suggested_code": "..." },
                  { "change_type": "extract_method", "details": "...", "suggested_code": "..." }
                ]
              }
            }
            ```
5.  **IDE Plugin:** Receives the `INFORM` message and displays the suggestions to the developer within the IDE.

**Considerations for Tool Integration:**

*   **Transport Layer:** How MCP messages are sent between the tool and ElizaOS (e.g., HTTP, WebSockets, local IPC).
*   **Authentication/Authorization:** Securing the communication channel.
*   **Service Discovery:** How does the IDE plugin discover available ElizaOS agents and their capabilities?
*   **Ontology Alignment:** Ensuring the IDE plugin and agents share a common understanding of terms used in `ontology` and `payload` structures.

## 7. PoC Simplification (Eddy & Jules Delegation)

For the initial PoC involving Eddy delegating to Jules:

*   Performatives used: `REQUEST`, `ACCEPT`, `INFORM` (with a `result` type payload that can indicate success or failure implicitly or explicitly).
*   `message_id` and `reply_with`/`in_reply_to` will be crucial for tracking the delegation.
*   `language` will be `application/json`.
*   `ontology` will be simple strings like `elizaos:debug_python_code`.
*   The actual transport mechanism will be simulated within the ElizaOS runtime for the PoC.

## 8. Future Considerations

*   More complex performatives (e.g., `SUBSCRIBE`, `CANCEL`, `PROPOSE`).
*   Negotiation of language and ontology.
*   Directory services for agent discovery (Yellow Pages).
*   Error handling and exception propagation.
*   Security: message signing, encryption.
*   Conversation management protocols (managing sequences of related messages).

This draft provides a starting point. It will be refined based on the PoC implementation and further requirements.Tool output for `create_file_with_block`:
