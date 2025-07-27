"""
Workspace context management for CLI Pilot.
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import fnmatch
import mimetypes


class WorkspaceContextManager:
    """Manages workspace context for chat requests."""
    
    def __init__(self, workspace_path: Path, verbose: bool = False):
        """Initialize workspace context manager.
        
        Args:
            workspace_path: Path to workspace directory
            verbose: Enable verbose logging
        """
        self.workspace_path = workspace_path
        self.verbose = verbose
        
        # Default file patterns
        self.include_patterns = [
            "*.py", "*.js", "*.ts", "*.jsx", "*.tsx", "*.java", "*.cpp", "*.c", "*.h",
            "*.cs", "*.php", "*.rb", "*.go", "*.rs", "*.swift", "*.kt", "*.scala",
            "*.md", "*.txt", "*.json", "*.yaml", "*.yml", "*.xml", "*.html", "*.css"
        ]
        
        self.exclude_patterns = [
            "node_modules/**", ".git/**", "__pycache__/**", "*.pyc", ".vscode/**",
            ".idea/**", "build/**", "dist/**", "target/**", ".DS_Store",
            "*.log", "*.tmp", "*.temp", ".env", ".env.*"
        ]
        
        self.max_file_size = 1024 * 1024  # 1MB
    
    def get_workspace_context(self) -> Dict[str, Any]:
        """Get comprehensive workspace context.
        
        Returns:
            Dictionary containing workspace information
        """
        context = {
            "path": str(self.workspace_path),
            "structure": self._get_directory_structure(),
            "files": self._get_relevant_files(),
            "git_info": self._get_git_info(),
            "project_info": self._get_project_info(),
            "stats": {}
        }
        
        # Calculate stats
        context["stats"] = {
            "total_files": len(context["files"]),
            "total_size": sum(f.get("size", 0) for f in context["files"]),
            "file_types": self._get_file_type_stats(context["files"])
        }
        
        if self.verbose:
            print(f"Gathered context for {len(context['files'])} files")
        
        return context
    
    def _get_directory_structure(self, max_depth: int = 3) -> Dict[str, Any]:
        """Get directory structure.
        
        Args:
            max_depth: Maximum depth to traverse
            
        Returns:
            Directory structure as nested dictionary
        """
        def build_tree(path: Path, current_depth: int = 0) -> Dict[str, Any]:
            if current_depth >= max_depth:
                return {"type": "directory", "truncated": True}
            
            tree = {"type": "directory", "children": {}}
            
            try:
                for item in sorted(path.iterdir()):
                    if self._should_exclude_path(item):
                        continue
                    
                    if item.is_dir():
                        tree["children"][item.name] = build_tree(item, current_depth + 1)
                    else:
                        tree["children"][item.name] = {
                            "type": "file",
                            "size": item.stat().st_size if item.exists() else 0
                        }
            except (PermissionError, OSError):
                tree["error"] = "Permission denied"
            
            return tree
        
        return build_tree(self.workspace_path)
    
    def _get_relevant_files(self, max_files: int = 50) -> List[Dict[str, Any]]:
        """Get relevant files from workspace.
        
        Args:
            max_files: Maximum number of files to include
            
        Returns:
            List of file information dictionaries
        """
        files = []
        
        for file_path in self._find_files():
            if len(files) >= max_files:
                break
            
            try:
                stat = file_path.stat()
                if stat.st_size > self.max_file_size:
                    continue
                
                # Try to read file content
                content = None
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except (UnicodeDecodeError, IOError):
                    # Binary file or read error
                    continue
                
                relative_path = file_path.relative_to(self.workspace_path)
                files.append({
                    "path": str(relative_path),
                    "full_path": str(file_path),
                    "size": stat.st_size,
                    "content": content,
                    "language": self._detect_language(file_path),
                    "modified_time": stat.st_mtime
                })
                
            except (OSError, ValueError):
                continue
        
        # Sort by relevance (modify time, then size)
        files.sort(key=lambda f: (-f["modified_time"], f["size"]))
        
        return files
    
    def _find_files(self):
        """Find files matching include patterns and not matching exclude patterns."""
        for root, dirs, files in os.walk(self.workspace_path):
            # Filter directories
            dirs[:] = [d for d in dirs if not self._should_exclude_path(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                if self._should_include_file(file_path):
                    yield file_path
    
    def _should_include_file(self, file_path: Path) -> bool:
        """Check if file should be included.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file should be included
        """
        if self._should_exclude_path(file_path):
            return False
        
        # Check include patterns
        relative_path = file_path.relative_to(self.workspace_path)
        for pattern in self.include_patterns:
            if fnmatch.fnmatch(file_path.name, pattern):
                return True
        
        return False
    
    def _should_exclude_path(self, path: Path) -> bool:
        """Check if path should be excluded.
        
        Args:
            path: Path to check
            
        Returns:
            True if path should be excluded
        """
        try:
            relative_path = path.relative_to(self.workspace_path)
        except ValueError:
            return True
        
        path_str = str(relative_path)
        
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
                return True
        
        return False
    
    def _detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension.
        
        Args:
            file_path: Path to file
            
        Returns:
            Language name or None
        """
        suffix = file_path.suffix.lower()
        
        language_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
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
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css'
        }
        
        return language_map.get(suffix)
    
    def _get_git_info(self) -> Dict[str, Any]:
        """Get Git repository information.
        
        Returns:
            Git information dictionary
        """
        git_info = {"available": False}
        
        try:
            # Check if this is a git repository
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                git_info["available"] = True
                
                # Get current branch
                result = subprocess.run(
                    ["git", "branch", "--show-current"],
                    cwd=self.workspace_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    git_info["branch"] = result.stdout.strip()
                
                # Get remote URL
                result = subprocess.run(
                    ["git", "remote", "get-url", "origin"],
                    cwd=self.workspace_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    git_info["remote"] = result.stdout.strip()
                
                # Get recent commits
                result = subprocess.run(
                    ["git", "log", "--oneline", "-n", "5"],
                    cwd=self.workspace_path,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    git_info["recent_commits"] = result.stdout.strip().split('\n')
        
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return git_info
    
    def _get_project_info(self) -> Dict[str, Any]:
        """Get project-specific information.
        
        Returns:
            Project information dictionary
        """
        project_info = {"type": "unknown", "files": {}}
        
        # Check for common project files
        project_files = [
            "package.json", "requirements.txt", "Pipfile", "pyproject.toml",
            "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "CMakeLists.txt",
            "Makefile", "composer.json", "Gemfile"
        ]
        
        for file_name in project_files:
            file_path = self.workspace_path / file_name
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    project_info["files"][file_name] = content[:1000]  # Limit size
                    
                    # Detect project type
                    if file_name == "package.json":
                        project_info["type"] = "nodejs"
                    elif file_name in ["requirements.txt", "Pipfile", "pyproject.toml"]:
                        project_info["type"] = "python"
                    elif file_name == "Cargo.toml":
                        project_info["type"] = "rust"
                    elif file_name == "go.mod":
                        project_info["type"] = "go"
                    elif file_name in ["pom.xml", "build.gradle"]:
                        project_info["type"] = "java"
                        
                except (IOError, UnicodeDecodeError):
                    continue
        
        return project_info
    
    def _get_file_type_stats(self, files: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get statistics about file types.
        
        Args:
            files: List of file information
            
        Returns:
            Dictionary mapping file extensions to counts
        """
        stats = {}
        
        for file_info in files:
            path = Path(file_info["path"])
            extension = path.suffix.lower() or "no_extension"
            stats[extension] = stats.get(extension, 0) + 1
        
        return stats