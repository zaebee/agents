# ElizaOS IDE Liaison - VS Code Extension

Connect your VS Code editor to the ElizaOS Multi-Agent Communication Protocol (MCP) to interact with agents like Jules (for coding assistance) and Eddy (for documentation).

## Features

*   **Code Explanation:** Select a code snippet and ask Jules to explain it.
*   **Documentation Lookup:** Select an API or code construct and ask Eddy to provide documentation.
*   **Refactoring Suggestions:** Select code and ask Jules for refactoring ideas.
*   **Agent Interaction Panel:** View requests and agent responses in a dedicated sidebar panel.
*   **Configurable Endpoints:** Set your ElizaOS MCP server details and target agent IDs.

## Installation

1.  **Prerequisites:**
    *   Node.js and npm installed.
    *   An ElizaOS runtime with an MCP server accessible (e.g., running locally at `http://localhost:8000`).
2.  **Clone the repository (or this extension's sub-directory).**
3.  **Navigate to the extension directory:**
    ```bash
    cd elizaos-ide-liaison
    ```
4.  **Install dependencies:**
    ```bash
    npm install
    ```
5.  **Compile the TypeScript:**
    ```bash
    npm run compile
    # Or for development: npm run watch
    ```
6.  **Launch the extension:**
    *   Open the `elizaos-ide-liaison` folder in VS Code.
    *   Press `F5` to open a new Extension Development Host window with the extension running.
    *   Alternatively, you can package the extension into a `.vsix` file and install it:
        ```bash
        npm install -g @vscode/vsce
        vsce package
        ```
        Then, in VS Code, go to the Extensions view, click the "..." menu, and select "Install from VSIX..."

## Configuration

Configure the extension via VS Code settings (File > Preferences > Settings, then search for "elizaos").

*   **`elizaos.mcpRequestEndpoint`**: (Default: `http://localhost:8000/mcp-request`)
    *   The URL where the extension sends MCP `REQUEST` messages (e.g., code explanation queries) via HTTP POST.
*   **`elizaos.mcpEventsEndpoint`**: (Default: `http://localhost:8000/mcp-events`)
    *   The URL for the Server-Sent Events (SSE) stream from which the extension receives MCP messages (e.g., `ACCEPT`, `INFORM_RESULT`) from agents.
*   **`elizaos.codingAgentId`**: (Default: `jules`)
    *   The MCP agent ID for coding-related tasks (explanation, refactoring).
*   **`elizaos.docsAgentId`**: (Default: `eddy`)
    *   The MCP agent ID for documentation lookup tasks.
*   **`elizaos.mcpServerEndpoint`**: (Default: `http://localhost:8000`)
    *   *DEPRECATED*. This setting was previously used as a base URL. Please use the more specific `mcpRequestEndpoint` and `mcpEventsEndpoint`.

## Usage

1.  **Open the ElizaOS Panel:**
    *   Click on the ElizaOS icon in the Activity Bar (if not visible, ensure the extension is enabled). This will open the "Agent Chat" panel.
2.  **Interacting with Agents:**
    *   **Select Code:** Highlight a piece of code in your editor.
    *   **Use Context Menu:** Right-click on the selected code. You'll see options like:
        *   "ElizaOS: Ask Jules to Explain Code"
        *   "ElizaOS: Ask Eddy for Docs on API"
        *   "ElizaOS: Ask Jules for Refactor Suggestion"
    *   **Use Command Palette:** Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and type "ElizaOS" to see the available commands.
3.  **View Responses:**
    *   Your request and the agent's responses (e.g., `ACCEPT`, `INFORM_RESULT`, `FAILURE`) will appear in the "Agent Chat" panel.

## Assumptions about ElizaOS MCP Server

*   **MCP Compliance:** The server adheres to the Multi-Agent Communication Protocol (MCP) structure for messages.
    *   `REQUEST` messages are sent via HTTP POST to the `mcpRequestEndpoint`.
    *   The server expects JSON payloads for these POST requests.
    *   The server may respond immediately to the POST with an MCP message (e.g., `ACCEPT`, `REJECT`, `FAILURE`, or even a quick `INFORM_RESULT`).
*   **Server-Sent Events (SSE):** The server provides an SSE endpoint at `mcpEventsEndpoint`.
    *   This stream is used to send asynchronous MCP messages to the client (e.g., `ACCEPT` if not sent in POST response, `INFORM_RESULT` for longer tasks).
    *   Messages on the SSE stream are expected to be JSON strings.
*   **Message Structure:** Messages (both sent and received) generally follow this structure:
    ```json
    {
      "conversation_id": "string",
      "performative": "REQUEST | ACCEPT | REJECT | FAILURE | INFORM_RESULT | ...",
      "ontology": "string (e.g., elizaos:ide:explain_code)",
      "payload": "any (structure depends on ontology)",
      "sender": "string (agent/user ID)",
      "receiver": "string (agent/user ID)",
      "timestamp": "ISO8601_string (optional)",
      "error": { // Optional, typically for REJECT/FAILURE
        "code": "number",
        "message": "string"
      }
    }
    ```
*   **Agent Ontologies:** ElizaOS agents (Jules, Eddy) are configured to understand and respond to the following ontologies with relevant payloads:
    *   `elizaos:ide:explain_code` (Payload: `{ "code_snippet": "...", "language": "...", "user_query": "..." }`)
    *   `elizaos:ide:get_documentation` (Payload: `{ "code_snippet": "...", "language": "...", "user_query": "..." }`)
    *   `elizaos:ide:refactor_suggestion` (Payload: `{ "code_snippet": "...", "language": "...", "user_query": "..." }`)
    *   Responses (`INFORM_RESULT`) will have payloads specific to the request (e.g., `{ "explanation": "..." }`).

## Development Notes

*   The extension is built with TypeScript.
*   Ensure `npm install` is run to fetch dependencies like `eventsource`.
*   Use `npm run watch` during development to automatically recompile TypeScript on changes.
*   Press `F5` in VS Code (with the extension folder open) to launch an Extension Development Host window.

---

This README provides a good starting point for users and developers.
