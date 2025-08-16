"""
PyFastMem - A fast and secure memory storage library for Python
"""

__version__ = "0.1.0"

from .storage import Storage, MemoryManager

def New(storage):
    """Create a new memory instance with the given storage configuration"""
    return MemoryManager(storage)

# Common exceptions
class PyFastMemError(Exception):
    """Base exception for pyfastmem errors"""
    pass

class MemoryError(PyFastMemError):
    """Memory-related errors"""
    pass

class SecurityError(PyFastMemError):
    """Security-related errors (e.g., wrong password)"""
    pass
