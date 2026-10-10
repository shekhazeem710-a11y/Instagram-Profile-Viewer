
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import threading
from datetime import datetime

try:
    import instaloader
except ImportError:
    instaloader = None


FIELDS = [
    "Username",
    "Full Name",
    "User ID",
    "Biography",
    "Profile URL",
    "Private Account",
    "Verified",
    "Business Account",
    "Followers",
    "Following",
    "Posts",
    "External URL",
    "Checked At",
]

history = []
current_result = {}


def lookup_profile():
    username = username_entry.get().strip().lstrip("@")

    if not username or "/" in username or " " in username:
        messagebox.showwarning(
            "Invalid username",
            "एक सही Instagram username डालो।"
        )
        return

    if instaloader is None:
        messagebox.showerror(
            "Missing library",
            "पहले इंस्टॉल करो:\n"
            "python -m pip install instaloader"
        )
        return

    search_button.config(state="disabled")
    status_var.set("सार्वजनिक प्रोफ़ाइल की जाँच हो रही है...")
    clear_results()

    threading.Thread(
        target=fetch_profile,
        args=(username,),
        daemon=True
    ).start()


def fetch_profile(username):
    try:
        loader = instaloader.Instaloader(
            quiet=True,
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
        )

        profile = instaloader.Profile.from_username(
            loader.context, username
        )

        data = {
            "Username": profile.username,
            "Full Name": profile.full_name or "",
            "User ID": str(profile.userid),
            "Biography": profile.biography or "",
            "Profile URL": f"https://www.instagram.com/{profile.username}/",
            "Private Account": str(profile.is_private),
            "Verified": str(profile.is_verified),
            "Business Account": str(profile.is_business_account),
            "Followers": str(profile.followers),
            "Following": str(profile.followees),
            "Posts": str(profile.mediacount),
            "External URL": profile.external_url or "",
            "Checked At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        root.after(0, lambda: display_result(data))

    except Exception as error:
        error_text = str(error)[:350]
        root.after(
            0,
            lambda: show_error(error_text)
        )


def display_result(data):
    global current_result

    current_result = data
    history.append(data)

    for key in FIELDS:
        value = data.get(key, "")
        result_tree.insert("", "end", values=(key, value))

    status_var.set("जानकारी प्राप्त हुई।")
    search_button.config(state="normal")
    update_history()


def show_error(error):
    search_button.config(state="normal")
    status_var.set("जानकारी उपलब्ध नहीं है।")

    messagebox.showerror(
        "Profile lookup failed",
        "प्रोफ़ाइल प्राप्त नहीं हो सकी।\n\n"
        "संभव कारण:\n"
        "• Username गलत है\n"
        "• प्रोफ़ाइल उपलब्ध नहीं है\n"
        "• Instagram ने अनुरोध सीमित किया है\n"
        "• लॉगिन या अतिरिक्त अनुमति आवश्यक है\n\n"
        f"विवरण: {error}"
    )


def clear_results():
    for item in result_tree.get_children():
        result_tree.delete(item)


def update_history():
    for item in history_tree.get_children():
        history_tree.delete(item)

    for data in reversed(history):
        history_tree.insert(
            "",
            "end",
            values=(
                data["Username"],
                data["Full Name"],
                data["Followers"],
                data["Following"],
                data["Checked At"],
            )
        )


def show_history():
    history_window.deiconify()
    history_window.lift()
    update_history()


def export_data(filetype):
    if not history:
        messagebox.showinfo(
            "No data",
            "पहले कोई सार्वजनिक प्रोफ़ाइल खोजो।"
        )
        return

    extension = ".csv" if filetype == "csv" else ".txt"

    path = filedialog.asksaveasfilename(
        defaultextension=extension,
        filetypes=[
            ("CSV file", "*.csv"),
            ("Text file", "*.txt"),
        ],
    )

    if not path:
        return

    try:
        if filetype == "csv":
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(history)
        else:
            with open(path, "w", encoding="utf-8") as file:
                for data in history:
                    file.write("=" * 45 + "\n")
                    for key in FIELDS:
                        file.write(f"{key}: {data.get(key, '')}\n")
                    file.write("\n")

        messagebox.showinfo("Saved", f"फ़ाइल सेव हो गई:\n{path}")

    except OSError as error:
        messagebox.showerror("Save error", str(error))


def copy_result():
    if not current_result:
        messagebox.showinfo("No data", "पहले प्रोफ़ाइल खोजो।")
        return

    text = "\n".join(
        f"{key}: {current_result.get(key, '')}"
        for key in FIELDS
    )

    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

    status_var.set("जानकारी कॉपी हो गई।")


def clear_history():
    if messagebox.askyesno(
        "Clear history",
        "क्या पूरी search history हटानी है?"
    ):
        history.clear()
        update_history()


root = tk.Tk()
root.title("Instagram Public Profile Tool")
root.geometry("900x690")
root.minsize(700, 520)
root.configure(bg="#10141c")

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background="#1b2330",
    foreground="white",
    fieldbackground="#1b2330",
    rowheight=27,
)
style.configure(
    "Treeview.Heading",
    background="#303c50",
    foreground="white",
)
style.configure(
    "TNotebook",
    background="#10141c",
)
style.configure(
    "TNotebook.Tab",
    padding=(16, 8),
)

