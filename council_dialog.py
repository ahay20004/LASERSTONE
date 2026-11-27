"""Local human-operated council workspace; no network or execution."""
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from council_workspace import CouncilWorkspace
from agent_council import ROLES

def open_council():
    from local_unified_view import build
    import webbrowser
    workspace = CouncilWorkspace()
    root = tk.Tk()
    root.title("LASERSTONE | مجلس الوكلاء")
    root.geometry("850x720")
    root.minsize(640, 520)
    header = tk.Frame(root, bg="#102b47", padx=20, pady=18)
    header.pack(fill="x")
    tk.Label(header, text="LASERSTONE™", font=("Segoe UI",22,"bold"), bg="#102b47", fg="#9de5ee").pack(anchor="w")
    tk.Label(header, text="Scientific Advisory Council | مجلس المراجعة العلمية", bg="#102b47", fg="white").pack(anchor="w")
    def open_scientific_view():
        try:
            if not webbrowser.open(build().as_uri()):
                raise OSError("Browser could not be opened")
        except (OSError, ValueError) as exc:
            messagebox.showerror("LASERSTONE", str(exc), parent=root)
    ttk.Button(root, text="Scientific platform | المنصة العلمية", command=open_scientific_view).pack(anchor="e", padx=16, pady=6)
    tabs = ttk.Notebook(root)
    tabs.pack(fill="x", padx=16, pady=12)
    task, rev, dec = [ttk.Frame(tabs,padding=12) for _ in range(3)]
    for frame, name in zip((task,rev,dec),("Task | المهمة","Review | المراجعة","Decision | القرار")):
        tabs.add(frame,text=name)
    def field(frame,label):
        ttk.Label(frame,text=label).pack(anchor="w")
        v=tk.StringVar()
        ttk.Entry(frame,textvariable=v).pack(fill="x",pady=(0,6))
        return v
    ident=field(task,"Task ID | معرف المهمة")
    summary=field(task,"Summary | وصف المهمة")
    roles={role:tk.BooleanVar() for role in ROLES}
    for role,var in roles.items():
        ttk.Checkbutton(task,text=role,variable=var).pack(anchor="w")
    reviewer=field(rev,"Assigned reviewer | المراجع المكلف")
    position=tk.StringVar(value="revise")
    ttk.Combobox(rev,textvariable=position,values=("approve","revise","reject"),state="readonly").pack(fill="x")
    reason=field(rev,"Rationale | المبررات")
    evidence=field(rev,"Evidence references, separated by semicolons | الأدلة")
    decision=tk.StringVar(value="revise")
    ttk.Combobox(dec,textvariable=decision,values=("approve","revise","reject"),state="readonly").pack(fill="x")
    rationale=field(dec,"Human rationale | مبررات القرار البشري")
    output=tk.Text(root,state="disabled",wrap="word",height=10)
    status=tk.StringVar(value="Awaiting task | في انتظار المهمة")
    def perform(fn):
        try:
            result=fn()
            output.config(state="normal")
            output.delete("1.0","end")
            output.insert("1.0",json.dumps(result,ensure_ascii=False,indent=2))
            output.config(state="disabled")
            status.set(result.get("review_status","Recorded")+" | Execution: NONE")
        except (ValueError,KeyError,TypeError,OSError) as exc:
            messagebox.showerror("Council | المجلس",str(exc),parent=root)
    ttk.Button(task,text="Convene | تسجيل المهمة",command=lambda:perform(lambda:workspace.convene({"id":ident.get(),"summary":summary.get(),"specialties":[r for r,v in roles.items() if v.get()]}))).pack(anchor="e")
    ttk.Button(rev,text="Submit review | تسجيل المراجعة",command=lambda:perform(lambda:workspace.submit_review({"reviewer":reviewer.get(),"position":position.get(),"reason":reason.get(),"evidence":[s.strip() for s in evidence.get().split(";") if s.strip()]}))).pack(anchor="e")
    ttk.Button(dec,text="Record decision | تسجيل القرار",command=lambda:perform(lambda:workspace.human_decision(decision.get(),rationale.get()))).pack(anchor="e")
    files=ttk.Frame(root)
    files.pack(fill="x",padx=16)
    def save_session():
        path=filedialog.asksaveasfilename(parent=root,defaultextension=".json",filetypes=[("Council JSON","*.json")])
        if path:
            try:
                workspace.export(path)
                status.set("Session saved | تم الحفظ")
            except (OSError,ValueError,TypeError) as exc:
                messagebox.showerror("Council | المجلس",str(exc),parent=root)
    def restore_session():
        path=filedialog.askopenfilename(parent=root,filetypes=[("Council JSON","*.json")])
        if path:
            perform(lambda:workspace.restore(path))
    ttk.Button(files,text="Save session | حفظ الجلسة",command=save_session).pack(side="left")
    ttk.Button(files,text="Restore session | استعادة الجلسة",command=restore_session).pack(side="left",padx=8)
    ttk.Label(root,textvariable=status).pack(anchor="w",padx=16)
    output.pack(fill="both",expand=True,padx=16,pady=8)
    ttk.Label(root,text="Local files are not authenticated • No verified AI agents • No execution authorization").pack(pady=8)
    root.mainloop()

if __name__=="__main__":
    open_council()
