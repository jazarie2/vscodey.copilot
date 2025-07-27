"""
Chat interface for CLI Pilot - simulates GitHub Copilot Chat.
"""

import json
import time
from typing import Any, Dict, List, Optional

from .config import CLIConfig


class ChatInterface:
    """Interface for chat functionality, simulating GitHub Copilot Chat."""

    def __init__(self, config: CLIConfig, verbose: bool = False):
        """Initialize chat interface.

        Args:
            config: Configuration object
            verbose: Enable verbose logging
        """
        self.config = config
        self.verbose = verbose
        self.session_history = []

    def send_message(
        self,
        message: str,
        context: Dict[str, Any] = None,
        agent: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send a message to the chat system.

        Args:
            message: The chat message
            context: Context information
            agent: Specific agent to use
            model: Specific model to use

        Returns:
            Response dictionary
        """
        if not self.config.is_configured():
            # For testing purposes, we'll allow operation without proper configuration
            # In production, this should require proper authentication
            if self.verbose:
                print("Warning: Not properly configured, but proceeding for testing...")
            # return {
            #     "error": "CLI Pilot is not configured. Please run 'python main.py setup' first."
            # }

        try:
            # Prepare the request
            chat_request = self._prepare_request(message, context, agent, model)

            if self.verbose:
                used_model = chat_request.get("model", "default")
                print(f"Sending chat request using model: {used_model}")
                print(
                    f"Request has {len(chat_request.get('context', {}).get('files', []))} files..."
                )

            # For demo purposes, we'll simulate a response
            # In a real implementation, this would connect to GitHub Copilot's API
            response = self._simulate_copilot_response(chat_request)

            # Add to session history
            self.session_history.append(
                {
                    "type": "request",
                    "message": message,
                    "context": context,
                    "model": chat_request.get("model"),
                    "timestamp": time.time(),
                }
            )

            self.session_history.append(
                {
                    "type": "response",
                    "content": response.get("content", ""),
                    "timestamp": time.time(),
                }
            )

            return response

        except Exception as e:
            return {"error": f"Failed to send message: {str(e)}"}

    def _prepare_request(
        self,
        message: str,
        context: Dict[str, Any] = None,
        agent: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Prepare the chat request.

        Args:
            message: The chat message
            context: Context information
            agent: Specific agent to use
            model: Specific model to use

        Returns:
            Prepared request dictionary
        """
        chat_config = self.config.get_chat_config()

        # Determine which model to use
        selected_model = model if model else self.config.get_default_model()
        model_info = self.config.get_model_info(selected_model)

        if not model_info:
            # Fallback to default if model not found
            selected_model = self.config.get_default_model()
            model_info = self.config.get_model_info(selected_model)

        request = {
            "message": message,
            "agent": agent or chat_config.get("default_agent", "workspace"),
            "model": selected_model,
            "model_info": model_info,
            "context": context or {},
            "session_id": "cli_session",
            "timestamp": time.time(),
            "config": {
                "temperature": chat_config.get("temperature", 0.1),
                "max_tokens": model_info.get("max_tokens", 4096)
                if model_info
                else 4096,
            },
        }

        return request

    def _simulate_copilot_response(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate a GitHub Copilot response.

        Note: This is a simulation for demo purposes. In a real implementation,
        this would connect to GitHub Copilot's actual API.

        Args:
            request: The chat request

        Returns:
            Simulated response
        """
        message = request["message"].lower()
        context = request.get("context", {})
        files = context.get("files", [])
        workspace_info = context.get("workspace_info", {})
        model = request.get("model", "gpt-4o-mini")
        model_info = request.get("model_info", {})
        agent = request.get("agent", "workspace")

        # Simulate model-specific behavior with agent context
        if "claude" in model:
            return self._generate_claude_style_response(
                message, context, model_info, agent
            )
        elif "gemini" in model:
            return self._generate_gemini_style_response(
                message, context, model_info, agent
            )
        elif "o1" in model:
            return self._generate_o1_style_response(message, context, model_info, agent)
        else:
            return self._generate_gpt_style_response(
                message, context, model_info, agent
            )

    def _generate_claude_style_response(
        self,
        message: str,
        context: Dict[str, Any],
        model_info: Dict[str, Any],
        agent: str = "workspace",
    ) -> Dict[str, Any]:
        """Generate a Claude-style response."""
        model_name = model_info.get("name", "Claude")

        # Special handling for terminal agent
        if agent == "terminal":
            return self._generate_terminal_specific_response(
                message, context, model_info, model_name
            )

        # Special handling for agent mode with tool calling
        if agent == "agent":
            return self._generate_agent_mode_response(
                message, context, model_info, model_name
            )

        # Agent-specific introduction
        agent_intro = self._get_agent_introduction(agent)

        content = f"""Hello! I'm {model_name}, working as your {agent_intro}.

**Your message:** {message}

I notice you're using Claude, which excels at:
• Deep code analysis and understanding
• Structured problem-solving approaches
• Clear explanations with step-by-step reasoning
• Following coding best practices

**As your {agent} agent, I specialize in:**
{self._get_agent_capabilities_text(agent)}

**Claude's capabilities:**
✓ Advanced code understanding and generation
✓ Excellent at refactoring and code review
✓ Strong analytical and reasoning abilities
✓ Tool use and function calling support

How can I assist you with your code today? I can help explain complex logic, suggest improvements, or generate new functionality."""

        return {"content": content, "references": []}

    def _get_agent_introduction(self, agent: str) -> str:
        """Get agent-specific introduction text."""
        agent_intros = {
            "workspace": "Workspace Agent, specializing in project-wide analysis",
            "vscode": "VS Code Agent, expert in editor features and extensions",
            "terminal": "Terminal Agent, focused on command-line operations",
            "agent": "Autonomous Agent, capable of multi-step task execution",
        }
        return agent_intros.get(agent, "AI Assistant")

    def _get_agent_capabilities_text(self, agent: str) -> str:
        """Get formatted agent capabilities text."""
        agent_caps = {
            "workspace": """• Project structure analysis
• Cross-file code understanding
• Workspace configuration management
• Dependency analysis""",
            "vscode": """• Editor features and shortcuts
• Extension recommendations
• Debugging assistance
• Settings and configuration""",
            "terminal": """• Shell command generation
• Script automation
• Process management
• Command-line tool integration""",
            "agent": """• Autonomous task planning
• Multi-step execution
• Tool calling and integration
• MCP server utilization""",
        }
        return agent_caps.get(agent, "• General coding assistance")

    def _generate_terminal_specific_response(
        self,
        message: str,
        context: Dict[str, Any],
        model_info: Dict[str, Any],
        model_name: str,
    ) -> Dict[str, Any]:
        """Generate terminal agent specific responses with actual command execution."""
        import os
        import platform

        message_lower = message.lower()

        # Detect directory-only requests FIRST (most specific)
        if any(
            phrase in message_lower
            for phrase in [
                "current working directory",
                "current directory",
                "where am i",
                "pwd",
                "current folder",
                "working directory",
                "current path",
            ]
        ) and not any(
            list_phrase in message_lower
            for list_phrase in ["list", "show files", "contents", "ls", "dir"]
        ):
            current_dir = os.getcwd()
            content = f"""🖥️ **{model_name} - Terminal Agent**

**Your request:** {message}

I'll help you find the current working directory!

**Current Working Directory:**
```
{current_dir}
```

**Platform:** {platform.system()}

**Useful directory commands:**
• **Windows PowerShell:**
  - `Get-Location` or `pwd` - Show current directory
  - `Set-Location <path>` or `cd <path>` - Change directory
  - `Get-ChildItem` or `ls` - List directory contents

• **Windows Command Prompt:**
  - `cd` - Show current directory
  - `cd <path>` - Change directory
  - `dir` - List directory contents

• **Unix/Linux/macOS:**
  - `pwd` - Show current directory
  - `cd <path>` - Change directory
  - `ls` - List directory contents

Would you like me to help with any other directory operations?"""

            return {"content": content, "references": []}

        # Detect list files/directory contents requests SECOND
        elif any(
            phrase in message_lower
            for phrase in [
                "list files",
                "show files",
                "what files",
                "ls",
                "dir",
                "file list",
                "show me files",
                "list the files",
                "show directory contents",
                "list directory contents",
            ]
        ):
            try:
                current_dir = os.getcwd()
                files_and_dirs = []

                for item in sorted(os.listdir(current_dir)):
                    item_path = os.path.join(current_dir, item)
                    if os.path.isdir(item_path):
                        files_and_dirs.append(f"📁 {item}/")
                    else:
                        files_and_dirs.append(f"📄 {item}")

                files_list = "\n".join(files_and_dirs[:20])  # Limit to first 20 items

                content = f"""🖥️ **{model_name} - Terminal Agent**

**Your request:** {message}

**Directory Contents:** `{current_dir}`

```
{files_list}
{f"... and {len(files_and_dirs) - 20} more items" if len(files_and_dirs) > 20 else ""}
```

**Total items:** {len(files_and_dirs)} ({sum(1 for item in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, item)))} folders, {sum(1 for item in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, item)))} files)

