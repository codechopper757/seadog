from engine.downloader import Downloader
from utils.config import ConfigManager

class MusicController:
    def __init__(self):
        self.config = ConfigManager()
        self.downloader = Downloader()
        self.current_thread = None

    def start_download(self, url, output_dir=None, open_kid3=False, progress_callback=None, finished_callback=None):
        """
        Starts a background download using Downloader.
        """
        if output_dir is None or output_dir.strip() == "":
            output_dir = self.config.get("music_output_dir")

        # Playlist delay from config (default 0)
        delay = self.config.get("playlist_delay", 0)

        # Threaded download
        self.current_thread = self.downloader.download(
            url=url,
            out_dir=output_dir,
            mode="audio",
            delay=delay,
            status_callback=progress_callback,
            finished_callback=lambda ok: self._on_finished(ok, output_dir, open_kid3, finished_callback)
        )
        return self.current_thread

    def cancel_download(self):
        """Stop any ongoing download."""
        self.downloader.stop()

    # -----------------
    # Internal helper
    # -----------------
    def _on_finished(self, success, output_dir, open_kid3, user_finished_callback):
        if open_kid3 and success:
            # open kid3 for the downloaded folder
            kid3_path = self.config.get("kid3_path", "kid3")
            try:
                import subprocess
                subprocess.Popen([kid3_path, output_dir])
            except Exception as e:
                print(f"Failed to open Kid3: {e}")

        # propagate to GUI if needed
        if user_finished_callback:
            user_finished_callback(success)
