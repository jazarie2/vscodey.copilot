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
            return {
                "error": "CLI Pilot is not configured. Please run authentication first:\n"
                        "  vscodey-copilot auth login\n"
                        "  or\n"
                        "  vscodey-copilot setup --token <your-token>"
            }

        try:
            # Prepare the request
            chat_request = self._prepare_request(message, context, agent, model)

            if self.verbose:
                used_model = chat_request.get("model", "default")
                print(f"Sending chat request using model: {used_model}")
                print(
                    f"Request has {len(chat_request.get('context', {}).get('files', []))} files..."
                )

            # TODO: Connect to actual GitHub Copilot API
            # This is where the real API integration would go
            response = self._call_github_copilot_api(chat_request)

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

    def _call_github_copilot_api(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Call the actual GitHub Copilot API.

        Args:
            request: The chat request

        Returns:
            API response
        """
        # TODO: Implement actual GitHub Copilot API integration
        # This would involve:
        # 1. Getting the authentication token
        # 2. Making HTTP requests to GitHub Copilot's API endpoints
        # 3. Handling the response and formatting it appropriately
        
        return {
            "error": "GitHub Copilot API integration not yet implemented.\n\n"
                    "This CLI tool requires connection to GitHub Copilot's API.\n"
                    "To implement this, you would need to:\n\n"
                    "1. Obtain GitHub Copilot API access\n"
                    "2. Implement the API client in this method\n"
                    "3. Handle authentication and request formatting\n\n"
                    "For now, this is a framework for building the integration."
        }

    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get the current session history.

        Returns:
            List of session messages
        """
        return self.session_history.copy()

    def clear_session_history(self):
        """Clear the session history."""
        self.session_history.clear()

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
            file_content = file.get("content", "")
            file_path = file.get("path", "unknown")
            file_size = file.get("size", 0)
            lines = len(file_content.split("\n"))
            
            # Detect language from file extension
            language = self._detect_language(file_path)
            
            # Analyze the actual content
            analysis = self._analyze_file_content(file_content, language, file_path)

            content = f"""📄 **Code Analysis for `{file_path}`**

**File Overview:**
- Language: {language.title()}
- Size: {file_size} bytes ({lines} lines)
- File: {file_path}

**📊 Content Analysis:**
{analysis['overview']}

**🔍 Code Structure:**
{analysis['structure']}

**💡 Key Components:**
{analysis['components']}

**🔧 Suggestions:**
{analysis['suggestions']}

**❓ Questions or Focus Areas:**
Is there a specific part of this code you'd like me to explain in more detail? I can help with:
• Function/class explanations
• Logic flow analysis
• Performance considerations
• Best practices review"""

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
            file_content = file.get("content", "")
            file_path = file.get("path", "unknown")
            language = self._detect_language(file_path)
            
            # Analyze the file for potential issues
            issues = self._detect_potential_issues(file_content, language, file_path)

            content = f"""🔧 **Debugging Analysis for `{file_path}`**

**File Overview:**
• File: {file_path}
• Language: {language.title()}
• Size: {file.get('size', 0)} bytes
• Lines: {len(file_content.split('\n'))}

**🔍 Potential Issues Detected:**
{issues['syntax_issues']}

**⚠️ Code Quality Concerns:**
{issues['quality_issues']}

**💡 Improvement Suggestions:**
{issues['suggestions']}

**🎯 Next Steps:**
1. Review the specific issues highlighted above
2. Check for any error messages in your console/terminal
3. Test the fixes incrementally

**Common {language.title()} Issues to Check:**
{issues['language_specific']}

What specific error message or behavior are you experiencing? I can provide more targeted help with the exact problem."""

        return {"content": content, "references": [f.get("path") for f in files]}

    def _detect_potential_issues(self, content: str, language: str, file_path: str) -> Dict[str, str]:
        """Detect potential issues in code files."""
        if language == 'python':
            return self._detect_python_issues(content, file_path)
        elif language in ['javascript', 'typescript']:
            return self._detect_javascript_issues(content, file_path)
        elif language == 'json':
            return self._detect_json_issues(content, file_path)
        else:
            return {
                'syntax_issues': f"• No automated {language} syntax checking available",
                'quality_issues': "• Manual review recommended",
                'suggestions': "• Use language-specific linting tools",
                'language_specific': f"• Check {language} documentation for best practices"
            }

    def _detect_python_issues(self, content: str, file_path: str) -> Dict[str, str]:
        """Detect potential issues in Python code."""
        import re
        
        issues = []
        quality_issues = []
        suggestions = []
        
        lines = content.split('\n')
        
        # Check for common Python issues
        for i, line in enumerate(lines, 1):
            # Indentation issues (mixing tabs and spaces)
            if '\t' in line and '    ' in line:
                issues.append(f"Line {i}: Mixed tabs and spaces")
                
            # Long lines (>100 characters)
            if len(line) > 100:
                quality_issues.append(f"Line {i}: Long line ({len(line)} chars) - consider breaking")
                
            # Bare except clauses
            if re.match(r'^\s*except\s*:', line):
                issues.append(f"Line {i}: Bare except clause - specify exception type")
                
            # Print statements (might be debug code)
            if re.match(r'^\s*print\s*\(', line):
                quality_issues.append(f"Line {i}: Print statement found - remove if not needed")
        
        # Check for missing imports
        if 'json.' in content and 'import json' not in content:
            issues.append("Missing import: 'import json' required")
            
        if 'os.' in content and 'import os' not in content:
            issues.append("Missing import: 'import os' required")
            
        if 're.' in content and 'import re' not in content:
            issues.append("Missing import: 'import re' required")
        
        # Check for potential logic issues
        if_without_else = len(re.findall(r'\bif\s+.*:', content)) - len(re.findall(r'\belse\s*:', content))
        if if_without_else > 3:
            quality_issues.append(f"{if_without_else} if statements without else - check edge cases")
        
        # Functions without docstrings
        functions = re.findall(r'^\s*def\s+(\w+)', content, re.MULTILINE)
        docstrings = len(re.findall(r'""".*?"""', content, re.DOTALL))
        if len(functions) > docstrings:
            suggestions.append(f"Add docstrings to {len(functions) - docstrings} functions")
        
        return {
            'syntax_issues': '\n'.join([f"• {issue}" for issue in issues]) or "• No obvious syntax issues detected",
            'quality_issues': '\n'.join([f"• {issue}" for issue in quality_issues]) or "• Code quality looks reasonable",
            'suggestions': '\n'.join([f"• {suggestion}" for suggestion in suggestions]) or "• Code structure appears good",
            'language_specific': "• Check indentation consistency\n• Verify all imports are present\n• Test exception handling\n• Run with python -m py_compile to check syntax"
        }

    def _detect_javascript_issues(self, content: str, file_path: str) -> Dict[str, str]:
        """Detect potential issues in JavaScript code."""
        import re
        
        issues = []
        quality_issues = []
        suggestions = []
        
        lines = content.split('\n')
        
        # Check for common JavaScript issues
        for i, line in enumerate(lines, 1):
            # Missing semicolons (basic check)
            if re.match(r'^\s*(var|let|const|function|return)', line) and not line.rstrip().endswith((';', '{', '}')):
                quality_issues.append(f"Line {i}: Consider adding semicolon")
                
            # == instead of === (loose equality)
            if '==' in line and '===' not in line and '!=' in line:
                issues.append(f"Line {i}: Use === or !== instead of == or !=")
                
            # Console.log statements
            if 'console.log' in line:
                quality_issues.append(f"Line {i}: Console.log found - remove if not needed")
        
        # Check for undefined variables (basic check)
        var_declarations = re.findall(r'\b(var|let|const)\s+(\w+)', content)
        declared_vars = set(var[1] for var in var_declarations)
        
        # Function declarations
        function_names = re.findall(r'function\s+(\w+)', content)
        declared_vars.update(function_names)
        
        # Check for potential undefined usage (very basic)
        used_vars = re.findall(r'\b(\w+)\s*\(', content)  # Function calls
        undefined_potential = set(used_vars) - declared_vars - {'console', 'document', 'window', 'require', 'module', 'exports'}
        
        if undefined_potential:
            for var in list(undefined_potential)[:3]:  # Limit to 3 examples
                issues.append(f"Potential undefined variable: '{var}'")
        
        return {
            'syntax_issues': '\n'.join([f"• {issue}" for issue in issues]) or "• No obvious syntax issues detected",
            'quality_issues': '\n'.join([f"• {issue}" for issue in quality_issues]) or "• Code quality looks reasonable",
            'suggestions': '\n'.join([f"• {suggestion}" for suggestion in suggestions]) or "• Consider using a linter like ESLint",
            'language_specific': "• Check for missing semicolons\n• Use strict equality (===)\n• Verify variable declarations\n• Test in browser console for runtime errors"
        }

    def _detect_json_issues(self, content: str, file_path: str) -> Dict[str, str]:
        """Detect potential issues in JSON files."""
        try:
            import json
            json.loads(content)
            return {
                'syntax_issues': "• Valid JSON syntax ✓",
                'quality_issues': "• No structural issues detected",
                'suggestions': "• Consider schema validation for data integrity",
                'language_specific': "• JSON is well-formed\n• All quotes and brackets are properly matched"
            }
        except json.JSONDecodeError as e:
            return {
                'syntax_issues': f"• JSON Syntax Error: {str(e)}\n• Location: Line {getattr(e, 'lineno', 'unknown')}, Column {getattr(e, 'colno', 'unknown')}",
                'quality_issues': "• File cannot be parsed as valid JSON",
                'suggestions': "• Fix syntax error before proceeding\n• Use a JSON validator or formatter",
                'language_specific': "• Check for missing quotes around strings\n• Verify all brackets and braces are matched\n• Ensure no trailing commas\n• Confirm proper escaping of special characters"
            }

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
            content += "\n\n**Files to Test:**\n"
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
                content += """

**What would you like to focus on?**
• Performance optimization
• Code readability
• Better structure/organization
• Specific code smells you've noticed"""

        return {"content": content, "references": [f.get("path") for f in files]}

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension."""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.java': 'java',
            '.c': 'c',
            '.cpp': 'cpp',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sass': 'sass',
            '.json': 'json',
            '.xml': 'xml',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.md': 'markdown',
            '.sql': 'sql',
            '.sh': 'bash',
            '.bat': 'batch',
            '.ps1': 'powershell',
        }
        
        if '.' in file_path:
            extension = '.' + file_path.split('.')[-1].lower()
            return extension_map.get(extension, 'unknown')
        return 'unknown'

    def _analyze_file_content(self, content: str, language: str, file_path: str) -> Dict[str, str]:
        """Analyze file content and provide structured insights."""
        lines = content.split('\n')
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        
        analysis = {
            'overview': '',
            'structure': '',
            'components': '',
            'suggestions': ''
        }
        
        if language == 'python':
            analysis = self._analyze_python_content(content, lines, file_path)
        elif language in ['javascript', 'typescript']:
            analysis = self._analyze_javascript_content(content, lines, file_path)
        elif language == 'json':
            analysis = self._analyze_json_content(content, lines, file_path)
        elif language == 'markdown':
            analysis = self._analyze_markdown_content(content, lines, file_path)
        else:
            analysis = {
                'overview': f"This is a {language} file with {total_lines} total lines ({non_empty_lines} non-empty).",
                'structure': "Generic file structure analysis not available for this language.",
                'components': "File components detection not implemented for this language.",
                'suggestions': "Language-specific suggestions not available."
            }
        
        return analysis

    def _analyze_python_content(self, content: str, lines: List[str], file_path: str) -> Dict[str, str]:
        """Analyze Python file content."""
        import re
        
        # Count different elements
        imports = len([line for line in lines if re.match(r'^\s*(import|from)', line.strip())])
        functions = len(re.findall(r'^\s*def\s+(\w+)', content, re.MULTILINE))
        classes = len(re.findall(r'^\s*class\s+(\w+)', content, re.MULTILINE))
        comments = len([line for line in lines if line.strip().startswith('#')])
        docstrings = len(re.findall(r'""".*?"""', content, re.DOTALL))
        
        # Extract function and class names
        function_names = re.findall(r'^\s*def\s+(\w+)', content, re.MULTILINE)
        class_names = re.findall(r'^\s*class\s+(\w+)', content, re.MULTILINE)
        
        # Basic complexity analysis
        complexity_indicators = {
            'try_except': len(re.findall(r'\btry\s*:', content)),
            'if_statements': len(re.findall(r'\bif\s+', content)),
            'loops': len(re.findall(r'\b(for|while)\s+', content)),
            'decorators': len(re.findall(r'@\w+', content))
        }
        
        return {
            'overview': f"Python file with {len(lines)} lines, {imports} imports, {functions} functions, {classes} classes, {comments} comments.",
            'structure': f"• Imports: {imports}\n• Functions: {functions} ({', '.join(function_names[:5])}{'...' if len(function_names) > 5 else ''})\n• Classes: {classes} ({', '.join(class_names[:3])}{'...' if len(class_names) > 3 else ''})\n• Documentation: {docstrings} docstrings, {comments} comments",
            'components': f"• Control Flow: {complexity_indicators['if_statements']} conditionals, {complexity_indicators['loops']} loops\n• Error Handling: {complexity_indicators['try_except']} try/except blocks\n• Decorators: {complexity_indicators['decorators']} decorators found",
            'suggestions': f"• Documentation: {'Good' if docstrings > functions//2 else 'Could be improved'}\n• Error Handling: {'Present' if complexity_indicators['try_except'] > 0 else 'Consider adding'}\n• Code Organization: {'Well-structured' if classes > 0 or functions > 3 else 'Could benefit from more structure'}"
        }

    def _analyze_javascript_content(self, content: str, lines: List[str], file_path: str) -> Dict[str, str]:
        """Analyze JavaScript/TypeScript file content."""
        import re
        
        # Count different elements
        imports = len(re.findall(r'^\s*(import|require)', content, re.MULTILINE))
        functions = len(re.findall(r'(function\s+\w+|const\s+\w+\s*=\s*\(|let\s+\w+\s*=\s*\(|var\s+\w+\s*=\s*\()', content))
        arrow_functions = len(re.findall(r'=>', content))
        classes = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
        async_functions = len(re.findall(r'\basync\s+(function|\w+)', content))
        
        return {
            'overview': f"JavaScript file with {len(lines)} lines, {imports} imports, {functions} functions, {classes} classes.",
            'structure': f"• Imports/Requires: {imports}\n• Functions: {functions} total\n• Arrow Functions: {arrow_functions}\n• Classes: {classes}\n• Async Functions: {async_functions}",
            'components': f"• Modern JS Features: {'Yes' if arrow_functions > 0 or async_functions > 0 else 'Limited'}\n• Object-Oriented: {'Yes' if classes > 0 else 'Functional style'}\n• Asynchronous Code: {'Present' if async_functions > 0 else 'Synchronous'}",
            'suggestions': f"• Modern Syntax: {'Good use of ES6+' if arrow_functions > 0 else 'Consider modern syntax'}\n• Async Handling: {'Uses async/await' if async_functions > 0 else 'Check for Promise handling'}\n• Code Style: 'Review for consistency'"
        }

    def _analyze_json_content(self, content: str, lines: List[str], file_path: str) -> Dict[str, str]:
        """Analyze JSON file content."""
        try:
            import json
            data = json.loads(content)
            
            def count_nested_items(obj, depth=0):
                if isinstance(obj, dict):
                    return sum(count_nested_items(v, depth+1) for v in obj.values()) + len(obj)
                elif isinstance(obj, list):
                    return sum(count_nested_items(item, depth+1) for item in obj) + len(obj)
                else:
                    return 1
            
            total_items = count_nested_items(data)
            
            if isinstance(data, dict):
                top_keys = list(data.keys())[:5]
                structure_type = "Object"
            elif isinstance(data, list):
                top_keys = [f"Array[{len(data)}]"]
                structure_type = "Array"
            else:
                top_keys = [str(type(data).__name__)]
                structure_type = "Primitive"
                
            return {
                'overview': f"Valid JSON {structure_type.lower()} with {total_items} total items across all nesting levels.",
                'structure': f"• Type: {structure_type}\n• Top-level keys: {', '.join(map(str, top_keys))}\n• Nesting: {'Complex' if total_items > 20 else 'Simple'}",
                'components': f"• Structure: {structure_type}\n• Size: {len(content)} characters\n• Complexity: {'High' if total_items > 50 else 'Moderate' if total_items > 10 else 'Low'}",
                'suggestions': "• Syntax: Valid JSON format\n• Structure: Well-formed\n• Consider: Validation against schema if applicable"
            }
        except json.JSONDecodeError as e:
            return {
                'overview': f"JSON file with syntax error at line {getattr(e, 'lineno', 'unknown')}.",
                'structure': f"• Error: {str(e)}\n• Location: Line {getattr(e, 'lineno', 'unknown')}",
                'components': "• Status: Invalid JSON syntax\n• Needs: Syntax correction",
                'suggestions': f"• Fix: {str(e)}\n• Validate: Use JSON linter\n• Check: Quotes, commas, brackets"
            }

    def _analyze_markdown_content(self, content: str, lines: List[str], file_path: str) -> Dict[str, str]:
        """Analyze Markdown file content."""
        import re
        
        headers = len(re.findall(r'^#+\s+', content, re.MULTILINE))
        code_blocks = len(re.findall(r'```', content)) // 2
        links = len(re.findall(r'\[.*?\]\(.*?\)', content))
        images = len(re.findall(r'!\[.*?\]\(.*?\)', content))
        lists = len(re.findall(r'^\s*[-*+]\s+', content, re.MULTILINE))
        
        # Extract header hierarchy
        header_matches = re.findall(r'^(#+)\s+(.*)', content, re.MULTILINE)
        header_levels = [len(match[0]) for match in header_matches]
        
        return {
            'overview': f"Markdown document with {len(lines)} lines, {headers} headers, {code_blocks} code blocks.",
            'structure': f"• Headers: {headers} total (levels: {min(header_levels) if header_levels else 0}-{max(header_levels) if header_levels else 0})\n• Code blocks: {code_blocks}\n• Lists: {lists} items\n• Links: {links}, Images: {images}",
            'components': f"• Content types: Text, {'code' if code_blocks > 0 else 'no code'}, {'media' if images > 0 else 'no media'}\n• Navigation: {'Well-structured' if headers > 2 else 'Simple'}\n• Interactivity: {links} external references",
            'suggestions': f"• Structure: {'Good hierarchy' if len(set(header_levels)) > 1 else 'Consider header levels'}\n• Content: {'Rich content' if code_blocks + images > 2 else 'Text-focused'}\n• Documentation: {'Complete' if headers > 3 else 'Consider more sections'}"
        }

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