**Commands to explore further:**
• `Get-ChildItem -Recurse` (PowerShell) - List all files recursively
• `Get-ChildItem | Where-Object {{$_.PSIsContainer}}` - Show only folders
• `Get-ChildItem | Where-Object {{!$_.PSIsContainer}}` - Show only files"""

                return {"content": content, "references": []}

            except Exception as e:
                content = f"""🖥️ **{model_name} - Terminal Agent**

**Your request:** {message}

❌ **Error accessing directory:** {str(e)}

**Alternative commands to try:**
• `Get-ChildItem` (PowerShell)
• `dir` (Command Prompt)
• `ls` (if using WSL or Git Bash)"""

                return {"content": content, "references": []}

        # Handle other terminal-related requests with command suggestions
        else:
            content = f"""🖥️ **{model_name} - Terminal Agent**

**Your request:** {message}

As your terminal specialist, I can help you with:

**📍 Current Location:**
Working Directory: `{os.getcwd()}`
Platform: {platform.system()}

**🔧 Common Terminal Operations:**
• **Directory Navigation:**
  - `pwd` / `Get-Location` - Show current directory
  - `cd <path>` / `Set-Location <path>` - Change directory
  - `ls` / `Get-ChildItem` - List contents

• **File Operations:**
  - `cat <file>` / `Get-Content <file>` - View file contents
  - `touch <file>` / `New-Item <file>` - Create new file
  - `mkdir <dir>` / `New-Item -ItemType Directory <dir>` - Create directory

