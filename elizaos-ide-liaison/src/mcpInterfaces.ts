// Basic MCP Message Structure
export interface McpMessage {
    conversation_id: string;
    performative: McpPerformative;
    ontology: string; // e.g., "elizaos:ide:explain_code"
    payload: any; // Could be more specific based on ontology
    sender: string; // Agent ID or user ID
    receiver: string; // Agent ID or user ID (or '*' for broadcast)
    timestamp?: string; // ISO 8601 timestamp
    error?: McpError;
}

export type McpPerformative =
    | "REQUEST"
    | "ACCEPT"
    | "REJECT"
    | "FAILURE"
    | "INFORM_RESULT"
    | "QUERY_REF" // For asking about something
    | "INFORM_REF" // For responding to a QUERY_REF
    | "SUBSCRIBE"
    | "NOTIFY"
    | "CANCEL";

export interface McpError {
    code: number; // e.g., 404, 500
    message: string;
    details?: any;
}

// Specific Payloads (Examples - can be expanded)
export interface ExplainCodePayload {
    code_snippet: string;
    language: string;
    user_query: string;
}

export interface GetDocumentationPayload {
    code_snippet: string; // e.g., API name, function call
    language: string;
    user_query: string;
}

export interface RefactorSuggestionPayload {
    code_snippet: string;
    language: string;
    user_query: string;
}

export interface InformExplainCodeResultPayload {
    explanation: string; // Can be markdown
    language?: string; // To help with rendering
}

export interface InformGetDocumentationResultPayload {
    documentation: string; // Can be markdown
    source_url?: string;
}

export interface InformRefactorSuggestionResultPayload {
    suggestions: RefactorSuggestion[]; // Array of suggestions
    original_snippet: string;
}

export interface RefactorSuggestion {
    description: string;
    diff?: string; // A diff string (e.g., unified diff format)
    suggested_code?: string; // Or the full suggested code
}

// For communication with the SADS Panel Webview
export interface PanelMessage {
    type: string;
    requestId?: string; // To correlate requests and responses
    content?: any;
    isAgent?: boolean;
    sender?: string;
}
