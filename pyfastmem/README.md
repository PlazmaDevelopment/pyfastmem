# PyFastMem

A fast and secure memory storage library for Python applications.

## Features

- **Secure Storage**: Encrypted storage of key-value pairs
- **Password Protection**: Optional password protection for memory access
- **Thread-Safe**: Built-in locking mechanism for thread safety
- **Persistence**: Save and load memory states
- **Simple API**: Easy-to-use interface for common operations

## Installation

```bash
pip install pyfastmem
```

## Quick Start

### Initialize a new storage

```bash
pyfastmem init my_storage
```

### Set a value

```bash
pyfastmem set my_storage my_key "my value"
```

### Get a value

```bash
pyfastmem get my_storage my_key
```

### Set a password

```bash
pyfastmem set-password my_storage mypassword
```

## Python API

```python
from pyfastmem import Storage, MemoryManager

# Initialize storage
storage = Storage(name="my_app_data", path="./data")
memory = MemoryManager(storage)

# Set a password (optional)
storage.set_password("my_secure_password")

# Store data
memory.set("username", "johndoe")
memory.set("preferences", {"theme": "dark", "notifications": True})

# Retrieve data
username = memory.get("username")
prefs = memory.get("preferences")

# Delete data
memory.delete("username")

# Save memory state
memory.save("backup_2023")

# Clear all data
memory.clear()

# Lock/unlock memory
memory.lock()
# ... do some operations ...
memory.unlock()
```

## Security

- All data is encrypted using AES-256 in GCM mode
- Passwords are hashed using PBKDF2 with SHA-256
- Each storage gets a unique encryption key derived from the password
- Memory locking prevents unauthorized access

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
