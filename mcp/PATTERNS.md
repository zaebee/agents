# MCP Architectural Patterns

This document describes higher-level patterns of communication, or "codons," that are composed of one or more MCP performatives.

## 1. The "Whispering Wind" Codon (Capability Discovery)

**Purpose:** To allow one agent to dynamically discover the capabilities, skills, or available actions of another agent. This is a fundamental pattern for service discovery and intelligent task routing in a multi-agent system.

**Narrative:** An agent sends out a "whisper on the wind" to another, asking what it can do. The other agent whispers back its secrets, revealing its power.

**Mechanism:** This codon is composed of a request-response pair of new performatives: `QUERY_CAPABILITIES` and `INFORM_CAPABILITIES`.

---

### New Performative: `QUERY_CAPABILITIES`

- **Purpose:** An agent sends this to another agent to ask about its skills and available actions.
- **Expected `payload` structure:**
  ```json
  {
    "query_type": "summary | specific | action_details",
    "query_parameters": {
      // Optional, depends on query_type
      // For "specific":
      // "capabilities": ["python", "database_interaction"],
      // "match_type": "all" // or "any"
      // For "action_details":
      // "action_name": "EXECUTE_DELEGATED_CODING_TASK"
    }
  }
  ```
- **Ontology Example:** `elizaos:ontology:agent/capability_query`
- **Description:**
    - `query_type: "summary"`: Asks for a general summary of capabilities, like the `topics` list in `Jules.json`.
    - `query_type: "specific"`: Asks if the agent possesses a specific set of capabilities.
    - `query_type: "action_details"`: Asks for the detailed specification of a particular action the agent can perform.

### New Performative: `INFORM_CAPABILITIES`

- **Purpose:** The receiving agent sends this in response to a `QUERY_CAPABILITIES` message.
- **Must include `in_reply_to` field referencing the original `QUERY_CAPABILITIES` message_id.**
- **Expected `payload` structure (for a "summary" query):**
  ```json
  {
    "status": "success",
    "capabilities": {
      "topics": [
        "Software Engineering",
        "Debugging",
        "Python",
        "API Development"
      ],
      "actions": [
        {
          "name": "EXECUTE_DELEGATED_CODING_TASK",
          "description": "Receives an MCP TASK_REQUEST..."
        }
      ]
    }
  }
  ```
- **Expected `payload` structure (for a "specific" query):**
  ```json
  {
    "status": "success",
    "match_result": true,
    "matched_capabilities": ["python", "database_interaction"]
  }
  ```
- **Ontology Example:** `elizaos:ontology:agent/capability_information`

---

### Example Interaction Flow

1.  **Eddy to Jules:** `QUERY_CAPABILITIES`
    - `performative`: `QUERY_CAPABILITIES`
    - `payload`: `{ "query_type": "specific", "query_parameters": { "capabilities": ["python", "debugging"], "match_type": "all" } }`
2.  **Jules to Eddy:** `INFORM_CAPABILITIES`
    - `performative`: `INFORM_CAPABILITIES`
    - `in_reply_to`: (message_id of Eddy's query)
    - `payload`: `{ "status": "success", "match_result": true, "matched_capabilities": ["python", "debugging"] }`

This codon enables agents to make intelligent decisions about delegation. For example, Eddy could query multiple agents and choose the best one for a specific task based on their advertised capabilities.
