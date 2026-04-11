# ===================== MODULES =====================
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os
from collections import Counter


# ===================== FILE HANDLING =====================
FILE = "data.json"

def load_data():
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


# ===================== DICTIONARIES =====================
# Example structure:
"""
{
    "problem": "Two Sum",
    "platform": "LeetCode",
    "difficulty": "Easy",
    "topic": "Arrays",
    "date": "2026-04-11"
}
"""


# ===================== FUNCTIONS =====================

# Add Entry
def add_entry(problem, platform, difficulty, topic):
    try:
        data = load_data()

        entry = {
            "problem": problem,
            "platform": platform,
            "difficulty": difficulty if difficulty else "Unknown",
            "topic": topic if topic else "General",
            "date": datetime.now().strftime("%Y-%m-%d")
        }

        data.append(entry)
        save_data(data)

        return True
    except Exception as e:
        print("Error:", e)
        return False


# View Entries
def get_entries():
    return load_data()


# ===================== SETS + ANALYTICS =====================
def get_analytics():
    data = load_data()

    if not data:
        return "No data available"

    total = len(data)

    # Difficulty count
    difficulties = [d["difficulty"] for d in data]
    diff_count = Counter(difficulties)

    # Topic analysis
    topics = [d["topic"] for d in data]
    topic_count = Counter(topics)

    min_count = min(topic_count.values())
    weak_topics = [t for t in topic_count if topic_count[t] == min_count]

    # SET used to remove duplicate dates
    dates = sorted(set(d["date"] for d in data))
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]

    streak = 1
    max_streak = 1

    for i in range(1, len(dates)):
        if (dates[i] - dates[i-1]).days == 1:
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1

    return f"""
Total Solved: {total}

Difficulty:
{dict(diff_count)}

Weak Topics:
{weak_topics}

🔥 Streak:
{max_streak} days
"""


# ===================== GUI FUNCTIONS =====================
def handle_add():
    problem = entry_problem.get()
    platform = entry_platform.get()
    difficulty = difficulty_var.get()
    topic = entry_topic.get()

    if not problem or not platform:
        messagebox.showerror("Error", "Fill required fields")
        return

    success = add_entry(problem, platform, difficulty, topic)

    if success:
        messagebox.showinfo("Success", "Entry Added")
        clear_fields()
    else:
        messagebox.showerror("Error", "Failed to add entry")


def handle_view():
    data = get_entries()
    text_area.delete("1.0", tk.END)

    if not data:
        text_area.insert(tk.END, "No entries found\n")
        return

    for d in data:
        line = f"{d['problem']} | {d['platform']} | {d['difficulty']} | {d['topic']} | {d['date']}\n"
        text_area.insert(tk.END, line)


def handle_analytics():
    result = get_analytics()
    messagebox.showinfo("Analytics", result)


def clear_fields():
    entry_problem.delete(0, tk.END)
    entry_platform.delete(0, tk.END)
    entry_topic.delete(0, tk.END)


# ===================== GUI (TKINTER) =====================
root = tk.Tk()
root.title("CodeTrack Pro")
root.geometry("600x500")

tk.Label(root, text="Problem").pack()
entry_problem = tk.Entry(root)
entry_problem.pack()

tk.Label(root, text="Platform").pack()
entry_platform = tk.Entry(root)
entry_platform.pack()

tk.Label(root, text="Difficulty").pack()
difficulty_var = tk.StringVar()
tk.OptionMenu(root, difficulty_var, "Easy", "Medium", "Hard").pack()

tk.Label(root, text="Topic").pack()
entry_topic = tk.Entry(root)
entry_topic.pack()

tk.Button(root, text="Add Entry", command=handle_add).pack(pady=5)
tk.Button(root, text="View Entries", command=handle_view).pack(pady=5)
tk.Button(root, text="Show Analytics", command=handle_analytics).pack(pady=5)

text_area = tk.Text(root, height=15)
text_area.pack()

root.mainloop()
