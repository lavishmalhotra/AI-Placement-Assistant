import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from datetime import datetime
from openai import OpenAI
import threading
import pyttsx3
import speech_recognition as sr

# ---------------- API SETUP ---------------- #

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your api key" 
)

# ---------------- TEXT TO SPEECH ---------------- #

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- CHAT MEMORY ---------------- #

chat_memory = [
    {
        "role": "system",
        "content": (
            "You are an AI Placement Preparation Assistant. "
            "Help students with coding, placements, resumes, aptitude, AI, "
            "machine learning, projects, and interview preparation."
        )
    }
]

# ---------------- SAVE CHAT ---------------- #

def save_chat(message):

    with open("chat_history.txt", "a", encoding="utf-8") as file:
        file.write(message + "\n")

# ---------------- AI RESPONSE ---------------- #

def get_ai_response(user_text):

    try:

        chat_memory.append(
            {
                "role": "user",
                "content": user_text
            }
        )

        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=chat_memory
        )

        reply = response.choices[0].message.content

        chat_memory.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        return reply

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- PROCESS MESSAGE ---------------- #

def process_message(user_text, current_time):

    chat_box.config(state=tk.NORMAL)

    chat_box.insert(
        tk.END,
        f"[{current_time}] Assistant is typing...\n\n",
        "typing"
    )

    chat_box.config(state=tk.DISABLED)

    chat_box.yview(tk.END)

    bot_reply = get_ai_response(user_text)

    chat_box.config(state=tk.NORMAL)

    chat_box.delete("end-3l", "end-1l")

    chat_box.insert(
        tk.END,
        f"[{current_time}] Assistant: {bot_reply}\n\n",
        "bot"
    )

    chat_box.config(state=tk.DISABLED)

    chat_box.yview(tk.END)

    save_chat(f"[{current_time}] You: {user_text}")
    save_chat(f"[{current_time}] Assistant: {bot_reply}")

    
# ---------------- SEND MESSAGE ---------------- #

def send_message():

    user_text = input_box.get()

    if user_text.strip() == "":
        return

    current_time = datetime.now().strftime("%H:%M")

    chat_box.config(state=tk.NORMAL)

    chat_box.insert(
        tk.END,
        f"[{current_time}] You: {user_text}\n\n",
        "user"
    )

    chat_box.config(state=tk.DISABLED)

    chat_box.yview(tk.END)

    input_box.delete(0, tk.END)

    threading.Thread(
        target=process_message,
        args=(user_text, current_time)
    ).start()

# ---------------- VOICE INPUT ---------------- #

def voice_input():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            status_label.config(text="Listening...")

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            input_box.delete(0, tk.END)

            input_box.insert(0, text)

            status_label.config(text="Voice captured")

    except:
        status_label.config(text="Voice input failed")

# ---------------- CLEAR CHAT ---------------- #

def clear_chat():

    chat_box.config(state=tk.NORMAL)

    chat_box.delete(1.0, tk.END)

    chat_box.insert(
        tk.END,
        "Assistant: Chat cleared successfully.\n\n",
        "bot"
    )

    chat_box.config(state=tk.DISABLED)

# ---------------- EXPORT CHAT ---------------- #

def export_chat():

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")]
    )

    if file_path:

        content = chat_box.get(1.0, tk.END)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        status_label.config(text="Chat exported successfully")

# ---------------- MAIN WINDOW ---------------- #

window = tk.Tk()

window.title("AI Placement Assistant - Lavish Malhotra")

window.geometry("1000x780")

window.configure(bg="#1f1f1f")

# ---------------- TITLE ---------------- #

title_label = tk.Label(
    window,
    text="AI Placement Assistant",
    font=("Arial", 28, "bold"),
    bg="#1f1f1f",
    fg="#00ffcc"
)

title_label.pack(pady=15)

# ---------------- CHAT AREA ---------------- #

chat_box = scrolledtext.ScrolledText(
    window,
    wrap=tk.WORD,
    width=100,
    height=32,
    font=("Consolas", 11),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT
)

chat_box.pack(padx=15, pady=10)

chat_box.tag_config("user", foreground="#00ffcc")

chat_box.tag_config("bot", foreground="#ffffff")

chat_box.tag_config("typing", foreground="#ffaa00")

chat_box.config(state=tk.NORMAL)

chat_box.insert(
    tk.END,
    "Assistant: Hello Lavish!\n"
    "I am your AI Placement Preparation Assistant.\n"
    "Ask me about coding, DSA, AI, resumes, projects, or interviews.\n\n",
    "bot"
)

chat_box.config(state=tk.DISABLED)

# ---------------- INPUT FRAME ---------------- #

input_frame = tk.Frame(
    window,
    bg="#1f1f1f"
)

input_frame.pack(pady=15)

# ---------------- INPUT BOX ---------------- #

input_box = tk.Entry(
    input_frame,
    width=65,
    font=("Consolas", 12),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT
)

input_box.grid(
    row=0,
    column=0,
    padx=10,
    ipady=8
)

# ---------------- SEND BUTTON ---------------- #

send_button = tk.Button(
    input_frame,
    text="Send",
    command=send_message,
    bg="#00ffcc",
    fg="black",
    font=("Arial", 11, "bold"),
    width=10,
    relief=tk.FLAT,
    cursor="hand2"
)

send_button.grid(
    row=0,
    column=1,
    padx=5
)

# ---------------- VOICE BUTTON ---------------- #

voice_button = tk.Button(
    input_frame,
    text="Voice",
    command=voice_input,
    bg="#ffaa00",
    fg="black",
    font=("Arial", 11, "bold"),
    width=10,
    relief=tk.FLAT,
    cursor="hand2"
)

voice_button.grid(
    row=0,
    column=2,
    padx=5
)

# ---------------- CLEAR BUTTON ---------------- #

clear_button = tk.Button(
    input_frame,
    text="Clear",
    command=clear_chat,
    bg="#ff4d4d",
    fg="white",
    font=("Arial", 11, "bold"),
    width=10,
    relief=tk.FLAT,
    cursor="hand2"
)

clear_button.grid(
    row=0,
    column=3,
    padx=5
)

# ---------------- EXPORT BUTTON ---------------- #

export_button = tk.Button(
    input_frame,
    text="Export",
    command=export_chat,
    bg="#4d79ff",
    fg="white",
    font=("Arial", 11, "bold"),
    width=10,
    relief=tk.FLAT,
    cursor="hand2"
)

export_button.grid(
    row=0,
    column=4,
    padx=5
)

# ---------------- STATUS LABEL ---------------- #

status_label = tk.Label(
    window,
    text="Ready",
    font=("Arial", 10),
    bg="#1f1f1f",
    fg="#aaaaaa"
)

status_label.pack(pady=5)

# ---------------- ENTER KEY ---------------- #

window.bind(
    '<Return>',
    lambda event: send_message()
)

# ---------------- RUN APP ---------------- #

window.mainloop()