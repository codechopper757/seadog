"""
Unified threaded downloader using yt-dlp.

Usage (example):
    from engine.downloader import Downloader

    dl = Downloader()
    # start a threaded download
    thread = dl.download(
        url="https://www.youtube.com/playlist?list=...",
        out_dir="/home/eric/konosuba-Music",
        mode="audio",              # "audio" or "video"
        delay=5,                   # seconds between playlist items
        status_callback=print,     # receives status lines/messages
        finished_callback=lambda ok: print("done", ok)
    )

    # to stop/cancel:
    dl.stop()
"""

import subprocess
import threading
import time
import json
import shlex
import os
from typing import Callable, Optional


class Downloader:
    def __init__(self):
        # threading/process control
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._current_process: Optional[subprocess.Popen] = None

    # -----------------
    # Public API
    # -----------------
    def download(
        self,
        url: str,
        out_dir: str,
        mode: str = "audio",                 # "audio" or "video"
        delay: float = 0.0,                  # seconds between playlist items
        retries: int = 0,                    # retries per item
        retry_delay: float = 5.0,            # seconds between retries
        status_callback: Optional[Callable[[str], None]] = None,
        finished_callback: Optional[Callable[[bool], None]] = None,
        extra_ytdlp_args: Optional[list] = None
    ) -> threading.Thread:
        """
        Start a threaded download. Returns the Thread object.

        - status_callback(msg) will be called with output lines and status updates.
        - finished_callback(success_bool) will be called when entire operation finishes.
        """
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Downloader already running")

        # clear stop flag
        self._stop_event.clear()

        # -----------------
        # Build yt-dlp args
        # -----------------
        # Copy list so we don't mutate the caller's list
        extra_args = list(extra_ytdlp_args) if extra_ytdlp_args else []

        # Native yt-dlp playlist delay
        if delay and delay > 0:
            extra_args.extend([
                "--sleep-interval", str(delay)
            ])

        # -----------------
        # Start worker thread
        # -----------------
        self._thread = threading.Thread(
            target=self._run,
            args=(
                url,
                out_dir,
                mode,
                delay,
                retries,
                retry_delay,
                status_callback,
                finished_callback,
                extra_args,   # ← pass modified args
            ),
            daemon=True,
        )
        self._thread.start()
        return self._thread


    def stop(self):
        """
        Signal to stop and terminate any running yt-dlp process.
        """
        self._stop_event.set()
        if self._current_process:
            try:
                self._current_process.terminate()
            except Exception:
                pass

    # -----------------
    # Internal helpers
    # -----------------
    def _run(
        self,
        url, out_dir, mode, delay, retries, retry_delay, status_callback, finished_callback, extra_ytdlp_args
    ):
        ok = True
        try:
            if status_callback:
                status_callback(f"Preparing download: mode={mode} url={url}")

            os.makedirs(out_dir, exist_ok=True)

            # Detect playlist
            playlist_entries = self._probe_playlist(url, status_callback)
            if playlist_entries:
                if status_callback:
                    status_callback(f"Detected playlist with {len(playlist_entries)} entries.")
                for idx, entry_url in enumerate(playlist_entries, start=1):
                    if self._stop_event.is_set():
                        ok = False
                        if status_callback:
                            status_callback("Download cancelled by user.")
                        break

                    if status_callback:
                        status_callback(f"Downloading item {idx}/{len(playlist_entries)}: {entry_url}")

                    success = self._download_one_with_retries(
                        entry_url, out_dir, mode, retries, retry_delay, status_callback, extra_ytdlp_args
                    )
                    if not success:
                        ok = False
                        # continue to next item or break? We'll continue but mark overall as failed.
                        if status_callback:
                            status_callback(f"Failed to download item: {entry_url}")

                    # Delay between playlist items (respect stop)
                    for s in range(int(delay)):
                        if self._stop_event.is_set():
                            break
                        time.sleep(1)
                    # handle fractional seconds
                    frac = delay - int(delay)
                    if frac and not self._stop_event.is_set():
                        time.sleep(frac)

            else:
                # Single URL (not a detected playlist)
                if status_callback:
                    status_callback("Downloading single item...")
                success = self._download_one_with_retries(
                    url, out_dir, mode, retries, retry_delay, status_callback, extra_ytdlp_args
                )
                ok = ok and success

        except Exception as e:
            ok = False
            if status_callback:
                status_callback(f"Downloader error: {e}")

        finally:
            # cleanup
            self._current_process = None
            if finished_callback:
                try:
                    finished_callback(ok)
                except Exception:
                    pass

    def _probe_playlist(self, url: str, status_callback: Optional[Callable[[str], None]] = None):
        """
        Probe the URL to see if it's a playlist. If playlist, return list of item URLs in order.
        Returns [] if not a playlist or probe failed.
        """
        try:
            # use --flat-playlist -J to get JSON with entries (lightweight)
            cmd = ["yt-dlp", "--flat-playlist", "-J", url]
            proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
            if proc.returncode != 0:
                # not necessarily an error; treat as single item
                if status_callback:
                    status_callback(f"Playlist probe returned non-zero (treat as single item): {proc.stderr.strip()}")
                return []

            payload = proc.stdout
            data = json.loads(payload)
            entries = data.get("entries")
            if not entries:
                return []

            # entries may be dicts with 'url' or 'id' or 'webpage_url'
            item_urls = []
            for e in entries:
                if isinstance(e, dict):
                    url_piece = e.get("url") or e.get("id") or e.get("webpage_url")
                else:
                    url_piece = e  # sometimes it's a string id
                if not url_piece:
                    continue
                # if it's an ID like 'VIDEOID', convert to full youtube watch URL
                if len(url_piece) == 11 and not url_piece.startswith("http"):
                    item_urls.append(f"https://www.youtube.com/watch?v={url_piece}")
                elif url_piece.startswith("http"):
                    item_urls.append(url_piece)
                else:
                    # fallback - assume ID
                    item_urls.append(f"https://www.youtube.com/watch?v={url_piece}")

            return item_urls

        except Exception as e:
            if status_callback:
                status_callback(f"Playlist probe exception: {e}")
            return []

    def _download_one_with_retries(self, url, out_dir, mode, retries, retry_delay, status_callback, extra_ytdlp_args):
        attempts = 0
        while attempts <= retries and not self._stop_event.is_set():
            attempts += 1
            if status_callback:
                status_callback(f"Attempt {attempts} for {url}")
            success = self._download_one(url, out_dir, mode, status_callback, extra_ytdlp_args)
            if success:
                return True
            if attempts <= retries:
                if status_callback:
                    status_callback(f"Retrying in {retry_delay} seconds...")
                for _ in range(int(retry_delay)):
                    if self._stop_event.is_set():
                        break
                    time.sleep(1)
                frac = retry_delay - int(retry_delay)
                if frac and not self._stop_event.is_set():
                    time.sleep(frac)
        return False

    def _download_one(self, url, out_dir, mode, status_callback, extra_ytdlp_args):
        """
        Build a yt-dlp command for either audio or video and run it, streaming output to status_callback.
        Returns True on success, False otherwise.
        """
        # output template: include playlist_index if playlist; otherwise just title
        out_template = os.path.join(out_dir, "%(playlist_index)s - %(title)s.%(ext)s")
        # For single items, playlist_index may not be present; that's okay.

        base_cmd = ["yt-dlp"]

        # append extra args if provided
        if extra_ytdlp_args:
            base_cmd.extend(extra_ytdlp_args)

        if mode == "audio":
            cmd = base_cmd + [
                "-x",
                "--audio-format", "mp3",
                "--embed-thumbnail",
                "--embed-metadata",
                "--add-metadata",
                "-o", out_template,
                url
            ]
        else:
            # video mode - prefer requested extension if possible, allow best fallback
            # user can pass extra_ytdlp_args to change format selection
            cmd = base_cmd + [
                "-f", "bv*+ba/best",
                "-o", os.path.join(out_dir, "%(playlist_index)s - %(title)s.%(ext)s"),
                url
            ]

        if status_callback:
            status_callback(f"Running: {' '.join(shlex.quote(x) for x in cmd)}")

        try:
            # start process
            self._current_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1
            )

            # stream output
            assert self._current_process.stdout is not None
            for line in self._current_process.stdout:
                if self._stop_event.is_set():
                    # try to terminate process gracefully
                    try:
                        self._current_process.terminate()
                    except Exception:
                        pass
                    break
                if status_callback:
                    status_callback(line.rstrip())

            self._current_process.wait()
            code = self._current_process.returncode
            self._current_process = None

            if code == 0:
                if status_callback:
                    status_callback("yt-dlp finished successfully for item.")
                return True
            else:
                if status_callback:
                    status_callback(f"yt-dlp exited with code {code}")
                return False

        except Exception as e:
            if status_callback:
                status_callback(f"Exception running yt-dlp: {e}")
            try:
                if self._current_process:
                    self._current_process.terminate()
            except Exception:
                pass
            self._current_process = None
            return False
