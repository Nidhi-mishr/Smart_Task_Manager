import tkinter as tk
from tkinter import ttk, messagebox
import psutil

class EnhancedProcessTab:
    def __init__(self, parent):
        self.parent = parent
        self.processes = []
        self.setup_process_management_ui()

    def setup_process_management_ui(self):
        self.proc_tree = ttk.Treeview(self.parent, columns=('PID', 'Name', 'CPU', 'Memory', 'Status'), show='headings')
        for col in self.proc_tree["columns"]:
            self.proc_tree.heading(col, text=col)
            self.proc_tree.column(col, width=120)
        self.proc_tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.refresh_btn = tk.Button(self.parent, text="Refresh", command=self.refresh_process_list)
        self.refresh_btn.pack(pady=5)

        self.kill_btn = tk.Button(self.parent, text="End Task", command=self.kill_process)
        self.kill_btn.pack(pady=5)

        self.suspend_btn = tk.Button(self.parent, text="Suspend", command=self.suspend_process)
        self.suspend_btn.pack(pady=5)

        self.resume_btn = tk.Button(self.parent, text="Resume", command=self.resume_process)
        self.resume_btn.pack(pady=5)

        self.refresh_process_list()

    def refresh_process_list(self):
        for row in self.proc_tree.get_children():
            self.proc_tree.delete(row)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                self.proc_tree.insert('', 'end', values=(info['pid'], info['name'], f"{info['cpu_percent']}%", f"{info['memory_percent']}%", info['status']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def get_selected_pid(self):
        selected = self.proc_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "No process selected.")
            return None
        return int(self.proc_tree.item(selected[0])['values'][0])

    def kill_process(self):
        pid = self.get_selected_pid()
        if pid is not None:
            try:
                psutil.Process(pid).terminate()
                self.refresh_process_list()
                messagebox.showinfo("Success", f"Process {pid} terminated.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def suspend_process(self):
        pid = self.get_selected_pid()
        if pid is not None:
            try:
                psutil.Process(pid).suspend()
                self.refresh_process_list()
                messagebox.showinfo("Success", f"Process {pid} suspended.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def resume_process(self):
        pid = self.get_selected_pid()
        if pid is not None:
            try:
                psutil.Process(pid).resume()
                self.refresh_process_list()
                messagebox.showinfo("Success", f"Process {pid} resumed.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
