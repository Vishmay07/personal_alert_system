# main.py
import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import threading
import speech_recognition as sr
from emergency_core import emergency_procedure

class EmergencyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 Emergency Alert System")
        self.root.geometry("800x600")

        # Video feed
        self.video_label = tk.Label(self.root)
        self.video_label.pack()

        # Panic button
        self.panic_button = tk.Button(root, text="🚨 PANIC", bg="red", fg="white",
                                      font=("Arial", 20), command=self.trigger_alert)
        self.panic_button.pack(pady=20)

        self.status = tk.Label(root, text="Listening for voice...", font=("Arial", 14))
        self.status.pack()

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        self.update_video()

        # Start voice recognition in background
        threading.Thread(target=self.listen_voice, daemon=True).start()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb)
            imgtk = ImageTk.PhotoImage(img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.root.after(10, self.update_video)

    def trigger_alert(self):
        self.status.config(text="🚨 Emergency Triggered!")
        threading.Thread(target=emergency_procedure, daemon=True).start()

    def listen_voice(self):
        recognizer = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as source:
                    self.status.config(text="🎙️ Say 'help me' to trigger alert...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    print("🗣️ Detected:", command)
                    if "help me" in command.lower():
                        self.trigger_alert()
                        break
            except:
                continue

if __name__ == "__main__":
    root = tk.Tk()
    app = EmergencyGUI(root)
    root.mainloop()
