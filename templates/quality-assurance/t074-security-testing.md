## Scope and test accounts
- Confirm the scope and obtain written approval for security testing (If applicable)
- List the roles, permissions, and entry points to cover
- Create an account for every role, including one with no permissions
## Authentication
-! Test the password rules and the lockout after repeated failed attempts
- Reuse a password reset link and see whether it works a second time
- Open an expired reset link and check the result
- Go through multi-factor authentication when it is enabled for the account
- Submit a non-existent email at login and read what the error reveals
## Session management
- Compare the session token before and after login
- Log out and replay the previous session token
- Leave a session idle past the timeout and see whether it expires
- Inspect cookies for the Secure, HttpOnly, and SameSite attributes
## Access control
-! Change the record ID in the URL and confirm access is denied
-! Open restricted pages and endpoints as a user without the role
- Call admin actions from a regular account through the UI and the API
- Use a file download link from an account without permission to that file
## Input validation
- Submit SQL syntax in text inputs and see how it is handled
- Submit script tags and check whether the output is escaped
- Upload a forbidden file type, an oversized file, and an executable
- Pass an external destination to a redirect parameter
## Data protection
- Open the main flows over HTTP and watch for the redirect to HTTPS
- Search logs and URLs of the main flows for sensitive data
- Make sure personal data is masked in the interface where required
## Configuration and dependencies
- Remove default and test accounts from the environment
- Confirm debug mode and directory listing are disabled
- Run a dependency scan and review the reported vulnerabilities
- Inspect responses for the required security headers
## Reporting
- Record each finding with severity, steps, and the affected area
-! Make sure all critical and high-priority findings are fixed and retested
