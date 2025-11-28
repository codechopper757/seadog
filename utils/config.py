import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        # Default config path: ~/.config/project_seadog/config.json
        self.config_dir = Path.home() / ".config" / "project_seadog"
        self.config_file = self.config_dir / "config.json"
        self.config = {}
        self.default_config = {
            "music_output_dir": str(Path.home() / "konosuba-Music"),
            "video_output_dir": str(Path.home() / "Videos"),
            "open_kid3_after_download": False,
            "kid3_path": "kid3",
            "gotify_enabled": False,
            "gotify_url": "",
            "gotify_token": "",
            "playlist_monitor_enabled": False,
            "playlist_monitor_interval": 60,
            "follow_playlists": {}
        }
        self.load_config()

    def load_config(self):
        """Load config from file or create default if missing."""
        if not self.config_file.exists():
            self._create_default_config()
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except json.JSONDecodeError:
            print("Warning: Config file corrupted. Recreating default.")
            self._create_default_config()
            self.config = self.default_config.copy()

    def _create_default_config(self):
        """Create config directory and default config file."""
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.default_config, f, indent=4)

    def save_config(self):
        """Save current config dict to file."""
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    def get(self, key, default=None):
        """Safe getter for config keys."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a config key and save immediately."""
        self.config[key] = value
        self.save_config()


# Example usage
if __name__ == "__main__":
    cfg = ConfigManager()
    print("Music directory:", cfg.get("music_output_dir"))
    cfg.set("open_kid3_after_download", True)
