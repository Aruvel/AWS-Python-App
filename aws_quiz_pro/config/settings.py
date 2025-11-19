"""
Configuration Management
"""

import json
import os
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        "auto_save_progress": True,
        "show_explanations": True,
        "randomize_questions": True,
        "randomize_options": False,
        "timer_enabled": False,
        "time_per_question": 90,
        "exam_time_limit": 90,
        "sound_enabled": True,
        "theme": "dark",
        "appearance_mode": "dark",
        "default_question_order": "Random"
    }
    
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = self.load()
    
    def load(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                    return {**self.DEFAULT_CONFIG, **loaded_config}
            else:
                self.save(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save(self, config: Dict[str, Any] = None) -> bool:
        """Save configuration to file"""
        try:
            config_to_save = config if config else self.config
            with open(self.config_file, 'w') as f:
                json.dump(config_to_save, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
    
    def reset(self) -> None:
        """Reset to default configuration"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()