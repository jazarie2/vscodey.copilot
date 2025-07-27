"""
GitHub OAuth authentication for CLI Pilot.
Handles device flow authentication to get GitHub tokens.
"""

import json
import time
import webbrowser
from typing import Optional, Dict, Any
import requests
from urllib.parse import urlencode


class GitHubAuth:
    """Handles GitHub OAuth device flow authentication."""
    
    # GitHub OAuth endpoints
    DEVICE_CODE_URL = "https://github.com/login/device/code"
    ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    USER_URL = "https://api.github.com/user"
    
    def __init__(self, client_id: str = None, verbose: bool = False):
        """Initialize GitHub authentication.
        
        Args:
            client_id: GitHub OAuth app client ID
            verbose: Enable verbose logging
        """
        # Default client ID for CLI applications (GitHub CLI)
        # In production, you should use your own client ID
        self.client_id = client_id or "178c6fc778ccc68e1d6a"  # GitHub CLI client ID
        self.verbose = verbose
        
    def authenticate(self) -> Optional[str]:
        """Perform device flow authentication.
        
        Returns:
            Access token if successful, None otherwise
        """
        try:
            print("Starting GitHub authentication...")
            
            # Step 1: Request device code
            device_info = self._request_device_code()
            if not device_info:
                return None
            
            # Step 2: Show user code and open browser
            self._display_user_code(device_info)
            
            # Step 3: Poll for access token
            access_token = self._poll_for_token(device_info)
            
            if access_token:
                print("✓ Authentication successful!")
                return access_token
            else:
                print("✗ Authentication failed or timed out.")
                return None
                
        except Exception as e:
            print(f"Authentication error: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
            return None
    
    def _request_device_code(self) -> Optional[Dict[str, Any]]:
        """Request device code from GitHub.
        
        Returns:
            Device code information or None
        """
        data = {
            "client_id": self.client_id,
            "scope": "read:user user:email"  # Basic scopes for user info
        }
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "CLI-Pilot/1.0"
        }
        
        response = requests.post(
            self.DEVICE_CODE_URL,
            data=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to request device code: {response.status_code}")
            if self.verbose:
                print(f"Response: {response.text}")
            return None
    
    def _display_user_code(self, device_info: Dict[str, Any]):
        """Display user code and verification URL.
        
        Args:
            device_info: Device code information from GitHub
        """
        user_code = device_info.get("user_code")
        verification_uri = device_info.get("verification_uri")
        
        print("\n" + "="*60)
        print("GitHub Authentication Required")
        print("="*60)
        print(f"1. Open this URL in your browser: {verification_uri}")
        print(f"2. Enter this code: {user_code}")
        print("="*60)
        
        try:
            # Try to open browser automatically
            webbrowser.open(verification_uri)
            print("✓ Browser opened automatically")
        except Exception:
            print("Note: Could not open browser automatically")
        
        input("\nPress Enter after completing authentication in browser...")
    
    def _poll_for_token(self, device_info: Dict[str, Any]) -> Optional[str]:
        """Poll GitHub for access token.
        
        Args:
            device_info: Device code information from GitHub
            
        Returns:
            Access token if successful, None otherwise
        """
        device_code = device_info.get("device_code")
        interval = device_info.get("interval", 5)
        expires_in = device_info.get("expires_in", 900)
        
        data = {
            "client_id": self.client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }
        
        headers = {
            "Accept": "application/json",
            "User-Agent": "CLI-Pilot/1.0"
        }
        
        start_time = time.time()
        
        while time.time() - start_time < expires_in:
            if self.verbose:
                print("Polling for token...")
            
            response = requests.post(
                self.ACCESS_TOKEN_URL,
                data=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if "access_token" in result:
                    return result["access_token"]
                elif result.get("error") == "authorization_pending":
                    # Still waiting for user to authorize
                    time.sleep(interval)
                    continue
                elif result.get("error") == "slow_down":
                    # Increase polling interval
                    interval += 5
                    time.sleep(interval)
                    continue
                else:
                    print(f"Authentication error: {result.get('error_description', 'Unknown error')}")
                    return None
            else:
                print(f"Failed to poll for token: {response.status_code}")
                if self.verbose:
                    print(f"Response: {response.text}")
                return None
        
        print("Authentication timed out")
        return None
    
    def verify_token(self, token: str) -> bool:
        """Verify that a token is valid.
        
        Args:
            token: GitHub access token
            
        Returns:
            True if token is valid, False otherwise
        """
        headers = {
            "Authorization": f"token {token}",
            "User-Agent": "CLI-Pilot/1.0"
        }
        
        try:
            response = requests.get(self.USER_URL, headers=headers, timeout=30)
            return response.status_code == 200
        except Exception as e:
            if self.verbose:
                print(f"Token verification error: {e}")
            return False
    
    def get_user_info(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user information using the token.
        
        Args:
            token: GitHub access token
            
        Returns:
            User information or None
        """
        headers = {
            "Authorization": f"token {token}",
            "User-Agent": "CLI-Pilot/1.0"
        }
        
        try:
            response = requests.get(self.USER_URL, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            if self.verbose:
                print(f"Failed to get user info: {e}")
            return None


def perform_github_login(verbose: bool = False) -> Optional[str]:
    """Convenience function to perform GitHub login.
    
    Args:
        verbose: Enable verbose logging
        
    Returns:
        Access token if successful, None otherwise
    """
    auth = GitHubAuth(verbose=verbose)
    return auth.authenticate()


def verify_github_token(token: str, verbose: bool = False) -> bool:
    """Convenience function to verify GitHub token.
    
    Args:
        token: GitHub access token
        verbose: Enable verbose logging
        
    Returns:
        True if token is valid, False otherwise
    """
    auth = GitHubAuth(verbose=verbose)
    return auth.verify_token(token)