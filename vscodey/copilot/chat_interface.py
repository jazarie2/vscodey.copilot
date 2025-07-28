"""
Chat interface for VSCodey Copilot - Real GitHub Copilot integration framework.
"""

import time
import os
import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
import subprocess
import platform
import requests
from urllib.parse import urlencode

from .config import CLIConfig


class GitHubAuth:
    """GitHub authentication framework - real OAuth integration based on ori/clipilot/github_auth.py"""
    
    # GitHub OAuth endpoints
    DEVICE_CODE_URL = "https://github.com/login/device/code"
    ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_URL = "https://api.github.com/user"
    COPILOT_TOKEN_URL = "https://api.github.com/copilot_internal/v2/token"
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        # Default client ID for CLI applications (GitHub CLI)
        self.client_id = "178c6fc778ccc68e1d6a"  # GitHub CLI client ID
    
    def authenticate(self) -> Optional[str]:
        """Perform GitHub authentication using device flow."""
        try:
            if self.verbose:
                print("🔑 Starting GitHub authentication...")
            
            # Step 1: Request device code
            device_info = self._request_device_code()
            if not device_info:
                return None
            
            # Step 2: Show user code and open browser
            self._display_user_code(device_info)
            
            # Step 3: Poll for access token
            access_token = self._poll_for_token(device_info)
            
            if access_token and self.verify_token(access_token):
                if self.verbose:
                    print("✓ GitHub authentication successful!")
                return access_token
            else:
                if self.verbose:
                    print("✗ GitHub authentication failed or timed out.")
                return None
                
        except Exception as e:
            if self.verbose:
                print(f"Authentication error: {e}")
            return None
    
    def _request_device_code(self) -> Optional[Dict[str, Any]]:
        """Request device code from GitHub."""
        data = {
            "client_id": self.client_id,
            "scope": "read:user user:email"
        }
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "VSCodey-Copilot/1.0"
        }
        
        try:
            response = requests.post(
                self.DEVICE_CODE_URL,
                data=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                if self.verbose:
                    print(f"Failed to request device code: {response.status_code}")
                return None
        except Exception as e:
            if self.verbose:
                print(f"Device code request error: {e}")
            return None
    
    def _display_user_code(self, device_info: Dict[str, Any]):
        """Display user code and verification URL."""
        print(f"\n🔑 GitHub Authentication Required")
        print(f"Please visit: {device_info['verification_uri']}")
        print(f"Enter code: {device_info['user_code']}")
        print(f"This code expires in {device_info.get('expires_in', 900)} seconds.")
        
        # Try to open browser automatically
        try:
            import webbrowser
            webbrowser.open(device_info['verification_uri'])
            print("Browser opened automatically.")
        except:
            pass
    
    def _poll_for_token(self, device_info: Dict[str, Any]) -> Optional[str]:
        """Poll for access token."""
        interval = device_info.get('interval', 5)
        expires_in = device_info.get('expires_in', 900)
        device_code = device_info['device_code']
        
        start_time = time.time()
        
        while time.time() - start_time < expires_in:
            try:
                data = {
                    "client_id": self.client_id,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                }
                
                headers = {
                    "Accept": "application/json",
                    "User-Agent": "VSCodey-Copilot/1.0"
                }
                
                response = requests.post(
                    self.ACCESS_TOKEN_URL,
                    data=data,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'access_token' in result:
                        return result['access_token']
                
                # Check for specific error codes
                if response.status_code == 400:
                    error_data = response.json()
                    error = error_data.get('error', '')
                    
                    if error == 'authorization_pending':
                        # Still waiting for user authorization
                        time.sleep(interval)
                        continue
                    elif error == 'slow_down':
                        # Increase polling interval
                        interval += 5
                        time.sleep(interval)
                        continue
                    elif error in ('expired_token', 'access_denied'):
                        # Terminal errors
                        if self.verbose:
                            print(f"Authentication {error}")
                        return None
                
                time.sleep(interval)
                
            except Exception as e:
                if self.verbose:
                    print(f"Polling error: {e}")
                time.sleep(interval)
        
        return None
    
    def verify_token(self, token: str) -> bool:
        """Verify GitHub token validity."""
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "User-Agent": "VSCodey-Copilot/1.0"
            }
            
            response = requests.get(self.USER_URL, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False


class CopilotTokenManager:
    """Manages Copilot token exchange from GitHub token - based on ori token manager"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.copilot_token = None
        self.github_token = None
    
    def get_copilot_token(self, github_token: str) -> Optional[str]:
        """Exchange GitHub token for Copilot token."""
        if self.copilot_token and self._is_token_valid():
            return self.copilot_token
        
        try:
            # Get Copilot token from GitHub token
            # Note: This endpoint is internal and not publicly accessible
            # Based on VS Code extension analysis from ori/ folder
            headers = {
                "Authorization": f"token {github_token}",
                "X-GitHub-Api-Version": "2025-04-01",
                "Accept": "application/json",
                "User-Agent": "copilot-chat/0.30.0",
                "Editor-Version": "vscode/1.95.0",
                "Editor-Plugin-Version": "copilot-chat/0.30.0"
            }
            
            response = requests.post(
                "https://api.github.com/copilot_internal/v2/token",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                token_info = response.json()
                self.copilot_token = token_info.get('token')
                self.token_expires_at = time.time() + token_info.get('expires_in', 3600)
                self.github_token = github_token
                
                if self.verbose:
                    print("✓ Copilot token obtained successfully")
                
                return self.copilot_token
            elif response.status_code == 401:
                if self.verbose:
                    print("✗ GitHub token invalid for Copilot access")
                return None
            elif response.status_code == 403:
                if self.verbose:
                    error_data = response.json()
                    if "rate limit" in error_data.get('message', '').lower():
                        print("✗ Rate limit exceeded")
                    else:
                        print("✗ No Copilot access - subscription required")
                return None
            else:
                if self.verbose:
                    print(f"✗ Failed to get Copilot token: {response.status_code}")
                return None
                
        except Exception as e:
            if self.verbose:
                print(f"Copilot token error: {e}")
            return None
    
    def _is_token_valid(self) -> bool:
        """Check if current Copilot token is still valid."""
        if not self.copilot_token:
            return False
        
        # Check expiration (with 5 minute buffer)
        return hasattr(self, 'token_expires_at') and time.time() < (self.token_expires_at - 300)


class WorkspaceContextManager:
    """Enhanced workspace context management with real file analysis."""
    
    def __init__(self, workspace_path: Path, verbose: bool = False):
        self.workspace_path = workspace_path
        self.verbose = verbose
    
    def get_workspace_context(self) -> Dict[str, Any]:
        """Get comprehensive workspace context with real data."""
        try:
            context = {
                "path": str(self.workspace_path),
                "exists": self.workspace_path.exists(),
                "is_git_repo": (self.workspace_path / ".git").exists(),
                "project_info": self._get_project_info(),
                "git_info": self._get_git_info() if (self.workspace_path / ".git").exists() else None,
                "file_structure": self._get_basic_structure()
            }
            return context
        except Exception as e:
            return {"error": str(e)}
    
    def _get_project_info(self) -> Dict[str, Any]:
        """Detect project type and configuration."""
        project_info = {"type": "unknown", "configs": []}
        
        # Check for common project files
        project_files = {
            "package.json": "nodejs",
            "requirements.txt": "python", 
            "pyproject.toml": "python",
            "Cargo.toml": "rust",
            "go.mod": "go",
            "pom.xml": "java"
        }
        
        for file_name, project_type in project_files.items():
            if (self.workspace_path / file_name).exists():
                project_info["type"] = project_type
                project_info["configs"].append(file_name)
        
        return project_info
    
    def _get_git_info(self) -> Dict[str, Any]:
        """Get real Git repository information."""
        try:
            # Get current branch
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            git_info = {}
            if result.returncode == 0:
                git_info["branch"] = result.stdout.strip()
            
            # Get status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                git_info["has_changes"] = bool(result.stdout.strip())
            
            return git_info
        except Exception:
            return {"error": "Git information unavailable"}
    
    def _get_basic_structure(self) -> Dict[str, Any]:
        """Get basic directory structure."""
        try:
            items = list(self.workspace_path.iterdir())
            return {
                "total_items": len(items),
                "directories": len([item for item in items if item.is_dir()]),
                "files": len([item for item in items if item.is_file()])
            }
        except Exception:
            return {"error": "Structure analysis failed"}


class GitHubCopilotAPIClient:
    """Real GitHub Copilot API client based on ori extension architecture"""
    
    # API endpoints based on ori extension
    CHAT_COMPLETIONS_URL = "https://api.githubcopilot.com/chat/completions"
    
    def __init__(self, copilot_token: str, verbose: bool = False):
        self.copilot_token = copilot_token
        self.verbose = verbose
        self.session = requests.Session()
        
        # Set default headers based on ori extension
        self.session.headers.update({
            "Authorization": f"Bearer {copilot_token}",
            "Accept": "application/json",
            "User-Agent": "GitHubCopilotChat/1.0",
            "X-GitHub-Api-Version": "2025-04-01",
            "Content-Type": "application/json"
        })
    
    def send_chat_request(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.1,
        max_tokens: int = 4096,
        stream: bool = False,
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Send chat completion request to GitHub Copilot API."""
        try:
            # Prepare request body based on ori extension structure
            request_body = {
                "messages": messages,
                "model": model,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": stream
            }
            
            if tools:
                request_body["tools"] = tools
            
            # Add request ID for tracking
            request_id = str(uuid.uuid4())
            headers = {
                "X-Request-Id": request_id,
                "X-Interaction-Id": str(uuid.uuid4())
            }
            
            if self.verbose:
                print(f"🚀 Sending chat request to GitHub Copilot API")
                print(f"   Model: {model}")
                print(f"   Messages: {len(messages)}")
                print(f"   Request ID: {request_id}")
            
            response = self.session.post(
                self.CHAT_COMPLETIONS_URL,
                json=request_body,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if self.verbose:
                    print("✓ Chat completion successful")
                
                return {
                    "success": True,
                    "content": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "model": result.get("model", model),
                    "usage": result.get("usage", {}),
                    "request_id": request_id
                }
            
            elif response.status_code == 401:
                return {"success": False, "error": "Unauthorized - invalid Copilot token"}
            elif response.status_code == 403:
                return {"success": False, "error": "Forbidden - no Copilot access or quota exceeded"}
            elif response.status_code == 429:
                return {"success": False, "error": "Rate limit exceeded"}
            else:
                error_text = response.text
                if self.verbose:
                    print(f"✗ API request failed: {response.status_code}")
                    print(f"   Error: {error_text}")
                
                return {
                    "success": False, 
                    "error": f"API request failed: {response.status_code}",
                    "details": error_text
                }
                
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Connection error - check internet connection"}
        except Exception as e:
            if self.verbose:
                print(f"✗ Unexpected error: {e}")
            return {"success": False, "error": f"Unexpected error: {str(e)}"}


class ChatInterface:
    """Interface for chat functionality with real GitHub Copilot API integration."""

    def __init__(self, config: CLIConfig, verbose: bool = False):
        """Initialize chat interface.

        Args:
            config: Configuration object
            verbose: Enable verbose logging
        """
        self.config = config
        self.verbose = verbose
        self.session_history = []
        self.github_auth = GitHubAuth(verbose=verbose)
        self.token_manager = CopilotTokenManager(verbose=verbose)
        self.github_token = None
        self.api_client = None

    def authenticate(self) -> bool:
        """Authenticate with GitHub and get Copilot token."""
        if self.verbose:
            print("🔑 Starting GitHub Copilot authentication process...")
        
        # Step 1: Get GitHub token
        self.github_token = self.github_auth.authenticate()
        if not self.github_token:
            if self.verbose:
                print("✗ GitHub authentication failed")
            return False
        
        # Step 2: Exchange for Copilot token
        copilot_token = self.token_manager.get_copilot_token(self.github_token)
        if not copilot_token:
            if self.verbose:
                print("✗ Failed to get Copilot token - check subscription")
            return False
        
        # Step 3: Initialize API client
        self.api_client = GitHubCopilotAPIClient(copilot_token, verbose=self.verbose)
        
        if self.verbose:
            print("✅ GitHub Copilot authentication complete!")
        
        return True

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
        try:
            # Check if authenticated
            if not self.api_client:
                return {
                    "error": "Not authenticated. Please run authenticate() first.",
                    "available": False
                }

            # Prepare the request with real context analysis
            chat_request = self._prepare_request(message, context, agent, model)

            if self.verbose:
                used_model = chat_request.get("model", "default")
                print(f"Sending chat request using model: {used_model}")
                print(f"Request has {len(chat_request.get('context', {}).get('files', []))} files...")

            # Call the real GitHub Copilot API
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
            return {"error": f"Failed to send message: {str(e)}", "available": False}

    def _prepare_request(
        self,
        message: str,
        context: Dict[str, Any] = None,
        agent: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Prepare the chat request with enhanced context analysis.

        Args:
            message: The chat message
            context: Context information
            agent: Specific agent to use
            model: Specific model to use

        Returns:
            Prepared request dictionary with real workspace analysis
        """
        chat_config = self.config.get_chat_config()

        # Determine which model to use
        selected_model = model if model else self.config.get_default_model()
        model_info = self.config.get_model_info(selected_model)

        if not model_info:
            # Fallback to default if model not found
            selected_model = self.config.get_default_model()
            model_info = self.config.get_model_info(selected_model)

        # Get real workspace context if available
        workspace_context = {}
        if context and context.get("workspace"):
            workspace_manager = WorkspaceContextManager(
                Path(context["workspace"]), 
                verbose=self.verbose
            )
            workspace_context = workspace_manager.get_workspace_context()

        request = {
            "message": message,
            "agent": agent or chat_config.get("default_agent", "workspace"),
            "model": selected_model,
            "model_info": model_info,
            "context": context or {},
            "workspace_context": workspace_context,
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
        """Call the real GitHub Copilot API.

        Args:
            request: The chat request

        Returns:
            API response with real data analysis
        """
        if not self.api_client:
            return {
                "error": "API client not initialized. Authentication required.",
                "available": False
            }

        message = request.get("message", "")
        agent = request.get("agent", "workspace")
        model = request.get("model", "gpt-4o-mini")
        context = request.get("context", {})
        workspace_context = request.get("workspace_context", {})
        config = request.get("config", {})
        
        # Prepare messages for the API
        messages = self._build_messages(message, agent, context, workspace_context)
        
        # Make the real API call
        response = self.api_client.send_chat_request(
            messages=messages,
            model=model,
            temperature=config.get("temperature", 0.1),
            max_tokens=config.get("max_tokens", 4096)
        )
        
        if response.get("success"):
            return {
                "content": response.get("content", ""),
                "references": self._extract_references(context),
                "metadata": {
                    "model": response.get("model", model),
                    "usage": response.get("usage", {}),
                    "request_id": response.get("request_id"),
                    "agent": agent,
                    "real_api": True,
                    "available": True
                }
            }
        else:
            return {
                "error": response.get("error", "Unknown API error"),
                "details": response.get("details"),
                "available": False
            }

    def _build_messages(
        self, 
        message: str, 
        agent: str, 
        context: Dict[str, Any], 
        workspace_context: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """Build messages array for the API based on agent and context."""
        messages = []
        
        # System message based on agent
        system_prompts = {
            "workspace": """You are GitHub Copilot, an AI coding assistant. You help developers understand, write, and improve code. 
You have access to the current workspace context and can provide insights about the codebase, suggest improvements, and answer coding questions.
Be helpful, accurate, and concise in your responses.""",
            
            "terminal": """You are GitHub Copilot in terminal mode. You help with command-line operations, shell commands, and system administration tasks.
You can analyze system information and suggest appropriate commands for the user's platform.
Be practical and provide working command examples.""",
            
            "explain": """You are GitHub Copilot in explanation mode. You excel at explaining code, algorithms, and programming concepts.
Break down complex topics into understandable parts and provide clear, educational explanations.
Use examples and analogies when helpful."""
        }
        
        system_message = system_prompts.get(agent, system_prompts["workspace"])
        
        # Add workspace context to system message if available
        if workspace_context:
            context_info = []
            if workspace_context.get("project_info", {}).get("type") != "unknown":
                context_info.append(f"Project type: {workspace_context['project_info']['type']}")
            
            if workspace_context.get("git_info", {}).get("branch"):
                context_info.append(f"Git branch: {workspace_context['git_info']['branch']}")
            
            if context_info:
                system_message += f"\n\nCurrent workspace context: {', '.join(context_info)}"
        
        messages.append({
            "role": "system",
            "content": system_message
        })
        
        # Add file context if provided
        files = context.get("files", [])
        if files:
            file_context = "Files in context:\n"
            for file_info in files[:3]:  # Limit to first 3 files
                file_path = file_info.get("path", "unknown")
                content = file_info.get("content", "")
                preview = content[:1000] + "..." if len(content) > 1000 else content
                file_context += f"\n--- {file_path} ---\n{preview}\n"
            
            messages.append({
                "role": "user", 
                "content": file_context
            })
        
        # Add the user's message
        messages.append({
            "role": "user",
            "content": message
        })
        
        return messages

    def _extract_references(self, context: Dict[str, Any]) -> List[str]:
        """Extract file references from context."""
        files = context.get("files", [])
        return [f["path"] for f in files if "path" in f]

    def _detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension."""
        suffix = file_path.suffix.lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp',
            '.c': 'c',
            '.h': 'c', '.hpp': 'cpp',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.md': 'markdown',
            '.json': 'json',
            '.yaml': 'yaml', '.yml': 'yaml',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css'
        }
        
        return language_map.get(suffix)

    def get_session_history(self) -> List[Dict[str, Any]]:
        """Get the current session history.

        Returns:
            List of session messages
        """
        return self.session_history.copy()

    def clear_session_history(self):
        """Clear the session history."""
        self.session_history.clear()

    def is_authenticated(self) -> bool:
        """Check if properly authenticated with GitHub Copilot."""
        return self.api_client is not None
    
    def get_authentication_status(self) -> Dict[str, Any]:
        """Get detailed authentication status."""
        return {
            "github_token": self.github_token is not None,
            "copilot_token": self.token_manager.copilot_token is not None,
            "api_client": self.api_client is not None,
            "authenticated": self.is_authenticated()
        }
