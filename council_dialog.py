"""Local council interaction; no network, execution or automatic approvals."""
import json
import tkinter as tk
from tkinter import messagebox
from council_workspace import CouncilWorkspace

def open_council():
    workspace = CouncilWorkspace()
    root = tk.Tk()
    root.title("LASERSTONE — Advisory Council / مجلس الوكلاء")
    root.geometry("760x620")
    tk.Label(root, text="Manual review only / مراجعة بشرية فقط").pack()
    tk.Label(root, text="Enter JSON task, review, or decision / أدخل بيانات المهمة أو المراجعة").pack()
    entry = tk.Text(root, height=10)
    entry.pack(fill="x", padx=12)
    entry.insert("1.0", '{"id":"T1","summary":"Physics review","specialties":["physics"]}')
    output = tk.Text(root, state="disabled")
    def action(kind):
        try:
            data = json.loads(entry.get("1.0", "end"))
            if not isinstance(data, dict):
                raise ValueError("JSON object required")
            if kind == "task":
                result = workspace.convene(data)
            elif kind == "review":
                result = workspace.submit_review(data)
            else:
                result = workspace.human_decision(data["decision"], data["rationale"])
            output.config(state="normal")
            output.delete("1.0", "end")
            output.insert("1.0", json.dumps(result, ensure_ascii=False, indent=2))
            output.config(state="disabled")
        except (ValueError, KeyError, TypeError) as exc:
            messagebox.showerror("Council / المجلس", str(exc), parent=root)
    buttons = tk.Frame(root)
    buttons.pack()
    for kind, label in (("task","Convene / مهمة"),("review","Review / مراجعة"),("decision","Decision / قرار")):
        tk.Button(buttons, text=label, command=lambda k=kind: action(k)).pack(side="left")
    output.pack(fill="both", expand=True, padx=12, pady=12)
    tk.Label(root, text="Session only; no execution authorization / لا إذن بالتنفيذ").pack()
    root.mainloop()

if __name__ == "__main__":
    open_council()
