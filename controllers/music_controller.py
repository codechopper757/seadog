import subprocess
import threading
from utils.config import ConfigManager

class MusicController:
    def __init__(self):
        self.config = ConfigManager()
        self.current_process = None

    def download_music(self, url, output_dir=None, open_kid3=False, progress_callback=None):
        """Download music in a background thread."""
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, output_dir, open_kid3, progress_callback),
            daemon=True
        )
        thread.start()
        return thread

    def _download_thread(self, url, output_dir, open_kid3, progress_callback):
        if output_dir is None or output_dir.strip() == "":
            output_dir = self.config.get("music_output_dir")

        subprocess.run(["mkdir", "-p", output_dir])

        cmd = [
            "yt-dlp",
            "-x",
            "--audio-format", "mp3",
            "--embed-thumbnail",
            "--embed-metadata",
            "--add-metadata",
            "-o", f"{output_dir}/%(playlist_index)s - %(title)s.%(ext)s",
            url
        ]

        if progress_callback:
            progress_callback(f"Starting download: {url}")

        self.current_process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        for line in self.current_process.stdout:
            if progress_callback:
                progress_callback(line.strip())

        self.current_process.wait()
        self.current_process = None

        if self.current_process is None:  # Normal termination
            if self.current_process and open_kid3:
                kid3_path = self.config.get("kid3_path", "kid3")
                subprocess.Popen([kid3_path, output_dir])
                if progress_callback:
                    progress_callback("Opened Kid3 for editing metadata.")
            elif progress_callback:
                progress_callback("Download finished successfully.")
