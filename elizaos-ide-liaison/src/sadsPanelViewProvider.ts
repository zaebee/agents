import * as vscode from 'vscode';
import { McpMessage, PanelMessage } from './mcpInterfaces'; // PanelMessage for webview communication

export class SadsPanelViewProvider implements vscode.WebviewViewProvider {
    public static readonly viewType = 'elizaosSadsPanel'; // Matches package.json

    private _view?: vscode.WebviewView;
    private readonly _extensionUri: vscode.Uri;
    private _currentConversationId: string | null = null; // To track ongoing interaction for context

    constructor(private readonly context: vscode.ExtensionContext) {
        this._extensionUri = context.extensionUri;
    }

    public resolveWebviewView(
        webviewView: vscode.WebviewView,
        context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken,
    ) {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [vscode.Uri.joinPath(this._extensionUri, 'media')]
        };

        webviewView.webview.html = this._getHtmlForWebview(webviewView.webview);

        // Handle messages from the webview (if any)
        webviewView.webview.onDidReceiveMessage(data => {
            switch (data.command) {
                case 'alert': // Example
                    vscode.window.showErrorMessage(data.text);
                    return;
            }
        });

        // Let the extension know the panel is ready (optional)
        // vscode.commands.executeCommand('elizaos-ide-liaison.sadsPanelReady');

