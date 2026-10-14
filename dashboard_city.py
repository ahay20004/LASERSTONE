import tkinter as tk
from tkinter import ttk, messagebox

from recommendation_engine import generate_recommendations
from executive_summary_engine import generate_executive_summary
from project_registry import PROJECT_REGISTRY


def safe_score(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def draw_bar_chart(canvas, ranked_plants, key, title=None):
    canvas.delete("all")
    x_start = 80
    y_base = 180
    bar_width = 75
    gap = 45
    max_bar_height = 125

    scores = []
    for plant in ranked_plants:
        if key == "intelligence_score":
            score = plant.get("intelligence_summary", {}).get("intelligence_score", 0)
        else:
            score = plant.get(key, 0)
        scores.append(safe_score(score))

    max_score = max(scores) if scores else 1
    if max_score <= 0:
        max_score = 1

    canvas.create_text(550, 20, text=title or key, font=("Arial", 12, "bold"))

    for index, plant in enumerate(ranked_plants):
        score = scores[index]
        name = plant.get("name", "Unknown")

        bar_height = (score / max_score) * max_bar_height
        x1 = x_start + index * (bar_width + gap)
        y1 = y_base - bar_height
        x2 = x1 + bar_width
        y2 = y_base

        canvas.create_rectangle(x1, y1, x2, y2)
        canvas.create_text(x1 + bar_width / 2, y1 - 10, text=f"{score:.2f}", font=("Arial", 9, "bold"))
        canvas.create_text(x1 + bar_width / 2, y_base + 18, text=name, font=("Arial", 8))

    canvas.create_line(50, y_base, 1060, y_base)


def open_text_window(parent, title, report, geometry="760x560"):
    report_window = tk.Toplevel(parent)
    report_window.title(title)
    report_window.geometry(geometry)

    text_box = tk.Text(report_window, wrap="word", font=("Arial", 11))
    text_box.pack(fill="both", expand=True, padx=10, pady=10)
    text_box.insert("1.0", report)
    text_box.config(state="disabled")


def launch_dashboard(ranked_plants, runtime_state=None):
    print("CITY DASHBOARD STARTED")
    window = tk.Tk()
    window.title("LASERSTONE™ Scientific City")
    window.geometry("1350x1000")

    total_materials = len(ranked_plants)
    from system_health_engine import describe_runtime_state, format_runtime_evidence
    evidence = describe_runtime_state(ranked_plants, runtime_state, PROJECT_REGISTRY)
    total_engines = evidence["registered_engines"]
    connected_engines = evidence["declared_connected"]
    isolated_engines = evidence["declared_isolated"]
    platform_maturity = evidence["declared_connectivity_percent"]
    system_status = evidence["status"]
    platform_class = "HEURISTIC RESEARCH TRIAGE"

    top_material = ranked_plants[0] if ranked_plants else {}

    best_intelligence = (
        max(
            ranked_plants,
            key=lambda plant: plant.get("intelligence_summary", {}).get("intelligence_score", 0)
        )
        if ranked_plants else {}
    )

    best_patent = (
        max(ranked_plants, key=lambda plant: plant.get("patent_potential_score", 0))
        if ranked_plants else {}
    )

    recommendations = generate_recommendations(ranked_plants)

    def top_value(key, default="N/A"):
        return top_material.get(key, default)

    def show_system_integrity():
        report = format_runtime_evidence(evidence)
        open_text_window(window, "LASERSTONE SYSTEM INTEGRITY", report, "620x460")

    def show_knowledge_center():
        report = (
            "LASERSTONE KNOWLEDGE CENTER\n\n"
            f"Total Materials: {total_materials}\n\n"
            f"Top Material: {top_value('name')}\n"
            f"Best Intelligence: {best_intelligence.get('name', 'N/A')}\n"
            f"Best Patent Candidate: {best_patent.get('name', 'N/A')}\n\n"
            "Knowledge Status: ACTIVE\n"
            "Plant Database: AVAILABLE\n"
            "Reference Layer: AVAILABLE\n"
            "Plant Profiles: AVAILABLE\n\n"
            "Platform Knowledge Level: EXPANDING\n"
        )
        open_text_window(window, "LASERSTONE KNOWLEDGE CENTER", report)

    def show_material_analysis():
        average_score = 0
        if ranked_plants:
            average_score = sum(safe_score(plant.get("material_score", 0)) for plant in ranked_plants) / len(ranked_plants)

        report = (
            "LASERSTONE MATERIAL ANALYSIS\n\n"
            f"Top Material: {top_value('name')}\n"
            f"Material Score: {safe_score(top_value('material_score', 0)):.2f}\n"
            f"Material Class: {top_value('material_class')}\n\n"
            "TOP 3 MATERIALS\n\n"
        )

        for plant in ranked_plants[:3]:
            report += (
                f"{plant.get('global_rank', '-')}. "
                f"{plant.get('name', 'Unknown')} | "
                f"Score: {safe_score(plant.get('material_score', 0)):.2f}\n"
            )

        report += (
            f"\nAverage Material Score: {average_score:.2f}\n\n"
            "Platform Recommendation:\n"
            "Focus on the highest-ranked materials for prototype and optimization studies.\n"
        )
        open_text_window(window, "LASERSTONE MATERIAL ANALYSIS", report)

    def show_physics_evidence():
        report = (
            "LASERSTONE PHYSICS EVIDENCE\n\n"
            f"Top Material: {top_value('name')}\n\n"
            f"Physics Consistency Score: {top_value('physics_consistency_score')}\n"
            f"Physics Consistency Class: {top_value('physics_consistency_class')}\n\n"
            f"Scientific Confidence Score: {top_value('scientific_confidence_score')}\n"
            f"Scientific Confidence Class: {top_value('scientific_confidence_class')}\n\n"
            f"Experimental Success Score: {top_value('experimental_success_score')}\n"
            f"System Integrity Score: {top_value('system_integrity_score')}\n\n"
            "Physics Assessment:\n"
            "The physics layer supports the scientific ranking through consistency, confidence, and validation indicators.\n"
        )
        open_text_window(window, "LASERSTONE PHYSICS EVIDENCE", report)

    def show_executive_decision():
        report = (
            "LASERSTONE EXECUTIVE DECISION CENTER\n\n"
            f"TOP MATERIAL: {top_value('name')}\n\n"
            f"GLOBAL RANK: #{top_value('global_rank')}\n"
            f"MATERIAL SCORE: {top_value('material_score')}\n"
            f"PHYSICS CONSISTENCY: {top_value('physics_consistency_score')}\n"
            f"SCIENTIFIC CONFIDENCE: {top_value('scientific_confidence_score')}\n"
            f"EXPERIMENTAL SUCCESS: {top_value('experimental_success_score')}\n"
            f"SYSTEM INTEGRITY: {top_value('system_integrity_score')}\n\n"
            f"GOVERNOR DECISION:\n{top_value('governor_decision')}\n\n"
            "STRATEGIC STATUS:\nHIGH PRIORITY RESEARCH CANDIDATE\n\n"
            "NEXT ACTION:\nContinue experimental validation before prototype deployment."
        )
        open_text_window(window, "LASERSTONE EXECUTIVE DECISION CENTER", report)

    def show_repair_advisor():
        report = (
            "LASERSTONE REPAIR ADVISOR\n\n"
            f"Top Material: {top_value('name')}\n\n"
            "Detected Improvement Areas:\n\n"
            f"Experimental Success Score: {top_value('experimental_success_score')}\n"
            f"Patent Potential Score: {top_value('patent_potential_score')}\n"
            f"Research Novelty Score: {top_value('research_novelty_score')}\n\n"
            "Recommended Actions:\n\n"
            "1. Increase experimental validation.\n"
            "2. Improve prototype verification.\n"
            "3. Explore patent opportunities.\n"
            "4. Expand novelty and innovation studies.\n\n"
            "Repair Status:\nSYSTEM READY FOR OPTIMIZATION"
        )
        open_text_window(window, "LASERSTONE REPAIR ADVISOR", report)

    def show_scientific_repository():
        report = (
            "LASERSTONE SCIENTIFIC REPOSITORY\n\n"
            f"Registered Materials: {total_materials}\n"
            f"Total Engines: {total_engines}\n"
            f"Connected Engines: {connected_engines}\n\n"
            f"Top Material: {top_value('name')}\n"
            f"Best Patent Candidate: {best_patent.get('name', 'N/A')}\n\n"
            "Knowledge Status: AVAILABLE\n"
            "Repository Status: ACTIVE\n\n"
            "Scientific Assets:\n"
            "- Material Database\n"
            "- Intelligence Layer\n"
            "- Physics Evidence Layer\n"
            "- Executive Decision Layer\n"
        )
        open_text_window(window, "LASERSTONE SCIENTIFIC REPOSITORY", report)

    def show_discovery_center():
        report = (
            "LASERSTONE DISCOVERY CENTER\n\n"
            f"Discovery Candidate: {top_value('name')}\n\n"
            f"Research Novelty: {top_value('research_novelty_score')}\n"
            f"Patent Potential: {top_value('patent_potential_score')}\n"
            f"Scientific Confidence: {top_value('scientific_confidence_score')}\n\n"
            "Future Research Directions:\n\n"
            "1. Experimental validation\n"
            "2. Optical gain investigation\n"
            "3. Prototype development\n"
            "4. Patent exploration\n\n"
            "Discovery Status: ACTIVE"
        )
        open_text_window(window, "LASERSTONE DISCOVERY CENTER", report)

    def build_engine_group_report(title, subtitle, engine_names):
        report = f"{title}\n\n{subtitle}\n\n"
        for index, engine_name in enumerate(engine_names, start=1):
            info = PROJECT_REGISTRY.get(engine_name, {})
            inputs = ", ".join(info.get("inputs", []))
            outputs = ", ".join(info.get("outputs", []))
            report += (
                f"{index}. {engine_name}\n"
                f"Category: {info.get('category', 'N/A')}\n"
                f"Status: {info.get('status', 'N/A')}\n"
                f"Inputs: {inputs if inputs else 'N/A'}\n"
                f"Outputs: {outputs if outputs else 'N/A'}\n"
                + "-" * 55 + "\n"
            )
        return report

    def show_engine_hall_of_fame():
        report = "LASERSTONE ENGINE HALL OF FAME\n\n"
        report += f"Total Registered Engines: {len(PROJECT_REGISTRY)}\n\n"
        if PROJECT_REGISTRY:
            for index, (engine_name, info) in enumerate(PROJECT_REGISTRY.items(), start=1):
                report += (
                    f"{index}. {engine_name}\n"
                    f"Category: {info.get('category', 'N/A')}\n"
                    f"Status: {info.get('status', 'N/A')}\n"
                    + "-" * 55 + "\n"
                )
        else:
            report += "Registry data is not available in this runtime.\n"
        open_text_window(window, "LASERSTONE ENGINE HALL OF FAME", report, "900x700")

    def show_kingdom_guardians():
        engine_names = [
            "project_health_engine",
            "system_health_engine",
            "system_integrity_engine",
            "runtime_monitor_engine",
            "network_intelligence_engine",
        ]
        report = build_engine_group_report(
            "LASERSTONE KINGDOM GUARDIANS",
            "SYSTEM PROTECTION AND MONITORING LAYER",
            engine_names
        )
        open_text_window(window, "LASERSTONE KINGDOM GUARDIANS", report, "900x700")

    def show_physics_core_hall():
        engine_names = [
            "physics_consistency_engine",
            "scientific_confidence_engine",
            "research_novelty_engine",
            "patent_potential_engine",
        ]
        report = build_engine_group_report(
            "LASERSTONE PHYSICS CORE HALL",
            "SCIENTIFIC VALIDATION AND CONFIDENCE LAYER",
            engine_names
        )
        open_text_window(window, "LASERSTONE PHYSICS CORE HALL", report, "900x700")

    def show_laser_engineering_center():
        engine_names = [
            "spectral_analysis",
            "spectral_region",
            "laser_sources",
            "beam_quality_engine",
            "spectral_quality_engine",
        ]
        report = build_engine_group_report(
            "LASERSTONE LASER ENGINEERING CENTER",
            "SPECTRAL AND LASER DESIGN LAYER",
            engine_names
        )
        open_text_window(window, "LASERSTONE LASER ENGINEERING CENTER", report, "900x700")

    def show_intelligence_ecosystem():
        engine_names = [
            "intelligence_hub",
            "scientific_recommendation_engine",
            "strategic_advisor_engine",
            "final_decision_engine",
            "recommendation_engine",
        ]
        report = build_engine_group_report(
            "LASERSTONE INTELLIGENCE ECOSYSTEM",
            "INTELLIGENCE, STRATEGY, AND DECISION LAYER",
            engine_names
        )
        open_text_window(window, "LASERSTONE INTELLIGENCE ECOSYSTEM", report, "900x700")

    def show_expert_house():
        material_score = safe_score(top_value("material_score", 0))
        physics_score = safe_score(top_value("physics_evidence_score", top_value("physics_consistency_score", 0)))
        patent_score = safe_score(top_value("patent_potential_score", 0))
        decision = top_value("final_decision", top_value("governor_decision", "UNDER REVIEW"))

        report = (
            "LASERSTONE EXPERT HOUSE REPORT\n\n"
            f"Top Candidate: {top_value('name')}\n\n"
            f"Material Score: {material_score:.2f}\n"
            f"Physics Evidence: {physics_score:.2f}\n"
            f"Patent Potential: {patent_score:.2f}\n\n"
            "Scientific Assessment:\n"
            "This candidate demonstrates the strongest overall scientific performance according to the integrated LASERSTONE evaluation.\n\n"
            "Recommended Action:\n"
            "Proceed to advanced characterization and prototype planning.\n\n"
            f"Final Decision: {decision}\n"
        )
        open_text_window(window, "LASERSTONE EXPERT HOUSE", report, "760x560")

    def show_strategic_roadmap():
        leader = top_value("name")
        score = safe_score(top_value("material_score", 0))

        if score >= 85:
            current_stage = "PROTOTYPE READY"
            next_step = "Prototype Construction"
            future_step = "Laser Cavity Optimization"
        elif score >= 70:
            current_stage = "ADVANCED VALIDATION"
            next_step = "Spectroscopic Verification"
            future_step = "Prototype Preparation"
        else:
            current_stage = "RESEARCH STAGE"
            next_step = "Additional Characterization"
            future_step = "Material Improvement"

        report = (
            "LASERSTONE STRATEGIC ROADMAP\n\n"
            f"Current Leader: {leader}\n"
            f"Material Score: {score:.2f}\n\n"
            f"Current Stage: {current_stage}\n\n"
            f"Next Step:\n{next_step}\n\n"
            f"Future Step:\n{future_step}\n\n"
            "Long-Term Objective:\nPatent Preparation and Scientific Publication\n\n"
            "Strategic Recommendation:\n"
            "Focus resources on the leading candidate while maintaining comparative monitoring of alternative materials.\n"
        )
        open_text_window(window, "LASERSTONE STRATEGIC ROADMAP", report, "760x560")

    def show_prototype_planner():
        score = safe_score(top_value("material_score", 0))
        report = (
            "LASERSTONE PROTOTYPE PLANNER\n\n"
            f"Selected Material: {top_value('name')}\n"
            f"Material Score: {score:.2f}\n\n"
            "PROTOTYPE DEVELOPMENT PLAN\n\n"
            "STEP 1:\nMaterial purification and preparation.\n\n"
            "STEP 2:\nOptical absorption characterization.\n\n"
            "STEP 3:\nEmission spectrum verification.\n\n"
            "STEP 4:\nLaser cavity compatibility assessment.\n\n"
            "STEP 5:\nPrototype laser assembly.\n\n"
            "STEP 6:\nOutput power and stability testing.\n\n"
            "FINAL TARGET:\nExperimental laser prototype.\n"
        )
        open_text_window(window, "LASERSTONE PROTOTYPE PLANNER", report, "760x560")

    def open_wing(title, subtitle, buttons, color="lightgreen"):
        wing = tk.Toplevel(window)
        wing.title(title)
        wing.geometry("760x520")

        header = tk.Label(
            wing,
            text=f"{title}\n{subtitle}",
            font=("Arial", 16, "bold")
        )
        header.pack(pady=18)

        frame = tk.Frame(wing)
        frame.pack(fill="both", expand=True, padx=25, pady=20)

        for index, (text, command) in enumerate(buttons):
            btn = tk.Button(
                frame,
                text=text,
                font=("Arial", 11, "bold"),
                width=30,
                height=4,
                bg=color,
                command=command
            )
            btn.grid(row=index // 2, column=index % 2, padx=14, pady=14)

    def show_executive_wing():
        open_wing(
            "LASERSTONE EXECUTIVE WING",
            "Decision • Strategy • Prototype",
            [
                ("EXECUTIVE DECISION", show_executive_decision),
                ("EXPERT HOUSE", show_expert_house),
                ("STRATEGIC ROADMAP", show_strategic_roadmap),
                ("PROTOTYPE PLANNER", show_prototype_planner),
            ],
            "lightgreen"
        )

    def show_knowledge_wing():
        open_wing(
            "LASERSTONE KNOWLEDGE WING",
            "Knowledge • Repository • Discovery",
            [
                ("KNOWLEDGE CENTER", show_knowledge_center),
                ("SCIENTIFIC REPOSITORY", show_scientific_repository),
                ("DISCOVERY CENTER", show_discovery_center),
            ],
            "lightblue"
        )

    def show_physics_wing():
        open_wing(
            "LASERSTONE PHYSICS WING",
            "Evidence • Physics Core • Laser Engineering",
            [
                ("PHYSICS EVIDENCE", show_physics_evidence),
                ("PHYSICS CORE", show_physics_core_hall),
                ("LASER ENGINEERING", show_laser_engineering_center),
            ],
            "lightyellow"
        )

    def show_platform_wing():
        open_wing(
            "LASERSTONE PLATFORM WING",
            "Integrity • Engines • Guardians • Repair",
            [
                ("SYSTEM INTEGRITY", show_system_integrity),
                ("ENGINE HALL", show_engine_hall_of_fame),
                ("KINGDOM GUARDIANS", show_kingdom_guardians),
                ("REPAIR ADVISOR", show_repair_advisor),
            ],
            "khaki"
        )

    def show_intelligence_wing():
        open_wing(
            "LASERSTONE INTELLIGENCE WING",
            "Analysis • Ecosystem • Scientific Intelligence",
            [
                ("MATERIAL ANALYSIS", show_material_analysis),
                ("INTELLIGENCE ECOSYSTEM", show_intelligence_ecosystem),
            ],
            "lightgreen"
        )

    def show_startup_then_city():
        startup = tk.Toplevel(window)
        startup.title("LASERSTONE STARTUP")
        startup.geometry("720x420")
        startup.configure(bg="white")

        label = tk.Label(
            startup,
            text=(
                "LASERSTONE™\n\n"
                "Welcome, Researcher\n\n"
                "Loading Scientific Engines...\n"
                "Loading Knowledge Tree...\n"
                "Preparing Expert House...\n\n"
                "The Scientific City is opening..."
            ),
            font=("Arial", 18, "bold"),
            bg="white",
            justify="center"
        )
        label.pack(expand=True)

        startup.after(1800, startup.destroy)

    def build_main_city():
        
        for child in window.winfo_children():
            child.destroy()

        header = tk.Label(
            window,
            text="LASERSTONE™ INTELLIGENT SCIENTIFIC PLATFORM",
            font=("Arial", 20, "bold")
        )
        header.pack(pady=10)

        control_frame = tk.LabelFrame(
            window,
            text="LASERSTONE™ CONTROL CENTER",
            font=("Arial", 12, "bold")
        )
        control_frame.pack(fill="x", padx=20, pady=8)

        control_cards = [
            ("SYSTEM STATUS", system_status),
            ("PLATFORM CLASS", platform_class),
            ("DECLARED LINKS", f"{platform_maturity}%"),
            ("TOTAL ENGINES", str(total_engines)),
            ("DECLARED CONNECTED", str(connected_engines)),
            ("ISOLATED", str(isolated_engines)),
            ("REGISTRY", "DECLARATIONS ONLY"),
        ]

        for title_text, value_text in control_cards:
            card = tk.Label(
                control_frame,
                text=f"{title_text}\n{value_text}",
                font=("Arial", 10, "bold"),
                relief="groove",
                width=28,
                height=3
            )
            card.pack(side=tk.LEFT, padx=6, pady=8)

        grand_hall = tk.LabelFrame(
            window,
            text="LASERSTONE GRAND HALL",
            font=("Arial", 12, "bold")
        )
        grand_hall.pack(fill="x", padx=20, pady=8)

        grand_text = (
            f"Top Material: {top_value('name')}     |     "
            f"Material Score: {top_value('material_score')}     |     "
            f"Best Patent Candidate: {best_patent.get('name', 'N/A')}     |     "
            f"Platform Status: {system_status}"
        )

        tk.Label(
            grand_hall,
            text=grand_text,
            font=("Arial", 12, "bold"),
            justify="left"
        ).pack(anchor="w", padx=12, pady=10)

        tree_frame = tk.LabelFrame(
            window,
            text="THE KNOWLEDGE TREE — Select Your Scientific Wing",
            font=("Arial", 12, "bold")
        )
        tree_frame.pack(fill="x", padx=20, pady=10)

        wing_cards = [
            ("🏛️ EXECUTIVE WING", "Decision • Strategy • Prototype", "lightgreen", show_executive_wing),
            ("🧠 KNOWLEDGE WING", "Repository • Discovery", "lightblue", show_knowledge_wing),
            ("🔬 PHYSICS WING", "Evidence • Laser Engineering", "lightyellow", show_physics_wing),
            ("⚙️ PLATFORM WING", "Integrity • Engines • Guardians", "khaki", show_platform_wing),
            ("🌿 INTELLIGENCE WING", "Analysis • Ecosystem", "lightgreen", show_intelligence_wing),
        ]

        for index, (wing_title, wing_subtitle, color, command) in enumerate(wing_cards):
            card = tk.Button(
                tree_frame,
                text=f"{wing_title}\n{wing_subtitle}\nENTER",
                font=("Arial", 12, "bold"),
                relief="raised",
                width=34,
                height=4,
                bg=color,
                command=command
            )
            card.grid(row=index // 3, column=index % 3, padx=12, pady=12)

        intelligence_frame = tk.LabelFrame(
            window,
            text="SCIENTIFIC INTELLIGENCE HUB",
            font=("Arial", 12, "bold")
        )
        intelligence_frame.pack(fill="x", padx=20, pady=8)

        hub_text = (
            f"Recommended Laser Material : {recommendations.get('recommended_material', 'N/A')}\n"
            f"Best Overall Material      : {recommendations.get('best_overall_material', 'N/A')}\n"
            f"Best Patent Candidate      : {recommendations.get('best_patent_candidate', 'N/A')}\n"
            f"System Assessment          : {recommendations.get('system_assessment', 'N/A')}\n"
            f"Platform Status            : {system_status}\n"
            f"Platform Class             : {platform_class}"
        )

        tk.Label(
            intelligence_frame,
            text=hub_text,
            justify="left",
            font=("Arial", 11)
        ).pack(anchor="w", padx=10, pady=10)

        columns = ("Rank", "Plant", "Material Score", "Intelligence", "Patent", "Decision")
        tree = ttk.Treeview(window, columns=columns, show="headings", height=7)

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, width=190)

        tree.pack(fill="x", padx=20, pady=8)

        for plant in ranked_plants:
            tree.insert(
                "",
                "end",
                values=(
                    plant.get("global_rank", "-"),
                    plant.get("name", "Unknown"),
                    f"{safe_score(plant.get('material_score', 0)):.2f}",
                    plant.get("intelligence_summary", {}).get("intelligence_score", "N/A"),
                    plant.get("patent_potential_score", "N/A"),
                    plant.get("final_decision", plant.get("governor_decision", "N/A")),
                )
            )

        chart_canvas = tk.Canvas(window, width=1100, height=220, bg="white")
        chart_canvas.pack(padx=20, pady=8)
        draw_bar_chart(chart_canvas, ranked_plants, "material_score", "Material Score Visualization")

    show_startup_then_city()
    window.after(1900, build_main_city)
    print("CITY WINDOW READY")
    window.mainloop()
