import hashlib
import hmac
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple

class AuthManager:
    """Handles user authentication and session management"""
    
    def __init__(self):
        self.users_db = {
            "admin": self._hash_password("admin123"),
            "user1": self._hash_password("password123"),
            "analyst": self._hash_password("analyst456"),
            "manager": self._hash_password("manager789")
        }
        
        self.active_sessions = {}
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, username: str, password: str) -> bool:
        """Verify if username and password match"""
        if username not in self.users_db:
            return False
        
        password_hash = self._hash_password(password)
        return hmac.compare_digest(
            password_hash, 
            self.users_db[username]
        )
    
    def create_session(self, username: str) -> str:
        """Create a new session for user"""
        session_token = hashlib.sha256(
            f"{username}{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        self.active_sessions[session_token] = {
            "username": username,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        
        return session_token
    
    def validate_session(self, token: str) -> Optional[str]:
        """Validate session token and return username"""
        if token not in self.active_sessions:
            return None
        
        session = self.active_sessions[token]
        
        # Check if session expired (24 hours)
        if datetime.now() - session["created_at"] > timedelta(hours=24):
            del self.active_sessions[token]
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now()
        return session["username"]
    
    def logout(self, token: str) -> bool:
        """Logout user by invalidating session token"""
        if token in self.active_sessions:
            del self.active_sessions[token]
            return True
        return False

# Global auth manager
auth_manager = AuthManager()