import * as vscode from 'vscode';
import { SadsPanelViewProvider } from './sadsPanelViewProvider';
import { McpClient } from './mcpClient';
import { ExplainCodePayload, GetDocumentationPayload, RefactorSuggestionPayload } from './mcpInterfaces';

export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "elizaos-ide-liaison" is now active!');

    // Initialize SADS Panel View Provider
    const sadsProvider = new SadsPanelViewProvider(context);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider(SadsPanelViewProvider.viewType, sadsProvider, {
            webviewOptions: { retainContextWhenHidden: true }
        })
    );

    // Initialize MCP Client
    const mcpClient = new McpClient(context);
    context.subscriptions.push(mcpClient); // Add to subscriptions for dispose to be called

    // Connect MCP Client messages to SADS Panel
    mcpClient.onMessage(message => {
        sadsProvider.handleMcpMessage(message);
    });

    // Register Commands
    const registerCommand = (command: string, handler: () => Promise<void>) => {
        context.subscriptions.push(vscode.commands.registerCommand(command, handler));
    };

    registerCommand('elizaos-ide-liaison.askJulesToExplain', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('No active editor found.');
            return;
        }
        const selection = editor.selection;
        const selectedText = editor.document.getText(selection);
        if (!selectedText) {
            vscode.window.showInformationMessage('No text selected to explain.');
            return;
        }

        const codingAgentId = mcpClient.getCodingAgentId();
        const userQuery = `Explain the following ${editor.document.languageId} code:\n\`\`\`${editor.document.languageId}\n${selectedText}\n\`\`\``;

        sadsProvider.postMessageToPanel({ content: userQuery, isAgent: false });

        const payload: ExplainCodePayload = {
            code_snippet: selectedText,
            language: editor.document.languageId,
            user_query: 'Explain this code snippet.' // Agent-facing query
        };

        const conversationId = `explain-${Date.now()}`;
        sadsProvider.setCurrentConversationId(conversationId);

        const immediateResponse = await mcpClient.sendRequest(codingAgentId, 'elizaos:ide:explain_code', payload, conversationId);
        if (immediateResponse) {
            // sadsProvider.handleMcpMessage(immediateResponse); // Already handled by the onMessage listener
            if (immediateResponse.performative === "REJECT" || immediateResponse.performative === "FAILURE") {
                sadsProvider.setCurrentConversationId(null);
            }
        } else {
             sadsProvider.postMessageToPanel({ content: `Failed to send request to ${codingAgentId}. Check console for errors.`, isError: true, sender: "System" });
             sadsProvider.setCurrentConversationId(null);
        }
    });

    registerCommand('elizaos-ide-liaison.askEddyForDocs', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('No active editor found.');
            return;
        }
        const selection = editor.selection;
        const selectedText = editor.document.getText(selection);
        if (!selectedText) {
            vscode.window.showInformationMessage('No text selected for documentation lookup.');
            return;
        }

        const docsAgentId = mcpClient.getDocsAgentId();
        const userQuery = `Find documentation for: ${selectedText}`;
        sadsProvider.postMessageToPanel({ content: userQuery, isAgent: false });

        const payload: GetDocumentationPayload = {
            code_snippet: selectedText,
            language: editor.document.languageId,
            user_query: 'Get documentation for this API or code snippet.' // Agent-facing query
        };

        const conversationId = `docs-${Date.now()}`;
        sadsProvider.setCurrentConversationId(conversationId);

        const immediateResponse = await mcpClient.sendRequest(docsAgentId, 'elizaos:ide:get_documentation', payload, conversationId);
        if (immediateResponse) {
            // sadsProvider.handleMcpMessage(immediateResponse); // Already handled by the onMessage listener
            if (immediateResponse.performative === "REJECT" || immediateResponse.performative === "FAILURE") {
                sadsProvider.setCurrentConversationId(null);
            }
        } else {
            sadsProvider.postMessageToPanel({ content: `Failed to send request to ${docsAgentId}. Check console for errors.`, isError: true, sender: "System" });
            sadsProvider.setCurrentConversationId(null);
       }
    });

    registerCommand('elizaos-ide-liaison.askJulesToRefactor', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('No active editor found.');
            return;
        }
        const selection = editor.selection;
        const selectedText = editor.document.getText(selection);
        if (!selectedText) {
            vscode.window.showInformationMessage('No text selected to refactor.');
            return;
        }

        const codingAgentId = mcpClient.getCodingAgentId();
        const userQuery = `Suggest refactorings for the following ${editor.document.languageId} code snippet:\n\`\`\`${editor.document.languageId}\n${selectedText}\n\`\`\``;
        sadsProvider.postMessageToPanel({ content: userQuery, isAgent: false });

        const payload: RefactorSuggestionPayload = {
            code_snippet: selectedText,
            language: editor.document.languageId,
            user_query: 'Suggest refactoring for this code.' // Agent-facing query
        };

        const conversationId = `refactor-${Date.now()}`;
        sadsProvider.setCurrentConversationId(conversationId);

        const immediateResponse = await mcpClient.sendRequest(codingAgentId, 'elizaos:ide:refactor_suggestion', payload, conversationId);

        if (immediateResponse) {
            // If server sends ACCEPT/REJECT/FAILURE immediately, SadsPanel handles it via onMessage.
            // We only need to manage conversation state if it's a definitive end.
            if (immediateResponse.performative === "REJECT" || immediateResponse.performative === "FAILURE") {
                sadsProvider.setCurrentConversationId(null);
            }
        } else {
            // Network error or client-side issue before sending
            sadsProvider.postMessageToPanel({ content: `Failed to send refactor request to ${codingAgentId}. Check console.`, isError: true, sender: "System" });
            sadsProvider.setCurrentConversationId(null);
        }
    });
}

export function deactivate() {
    // Resources managed by context.subscriptions (like McpClient) will be disposed automatically.
    console.log("ElizaOS IDE Liaison deactivated.");
}
