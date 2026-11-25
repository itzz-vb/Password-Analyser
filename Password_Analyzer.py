
import tkinter as tk
from tkinter import messagebox
import random
from datetime import datetime


# ==================== COLOR PALETTE ====================

BG = "#171322"
CARD = "#211B30"
CARD2 = "#2B2340"
CARD3 = "#352B4D"

PURPLE = "#A98BDB"
LAVENDER = "#C9B5F0"
PINK = "#D9B5D0"
WHITE = "#F7F2FF"
GREY = "#B4A9C8"

RED = "#F08099"
YELLOW = "#F2CD91"
GREEN = "#9AD9BA"
CYAN = "#A9DCE0"

special_characters = "!@#$%^&*()_+-=[]{};:,.?/"
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"

weak_passwords = [
    "password", "123456", "12345678", "qwerty",
    "abc123", "admin", "welcome", "password123",
    "iloveyou", "000000"
]


# ==================== PASSWORD ANALYSIS ====================

def check_weak_password(password):
    lower_password = password.lower()

    for word in weak_passwords:
        if word in lower_password:
            return True

    for year in range(1900, datetime.now().year + 1):
        if str(year) in password:
            return True

    sequences = [
        "123456", "abcdef", "qwerty",
        "654321", "987654"
    ]

    for sequence in sequences:
        if sequence in lower_password:
            return True

    return False


def analyze_password(password):
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters.")

    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append("Add lowercase letters.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Add numbers.")

    if any(char in special_characters for char in password):
        score += 1
    else:
        suggestions.append("Add special characters.")

    if check_weak_password(password):
        strength = "Weak"
        color = RED
        suggestions.append(
            "Avoid common words, sequences and years."
        )

    elif score <= 2:
        strength = "Weak"
        color = RED

    elif score == 3:
        strength = "Medium"
        color = YELLOW

    elif score == 4:
        strength = "Strong"
        color = CYAN

    else:
        strength = "Very Strong"
        color = GREEN

    return score, strength, color, suggestions


# ==================== PASSWORD HISTORY ====================

def save_log(password, strength):
    try:
        with open("password_history.txt", "a") as file:
            file.write(
                f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')} | "
                f"Length: {len(password)} | "
                f"Strength: {strength}\n"
            )

    except OSError:
        messagebox.showerror(
            "Error",
            "Unable to save password history."
        )


def show_history():
    history_window = tk.Toplevel(root)
    history_window.title("Password History")
    history_window.geometry("550x400")
    history_window.configure(bg=BG)

    tk.Label(
        history_window,
        text="PASSWORD HISTORY",
        font=("Segoe UI", 17, "bold"),
        bg=BG,
        fg=LAVENDER
    ).pack(pady=20)

    history_text = tk.Text(
        history_window,
        bg=CARD,
        fg=WHITE,
        font=("Consolas", 10),
        relief="flat",
        wrap="word",
        padx=15,
        pady=15
    )
    history_text.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    try:
        with open("password_history.txt", "r") as file:
            history = file.read()

        if history:
            history_text.insert(tk.END, history)
        else:
            history_text.insert(tk.END, "No history available.")

    except FileNotFoundError:
        history_text.insert(tk.END, "No history available.")

    history_text.config(state="disabled")


# ==================== PASSWORD GENERATOR ====================

def generate_password():
    try:
        length = int(length_entry.get())

        if length < 8 or length > 50:
            messagebox.showwarning(
                "Invalid Length",
                "Enter password length between 8 and 50."
            )
            return

        # SystemRandom provides stronger random selection.
        secure_random = random.SystemRandom()

        password = [
            secure_random.choice(lowercase),
            secure_random.choice(uppercase),
            secure_random.choice(digits),
            secure_random.choice(special_characters)
        ]

        all_characters = (
            lowercase + uppercase + digits + special_characters
        )

        for i in range(length - 4):
            password.append(
                secure_random.choice(all_characters)
            )

        secure_random.shuffle(password)

        final_password = "".join(password)

        password_entry.delete(0, tk.END)
        password_entry.insert(0, final_password)

        analyze_and_display()

    except ValueError:
        messagebox.showwarning(
            "Invalid Input",
            "Please enter a valid number."
        )


# ==================== PASSWORD VISIBILITY ====================

password_visible = False


def toggle_password():
    global password_visible

    password_visible = not password_visible

    if password_visible:
        password_entry.config(show="")
        visibility_button.config(text="HIDE")
    else:
        password_entry.config(show="*")
        visibility_button.config(text="SHOW")


# ==================== COPY PASSWORD ====================

def copy_password():
    password = password_entry.get()

    if password == "":
        messagebox.showwarning(
            "Empty Password",
            "Generate or enter a password first."
        )
        return

    root.clipboard_clear()
    root.clipboard_append(password)

    messagebox.showinfo(
        "Copied",
        "Password copied to clipboard!"
    )


# ==================== ANALYSIS DISPLAY ====================

