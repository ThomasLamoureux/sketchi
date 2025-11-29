# loading_screen.py - Animated loading screen with video
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import threading
import time

class SimpleLoadingScreen(ctk.CTk):
    def __init__(self, video_path="loading_screen.mp4", duration=3000):
        super().__init__()
        
        self.video_path = video_path
        self.duration = duration
        self.frame_index = 0
        self.frames = []
        
        # Window setup
        self.title("Sketchi")
        self.geometry("800x600")
        self.configure(fg_color="#1e1e1e")
        self.resizable(False, False)
        self.overrideredirect(True)
        
        # Center window
        self.center_window(800, 600)
        
        # Create video label
        self.video_label = ctk.CTkLabel(self, text="", fg_color="#1e1e1e")
        self.video_label.pack(expand=True, fill="both")
        
        # Load video frames
        self.load_frames()
        
        # Start animation
        if self.frames:
            self.animate()
        else:
            self.show_text_loading()
    
    def center_window(self, width, height):
        """Center the window"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_frames(self):
        """Load video frames"""
        try:
            cap = cv2.VideoCapture(self.video_path)
            
            if not cap.isOpened():
                print(f"Could not open video: {self.video_path}")
                return
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (800, 600))
                img = Image.fromarray(frame)
                img_tk = ImageTk.PhotoImage(image=img)
                
                self.frames.append(img_tk)
            
            cap.release()
            print(f"Loaded {len(self.frames)} frames")
            
        except Exception as e:
            print(f"Error loading video: {e}")
    
    def animate(self):
        """Animate frames"""
        if self.frame_index < len(self.frames):
            self.video_label.configure(image=self.frames[self.frame_index])
            self.frame_index += 1
            self.after(33, self.animate)
        else:
            self.after(500, self.destroy)
    
    def show_text_loading(self):
        """Fallback text loading"""
        self.video_label.configure(
            text="SKETCHI",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color="#ff6b35"
        )
        self.after(2000, self.destroy)