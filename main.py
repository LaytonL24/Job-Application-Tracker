"""
Job Application Tracker

A simple GUI application built with CustomTkinter to track job applications.
Features:
- Add, edit, delete applications
- Search and filter applications by company, date, and status
- Select all / individual row selection
- Export data to CSV
- Graphs placeholder for future implementation
"""

from customtkinter import *
import csv

# -------------------- Global -----------------------
rows = []  # Stores all application rows with their data and checkbox state

# -------------------- Functions --------------------
def add_app(edit_row=None):
    """
    Opens a modal window to add a new application or edit an existing one.
    
    Args:
        edit_row (dict, optional): Row to edit. Defaults to None.
    """
    modal = CTkToplevel(root); modal.geometry("400x380"); modal.title("Add Application"); modal.grab_set()
    CTkButton(modal, text="X", width=30, fg_color="#dc2626", hover_color="#b91c1c", command=modal.destroy).place(x=360, y=10)

    # Fields with max lengths for truncation
    fields = [("Company", 20), ("Role", 20), ("Location", 15), ("Follow-Up", 25)]
    entries = {}

    for i, (label_text, max_len) in enumerate(fields):
        CTkLabel(modal, text=label_text).place(x=20, y=50 + i*40)
        var = StringVar(); CTkEntry(modal, width=250, textvariable=var).place(x=120, y=50 + i*40)
        if edit_row: var.set(edit_row["data"].get(label_text,""))
        entries[label_text] = (var, max_len)

    # Dropdown fields
    applied_var = StringVar(value="Today"); status_var = StringVar(value="Applied")
    CTkLabel(modal, text="Applied").place(x=20, y=50 + len(fields)*40)
    CTkOptionMenu(modal, values=["Today","Yesterday","Last 7 Days","Older"], variable=applied_var, width=250).place(x=120, y=50 + len(fields)*40)
    CTkLabel(modal, text="Status").place(x=20, y=90 + len(fields)*40)
    CTkOptionMenu(modal, values=["Applied","Interview","Rejected","Offer"], variable=status_var, width=250).place(x=120, y=90 + len(fields)*40)
    if edit_row:
        applied_var.set(edit_row["data"].get("Applied","Today"))
        status_var.set(edit_row["data"].get("Status","Applied"))

    def save_application():
        """Collects data from modal and adds/updates a row in the table."""
        data = {label: var.get()[:max_len] for label, (var, max_len) in entries.items()}
        data["Applied"] = applied_var.get(); data["Status"] = status_var.get()
        add_row(edit_row, data); modal.destroy()

    CTkButton(modal, text="Save", width=150, command=save_application).place(x=120, y=330)


def add_row(edit_row, data):
    """
    Adds a new row to the applications table or updates an existing row.

    Args:
        edit_row (dict or None): If editing, the row to update.
        data (dict): Dictionary containing application info.
    """
    var = BooleanVar()
    if edit_row:
        row = edit_row["frame"]
        for w in row.winfo_children(): w.destroy()
        rows.remove(edit_row)
    else:
        row = CTkFrame(applications_frame); row.pack(fill="x", pady=2)

    row.grid_columnconfigure(0, weight=0)
    for col in range(1,7): row.grid_columnconfigure(col, weight=1)
    CTkCheckBox(row, text="", variable=var).grid(row=0, column=0, padx=10)
    fields = ["Company","Role","Location","Applied","Status","Follow-Up"]
    for col,key in enumerate(fields,start=1): CTkLabel(row,text=data[key],anchor="w").grid(row=0,column=col,sticky="nsew",padx=(4,10))
    rows.append({"var": var, "frame": row, "data": data})


def del_app():
    """Deletes selected application rows."""
    for r in rows[:]:
        if r["var"].get(): r["frame"].destroy(); rows.remove(r)


def select_all_app():
    """Selects or deselects all rows based on the header checkbox."""
    for r in rows: r["var"].set(select_all_var.get())


def edit_selected():
    """Opens the edit modal for the single selected row."""
    selected = [r for r in rows if r["var"].get()]
    if len(selected) == 1: add_app(edit_row=selected[0])


def apply_filters(*args):
    """Applies search, date, and status filters to the applications table."""
    search = search_var.get().lower(); date_val = date_filter_var.get(); status_val = status_filter_var.get()
    for r in rows:
        data = r["data"]; show = True
        if search and search not in data["Company"].lower(): show = False
        if status_val != "All Statuses" and data["Status"] != status_val: show = False
        if date_val != "All Dates" and data["Applied"] != date_val: show = False
        if show: r["frame"].pack(fill="x", pady=2)
        else: r["frame"].pack_forget()


