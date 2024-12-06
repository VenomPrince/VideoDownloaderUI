#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import yt_dlp

class VideoDownloader(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Media Downloader")
        self.geometry("800x700")
        
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Media Downloader", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=(0, 10))

        # URL Input Frame
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(url_frame, text="Video/Audio URL:", font=('Helvetica', 10)).pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50, font=('Helvetica', 10))
        self.url_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=10)

        # Platform Detection
        platform_frame = ttk.Frame(main_frame)
        platform_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(platform_frame, text="Platform:").pack(side=tk.LEFT, padx=(0,10))
        self.platform_var = tk.StringVar(value="Auto Detect")
        platform_options = [
            "Auto Detect", 
            "YouTube", 
            "Vimeo", 
            "Facebook", 
            "Instagram", 
            "TikTok",
            "Other Video Sites"
        ]
        self.platform_dropdown = ttk.Combobox(platform_frame, textvariable=self.platform_var, values=platform_options, width=20)
        self.platform_dropdown.pack(side=tk.LEFT)

        # Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Download Options", padding=(10, 5))
        options_frame.pack(fill='x', padx=10, pady=5)

        # Playlist/Multiple Media Options
        ttk.Label(options_frame, text="Media Limit:").grid(row=0, column=0, sticky='w', padx=5, pady=2)
        self.playlist_var = tk.StringVar(value="First 5 Items")
        playlist_options = [
            "First 5 Items", 
            "First 10 Items",
            "First 20 Items",
            "Entire Playlist/Collection", 
            "Single Item Only"
        ]
        self.playlist_dropdown = ttk.Combobox(options_frame, textvariable=self.playlist_var, values=playlist_options, width=20)
        self.playlist_dropdown.grid(row=0, column=1, padx=5, pady=2)

        # Format Options
        ttk.Label(options_frame, text="Format:").grid(row=1, column=0, sticky='w', padx=5, pady=2)
        self.format_var = tk.StringVar(value="Best Quality (Video + Audio)")
        format_options = [
            "Best Quality (Video + Audio)",
            "Video Only (Best Quality)",
            "Audio Only (Best Quality)",
            "Compressed (480p)",
            "Mobile Quality (360p)"
        ]
        self.format_dropdown = ttk.Combobox(options_frame, textvariable=self.format_var, values=format_options, width=20)
        self.format_dropdown.grid(row=1, column=1, padx=5, pady=2)

        # Output Directory
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(output_frame, text="Save Location:").pack(side=tk.LEFT, padx=(0,10))
        self.output_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var, width=50)
        self.output_entry.pack(side=tk.LEFT, expand=True, fill='x', padx=(0,10))
        
        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output)
        browse_btn.pack(side=tk.LEFT)

        # Progress Frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill='x', padx=10, pady=10)
        
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=300)
        self.progress_bar.pack(pady=5)

        # Download Button
        self.download_btn = ttk.Button(main_frame, text="Start Download", command=self.start_download)
        self.download_btn.pack(pady=10)

        # Status Text
        self.status_text = tk.Text(main_frame, height=10, width=60, font=('Courier', 9))
        self.status_text.pack(pady=10)
        self.status_text.config(state=tk.DISABLED)

    def browse_output(self):
        directory = filedialog.askdirectory(initialdir=self.output_var.get())
        if directory:
            self.output_var.set(directory)

    def update_progress(self, d):
        if d['status'] == 'downloading':
            try:
                total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                
                if total > 0:
                    percentage = (downloaded / total) * 100
                    self.progress_bar['value'] = percentage
                    
                speed = d.get('speed', 0)
                if speed:
                    speed_mb = speed / 1024 / 1024  # Convert to MB/s
                    progress_text = f"Downloading: {percentage:.1f}% ({speed_mb:.1f} MB/s)"
                else:
                    progress_text = f"Downloading: {percentage:.1f}%"
                    
                self.progress_var.set(progress_text)
            except Exception as e:
                self.progress_var.set(f"Downloading... (Progress calculation error)")
        
        elif d['status'] == 'finished':
            self.progress_var.set("Download Complete!")
            self.progress_bar['value'] = 100

    def append_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid URL")
            return

        # Disable UI elements during download
        self.download_btn.config(state=tk.DISABLED)
        self.progress_bar['value'] = 0
        self.progress_var.set("Starting download...")
        
        # Clear status text
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state=tk.DISABLED)

        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'progress_hooks': [self.update_progress],
            'outtmpl': os.path.join(self.output_var.get(), '%(title)s.%(ext)s'),
        }

        # Modify format based on selection
        format_selection = self.format_var.get()
        if format_selection == "Video Only (Best Quality)":
            ydl_opts['format'] = 'bestvideo[ext=mp4]'
        elif format_selection == "Audio Only (Best Quality)":
            ydl_opts['format'] = 'bestaudio[ext=m4a]'
        elif format_selection == "Compressed (480p)":
            ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]'
        elif format_selection == "Mobile Quality (360p)":
            ydl_opts['format'] = 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]'

        # Configure playlist options
        playlist_selection = self.playlist_var.get()
        if playlist_selection == "First 5 Items":
            ydl_opts['playlist_items'] = '1-5'
        elif playlist_selection == "First 10 Items":
            ydl_opts['playlist_items'] = '1-10'
        elif playlist_selection == "First 20 Items":
            ydl_opts['playlist_items'] = '1-20'
        elif playlist_selection == "Single Item Only":
            ydl_opts['noplaylist'] = True

        def download_thread():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    self.append_status(f"Starting download from: {url}")
                    ydl.download([url])
                    self.append_status("Download completed successfully!")
            except Exception as e:
                self.append_status(f"Error: {str(e)}")
                self.progress_var.set("Download failed")
            finally:
                self.download_btn.config(state=tk.NORMAL)

        # Start download in a separate thread
        threading.Thread(target=download_thread, daemon=True).start()

def main():
    app = VideoDownloader()
    app.mainloop()

if __name__ == '__main__':
    main()