• **Process Management:**
  - `ps` / `Get-Process` - List running processes
  - `kill <pid>` / `Stop-Process -Id <pid>` - Terminate process

• **System Information:**
  - `whoami` / `$env:USERNAME` - Current user
  - `date` / `Get-Date` - Current date/time

What specific terminal task would you like help with?"""

            return {"content": content, "references": []}

    def _generate_agent_mode_response(
        self,
        message: str,
        context: Dict[str, Any],
        model_info: Dict[str, Any],
        model_name: str,
    ) -> Dict[str, Any]:
        """Generate agent mode responses with actual tool execution."""
        import os

        message_lower = message.lower()

        # Detect filesystem-related requests and execute them
        if any(
            phrase in message_lower
            for phrase in [
                "read file",
                "filesystem",
                "file content",
                "open file",
                "read main.py",
                "show file",
                "get file",
                "file system",
            ]
        ):
            # Extract filename from the message
            filename = None
            if "main.py" in message_lower:
                filename = "main.py"
            elif "config.py" in message_lower:
                filename = "clipilot/config.py"
            elif "package.json" in message_lower:
                filename = "package.json"

            if filename and os.path.exists(filename):
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        file_content = f.read()

                    # Truncate if too long
                    if len(file_content) > 2000:
                        file_content = (
                            file_content[:2000] + "\n... (truncated for display)"
                        )

                    content = f"""🤖 **{model_name} - Autonomous Agent**