        this.postMessageToPanel({
            type: 'addMessage',
            content: "Welcome! Select code and use context menus or commands to interact with ElizaOS agents.",
            isInfo: true, // This will use the 'info-message' styling
            sender: "System"
        });
    }

    private _getHtmlForWebview(webview: vscode.Webview): string {
        const panelHtmlPath = vscode.Uri.joinPath(this._extensionUri, 'media', 'sadsPanel.html');
        let htmlContent = vscode.workspace.fs.readFile(panelHtmlPath).then(buffer => buffer.toString());

        // This is a simplified way; in reality, you might read the file content
        // For now, using the content directly from when it was created.
        // This should be replaced with actual file reading for robustness.
        return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ElizaOS SADS Panel</title>
    <style>
        body { font-family: var(--vscode-font-family); color: var(--vscode-editor-foreground); background-color: var(--vscode-editor-background); padding: 0.5em; }
        .message-container { margin-bottom: 10px; padding: 8px; border-radius: 4px; }
        .user-message { background-color: var(--vscode-list-activeSelectionBackground); color: var(--vscode-list-activeSelectionForeground); text-align: left; margin-left: 20px;}
        .agent-message { background-color: var(--vscode-editorWidget-background); border: 1px solid var(--vscode-editorWidget-border); margin-right: 20px;}
        .error-message { background-color: var(--vscode-inputValidation-errorBackground); color: var(--vscode-inputValidation-errorForeground); border: 1px solid var(--vscode-inputValidation-errorBorder); }
        .info-message { background-color: var(--vscode-inputValidation-infoBackground); color: var(--vscode-inputValidation-infoForeground); border: 1px solid var(--vscode-inputValidation-infoBorder); }
        pre { white-space: pre-wrap; word-wrap: break-word; background-color: var(--vscode-textCodeBlock-background); padding: 0.5em; border-radius: 3px; font-family: var(--vscode-editor-font-family); }
        strong { font-weight: bold; }
    </style>
</head>
<body>
    <div id="chat-history" style="overflow-y: auto; height: calc(100vh - 20px);">
        <!-- Initial message will be added by script if desired, or keep this as a static welcome -->
    </div>
    <script>
        const vscode = acquireVsCodeApi();
        const chatHistory = document.getElementById('chat-history');

        function escapeHtml(unsafe) {
            if (typeof unsafe !== 'string') {
                try { unsafe = JSON.stringify(unsafe, null, 2); } catch (e) { unsafe = String(unsafe); }
            }
            return unsafe.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
        }

        function addMessageToPanel(message) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message-container');
            let humanReadableSender = 'System';
            if (message.isAgent) {
                messageDiv.classList.add('agent-message');
                humanReadableSender = message.sender || 'Agent';
            } else if (message.isError) {
                messageDiv.classList.add('error-message');
                 humanReadableSender = 'Error';
            } else if (message.isInfo) {
                messageDiv.classList.add('info-message');
                 humanReadableSender = 'Info';
            }
            else {
                messageDiv.classList.add('user-message');
                humanReadableSender = 'You';
            }

            let content = message.content;
            if (typeof message.content === 'object') {
                content = JSON.stringify(message.content, null, 2);
            }

            messageDiv.innerHTML = \`<strong>\${humanReadableSender}:</strong><pre>\${escapeHtml(content)}</pre>\`;
            chatHistory.appendChild(messageDiv);
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }

        window.addEventListener('message', event => {
            const msg = event.data; // { type: 'addMessage', content: '...', isAgent: true/false, sender: 'Jules' }
            if (msg.type === 'addMessage') {
                addMessageToPanel(msg);
            } else if (msg.type === 'clearPanel') {
                chatHistory.innerHTML = ''; // Clear history
            }
        });
        // vscode.postMessage({ command: 'alert', text: 'WebView Initialized' });
    </script>
</body>
</html>`;
        // In a real scenario, you'd use webview.asWebviewUri for local resources like CSS/JS files.
    }

    public postMessageToPanel(panelMessage: PanelMessage) {
        if (this._view) {
            this._view.show(true); // Make sure the view is visible
            // panelMessage already includes the 'type' property.
            this._view.webview.postMessage(panelMessage);
        } else {
            vscode.window.showWarningMessage("ElizaOS Panel not available to display message.");
            console.warn("SADS Panel: Attempted to post message, but view is not available.", panelMessage);
        }
    }

    public clearPanel() {
        if (this._view) {
            this._view.webview.postMessage({ type: 'clearPanel' });
        }
    }

    public handleMcpMessage(mcpMessage: McpMessage) {
        console.log("SADS Panel: Received MCP Message to display:", mcpMessage);
        let panelContent: any;
        let title = `Agent: ${mcpMessage.sender || 'Unknown'}`;

        switch (mcpMessage.performative) {
            case "ACCEPT":
                panelContent = `Task accepted by ${mcpMessage.sender}. Conversation ID: ${mcpMessage.conversation_id}`;
                this.postMessageToPanel({ type: 'addMessage', content: panelContent, isAgent: true, sender: mcpMessage.sender, isInfo: true });
                this._currentConversationId = mcpMessage.conversation_id;
                break;
            case "REJECT":
                panelContent = `Task rejected by ${mcpMessage.sender}. Reason: ${mcpMessage.error?.message || 'No reason provided.'}`;
                this.postMessageToPanel({ type: 'addMessage', content: panelContent, isAgent: true, sender: mcpMessage.sender, isError: true });
                this._currentConversationId = null;
                break;
            case "FAILURE":
                panelContent = `Task failed for agent ${mcpMessage.sender}. Error: ${mcpMessage.error?.message || 'Unknown error.'}`;
                this.postMessageToPanel({ type: 'addMessage', content: panelContent, isAgent: true, sender: mcpMessage.sender, isError: true });
                this._currentConversationId = null;
                break;
            case "INFORM_RESULT":
                if (mcpMessage.conversation_id !== this._currentConversationId && this._currentConversationId !== null) {
                    // console.warn(`SADS Panel: Received INFORM_RESULT for a different conversation (${mcpMessage.conversation_id}) than current (${this._currentConversationId}). Displaying anyway.`);
                    // For now, we'll display it, but ideally, the panel might manage multiple conversations or focus.
                }
                panelContent = mcpMessage.payload; // Payload is expected to be the content to display.
                this.postMessageToPanel({ type: 'addMessage', content: panelContent, isAgent: true, sender: mcpMessage.sender });
                this._currentConversationId = null; // Conversation considered ended after result.
                break;
            default:
                console.log(`SADS Panel: Received MCP message with performative ${mcpMessage.performative}, not directly displaying.`);
                // panelContent = `Received ${mcpMessage.performative} from ${mcpMessage.sender}: ${JSON.stringify(mcpMessage.payload, null, 2)}`;
                // this.postMessageToPanel({ content: panelContent, isAgent: true, sender: mcpMessage.sender, isInfo: true });
                break;
        }
    }

    public setCurrentConversationId(conversationId: string | null) {
        this._currentConversationId = conversationId;
        if (conversationId) {
            // this.clearPanel(); // Optionally clear panel for new conversation
            // this.postMessageToPanel({content: `Starting new conversation: ${conversationId}`, isInfo: true, sender: "System"});
        }
    }
}