def export_csv():
    """Exports all application data to a CSV file."""
    with open("applications_export.csv","w",newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Company","Role","Location","Applied","Status","Follow-Up"])
        for r in rows:
            data = r["data"]
            writer.writerow([data["Company"],data["Role"],data["Location"],data["Applied"],data["Status"],data["Follow-Up"]])


def show_frame(frame):
    """
    Switches visible frame (tab) between Applications, Graphs, or Settings.

    Args:
        frame (CTkFrame): Frame to show.
    """
    for f in [applications_frame, graphs_frame, settings_frame]: f.pack_forget()
    frame.pack(fill="both", expand=True)


# -------------------- App Setup --------------------
set_appearance_mode("light"); set_default_color_theme("blue")
root = CTk(); root.geometry("1100x650"); root.resizable(False,False); root.title("Job Application Tracker")

# -------------------- Layout --------------------
menu_frame = CTkFrame(root, width=200, corner_radius=0); menu_frame.pack(side="left", fill="y")
content_frame = CTkFrame(root, fg_color="transparent"); content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

# Menu Buttons
CTkLabel(menu_frame, text="Menu", font=("Cursive",40,"bold")).pack(pady=(80,100))
CTkButton(menu_frame,text="Applications",height=40,command=lambda: show_frame(applications_frame)).pack(pady=10,padx=20,fill="x")
CTkButton(menu_frame,text="Graphs",height=40,command=lambda: show_frame(graphs_frame)).pack(pady=10,padx=20,fill="x")
CTkButton(menu_frame,text="Settings",height=40,command=lambda: show_frame(settings_frame)).pack(pady=10,padx=20,fill="x")

# -------------------- Applications Frame --------------------
applications_frame = CTkFrame(content_frame, fg_color="transparent"); applications_frame.pack(fill="both", expand=True)
header_frame = CTkFrame(applications_frame, fg_color="transparent"); header_frame.pack(fill="x")
CTkLabel(header_frame, text="Applications", font=("Arial",32,"bold")).pack(side="left", pady=30)
action_frame = CTkFrame(header_frame, fg_color="transparent"); action_frame.pack(side="right")
CTkButton(action_frame,text="+ Add Application",command=add_app).pack(side="left", padx=5)
CTkButton(action_frame,text="Edit Selected",command=edit_selected).pack(side="left", padx=5)
CTkButton(action_frame,text="Delete Selected",fg_color="#dc2626",hover_color="#b91c1c",command=del_app).pack(side="left", padx=5)

filter_frame = CTkFrame(applications_frame); filter_frame.pack(fill="x", pady=10)
search_var = StringVar(); search_var.trace_add("write", apply_filters)
date_filter_var = StringVar(value="All Dates"); status_filter_var = StringVar(value="All Statuses")
CTkEntry(filter_frame, placeholder_text="Search company...", width=500, textvariable=search_var).pack(side="left", padx=10)
CTkOptionMenu(filter_frame, values=["All Dates","Today","Yesterday","Last 7 Days","Older"], variable=date_filter_var, command=lambda _: apply_filters()).pack(side="left", padx=15)
CTkOptionMenu(filter_frame, values=["All Statuses","Applied","Interview","Rejected","Offer"], variable=status_filter_var, command=lambda _: apply_filters()).pack(side="left", padx=15)

table_wrapper = CTkFrame(applications_frame, fg_color="#f1f3f5", corner_radius=8); table_wrapper.pack(fill="both", expand=True, pady=15)
table_wrapper.grid_rowconfigure(1, weight=1); table_wrapper.grid_columnconfigure(0, weight=1)
header_row = CTkFrame(table_wrapper, fg_color="#e9ecef", height=45); header_row.grid(row=0, column=0, sticky="nsew"); header_row.grid_propagate(False)
select_all_var = BooleanVar(); CTkCheckBox(header_row,text="",variable=select_all_var,command=select_all_app).grid(row=0,column=0,padx=10)
headers = ["Company","Role","Location","Applied","Status","Follow-Up"]; header_row.grid_columnconfigure(0,weight=0)
for i in range(1,len(headers)+1): header_row.grid_columnconfigure(i,weight=1)
for col,text in enumerate(headers,start=1): CTkLabel(header_row,text=text,font=("Arial",13,"bold"),anchor="w").grid(row=0,column=col,sticky="nsew",padx=(4,10))
table_body = CTkScrollableFrame(table_wrapper, fg_color="transparent"); table_body.grid(row=1,column=0,sticky="nsew")

# -------------------- Graphs Placeholder --------------------
graphs_frame = CTkFrame(content_frame, fg_color="transparent")
CTkLabel(graphs_frame, text="Graphs coming soon 📊", font=("Arial",24,"bold")).pack(expand=True)

# -------------------- Settings --------------------
settings_frame = CTkFrame(content_frame, fg_color="transparent")
CTkButton(settings_frame, text="Export to CSV", command=export_csv).pack(pady=20)

# -------------------- Run App --------------------
root.mainloop()