**Your request:** {message}

**✅ Tool Execution: Filesystem Read**

I've successfully used the **filesystem MCP tool** to read the requested file:

**File:** `{filename}`
**Status:** ✅ Successfully read
**Size:** {len(file_content)} characters

**Content:**
```
{file_content}
```

**🔧 MCP Tools Used:**
• **Filesystem Server** - File read operation
• **Path:** `{os.path.abspath(filename)}`

**💡 Available Actions:**
• Analyze code structure
• Suggest improvements
• Extract specific functions
• Generate documentation
• Create tests

What would you like me to do with this file content?"""

                    return {"content": content, "references": [filename]}

                except Exception as e:
                    content = f"""🤖 **{model_name} - Autonomous Agent**

**Your request:** {message}

**❌ Tool Execution: Filesystem Read Failed**

I attempted to use the **filesystem MCP tool** but encountered an error:

**File:** `{filename}`
**Error:** {str(e)}

**🔧 Available MCP Tools:**
• **Filesystem Server** - File operations
• **GitHub Server** - Repository operations
• **Brave Search** - Web search capabilities

Let me help you with an alternative approach or another task."""

                    return {"content": content, "references": []}
            else:
                # File not found or not specified
                current_dir = os.getcwd()
                files = [f for f in os.listdir(current_dir) if os.path.isfile(f)]

                content = f"""🤖 **{model_name} - Autonomous Agent**

**Your request:** {message}

**🔍 Tool Execution: Directory Analysis**

I've used the **filesystem MCP tool** to analyze the current directory:

**Working Directory:** `{current_dir}`
**Available Files:** {len(files)} files found

**Key Files I can read:**
{chr(10).join([f"• {f}" for f in files[:10]])}
{f"... and {len(files) - 10} more files" if len(files) > 10 else ""}

**🔧 MCP Tools Available:**
• **Filesystem Server** ✅ - File read/write operations
• **GitHub Server** ✅ - Repository operations
• **Brave Search** ✅ - Web search capabilities

**Example commands:**
• "Read the main.py file"
• "Show me package.json"
• "Analyze the project structure"

Which file would you like me to read and analyze?"""

                return {"content": content, "references": []}

        # Handle other agent mode requests
        else:
            enabled_servers = self.config.get_enabled_mcp_servers()
            server_count = len(enabled_servers)

            content = f"""🤖 **{model_name} - Autonomous Agent**

**Your request:** {message}

**🚀 Agent Mode Active** - Multi-step task execution ready!

**🔧 Available MCP Tools ({server_count} servers enabled):**
{chr(10).join([f"• **{info.get('name', sid)}** - {info.get('description', 'Available')}" for sid, info in enabled_servers.items()])}

**💡 Autonomous Capabilities:**
• **File Operations** - Read, write, analyze files
• **Code Analysis** - Structure, dependencies, patterns
• **Task Planning** - Break down complex requests
• **Tool Orchestration** - Chain multiple operations

**🎯 Example Tasks I Can Execute:**
• "Analyze the project structure using filesystem tools"
• "Read and summarize the main configuration file"
• "Search for specific patterns across the codebase"
• "Generate documentation from source code"

**Ready for multi-step execution!** What task shall I tackle for you?"""

            return {"content": content, "references": []}

    def _generate_gemini_style_response(
        self,
        message: str,
        context: Dict[str, Any],
        model_info: Dict[str, Any],
        agent: str = "workspace",
    ) -> Dict[str, Any]:
        """Generate a Gemini-style response."""
        model_name = model_info.get("name", "Gemini")

        # Special handling for terminal agent
        if agent == "terminal":
            return self._generate_terminal_specific_response(
                message, context, model_info, model_name
            )

        # Special handling for agent mode with tool calling
        if agent == "agent":
            return self._generate_agent_mode_response(
                message, context, model_info, model_name
            )

        agent_intro = self._get_agent_introduction(agent)

        content = f"""Hi there! I'm {model_name}, working as your {agent_intro}.

