import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import vlc
import json
import requests
from io import BytesIO

class MediaPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FURRY GOON APP")
        self.root.geometry("1000x700")
        self.root.iconbitmap("ico.ico")
        self.setup_ui()
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media_list = self.load_media_list()
        self.current_index = 0
        self.populate_listbox()

    def setup_ui(self):
        self.apply_dark_mode()

        self.video_frame = ttk.Frame(self.root)
        self.video_frame.pack(pady=1, fill=tk.BOTH, expand=True)

        self.preview_label = ttk.Label(self.video_frame)
        self.preview_label.pack(pady=300)

        self.controls_frame = ttk.Frame(self.root)
        self.controls_frame.pack(pady=1, fill=tk.X)

        self.play_button = ttk.Button(self.controls_frame, text="Play", command=self.play_media)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.pause_button = ttk.Button(self.controls_frame, text="Pause", command=self.pause_media)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        self.prev_button = ttk.Button(self.controls_frame, text="Previous", command=self.prev_media)
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.controls_frame, text="Next", command=self.next_media)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.add_button = ttk.Button(self.controls_frame, text="Add Media", command=self.add_media)
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(self.root, bg="#555555", fg="#ffffff", selectbackground="#444444", selectforeground="#ffffff")
        self.listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.show_preview)

    def load_media_list(self):
        try:
            with open('media.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "media.json file not found")
            return []

    def save_media_list(self):
        with open('media.json', 'w') as file:
            json.dump(self.media_list, file, indent=4)

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for index, media in enumerate(self.media_list):
            self.listbox.insert(tk.END, media["name"])

    def show_preview(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.current_index = selected_index[0]
            image_url = self.media_list[self.current_index].get("image")
            if image_url:
                response = requests.get(image_url)
                image_data = Image.open(BytesIO(response.content))
                image_data = image_data.resize((200, 150), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image_data)
                self.preview_label.config(image=photo)
                self.preview_label.image = photo
            else:
                self.preview_label.config(image='')

    def play_media(self):
        if self.media_list:
            selected_index = self.listbox.curselection()
            if selected_index:
                self.current_index = selected_index[0]
            url = self.media_list[self.current_index]["url"]
            media = self.instance.media_new(url)
            self.player.set_media(media)
            self.player.set_hwnd(self.video_frame.winfo_id())
            self.player.play()
        else:
            messagebox.showerror("Error", "No media URLs found")

    def pause_media(self):
        if self.player.is_playing():
            self.player.pause()
            self.pause_button.config(text="Continue")
        else:
            self.player.play()
            self.pause_button.config(text="Pause")

    def stop_media(self):
        self.player.stop()
        self.pause_button.config(text="Pause")

    def prev_media(self):
        if self.media_list:
            self.current_index = (self.current_index - 1) % len(self.media_list)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.show_preview(None)
            self.play_media()

    def next_media(self):
        if self.media_list:
            self.current_index = (self.current_index + 1) % len(self.media_list)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.current_index)
            self.show_preview(None)
            self.play_media()

    def add_media(self):
        url = simpledialog.askstring("Media URL", "Enter the URL for the media:")
        if url:
            name = simpledialog.askstring("Media Name", "Enter a name for the media:")
            if name:
                new_media = {"name": name, "url": url, "image": ""}
                self.media_list.append(new_media)
                self.save_media_list()
                self.populate_listbox()

    def apply_dark_mode(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#333333", foreground="#ffffff")
        style.configure("TEntry", background="#555555", foreground="#ffffff", fieldbackground="#555555")
        style.configure("TButton", background="#444444", foreground="#ffffff")
        style.configure("TFrame", background="#333333")
        style.configure("TNotebook", background="#333333", foreground="#ffffff")
        style.configure("TNotebook.Tab", background="#444444", foreground="#ffffff")
        self.root.configure(bg="#333333")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayerApp(root)
    root.mainloop()