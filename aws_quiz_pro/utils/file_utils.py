"""
File Utility Functions
"""

import os
import json
from typing import Any, Dict, Optional


class FileUtils:
    """File operation utilities"""
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Ensure directory exists"""
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            return True
        except Exception as e:
            print(f"Error creating directory: {e}")
            return False
    
    @staticmethod
    def load_json(filepath: str, default: Any = None) -> Any:
        """Load JSON file"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            return default
        except Exception as e:
            print(f"Error loading JSON from {filepath}: {e}")
            return default
    
    @staticmethod
    def save_json(filepath: str, data: Any) -> bool:
        """Save JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON to {filepath}: {e}")
            return False
    
    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Check if file exists"""
        return os.path.exists(filepath) and os.path.isfile(filepath)
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(filepath)
        except:
            return 0
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
            return False
    
    @staticmethod
    def get_cache_files(prefix: str, directory: str = ".") -> list:
        """Get all cache files with given prefix"""
        try:
            return [f for f in os.listdir(directory) 
                   if f.startswith(prefix) and f.endswith('.json')]
        except:
            return []
    
    @staticmethod
    def clear_cache(prefix: str, directory: str = ".") -> int:
        """Clear all cache files with given prefix"""
        count = 0
        try:
            cache_files = FileUtils.get_cache_files(prefix, directory)
            for cache_file in cache_files:
                filepath = os.path.join(directory, cache_file)
                if FileUtils.delete_file(filepath):
                    count += 1
        except Exception as e:
            print(f"Error clearing cache: {e}")
        return count