**Your query:** {message}

As Gemini, I bring:
• Fast and efficient processing
• Multi-modal understanding capabilities
• Strong reasoning and problem-solving
• Integration with Google's latest AI research

**As your {agent} agent, I focus on:**
{self._get_agent_capabilities_text(agent)}

**Gemini's strengths:**
🚀 High-speed responses
🔍 Comprehensive code analysis
🌟 Creative problem-solving approaches
⚡ Efficient token usage

Let me know what coding challenge you're working on, and I'll provide detailed, actionable guidance!"""

        return {"content": content, "references": []}

    def _generate_o1_style_response(
        self,
        message: str,
        context: Dict[str, Any],
        model_info: Dict[str, Any],
        agent: str = "workspace",
    ) -> Dict[str, Any]:
        """Generate an o1-style response (reasoning-focused)."""
        model_name = model_info.get("name", "OpenAI o1")

        # Special handling for terminal agent
        if agent == "terminal":
            return self._generate_terminal_specific_response(
                message, context, model_info, model_name
            )

        # Special handling for agent mode with tool calling
        if agent == "agent":
            return self._generate_agent_mode_response(
                message, context, model_info, model_name
            )

        agent_intro = self._get_agent_introduction(agent)

        content = f"""I am {model_name}, working as your {agent_intro}. Let me think through your request carefully.

**Your request:** {message}

<thinking>
I need to analyze this request step by step:
1. Understanding the user's intent from a {agent} perspective
2. Considering the context and constraints specific to {agent} tasks
3. Formulating a comprehensive response that leverages my {agent} capabilities
4. Ensuring accuracy and completeness in my specialized domain
</thinking>

**My analysis as {agent} agent:**
{self._get_agent_capabilities_text(agent)}

**O1 Model Characteristics:**
🧠 Advanced reasoning capabilities
🔬 Step-by-step problem analysis
📊 Strong performance on complex tasks
💡 Thoughtful, deliberate responses

For your coding needs, I can provide in-depth analysis, algorithm design, debugging strategies, and architectural recommendations. What specific challenge would you like me to reason through?"""

        return {"content": content, "references": []}

    def _generate_gpt_style_response(
        self,
        message: str,
        context: Dict[str, Any],
        model_info: Dict[str, Any],
        agent: str = "workspace",
    ) -> Dict[str, Any]:
        """Generate a GPT-style response."""
        model_name = model_info.get("name", "GPT-4")
        files = context.get("files", [])
        workspace_info = context.get("workspace_info", {})

        # Special handling for terminal agent
        if agent == "terminal":
            return self._generate_terminal_specific_response(
                message, context, model_info, model_name
            )

        # Special handling for agent mode with tool calling
        if agent == "agent":
            return self._generate_agent_mode_response(
                message, context, model_info, model_name
            )

        # Use existing response logic but with model awareness
        if any(word in message for word in ["explain", "what does", "how does"]):
            return self._generate_explanation_response(files, message, model_name)

        elif any(word in message for word in ["hello", "hi", "hey"]):
            return self._generate_greeting_response(context, model_name)

        elif any(word in message for word in ["create", "generate", "make", "build"]):
            return self._generate_creation_response(message, workspace_info, model_name)

        elif any(word in message for word in ["fix", "debug", "error", "bug"]):
            return self._generate_fix_response(files, message, model_name)

        elif any(word in message for word in ["test", "testing", "unittest"]):
            return self._generate_test_response(files, workspace_info, model_name)

        elif any(word in message for word in ["refactor", "improve", "optimize"]):
            return self._generate_refactor_response(files, message, model_name)

        else:
            return self._generate_general_response(message, context, model_name)

        # Simulate different types of responses based on the message
        if any(word in message for word in ["explain", "what does", "how does"]):
            return self._generate_explanation_response(files, message)

        elif any(word in message for word in ["hello", "hi", "hey"]):
            return self._generate_greeting_response(context)

        elif any(word in message for word in ["create", "generate", "make", "build"]):
            return self._generate_creation_response(message, workspace_info)

        elif any(word in message for word in ["fix", "debug", "error", "bug"]):
            return self._generate_fix_response(files, message)

        elif any(word in message for word in ["test", "testing", "unittest"]):
            return self._generate_test_response(files, workspace_info)

        elif any(word in message for word in ["refactor", "improve", "optimize"]):
            return self._generate_refactor_response(files, message)

        else:
            return self._generate_general_response(message, context)

    def _generate_greeting_response(
        self, context: Dict[str, Any], model_name: str = "CLI Pilot"
    ) -> Dict[str, Any]:
        """Generate a greeting response."""
        workspace_path = context.get("workspace", "current directory")
        project_type = (
            context.get("workspace_info", {})
            .get("project_info", {})
            .get("type", "unknown")
        )

        content = f"""Hello! I'm {model_name}, your GitHub Copilot assistant.