def analyze_and_display():
    password = password_entry.get()

    if password == "":
        messagebox.showwarning(
            "Empty Password",
            "Please enter a password first."
        )
        return

    score, strength, color, suggestions = analyze_password(password)

    result_label.config(
        text=strength,
        fg=color
    )

    score_label.config(
        text=f"{score}/5"
    )

    progress.delete("all")

    progress_width = 350

    progress.create_rectangle(
        0, 0, progress_width, 12,
        fill=CARD3,
        outline=""
    )

    progress.create_rectangle(
        0, 0, progress_width * score / 5, 12,
        fill=color,
        outline=""
    )

    output.config(state="normal")
    output.delete("1.0", tk.END)

    output.insert(tk.END, "YOUR PASSWORD REPORT\n\n")
    output.insert(
        tk.END,
        f"Password Length : {len(password)} characters\n"
    )
    output.insert(
        tk.END,
        f"Security Score  : {score}/5\n"
    )
    output.insert(
        tk.END,
        f"Strength        : {strength}\n\n"
    )

    if suggestions:
        output.insert(tk.END, "IMPROVEMENT SUGGESTIONS\n\n")

        for suggestion in suggestions:
            output.insert(tk.END, "  • " + suggestion + "\n")

    else:
        output.insert(
            tk.END,
            "  ✓ Your password meets all basic checks!"
        )

    output.config(state="disabled")

    save_log(password, strength)


# ==================== CLEAR FIELDS ====================

def clear_fields():
    password_entry.delete(0, tk.END)
    length_entry.delete(0, tk.END)
    length_entry.insert(0, "12")

    result_label.config(
        text="Not Analyzed",
        fg=GREY
    )

    score_label.config(text="0/5")

    progress.delete("all")

    output.config(state="normal")
    output.delete("1.0", tk.END)
    output.config(state="disabled")

    password_entry.config(show="*")
    visibility_button.config(text="SHOW")

    global password_visible
    password_visible = False


# ==================== BUTTON DESIGN ====================

def create_button(parent, text, command, color, fg=WHITE):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg=color,
        fg=fg,
        activebackground=LAVENDER,
        activeforeground=BG,
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=12,
        pady=12
    )


# ==================== MAIN WINDOW ====================

root = tk.Tk()
root.title("Velvet Vault | Password Security")
root.geometry("1050x760")
root.minsize(900, 700)
root.configure(bg=BG)


# ==================== HEADER ====================

header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=45, pady=(25, 15))

tk.Label(
    header,
    text="✦  VELVET VAULT",
    font=("Segoe UI", 25, "bold"),
    bg=BG,
    fg=WHITE
).pack(side="left")

tk.Label(
    header,
    text="YOUR DIGITAL SECURITY SPACE",
    font=("Segoe UI", 9, "bold"),
    bg=BG,
    fg=LAVENDER
).pack(side="right", pady=12)


# ==================== SUBHEADING ====================

tk.Label(
    root,
    text="A little more security, a little more peace.",
    font=("Segoe UI", 11),
    bg=BG,
    fg=GREY
).pack(anchor="w", padx=48, pady=(0, 20))


# ==================== MAIN CONTENT ====================

main_frame = tk.Frame(root, bg=BG)
main_frame.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=5
)

main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)


# ==================== LEFT PANEL ====================

left_card = tk.Frame(
    main_frame,
    bg=CARD,
    highlightbackground="#493A62",
    highlightthickness=1
)

left_card.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=(0, 12)
)

left_content = tk.Frame(left_card, bg=CARD)
left_content.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=30
)

tk.Label(
    left_content,
    text="✧",
    font=("Segoe UI", 65),
    bg=CARD,
    fg=PURPLE
).pack(pady=(25, 10))

tk.Label(
    left_content,
    text="Protect what\nmatters most.",
    font=("Segoe UI", 25, "bold"),
    bg=CARD,
    fg=WHITE,
    justify="center"
).pack(pady=10)

tk.Label(
    left_content,
    text="Create stronger passwords.\nKeep your digital world safer.",
    font=("Segoe UI", 11),
    bg=CARD,
    fg=GREY,
    justify="center"
).pack(pady=10)

# Decorative divider

tk.Frame(
    left_content,
    bg="#59476F",
    height=1
).pack(fill="x", pady=25)

tk.Label(
    left_content,
    text="✦  SECURITY REMINDER",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LAVENDER
).pack(anchor="w")

tk.Label(
    left_content,
    text=(
        "Avoid using personal information,\n"
        "birth years or predictable patterns.\n\n"
        "A unique password for every account\n"
        "is always a better choice."
    ),
    font=("Segoe UI", 10),
    bg=CARD,
    fg=GREY,
    justify="left"
).pack(anchor="w", pady=12)

tk.Label(
    left_content,
    text="✧  PRIVATE BY DESIGN  ✧",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=PURPLE
).pack(side="bottom", pady=10)


# ==================== RIGHT PANEL ====================

right_card = tk.Frame(
    main_frame,
    bg=CARD,
    highlightbackground="#493A62",
    highlightthickness=1
)

