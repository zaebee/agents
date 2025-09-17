import * as vscode from 'vscode';
import { McpMessage, McpPerformative } from './mcpInterfaces';
import EventSource = require('eventsource'); // Using require for EventSource

// Define a type for the message handler
export type McpMessageHandler = (message: McpMessage) => void;

export class McpClient {
    private context: vscode.ExtensionContext;
    private eventSource: EventSource | null = null;
    private requestEndpoint: string = '';
    private eventsEndpoint: string = '';
    private codingAgentId: string = 'jules';
    private docsAgentId: string = 'eddy';
    private userId: string = 'vscode-user'; // Or generate a unique ID

    private onMessageEmitter = new vscode.EventEmitter<McpMessage>();
    public readonly onMessage: vscode.Event<McpMessage> = this.onMessageEmitter.event;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.loadConfiguration();
        this.connectToEventStream();

        // Reload configuration and reconnect if settings change
        context.subscriptions.push(vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('elizaos')) {
                this.loadConfiguration();
                this.connectToEventStream(); // Reconnect with new settings
            }
        }));
    }

    private loadConfiguration() {
        const config = vscode.workspace.getConfiguration('elizaos');
        this.requestEndpoint = config.get<string>('mcpRequestEndpoint', 'http://localhost:8000/mcp-request');
        this.eventsEndpoint = config.get<string>('mcpEventsEndpoint', 'http://localhost:8000/mcp-events');
        this.codingAgentId = config.get<string>('codingAgentId', 'jules');
        this.docsAgentId = config.get<string>('docsAgentId', 'eddy');

        console.log(`MCP Client Configured: Request Endpoint: ${this.requestEndpoint}, Events Endpoint: ${this.eventsEndpoint}`);
    }

    public getCodingAgentId(): string {
        return this.codingAgentId;
    }

    public getDocsAgentId(): string {
        return this.docsAgentId;
    }

    public connectToEventStream() {
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
            console.log('MCP EventSource: Previous connection closed.');
        }

        if (!this.eventsEndpoint) {
            vscode.window.showErrorMessage('ElizaOS: MCP Events Endpoint is not configured. Cannot receive agent messages.');
            console.error('MCP EventSource: Events endpoint is empty.');
            return;
        }

        try {
            console.log(`MCP EventSource: Connecting to ${this.eventsEndpoint}...`);
            this.eventSource = new EventSource(this.eventsEndpoint);

            this.eventSource.onopen = (event) => {
                console.log('MCP EventSource: Connection opened.');
                vscode.window.setStatusBarMessage('ElizaOS: Connected to event stream.', 3000);
            };

            this.eventSource.onmessage = (event) => {
                try {
                    const rawMessage = event.data;
                    console.log('MCP EventSource: Message received (raw):', rawMessage);
                    const message: McpMessage = JSON.parse(rawMessage);

                    // Basic validation
                    if (!message.performative || !message.conversation_id) {
                        console.warn('MCP EventSource: Received malformed message (missing performative or conversation_id):', message);
                        return;
                    }
                    console.log('MCP EventSource: Message received (parsed):', message);
                    this.onMessageEmitter.fire(message);
                } catch (error) {
                    console.error('MCP EventSource: Error parsing message:', error, 'Raw data:', event.data);
                    vscode.window.showErrorMessage(`ElizaOS: Error parsing message from agent: ${error}`);
                }
            };

            this.eventSource.onerror = (error) => {
                console.error('MCP EventSource: Error:', error);
                // Don't show too many popups for intermittent errors, but log them.
                // Potentially implement a retry mechanism with backoff here if EventSource doesn't do it.
                if (this.eventSource?.readyState === EventSource.CLOSED) {
                    vscode.window.showWarningMessage('ElizaOS: Disconnected from MCP event stream. Will attempt to reconnect if configuration changes or on next command.');
                }
            };
            console.log('MCP EventSource: Event listeners attached.');

        } catch (error) {
            console.error('MCP EventSource: Failed to create EventSource:', error);
            vscode.window.showErrorMessage(`ElizaOS: Failed to connect to event stream at ${this.eventsEndpoint}. ${error}`);
        }
    }

    public async sendRequest(
        agentId: string,
        ontology: string,
        payload: any,
        conversationId?: string
    ): Promise<McpMessage | null> {
        if (!this.requestEndpoint) {
            vscode.window.showErrorMessage('ElizaOS: MCP Request Endpoint is not configured. Cannot send requests.');
            console.error('MCP Client: Request endpoint is empty.');
            return null;
        }

        const message: McpMessage = {
            conversation_id: conversationId || `conv-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
            performative: "REQUEST" as McpPerformative,
            ontology: ontology,
            payload: payload,
            sender: this.userId,
            receiver: agentId,
            timestamp: new Date().toISOString()
        };

        console.log('MCP Client: Sending request:', JSON.stringify(message, null, 2));

        try {
            const response = await fetch(this.requestEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(message)
            });

            if (!response.ok) {
                const errorBody = await response.text();
                console.error(`MCP Client: Error sending request. Status: ${response.status}. Body: ${errorBody}`);
                vscode.window.showErrorMessage(`ElizaOS: Failed to send request to agent ${agentId}. Server responded with ${response.status}.`);
                // Try to parse as McpMessage if it's a structured error from the server
                try {
                    const errorJson = JSON.parse(errorBody);
                    if (errorJson.performative && errorJson.error) {
                        return errorJson as McpMessage;
                    }
                } catch (e) { /* Ignore if not JSON */ }
                return null;
            }

            const responseData: McpMessage = await response.json();
            console.log('MCP Client: Received immediate response:', JSON.stringify(responseData, null, 2));
            // This immediate response could be ACCEPT, REJECT, or even a quick INFORM_RESULT.
            // The EventSource will handle subsequent messages like INFORM_RESULT for long-running tasks.
            this.onMessageEmitter.fire(responseData); // Also emit it through the central handler
            return responseData;

        } catch (error: any) {
            console.error('MCP Client: Network or other error sending request:', error);
            vscode.window.showErrorMessage(`ElizaOS: Error sending request to ${agentId}: ${error.message || error}`);
            return null;
        }
    }

    public dispose() {
        this.onMessageEmitter.dispose();
        if (this.eventSource) {
            this.eventSource.close();
            this.eventSource = null;
            console.log('MCP EventSource: Disposed and connection closed.');
        }
    }
}