tk.Label(
    root,
    text="Instagram Public Profile Tool",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#10141c",
).pack(pady=(20, 5))

tk.Label(
    root,
    text="Public profile metadata • No session ID required",
    font=("Arial", 10),
    fg="#aab5c5",
    bg="#10141c",
).pack(pady=(0, 15))

input_frame = tk.Frame(root, bg="#1b2330", padx=15, pady=15)
input_frame.pack(fill="x", padx=20)

tk.Label(
    input_frame,
    text="Instagram username:",
    font=("Arial", 11, "bold"),
    fg="white",
    bg="#1b2330",
).pack(side="left", padx=(0, 10))

username_entry = tk.Entry(
    input_frame,
    font=("Arial", 13),
    bg="#303c50",
    fg="white",
    insertbackground="white",
    relief="flat",
)
username_entry.pack(side="left", fill="x", expand=True, ipady=7)

search_button = tk.Button(
    input_frame,
    text="Search",
    command=lookup_profile,
    font=("Arial", 11, "bold"),
    bg="#d62976",
    fg="white",
    activebackground="#b91d60",
    relief="flat",
    padx=18,
    pady=7,
)
search_button.pack(side="left", padx=(10, 0))

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=15)

result_tab = tk.Frame(notebook, bg="#10141c")
history_tab = tk.Frame(notebook, bg="#10141c")

notebook.add(result_tab, text="Profile Results")
notebook.add(history_tab, text="Search History")

result_tree = ttk.Treeview(
    result_tab,
    columns=("Property", "Value"),
    show="headings",
)
result_tree.heading("Property", text="Property")
result_tree.heading("Value", text="Value")
result_tree.column("Property", width=180, anchor="w")
result_tree.column("Value", width=600, anchor="w")

result_scroll = ttk.Scrollbar(
    result_tab,
    orient="vertical",
    command=result_tree.yview,
)
result_tree.configure(yscrollcommand=result_scroll.set)
result_tree.pack(side="left", fill="both", expand=True)
result_scroll.pack(side="right", fill="y")

history_tree = ttk.Treeview(
    history_tab,
    columns=("Username", "Name", "Followers", "Following", "Checked"),
    show="headings",
)

for column, width in [
    ("Username", 130),
    ("Name", 160),
    ("Followers", 100),
    ("Following", 100),
    ("Checked", 170),
]:
    history_tree.heading(column, text=column)
    history_tree.column(column, width=width)

history_tree.pack(fill="both", expand=True)

history_window = tk.Toplevel(root)
history_window.title("Search History")
history_window.geometry("750x350")
history_window.withdraw()

buttons = tk.Frame(root, bg="#10141c")
buttons.pack(pady=(0, 10))

tk.Button(
    buttons,
    text="Copy Result",
    command=copy_result,
    bg="#48566a",
    fg="white",
    relief="flat",
    padx=12,
    pady=7,
).pack(side="left", padx=4)

tk.Button(
    buttons,
    text="Export TXT",
    command=lambda: export_data("txt"),
    bg="#087f70",
    fg="white",
    relief="flat",
    padx=12,
    pady=7,
).pack(side="left", padx=4)

tk.Button(
    buttons,
    text="Export CSV",
    command=lambda: export_data("csv"),
    bg="#1769aa",
    fg="white",
    relief="flat",
    padx=12,
    pady=7,
).pack(side="left", padx=4)

tk.Button(
    buttons,
    text="Open History",
    command=show_history,
    bg="#48566a",
    fg="white",
    relief="flat",
    padx=12,
    pady=7,
).pack(side="left", padx=4)

tk.Button(
    buttons,
    text="Clear History",
    command=clear_history,
    bg="#a52a3a",
    fg="white",
    relief="flat",
    padx=12,
    pady=7,
).pack(side="left", padx=4)

status_var = tk.StringVar(value="Ready")
tk.Label(
    root,
    textvariable=status_var,
    fg="#aab5c5",
    bg="#10141c",
).pack(pady=(0, 10))

root.bind("<Return>", lambda event: lookup_profile())
username_entry.focus()

root.mainloop()
