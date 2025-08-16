"""
Core storage and memory management for PyFastMem
"""
import os
import json
import uuid
import base64
import hashlib
import secrets
from pathlib import Path
from typing import Dict, Any, Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Storage:
    """Storage configuration for memory management"""
    
    def __init__(self, name: str, path: str):
        """
        Initialize a new storage configuration
        
        Args:
            name: Name of the storage
            path: Path where memory files will be stored
        """
        self.name = name
        self.path = os.path.abspath(os.path.join(path, name))
        self._ensure_storage_path()
        self._password: Optional[bytes] = None
        self._fernet: Optional[Fernet] = None
        
    def _ensure_storage_path(self) -> None:
        """Ensure the storage directory exists"""
        os.makedirs(self.path, exist_ok=True)
    
    def set_password(self, password: str) -> None:
        """Set the password for encryption"""
        salt = secrets.token_bytes(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self._fernet = Fernet(key)
        
        # Save salt for later use
        with open(os.path.join(self.path, '.salt'), 'wb') as f:
            f.write(salt)
    
    def _load_salt(self) -> bytes:
        """Load the salt from storage"""
        salt_path = os.path.join(self.path, '.salt')
        if not os.path.exists(salt_path):
            raise ValueError("No password set for this storage")
        with open(salt_path, 'rb') as f:
            return f.read()
    
    def unlock(self, password: str) -> bool:
        """Unlock the storage with a password"""
        try:
            salt = self._load_salt()
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            self._fernet = Fernet(key)
            return True
        except Exception:
            return False
    
    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        if not self._fernet:
            raise ValueError("Storage is locked")
        return self._fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, token: str) -> str:
        """Decrypt data"""
        if not self._fernet:
            raise ValueError("Storage is locked")
        return self._fernet.decrypt(token.encode()).decode()


class MemoryManager:
    """Main memory management class"""
    
    def __init__(self, storage: Storage):
        """
        Initialize a new memory manager
        
        Args:
            storage: Storage configuration
        """
        self.storage = storage
        self._memory: Dict[str, str] = {}
        self._locked = False
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in memory"""
        if self._locked:
            raise RuntimeError("Memory is locked")
            
        # Convert value to JSON string and encrypt
        value_str = json.dumps(value)
        encrypted = self.storage.encrypt(value_str)
        
        # Generate a random filename for storage
        filename = f"{secrets.token_hex(16)}.dat"
        filepath = os.path.join(self.storage.path, filename)
        
        # Store the encrypted data
        with open(filepath, 'w') as f:
            f.write(encrypted)
        
        # Store the mapping from key to filename
        self._memory[key] = filename
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from memory"""
        if key not in self._memory:
            return default
            
        filename = self._memory[key]
        filepath = os.path.join(self.storage.path, filename)
        
        try:
            with open(filepath, 'r') as f:
                encrypted = f.read()
            
            # Decrypt the data
            decrypted = self.storage.decrypt(encrypted)
            return json.loads(decrypted)
        except Exception as e:
            raise RuntimeError(f"Failed to read key '{key}': {str(e)}")
    
    def delete(self, key: str) -> bool:
        """Delete a key from memory"""
        if key in self._memory:
            filename = self._memory.pop(key)
            try:
                os.remove(os.path.join(self.storage.path, filename))
                return True
            except OSError:
                return False
        return False
    
    def clear(self) -> None:
        """Clear all data from memory"""
        if self._locked:
            raise RuntimeError("Memory is locked")
            
        for filename in self._memory.values():
            try:
                os.remove(os.path.join(self.storage.path, filename))
            except OSError:
                pass
        self._memory.clear()
    
    def lock(self) -> None:
        """Lock the memory to prevent modifications"""
        self._locked = True
    
    def unlock(self) -> None:
        """Unlock the memory to allow modifications"""
        self._locked = False
    
    def save(self, name: str) -> None:
        """Save the current memory state"""
        if self._locked:
            raise RuntimeError("Memory is locked")
            
        state = {
            'memory': self._memory,
            'locked': self._locked
        }
        
        state_path = os.path.join(self.storage.path, f"{name}.state")
        with open(state_path, 'w') as f:
            json.dump(state, f)
    
    def load(self, name: str) -> None:
        """Load a previously saved memory state"""
        if self._locked:
            raise RuntimeError("Memory is locked")
            
        state_path = os.path.join(self.storage.path, f"{name}.state")
        try:
            with open(state_path, 'r') as f:
                state = json.load(f)
            
            self._memory = state.get('memory', {})
            self._locked = state.get('locked', False)
        except FileNotFoundError:
            raise ValueError(f"No saved state found with name '{name}'")
