import os
import json
from pathlib import Path


class ConfigManager:
    def __init__(self):
        # Final end-user config location
        self.config_dir = Path.home() / ".config" / "seadog"
        self.config_file = self.config_dir / "config.json"

        # Default config with SAFE examples and explanations
        self.default_config = {
            "__help": {
                "music_output_dir": "Default directory where downloaded music is saved",
                "video_output_dir": "Default directory where downloaded videos are saved",
                "open_kid3_after_download": "Automatically open Kid3 after music downloads complete",
                "kid3_path": "Path to the kid3 executable (usually just 'kid3')",
                "gotify_enabled": "Enable Gotify notifications",
                "gotify_url": "Base URL of your Gotify server (example: https://gotify.example.com)",
                "gotify_token": "Gotify application token",
                "playlist_delay": "Delay in seconds between playlist items to avoid rate limits",
                "playlist_monitor_enabled": "Enable automatic monitoring of followed playlists",
                "playlist_monitor_interval": "How often (seconds) to check playlists for new content",
                "follow_playlists": "Dictionary of playlist URLs to monitor"
            },

            "music_output_dir": str(Path.home() / "Music"),
            "video_output_dir": str(Path.home() / "Videos"),

            "open_kid3_after_download": False,
            "kid3_path": "kid3",

            "gotify_enabled": False,
            "gotify_url": "",
            "gotify_token": "",

            "playlist_delay": 0,

            "playlist_monitor_enabled": False,
            "playlist_monitor_interval": 60,
            "follow_playlists": {}
        }

        self.config = {}
        self.load_config()

    def load_config(self):
        """Load config or create it on first run. Merge new defaults safely."""
        if not self.config_file.exists():
            self._create_default_config()

        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except (json.JSONDecodeError, OSError):
            # Corrupt or unreadable config → reset safely
            self.config = self.default_config.copy()
            self.save_config()
            return

        # Merge in any new default keys (future-proof)
        changed = False
        for key, value in self.default_config.items():
            if key not in self.config:
                self.config[key] = value
                changed = True

        if changed:
            self.save_config()

    def _create_default_config(self):
        """Create config directory and write default config."""
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.default_config, f, indent=4)

    def save_config(self):
        """Persist config to disk."""
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
