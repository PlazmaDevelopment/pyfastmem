"""
Command-line interface for PyFastMem
"""
import os
import sys
import json
import click
from pathlib import Path
from typing import Optional

from . import MemoryManager, Storage, SecurityError

@click.group()
@click.version_option()
def cli():
    """PyFastMem - Fast and secure memory storage for Python"""
    pass

@cli.command()
@click.argument('name')
@click.option('--path', default='.', help='Path where to create the storage')
def init(name: str, path: str) -> None:
    """Initialize a new storage"""
    try:
        storage = Storage(name=name, path=path)
        click.echo(f"Initialized new storage at {storage.path}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('storage_path', type=click.Path(exists=True))
@click.argument('key')
@click.argument('value')
def set_value(storage_path: str, key: str, value: str) -> None:
    """Set a value in the storage"""
    try:
        storage = _load_storage(storage_path)
        memory = MemoryManager(storage)
        _unlock_if_needed(memory, storage)
        
        # Try to parse value as JSON, fallback to string
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            pass
            
        memory.set(key, value)
        click.echo(f"Set {key} = {value}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('storage_path', type=click.Path(exists=True))
@click.argument('key')
def get_value(storage_path: str, key: str) -> None:
    """Get a value from the storage"""
    try:
        storage = _load_storage(storage_path)
        memory = MemoryManager(storage)
        _unlock_if_needed(memory, storage)
        
        value = memory.get(key)
        if value is not None:
            click.echo(json.dumps(value, indent=2))
        else:
            click.echo(f"Key '{key}' not found", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('storage_path', type=click.Path(exists=True))
@click.argument('key')
def delete(storage_path: str, key: str) -> None:
    """Delete a key from the storage"""
    try:
        storage = _load_storage(storage_path)
        memory = MemoryManager(storage)
        _unlock_if_needed(memory, storage)
        
        if memory.delete(key):
            click.echo(f"Deleted key: {key}")
        else:
            click.echo(f"Key '{key}' not found", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('storage_path', type=click.Path(exists=True))
@click.option('--yes', is_flag=True, help='Skip confirmation')
def clear(storage_path: str, yes: bool) -> None:
    """Clear all data from the storage"""
    try:
        if not yes and not click.confirm('Are you sure you want to clear all data?'):
            return
            
        storage = _load_storage(storage_path)
        memory = MemoryManager(storage)
        _unlock_if_needed(memory, storage)
        
        memory.clear()
        click.echo("Cleared all data")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('storage_path', type=click.Path(exists=True))
@click.argument('password')
def set_password(storage_path: str, password: str) -> None:
    """Set a password for the storage"""
    try:
        storage = _load_storage(storage_path)
        storage.set_password(password)
        click.echo("Password set successfully")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

def _load_storage(storage_path: str) -> Storage:
    """Load a storage from the given path"""
    path = Path(storage_path).resolve()
    name = path.name
    parent = str(path.parent)
    return Storage(name=name, path=parent)

def _unlock_if_needed(memory: MemoryManager, storage: Storage) -> None:
    """Prompt for password if storage is locked"""
    try:
        # Try to access storage to check if it's locked
        memory.get('__test_key')
    except ValueError as e:
        if "Storage is locked" in str(e):
            password = click.prompt('Enter password', hide_input=True)
            if not storage.unlock(password):
                click.echo("Invalid password", err=True)
                sys.exit(1)
        else:
            raise

def main():
    cli()

if __name__ == '__main__':
    main()
