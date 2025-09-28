# Roblox Authentication Checker

A Python script for checking Roblox account credentials without any stimulation or automated actions.

## ⚠️ Disclaimer

This script is for **educational purposes only**. Use responsibly and respect Roblox's Terms of Service. The author is not responsible for any misuse of this tool.

## Features

- ✅ Proper Roblox API headers and authentication payloads
- ✅ Email:password credential checking
- ✅ CSRF token handling
- ✅ Rate limiting protection
- ✅ Error handling and logging
- ✅ Interactive and file-based input modes
- ✅ No stimulation or automated actions

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode
```bash
python roblox_auth_checker.py
```

### File Mode
Create a text file with credentials in `email:password` format (one per line):
```
user1@example.com:password123
user2@example.com:mypassword
```

Then run:
```bash
python roblox_auth_checker.py credentials.txt
```

## Output

The script will show:
- ✅ **VALID** - Account exists and credentials are correct
- ❌ **INVALID** - Account doesn't exist or credentials are wrong

For valid accounts, it will also display:
- User ID
- Username
- Display Name

## Rate Limiting

The script includes a 1-second delay between requests to avoid rate limiting and respect Roblox's servers.

## Security Notes

- This script only performs authentication checks
- No automated actions or stimulation
- Respects rate limits
- Uses proper headers to mimic legitimate browser requests
- Includes CSRF token handling for security compliance