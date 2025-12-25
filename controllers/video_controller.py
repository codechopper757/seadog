from engine.downloader import Downloader
from utils.config import ConfigManager
from utils.gotify import send_gotify_notification

class VideoController:
    def __init__(self):
        self.config = ConfigManager()
        self.downloader = Downloader()
        self.current_thread = None

    def start_download(self, url, output_dir=None, progress_callback=None, finished_callback=None, send_notification=False):
        if output_dir is None or output_dir.strip() == "":
            output_dir = self.config.get("video_output_dir")

        delay = self.config.get("playlist_delay", 0)

        # start threaded download
        self.current_thread = self.downloader.download(
            url=url,
            out_dir=output_dir,
            mode="video",
            delay=delay,
            status_callback=progress_callback,
            finished_callback=lambda ok: self._on_finished(ok, output_dir, send_notification, finished_callback)
        )
        return self.current_thread

    def cancel_download(self):
        self.downloader.stop()

    # -----------------
    # Internal helper
    # -----------------
    def _on_finished(self, success, output_dir, send_notification, user_finished_callback):
        if send_notification:
            title = "Video Download Completed" if success else "Video Download Failed"
            message = f"Output directory: {output_dir}"
            try:
                send_gotify_notification(title, message)
            except Exception as e:
                print(f"Gotify notification failed: {e}")

        if user_finished_callback:
            user_finished_callback(success)