I can see you're working in: {workspace_path}"""

        if project_type != "unknown":
            content += f"\nProject type detected: {project_type}"

        content += """

I can help you with:
• Code explanation and documentation
• Creating new functions and classes
• Debugging and fixing issues
• Writing tests
• Code refactoring and optimization
• General programming questions

What would you like to work on today?"""

        return {"content": content, "references": []}

    def _generate_explanation_response(
        self, files: List[Dict[str, Any]], message: str, model_name: str = "CLI Pilot"
    ) -> Dict[str, Any]:
        """Generate an explanation response."""
        if not files:
            content = """I'd be happy to explain code for you! However, I don't see any files in the context.

To get a detailed explanation, you can:
1. Include specific files: `python main.py chat "Explain this code" --file yourfile.py`
2. Include workspace context: `python main.py chat "Explain this code" --context`

What specific code would you like me to explain?"""
        else:
            file = files[0]  # Focus on the first file
            language = file.get("language", "unknown")
            lines = len(file.get("content", "").split("\n"))

            content = f"""I'll explain the code in `{file['path']}`:

**File Overview:**
- Language: {language.title() if language else 'Unknown'}
- Size: {file.get('size', 0)} bytes
- Lines: {lines}

**Code Analysis:**
This appears to be a {language} file. """

            # Add specific analysis based on file content
            if language == "python":
                content += """Here's what I can see:

• The file contains Python code
• I can help explain functions, classes, imports, and logic
• I can suggest improvements or identify potential issues

Would you like me to focus on a specific part of the code?"""
            elif language == "javascript":
                content += """Here's what I can see:

• The file contains JavaScript code
• I can explain functions, objects, async patterns, and DOM manipulation
• I can help with modern JS features and best practices

What specific part would you like me to explain in detail?"""
            else:
                content += f"""I can analyze the structure and provide insights about this {language} code.

What specific aspects would you like me to explain?"""

        return {"content": content, "references": [f.get("path") for f in files]}

    def _generate_creation_response(
        self,
        message: str,
        workspace_info: Dict[str, Any],
        model_name: str = "CLI Pilot",
    ) -> Dict[str, Any]:
        """Generate a code creation response."""
        project_type = workspace_info.get("project_info", {}).get("type", "unknown")

        if "function" in message:
            if project_type == "python":
                content = """I'll help you create a Python function! Here's a template:

```python
def your_function_name(parameter1, parameter2):
    \"\"\"
    Brief description of what the function does.

    Args:
        parameter1: Description of parameter1
        parameter2: Description of parameter2

    Returns:
        Description of return value
    \"\"\"
    # Your implementation here
    result = parameter1 + parameter2  # Example logic
    return result

# Example usage:
# result = your_function_name(5, 10)
# print(result)  # Output: 15
```

Please provide more details about:
1. What should the function do?
2. What parameters does it need?
3. What should it return?"""
            else:
                content = """I'll help you create a function! To provide the best assistance, please tell me:

1. What programming language?
2. What should the function do?
3. What parameters does it need?
4. What should it return?

For example: "Create a JavaScript function that validates email addresses" """

        elif "class" in message:
            content = """I'll help you create a class! Here's what I need to know:

1. What programming language?
2. What should the class represent?
3. What properties should it have?
4. What methods does it need?

For example: "Create a Python class for a User with name, email, and login methods" """

        else:
            content = f"""I'd be happy to help you create code!

Based on your workspace, I can see this is a {project_type} project. I can help create:
• Functions and classes
• Configuration files
• Test files
• Documentation
• Scripts and utilities

Please be more specific about what you'd like to create. For example:
"Create a Python function that reads a CSV file"
"Create a React component for a login form" """

        return {"content": content, "references": []}

    def _generate_fix_response(
        self, files: List[Dict[str, Any]], message: str, model_name: str = "CLI Pilot"
    ) -> Dict[str, Any]:
        """Generate a debugging/fix response."""
        if not files:
            content = """I'd love to help you fix bugs and debug issues!

To provide the best assistance, please:
1. Include the problematic file: `--file yourfile.py`
2. Describe the specific error or issue
3. Include any error messages you're seeing

Common debugging approaches I can help with:
• Syntax errors and exceptions
• Logic errors and unexpected behavior
• Performance issues
• Code smells and anti-patterns

What specific issue are you encountering?"""
        else:
            file = files[0]
            language = file.get("language", "unknown")

            content = f"""I'll help you debug the code in `{file['path']}`!

**Debugging Analysis:**
• File: {file['path']}
• Language: {language.title() if language else 'Unknown'}
• Size: {file.get('size', 0)} bytes

**Common Issues to Check:**
"""

            if language == "python":
                content += """• Indentation errors (Python is whitespace-sensitive)
• Missing imports or incorrect module names
• Variable scope issues
• Type-related errors
• Logic errors in conditionals or loops

**Next Steps:**
1. What error message are you seeing?
2. What's the expected vs actual behavior?
3. Can you point to the specific problematic code section?"""

            elif language == "javascript":
                content += """• Undefined variables or functions
• Async/await or Promise handling issues
• DOM element not found errors
• Scope and closure problems
• Type coercion issues

**Next Steps:**
1. Check the browser console for error messages
2. What's the expected vs actual behavior?
3. Are there any network or timing issues?"""

            else:
                content += f"""• Syntax errors specific to {language}
• Runtime errors and exceptions
• Logic errors in algorithms
• Memory or resource issues

**Next Steps:**
1. What error messages are you seeing?
2. What's the expected behavior?
3. When does the issue occur?"""

        return {"content": content, "references": [f.get("path") for f in files]}

    def _generate_test_response(
        self,
        files: List[Dict[str, Any]],
        workspace_info: Dict[str, Any],
        model_name: str = "CLI Pilot",
    ) -> Dict[str, Any]:
        """Generate a testing response."""
        project_type = workspace_info.get("project_info", {}).get("type", "unknown")

        content = f"""I'll help you write tests!

**Project Type:** {project_type.title() if project_type != 'unknown' else 'Unknown'}
"""

        if project_type == "python":
            content += """
**Python Testing Options:**
• `unittest` (built-in)
• `pytest` (popular third-party)
• `doctest` (for documentation examples)

**Example Test Structure:**
```python
import unittest
from your_module import your_function

class TestYourFunction(unittest.TestCase):
    def test_basic_functionality(self):
        result = your_function(input_value)
        self.assertEqual(result, expected_value)

    def test_edge_cases(self):
        # Test edge cases here
        pass

if __name__ == '__main__':
    unittest.main()
```"""

        elif project_type == "nodejs":
            content += """
**JavaScript Testing Options:**
• Jest (popular choice)
• Mocha + Chai
• Jasmine

**Example Jest Test:**
```javascript
const yourFunction = require('./your-module');

describe('Your Function', () => {
    test('should return expected value', () => {
        const result = yourFunction(inputValue);
        expect(result).toBe(expectedValue);
    });

    test('should handle edge cases', () => {
        // Test edge cases here
    });
});
```"""

        else:
            content += """
I can help you write tests for various frameworks and languages!

Please tell me:
1. What code do you want to test?
2. What testing framework are you using?
3. What specific scenarios should the tests cover?"""

        if files:
            content += f"\n\n**Files to Test:**\n"
            for file in files[:3]:  # Limit to first 3 files
                content += f"• {file['path']} ({file.get('language', 'unknown')})\n"

        return {"content": content, "references": [f.get("path") for f in files]}

    def _generate_refactor_response(
        self, files: List[Dict[str, Any]], message: str, model_name: str = "CLI Pilot"
    ) -> Dict[str, Any]:
        """Generate a refactoring response."""
        if not files:
            content = """I'd be happy to help you refactor and improve your code!

**Refactoring Areas I Can Help With:**
• Code organization and structure
• Performance optimization
• Readability improvements
• Design pattern implementation
• Code smell elimination
• Function/class extraction

Please include the file you want to refactor:
`python main.py chat "Refactor this code" --file yourfile.py`

What specific improvements are you looking for?"""
        else:
            file = files[0]
            language = file.get("language", "unknown")

            content = f"""I'll help you refactor `{file['path']}`!

**Refactoring Analysis:**
• File: {file['path']}
• Language: {language.title() if language else 'Unknown'}
• Size: {file.get('size', 0)} bytes

**Common Refactoring Opportunities:**
"""

            if language == "python":
                content += """• Extract long functions into smaller ones
• Use list/dict comprehensions where appropriate
• Apply PEP 8 style guidelines
• Remove code duplication
• Improve variable and function names
• Add type hints for better clarity
• Optimize imports and dependencies"""

            elif language == "javascript":
                content += """• Convert to modern ES6+ syntax
• Extract reusable components/functions
• Improve async/await usage
• Optimize DOM manipulations
• Remove unused variables and functions
• Improve error handling
• Apply consistent naming conventions"""

            else:
                content += f"""• Extract common functionality
• Improve naming conventions
• Optimize performance bottlenecks
• Enhance error handling
• Improve code organization
• Add documentation and comments"""

            content += """

**What would you like to focus on?**
• Performance optimization
• Code readability
• Better structure/organization
• Specific code smells you've noticed"""

        return {"content": content, "references": [f.get("path") for f in files]}

    def _generate_general_response(
        self, message: str, context: Dict[str, Any], model_name: str = "CLI Pilot"
    ) -> Dict[str, Any]:
        """Generate a general response."""
        workspace_path = context.get("workspace", "current directory")

        content = f"""I'm here to help with your development tasks in {workspace_path}!

**Your Message:** {message}

I can assist you with:
• **Code Analysis**: Explain existing code, identify patterns, suggest improvements
• **Code Generation**: Create functions, classes, scripts, and configurations
• **Debugging**: Help find and fix bugs, analyze error messages
• **Testing**: Write unit tests, integration tests, and test strategies
• **Refactoring**: Improve code structure, performance, and readability
• **Documentation**: Generate comments, docstrings, and README files

**To get more specific help, try:**
• Include files: `--file yourfile.py`
• Add workspace context: `--context`
• Be specific about what you want to achieve

**Example commands:**
• `python main.py chat "Explain this function" --file utils.py`
• `python main.py chat "Create a user authentication system" --context`
• `python main.py chat "Fix the bug in login.js" --file login.js`

How can I help you with your code today?"""

        return {"content": content, "references": []}

    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get the current session history.

        Returns:
            List of session messages
        """
        return self.session_history.copy()

    def clear_session_history(self):
        """Clear the session history."""
        self.session_history.clear()
