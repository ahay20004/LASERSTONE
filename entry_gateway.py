"""Display the prepared session; imports alone never establish readiness."""
import tkinter as tk


def check_system_status(runtime_state=None):
    issues = []
    if runtime_state is None:
        try:
            from main import prepare_runtime
            runtime_state = prepare_runtime()
        except Exception as error:
            issues.append(f"Runtime preparation failed: {error}")
            runtime_state = {}
    from system_health_engine import describe_runtime_state
    evidence = describe_runtime_state(runtime_state.get("ranked_plants", []), runtime_state)
    if evidence["status"] != "ANALYSIS_READY":
        issues.append("No complete checked analysis session")
    try:
        from dashboard import launch_dashboard
        dashboard_imported = callable(launch_dashboard)
        if not dashboard_imported:
            issues.append("Dashboard entry point is not callable")
    except Exception as error:
        dashboard_imported = False
        issues.append(f"Dashboard import error: {error}")
    try:
        from dashboard_city import launch_dashboard as launch_city
        city_imported = callable(launch_city)
    except Exception:
        city_imported = False
    return {
        "status": "ANALYSIS_READY" if not issues else "BLOCKED",
        "issues": issues,
        "plants_count": len(runtime_state.get("ranked_plants", [])),
        "dashboard_ready": dashboard_imported and not issues,
        "city_ready": city_imported and not issues,
        "runtime_state": runtime_state,
    }


def open_entry_gateway(on_approve, on_city=None, runtime_state=None):
    result = check_system_status(runtime_state)
    root = tk.Tk()
    root.title("LASERSTONE ENTRY GATEWAY")
    root.geometry("740x460")
    tk.Label(root, text="LASERSTONE ENTRY GATEWAY", font=("Arial", 16, "bold")).pack(pady=12)
    tk.Label(root, text=f"SYSTEM STATUS: {result['status']}",
             bg="lightgreen" if result["dashboard_ready"] else "khaki",
             font=("Arial", 13, "bold")).pack(pady=8)
    tk.Label(root, text=f"Checked materials: {result['plants_count']}").pack(pady=8)
    text = tk.Text(root, height=12, wrap="word")
    text.pack(fill="both", expand=True, padx=15, pady=10)
    if result["issues"]:
        text.insert("1.0", "Opening blocked:\n" + "\n".join(result["issues"]))
    else:
        text.insert("1.0", "Analysis and ranking completed. Choose a view.\n\n"
                    "Results are heuristic research triage. Physical validation is not established.\n"
                    "Simulator availability does not establish execution or integration.\n"
                    "This preparation has not exported reports or launched a simulator.")
    text.config(state="disabled")
    view_errors = []

    def open_view(callback, ready):
        if not ready:
            return
        # Close this Tk root before creating the selected view's root.
        root.destroy()
        try:
            callback()
        except Exception as error:
            print("VIEW LAUNCH ERROR:", error)
            # Tk catches callback exceptions; propagate after its loop ends so
            # the command-line launcher returns a failure exit status.
            view_errors.append(error)

    buttons = tk.Frame(root)
    buttons.pack(pady=12)
    tk.Button(buttons, text="OPEN DASHBOARD", state="normal" if result["dashboard_ready"] else "disabled",
              command=lambda: open_view(on_approve, result["dashboard_ready"])).pack(side=tk.LEFT, padx=8)
    tk.Button(buttons, text="OPEN SCIENTIFIC CITY",
              state="normal" if result["city_ready"] and on_city else "disabled",
              command=lambda: open_view(on_city, result["city_ready"] and on_city is not None)).pack(side=tk.LEFT, padx=8)
    tk.Button(buttons, text="CLOSE", command=root.destroy).pack(side=tk.LEFT, padx=8)
    root.mainloop()
    if view_errors:
        raise view_errors[0]
    return result