right_card.grid(
    row=0,
    column=1,
    sticky="nsew",
    padx=(12, 0)
)

right_content = tk.Frame(right_card, bg=CARD)
right_content.pack(
    fill="both",
    expand=True,
    padx=23,
    pady=25
)


# Password heading

tk.Label(
    right_content,
    text="PASSWORD ANALYZER",
    font=("Segoe UI", 15, "bold"),
    bg=CARD,
    fg=WHITE
).pack(anchor="w")

tk.Label(
    right_content,
    text="Enter a password to check its strength.",
    font=("Segoe UI", 9),
    bg=CARD,
    fg=GREY
).pack(anchor="w", pady=(4, 15))


# Password input

tk.Label(
    right_content,
    text="YOUR PASSWORD",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=LAVENDER
).pack(anchor="w", pady=(0, 7))

password_frame = tk.Frame(right_content, bg=CARD2)
password_frame.pack(fill="x", pady=(0, 15))

password_entry = tk.Entry(
    password_frame,
    font=("Segoe UI", 12),
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    show="*"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=11,
    padx=(12, 0)
)

visibility_button = tk.Button(
    password_frame,
    text="SHOW",
    command=toggle_password,
    bg=CARD2,
    fg=LAVENDER,
    activebackground=CARD2,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    font=("Segoe UI", 8, "bold"),
    cursor="hand2"
)

visibility_button.pack(side="right", padx=12)


# Password length

tk.Label(
    right_content,
    text="GENERATOR LENGTH",
    font=("Segoe UI", 9, "bold"),
    bg=CARD,
    fg=LAVENDER
).pack(anchor="w", pady=(0, 7))

length_entry = tk.Entry(
    right_content,
    font=("Segoe UI", 11),
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

length_entry.insert(0, "12")

length_entry.pack(
    fill="x",
    ipady=9,
    pady=(0, 15)
)


# Action buttons

button_frame = tk.Frame(right_content, bg=CARD)
button_frame.pack(fill="x", pady=(0, 18))

create_button(
    button_frame,
    "ANALYZE",
    analyze_and_display,
    PURPLE
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)

create_button(
    button_frame,
    "GENERATE",
    generate_password,
    "#765B9E"
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

create_button(
    button_frame,
    "COPY",
    copy_password,
    "#514264"
).pack(
    side="left",
    fill="x",
    expand=True,
    padx=(5, 0)
)


# ==================== RESULT CARD ====================

result_card = tk.Frame(
    right_content,
    bg=CARD2,
    highlightbackground="#59476F",
    highlightthickness=1
)

result_card.pack(fill="x", pady=(0, 15))

result_top = tk.Frame(result_card, bg=CARD2)
result_top.pack(
    fill="x",
    padx=15,
    pady=(12, 5)
)

tk.Label(
    result_top,
    text="PASSWORD STRENGTH",
    font=("Segoe UI", 9, "bold"),
    bg=CARD2,
    fg=GREY
).pack(side="left")

score_label = tk.Label(
    result_top,
    text="0/5",
    font=("Segoe UI", 11, "bold"),
    bg=CARD2,
    fg=LAVENDER
)

score_label.pack(side="right")

result_label = tk.Label(
    result_card,
    text="Not Analyzed",
    font=("Segoe UI", 19, "bold"),
    bg=CARD2,
    fg=GREY
)

result_label.pack(
    anchor="w",
    padx=15,
    pady=(0, 10)
)

progress = tk.Canvas(
    result_card,
    height=12,
    bg=CARD2,
    highlightthickness=0
)

progress.pack(
    fill="x",
    padx=15,
    pady=(0, 15)
)


# ==================== ANALYSIS DETAILS ====================

tk.Label(
    right_content,
    text="ANALYSIS DETAILS",
    font=("Segoe UI", 10, "bold"),
    bg=CARD,
    fg=LAVENDER
).pack(anchor="w", pady=(0, 8))

output = tk.Text(
    right_content,
    height=9,
    font=("Consolas", 9),
    bg="#191526",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    wrap="word",
    padx=12,
    pady=12
)

output.pack(
    fill="both",
    expand=True
)

output.config(state="disabled")


# ==================== FOOTER ====================

footer = tk.Frame(root, bg=BG)
footer.pack(fill="x", padx=45, pady=(10, 15))

tk.Button(
    footer,
    text="VIEW PASSWORD HISTORY  ↗",
    command=show_history,
    bg=BG,
    fg=LAVENDER,
    activebackground=BG,
    activeforeground=WHITE,
    relief="flat",
    bd=0,
    font=("Segoe UI", 9, "bold"),
    cursor="hand2"
).pack(side="left")

tk.Label(
    footer,
    text="VELVET VAULT  •  PYTHON PROJECT",
    font=("Segoe UI", 8, "bold"),
    bg=BG,
    fg=GREY
).pack(side="right")


# ==================== RUN APPLICATION ====================

root.mainloop()
