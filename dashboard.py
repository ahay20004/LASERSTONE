import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from executive_summary_engine import generate_executive_summary
from recommendation_engine import generate_recommendations
from project_registry import PROJECT_REGISTRY

def show_system_integrity():
    from system_health_engine import describe_runtime_state, format_runtime_evidence
    messagebox.showinfo("SYSTEM INTEGRITY CENTER",
                        format_runtime_evidence(describe_runtime_state([])))


def launch_dashboard(ranked_plants, runtime_state=None):

    window = tk.Tk()
    window.title("LASERSTONE™ V1 Control Center")
    window.geometry("1350x1000")

    title = tk.Label(
        window,
        text="LASERSTONE™ INTELLIGENT SCIENTIFIC PLATFORM",
        font=("Arial", 20, "bold")
    )

    title.pack(pady=10)
    

    control_frame = tk.LabelFrame(
        window,
        text="LASERSTONE™ CONTROL CENTER",
        font=("Arial", 12, "bold")
    )

    control_frame.pack(
        fill="x",
        padx=20,
        pady=10)

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
            key=lambda plant: plant.get(
                "intelligence_summary", {}
            ).get("intelligence_score", 0)
        )
        if ranked_plants else {}
    )

    best_patent = (
        max(
            ranked_plants,
            key=lambda plant: plant.get(
                "patent_potential_score", 0
            )
        )
        if ranked_plants else {}
    )

    gateway_cards = [
        ("SYSTEM INTEGRITY", "ACTIVE", "lightgreen"),
        ("EXECUTIVE DECISION", "ACTIVE", "lightgreen"),
        ("KNOWLEDGE CENTER", "ACTIVE", "lightgreen"),
        ("MATERIAL ANALYSIS", "ACTIVE", "lightgreen"),
        ("PHYSICS EVIDENCE", "ACTIVE", "lightgreen"),
        ("REPAIR ADVISOR", "STANDBY", "khaki"),
        ("SCIENTIFIC REPOSITORY", "ACTIVE", "lightgreen"),
        ("DISCOVERY CENTER", "ACTIVE", "lightgreen"), 
        ("ENGINE HALL", "ACTIVE", "lightgreen"),
        ("KINGDOM GUARDIANS", "ACTIVE", "lightgreen"),
        ("PHYSICS CORE", "ACTIVE", "lightgreen"),
        ("LASER ENGINEERING", "ACTIVE", "lightgreen"),
        ("INTELLIGENCE ECOSYSTEM", "ACTIVE", "lightgreen"),
        ("EXPERT HOUSE", "ACTIVE", "lightgreen"),
        ("STRATEGIC ROADMAP", "ACTIVE", "lightgreen"),
    ]
       

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

        card = tk.Button(
            control_frame,
            text=f"{title_text}\n{value_text}",
            font=("Arial", 10, "bold"),
            relief="groove",
            width=28,
            height=3
        )

        card.pack(
            side=tk.LEFT,
            padx=6,
            pady=8
        )

    gateway_frame = tk.LabelFrame(
        window,
        text="LASERSTONE CONTROL GATEWAY",
        font=("Arial", 12, "bold")
    )

    gateway_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    def show_system_integrity():
        integrity_window = tk.Toplevel(window)
        integrity_window.title("LASERSTONE SYSTEM INTEGRITY")
        integrity_window.geometry("520x420")

        report = format_runtime_evidence(evidence)

        text_box = tk.Text(integrity_window, wrap="word")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        text_box.insert("1.0", report)
        text_box.config(state="disabled")



     
    def show_knowledge_center():
        knowledge_window = tk.Toplevel(window)
        knowledge_window.title("LASERSTONE KNOWLEDGE CENTER")
        knowledge_window.geometry("520x420")

        report = (
            "LASERSTONE KNOWLEDGE CENTER\n\n"
            f"Total Materials: {len(ranked_plants)}\n\n"
            f"Top Material: {top_material.get('name', 'N/A')}\n"
            f"Best Intelligence: {best_intelligence.get('name', 'N/A')}\n"
            f"Best Patent Candidate: {best_patent.get('name', 'N/A')}\n\n"
            "Knowledge Status: ACTIVE\n"
            "Plant Database: AVAILABLE\n"
            "Reference Layer: AVAILABLE\n"
            "Plant Profiles: AVAILABLE\n\n"
            "Platform Knowledge Level: EXPANDING\n"
        )

        text_box = tk.Text(knowledge_window, wrap="word")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)
        text_box.insert("1.0", report)
        text_box.config(state="disabled")

    def show_material_analysis():
        analysis_window = tk.Toplevel(window)
        analysis_window.title("LASERSTONE MATERIAL ANALYSIS")
        analysis_window.geometry("600x500")

        average_score = 0

        if ranked_plants:
            average_score = sum(
                plant.get("material_score", 0)
                for plant in ranked_plants
            ) / len(ranked_plants)

        report = (
            "LASERSTONE MATERIAL ANALYSIS\n\n"
            f"Top Material: {top_material.get('name', 'N/A')}\n"
            f"Material Score: {top_material.get('material_score', 0):.2f}\n"
            f"Material Class: {top_material.get('material_class', 'N/A')}\n\n"
            "TOP 3 MATERIALS\n\n"
        )

        for plant in ranked_plants[:3]:

            report += (
                f"{plant.get('global_rank', '-')}. "
                f"{plant.get('name', 'Unknown')} | "
                f"Score: {plant.get('material_score', 0):.2f}\n"
            )

        report += (
            f"\nAverage Material Score: {average_score:.2f}\n\n"
            "Platform Recommendation:\n"
            "Focus on the highest-ranked materials "
            "for prototype and optimization studies.\n"
        )

        text_box = tk.Text(
            analysis_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )

    def show_physics_evidence():

        physics_window = tk.Toplevel(window)

        physics_window.title(
            "LASERSTONE PHYSICS EVIDENCE"
        )

        physics_window.geometry("600x500")

        print("\n===== TOP MATERIAL DATA =====")
        for key, value in top_material.items():
            print(f"{key} : {value}")
        print("=============================\n")

        report = (
            "LASERSTONE PHYSICS EVIDENCE\n\n"
            f"Top Material : {top_material.get('name', 'N/A')}\n\n"

            f"Physics Consistency Score : "
            f"{top_material.get('physics_consistency_score', 'N/A')}\n"

            f"Physics Consistency Class : "
            f"{top_material.get('physics_consistency_class', 'N/A')}\n\n"

            f"Scientific Confidence Score : "
            f"{top_material.get('scientific_confidence_score', 'N/A')}\n"

            f"Scientific Confidence Class : "
            f"{top_material.get('scientific_confidence_class', 'N/A')}\n\n"

            f"Experimental Success Score : "
            f"{top_material.get('experimental_success_score', 'N/A')}\n\n"

            f"System Integrity Score : "
            f"{top_material.get('system_integrity_score', 'N/A')}\n"

            f"System Integrity Class : "
            f"{top_material.get('system_integrity_class', 'N/A')}\n\n"

            "Physics Assessment:\n"
            "The physics layer supports the scientific ranking\n"
            "through consistency, confidence, and validation indicators.\n"
        )

        text_box = tk.Text(
            physics_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def show_executive_decision():

        executive_window = tk.Toplevel(window)

        executive_window.title(
            "LASERSTONE EXECUTIVE DECISION CENTER"
        )

        executive_window.geometry("700x600")

        report = (

            "LASERSTONE EXECUTIVE DECISION CENTER\n\n"

            f"TOP MATERIAL : "
            f"{top_material.get('name', 'N/A')}\n\n"

            f"GLOBAL RANK : "
            f"#{top_material.get('global_rank', 'N/A')}\n\n"

            f"MATERIAL SCORE : "
            f"{top_material.get('material_score', 'N/A')}\n\n"

            f"PHYSICS CONSISTENCY : "
            f"{top_material.get('physics_consistency_score', 'N/A')}\n\n"

            f"SCIENTIFIC CONFIDENCE : "
            f"{top_material.get('scientific_confidence_score', 'N/A')}\n\n"

            f"EXPERIMENTAL SUCCESS : "
            f"{top_material.get('experimental_success_score', 'N/A')}\n\n"

            f"SYSTEM INTEGRITY : "
            f"{top_material.get('system_integrity_score', 'N/A')}\n\n"

            f"GOVERNOR DECISION :\n"
            f"{top_material.get('governor_decision', 'N/A')}\n\n"

            "STRATEGIC STATUS :\n"
            "HIGH PRIORITY RESEARCH CANDIDATE\n\n"

            "NEXT ACTION :\n"
            "Continue experimental validation\n"
            "before prototype deployment."
        )

        text_box = tk.Text(
            executive_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def show_repair_advisor():

        repair_window = tk.Toplevel(window)

        repair_window.title(
            "LASERSTONE REPAIR ADVISOR"
        )

        repair_window.geometry("700x550")

        report = (

            "LASERSTONE REPAIR ADVISOR\n\n"

            f"Top Material : "
            f"{top_material.get('name', 'N/A')}\n\n"

            "Detected Improvement Areas:\n\n"

            f"Experimental Success Score : "
            f"{top_material.get('experimental_success_score', 'N/A')}\n"

            f"Patent Potential Score : "
            f"{top_material.get('patent_potential_score', 'N/A')}\n"

            f"Research Novelty Score : "
            f"{top_material.get('research_novelty_score', 'N/A')}\n\n"

            "Recommended Actions:\n\n"

            "1. Increase experimental validation.\n"

            "2. Improve prototype verification.\n"

            "3. Explore patent opportunities.\n"

            "4. Expand novelty and innovation studies.\n\n"

            "Repair Status:\n"

            "SYSTEM READY FOR OPTIMIZATION"
        )

        text_box = tk.Text(
            repair_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def show_scientific_repository():

        repository_window = tk.Toplevel(window)

        repository_window.title(
            "LASERSTONE SCIENTIFIC REPOSITORY"
        )

        repository_window.geometry("700x550")

        report = (

            "LASERSTONE SCIENTIFIC REPOSITORY\n\n"

            f"Registered Materials : "
            f"{len(ranked_plants)}\n\n"

            f"Total Engines : "
            f"{total_engines}\n"

            f"Connected Engines : "
            f"{connected_engines}\n\n"

            f"Top Material : "
            f"{top_material.get('name', 'N/A')}\n\n"

            f"Best Patent Candidate : "
            f"{best_patent.get('name', 'N/A')}\n\n"

            "Knowledge Status : AVAILABLE\n"

            "Repository Status : ACTIVE\n\n"

            "Scientific Assets:\n"

            "- Material Database\n"

            "- Intelligence Layer\n"

            "- Physics Evidence Layer\n"

            "- Executive Decision Layer\n"
        )

        text_box = tk.Text(
            repository_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def show_discovery_center():

        discovery_window = tk.Toplevel(window)

        discovery_window.title(
            "LASERSTONE DISCOVERY CENTER"
        )

        discovery_window.geometry("700x550")

        report = (

            "LASERSTONE DISCOVERY CENTER\n\n"

            f"Discovery Candidate : "
            f"{top_material.get('name', 'N/A')}\n\n"

            f"Research Novelty : "
            f"{top_material.get('research_novelty_score', 'N/A')}\n"

            f"Patent Potential : "
            f"{top_material.get('patent_potential_score', 'N/A')}\n"

            f"Scientific Confidence : "
            f"{top_material.get('scientific_confidence_score', 'N/A')}\n\n"

            "Future Research Directions:\n\n"

            "1. Experimental validation\n"

            "2. Optical gain investigation\n"

            "3. Prototype development\n"

            "4. Patent exploration\n\n"

            "Discovery Status : ACTIVE"
        )

        text_box = tk.Text(
            discovery_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def show_engine_hall_of_fame():

        hall_window = tk.Toplevel(window)

        hall_window.title(
            "LASERSTONE ENGINE HALL OF FAME"
        )

        hall_window.geometry("900x700")

        report = (
            "LASERSTONE ENGINE HALL OF FAME\n\n"
            f"Total Registered Engines : {len(PROJECT_REGISTRY)}\n\n"
        )

        for index, (engine_name, info) in enumerate(
            PROJECT_REGISTRY.items(),
            start=1
        ):

            inputs = ", ".join(
                info.get("inputs", [])
            )

            outputs = ", ".join(
                info.get("outputs", [])
            )

            report += (
                f"{index}. {engine_name}\n"
                f"Category : {info.get('category', 'N/A')}\n"
                f"Status   : {info.get('status', 'N/A')}\n"
                f"Inputs   : {inputs if inputs else 'N/A'}\n"
                f"Outputs  : {outputs if outputs else 'N/A'}\n"
                + "-" * 55 +
                "\n"
            )

        text_box = tk.Text(
            hall_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def show_kingdom_guardians():

        guardians_window = tk.Toplevel(window)

        guardians_window.title(
            "LASERSTONE KINGDOM GUARDIANS"
        )

        guardians_window.geometry("800x600")

        report = (
            "LASERSTONE KINGDOM GUARDIANS\n\n"
            "KINGDOM PROTECTION LAYER\n\n"
        )

        guardian_engines = [

            "project_health_engine",

            "system_health_engine",

            "system_integrity_engine",

            "runtime_monitor_engine",

            "network_intelligence_engine"

        ]

        for index, engine_name in enumerate(
            guardian_engines,
            start=1
        ):

            info = PROJECT_REGISTRY.get(
                engine_name,
                {}
            )

            report += (
                f"{index}. {engine_name}\n"
                f"Category : {info.get('category', 'N/A')}\n"
                f"Status : {info.get('status', 'N/A')}\n"
                + "-" * 50 +
                "\n"
            )

        text_box = tk.Text(
            guardians_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )
    
    def build_engine_group_report(title, subtitle, engine_names):

        report = (
            f"{title}\n\n"
            f"{subtitle}\n\n"
        )

        for index, engine_name in enumerate(engine_names, start=1):

            info = PROJECT_REGISTRY.get(engine_name, {})

            inputs = ", ".join(
                info.get("inputs", [])
            )

            outputs = ", ".join(
                info.get("outputs", [])
            )

            report += (
                f"{index}. {engine_name}\n"
                f"Category : {info.get('category', 'N/A')}\n"
                f"Status   : {info.get('status', 'N/A')}\n"
                f"Inputs   : {inputs if inputs else 'N/A'}\n"
                f"Outputs  : {outputs if outputs else 'N/A'}\n"
                + "-" * 55 +
                "\n"
            )

        return report


    def open_report_window(title, report):

        report_window = tk.Toplevel(window)

        report_window.title(title)

        report_window.geometry("900x700")

        text_box = tk.Text(
            report_window,
            wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
        )

        text_box.config(
            state="disabled"
        )


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

        open_report_window(
            "LASERSTONE KINGDOM GUARDIANS",
            report
        )


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

        open_report_window(
            "LASERSTONE PHYSICS CORE HALL",
            report
        )


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

        open_report_window(
            "LASERSTONE LASER ENGINEERING CENTER",
            report
        )


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

        open_report_window(
            "LASERSTONE INTELLIGENCE ECOSYSTEM",
            report
        )

    def show_expert_house():

        expert_window = tk.Toplevel(window)
        expert_window.title("LASERSTONE EXPERT HOUSE")
        expert_window.geometry("700x550")

        top_candidate = top_material.get("name", "N/A")

        material_score = top_material.get(
            "material_score", 0
        )

        physics_score = top_material.get("physics_evidence_score", 0)

        patent_score = top_material.get(
            "patent_potential_score",0   )

        decision = top_material.get(
            "final_decision",
            "UNDER REVIEW"
        )

        report = (
            "LASERSTONE EXPERT HOUSE REPORT\n\n"

            f"Top Candidate: {top_candidate}\n\n"

            f"Material Score: {material_score:.2f}\n"
            f"Physics Evidence: {physics_score:.2f}\n"
            f"Patent Potential: {patent_score:.2f}\n\n"

            "Scientific Assessment:\n"
            "This candidate demonstrates the strongest\n"
            "overall scientific performance according\n"
            "to the integrated LASERSTONE evaluation.\n\n"

            "Recommended Action:\n"
            "Proceed to advanced characterization\n"
            "and prototype planning.\n\n"

            f"Final Decision: {decision}\n"
        )

        text_box = tk.Text(
           expert_window,
           wrap="word"
        )

        text_box.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text_box.insert(
            "1.0",
            report
       )

        text_box.config(
            state="disabled"
       )

def show_strategic_roadmap():

    roadmap_window = tk.Toplevel(window)
    roadmap_window.title("LASERSTONE STRATEGIC ROADMAP")
    roadmap_window.geometry("700x550")

    leader = top_material.get("name", "N/A")

    score = top_material.get(
        "material_score",
        0
    )

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

        "Long-Term Objective:\n"
        "Patent Preparation and Scientific Publication\n\n"

        "Strategic Recommendation:\n"
        "Focus resources on the leading candidate "
        "while maintaining comparative monitoring "
        "of alternative materials.\n"
    )

    text_box = tk.Text(
        roadmap_window,
        wrap="word"
    )

    text_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    text_box.insert(
        "1.0",
        report
    )

    text_box.config(
        state="disabled"
    )

def show_prototype_planner():

    planner_window = tk.Toplevel(window)
    planner_window.title("LASERSTONE PROTOTYPE PLANNER")
    planner_window.geometry("750x600")

    candidate = top_material.get("name", "N/A")

    score = top_material.get(
        "material_score",
        0
    )

    report = (
        "LASERSTONE PROTOTYPE PLANNER\n\n"

        f"Selected Material: {candidate}\n"
        f"Material Score: {score:.2f}\n\n"

        "PROTOTYPE DEVELOPMENT PLAN\n\n"

        "STEP 1:\n"
        "Material purification and preparation.\n\n"

        "STEP 2:\n"
        "Optical absorption characterization.\n\n"

        "STEP 3:\n"
        "Emission spectrum verification.\n\n"

        "STEP 4:\n"
        "Laser cavity compatibility assessment.\n\n"

        "STEP 5:\n"
        "Prototype laser assembly.\n\n"

        "STEP 6:\n"
        "Output power and stability testing.\n\n"

        "FINAL TARGET:\n"
        "Experimental laser prototype.\n"
    )

    text_box = tk.Text(
        planner_window,
        wrap="word"
    )

    text_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    text_box.insert("1.0", report)

    text_box.config(
        state="disabled"
    )

    for index, (title_text, value_text, color_text) in enumerate(gateway_cards):
        command = None

        if title_text == "SYSTEM INTEGRITY":
           command = show_system_integrity
        elif title_text == "MATERIAL ANALYSIS":
            command = show_material_analysis
        elif title_text == "KNOWLEDGE CENTER":
            command = show_knowledge_center
        elif title_text == "PHYSICS EVIDENCE":
            command = show_physics_evidence
        elif title_text == "EXECUTIVE DECISION":
            command = show_executive_decision
        elif title_text == "REPAIR ADVISOR":
            command = show_repair_advisor
        elif title_text == "SCIENTIFIC REPOSITORY":
            command = show_scientific_repository
        elif title_text == "DISCOVERY CENTER":
            command = show_discovery_center
        elif title_text == "ENGINE HALL":
            command = show_engine_hall_of_fame
        elif title_text == "KINGDOM GUARDIANS":
            command = show_kingdom_guardians
        elif title_text == "PHYSICS CORE":
            command = show_physics_core_hall
        elif title_text == "LASER ENGINEERING":
           command = show_laser_engineering_center
        elif title_text == "INTELLIGENCE ECOSYSTEM":
           command = show_intelligence_ecosystem
        elif title_text == "EXPERT HOUSE":
           command = show_expert_house
        elif title_text == "PROTOTYPE PLANNER":
           command = show_prototype_planner
        elif title_text == "STRATEGIC ROADMAP":
           command = show_strategic_roadmap

        card = tk.Button(
            gateway_frame,
            text=f"{title_text}\n{value_text}",
            font=("Arial", 9, "bold"),
            relief="raised",
            width=24,
            height=3,
            bg=color_text,
            command=command
        )

              
        card.grid(
            row=index // 4,
            column=index % 4,
            padx=6,
            pady=6
    )
        
    for title_text, value_text in control_cards:

        card = tk.Label(
            control_frame,
            text=f"{title_text}\n{value_text}",
            font=("Arial", 10, "bold"),
            relief="groove",
            width=28,
            height=3
        )

        card.pack(
            side=tk.LEFT,
            padx=8,
            pady=8
        )
    recommendations = generate_recommendations(
        ranked_plants
    )

    intelligence_frame = tk.LabelFrame(
        window,
        text="SCIENTIFIC INTELLIGENCE HUB",
        font=("Arial", 12, "bold")
    )

    intelligence_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )

    hub_text = f"""
Recommended Laser Material : {recommendations.get('recommended_material', 'N/A')}
Best Overall Material      : {recommendations.get('best_overall_material', 'N/A')}
Best Patent Candidate      : {recommendations.get('best_patent_candidate', 'N/A')}
System Assessment          : {recommendations.get('system_assessment', 'N/A')}
Platform Status            : {system_status}
Platform Class             : {platform_class}
"""

    hub_label = tk.Label(
        intelligence_frame,
        text=hub_text,
        justify="left",
        font=("Arial", 11)
    )

    hub_label.pack(
        anchor="w",
        padx=10,
        pady=10
    )

    columns = (
        "Rank",
        "Plant",
        "Material Score",
        "Intelligence",
        "Patent",
        "Decision"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=8
    )

    for column in columns:

        tree.heading(
            column,
            text=column
    )

        tree.column(
            column,
        width=190
    )

        chart_title = tk.Label(
        window,
        text="Material Score Visualization",
        font=("Arial", 14, "bold")
    )

    chart_title.pack(
        pady=8
    )

    canvas = tk.Canvas(
        window,
        width=1100,
        height=230,
        bg="white"
    )

    canvas.pack(
        padx=20,
        pady=8
    )

    draw_material_score_chart(
        canvas,
        ranked_plants
    )

    intelligence_title = tk.Label(
        window,
        text="Intelligence Score Visualization",
        font=("Arial", 14, "bold")
    )

    intelligence_title.pack(
        pady=8
    )

    intelligence_canvas = tk.Canvas(
        window,
        width=1100,
        height=230,
        bg="white"
    )

    intelligence_canvas.pack(
        padx=20,
        pady=8
    )

    draw_intelligence_chart(
        intelligence_canvas,
        ranked_plants
    )

    window.mainloop()


def draw_material_score_chart(canvas, ranked_plants):

    x_start = 80
    y_base = 180
    bar_width = 80
    gap = 45
    max_bar_height = 130

    scores = [
        plant.get("material_score", 0)
        for plant in ranked_plants
    ]

    max_score = max(scores) if scores else 1

    for index, plant in enumerate(ranked_plants):

        score = plant.get("material_score", 0)
        name = plant.get("name", "Unknown")

        bar_height = (
            (score / max_score) * max_bar_height
            if max_score else 0
        )

        x1 = x_start + index * (bar_width + gap)
        y1 = y_base - bar_height
        x2 = x1 + bar_width
        y2 = y_base

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2
        )

        canvas.create_text(
            x1 + bar_width / 2,
            y1 - 10,
            text=str(score),
            font=("Arial", 10, "bold")
        )

        canvas.create_text(
            x1 + bar_width / 2,
            y_base + 18,
            text=name,
            font=("Arial", 9)
        )

    canvas.create_line(
        50,
        y_base,
        1050,
        y_base
    )


def draw_intelligence_chart(canvas, ranked_plants):

    x_start = 80
    y_base = 180
    bar_width = 80
    gap = 45
    max_bar_height = 130

    scores = []

    for plant in ranked_plants:

        intelligence_summary = plant.get(
            "intelligence_summary",
            {}
        )

        scores.append(
            intelligence_summary.get(
                "intelligence_score",
                0
            )
        )

    max_score = max(scores) if scores else 1

    for index, plant in enumerate(ranked_plants):

        intelligence_summary = plant.get(
            "intelligence_summary",
            {}
        )

        score = intelligence_summary.get(
            "intelligence_score",
            0
        )

        name = plant.get("name", "Unknown")

        bar_height = (
            (score / max_score) * max_bar_height
            if max_score else 0
        )

        x1 = x_start + index * (bar_width + gap)
        y1 = y_base - bar_height
        x2 = x1 + bar_width
        y2 = y_base

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2
        )

        canvas.create_text(
            x1 + bar_width / 2,
            y1 - 10,
            text=str(score),
            font=("Arial", 10, "bold")
        )

        canvas.create_text(
            x1 + bar_width / 2,
            y_base + 18,
            text=name,
            font=("Arial", 9)
        )

    canvas.create_line(
        50,
        y_base,
        1050,
        y_base
    )


def format_frequency(frequency_hz):

    try:
        frequency_hz = float(frequency_hz)
    except (TypeError, ValueError):
        return "N/A"

    if frequency_hz == 0:
        return "N/A"

    return f"{frequency_hz:.3e} Hz"


def add_section_title(parent, text):

    title = tk.Label(
        parent,
        text=text,
        font=("Arial", 13, "bold")
    )

    title.pack(
        anchor="w",
        padx=18,
        pady=(14, 6)
    )


def add_info_line(parent, text):

    label = tk.Label(
        parent,
        text=text,
        anchor="w",
        justify="left",
        font=("Arial", 11)
    )

    label.pack(
        fill="x",
        padx=25,
        pady=2
    )


def calculate_lri_score(selected_plant):

    lri_score = selected_plant.get(
        "lri_score",
        None
    )

    if lri_score is not None:
        return lri_score

    material_score = selected_plant.get(
        "material_score",
        0
    )

    thermal_score = selected_plant.get(
        "thermal_score",
        0
    )

    feasibility_score = selected_plant.get(
        "feasibility_score",
        0
    )

    q_factor_score = selected_plant.get(
        "q_factor_score",
        0
    )

    return round(
        (
            material_score
            + thermal_score
            + feasibility_score
            + q_factor_score
        ) / 4,
        2
    )


def classify_readiness(lri_score):

    if lri_score >= 85:

        return (
            "READY FOR PROTOTYPE",
            "HIGH"
        )

    if lri_score >= 60:

        return (
            "RESEARCH STAGE",
            "MEDIUM"
        )

    return (
        "NEEDS OPTIMIZATION",
        "LOW"
    )


def draw_digital_laser_twin(parent, selected_plant, laser_output, architecture):

    add_section_title(
        parent,
        "=== DIGITAL LASER TWIN ==="
    )

    twin_canvas = tk.Canvas(
        parent,
        width=620,
        height=280,
        bg="white"
    )

    twin_canvas.pack(
        pady=10
    )

    plant_name = selected_plant.get(
        "name",
        "PLANT"
    )

    wavelength = laser_output.get(
        "emission_wavelength_nm",
        "N/A"
    )

    color = laser_output.get(
        "laser_color",
        "Unknown"
    )

    pump = architecture.get(
        "pump_source",
        "PUMP"
    )

    cavity = architecture.get(
        "cavity",
        "RESONATOR"
    )

    twin_canvas.create_rectangle(
        30,
        110,
        150,
        160
    )

    twin_canvas.create_text(
        90,
        135,
        text=pump,
        width=105,
        font=("Arial", 9, "bold")
    )

    twin_canvas.create_line(
        150,
        135,
        205,
        135,
        arrow=tk.LAST
    )

    twin_canvas.create_rectangle(
        205,
        95,
        405,
        175
    )

    twin_canvas.create_text(
        305,
        118,
        text="ACTIVE MEDIUM",
        font=("Arial", 9, "bold")
    )

    twin_canvas.create_text(
        305,
        145,
        text=plant_name,
        font=("Arial", 11, "bold")
    )

    twin_canvas.create_line(
        405,
        135,
        470,
        135,
        arrow=tk.LAST
    )

    twin_canvas.create_rectangle(
        470,
        100,
        585,
        170
    )

    twin_canvas.create_text(
        528,
        122,
        text=cavity,
        width=95,
        font=("Arial", 9, "bold")
    )

    twin_canvas.create_text(
        528,
        152,
        text=f"{wavelength} nm\n{color}",
        font=("Arial", 9)
    )

    twin_canvas.create_text(
        305,
        225,
        text=(
            "Pump  →  Plant Active Medium  →  "
            "Resonator  →  Predicted Laser Output"
        ),
        font=("Arial", 10, "bold")
    )


def add_laser_readiness_section(parent, selected_plant):

    add_section_title(
        parent,
        "=== LASER READINESS INDEX ==="
    )

    lri_score = calculate_lri_score(
        selected_plant
    )

    readiness_status, confidence = classify_readiness(
        lri_score
    )

    add_info_line(
        parent,
        f"LRI Score : {lri_score}"
    )

    add_info_line(
        parent,
        readiness_status
    )

    add_info_line(
        parent,
        f"Prototype Confidence : {confidence}"
    )


def add_scientific_evidence_section(parent, selected_plant):

    add_section_title(
        parent,
        "=== SCIENTIFIC EVIDENCE ==="
    )

    trace_data = generate_scientific_trace(
        selected_plant
    )

    for item in trace_data:

        add_info_line(
            parent,
            item
        )

    add_section_title(
        parent,
        "=== SCIENTIFIC REASONING ==="
    )

    reasoning_data = generate_scientific_reasoning(
        selected_plant
    )

    for item in reasoning_data:

        add_info_line(
            parent,
            item
        )
        add_section_title(
        parent,
        "=== PHYSICS EVIDENCE ==="
    )

    physics_data = [

        f"Emission Strength : {selected_plant.get('emission_strength', 'N/A')}",

        f"Absorption Strength : {selected_plant.get('absorption_strength', 'N/A')}",

        f"Optical Quality : {selected_plant.get('optical_quality', 'N/A')}",

        f"Loss Indicator : {selected_plant.get('loss_indicator', 'N/A')}"

    ]

    for item in physics_data:

        add_info_line(
            parent,
            item
        )


def add_prototype_roadmap_section(parent):

    add_section_title(
        parent,
        "=== PROTOTYPE ROADMAP ==="
    )

    roadmap = [
        "✓ Material Selected",
        "✓ Laser Output Predicted",
        "✓ Laser Architecture Designed",
        "✓ Digital Twin Generated",
        "✓ Readiness Evaluated",
        "→ Next Step: Prototype Construction and Experimental Validation"
    ]

    for step in roadmap:

        add_info_line(
            parent,
            step
        )


def show_plant_details(event, tree, ranked_plants):

    selected_item = tree.selection()

    if not selected_item:
        return

    values = tree.item(
        selected_item[0]
    )["values"]

    plant_name = values[1]

    selected_plant = None

    for plant in ranked_plants:

        if plant.get("name") == plant_name:

            selected_plant = plant
            break

    if selected_plant is None:
        return

    details = tk.Toplevel()
    details.title(
        f"{plant_name} Scientific Profile"
    )
    details.geometry("820x900")

    outer_canvas = tk.Canvas(
        details
    )

    scrollbar = ttk.Scrollbar(
        details,
        orient="vertical",
        command=outer_canvas.yview
    )

    content = tk.Frame(
        outer_canvas
    )

    content.bind(
        "<Configure>",
        lambda event: outer_canvas.configure(
            scrollregion=outer_canvas.bbox("all")
        )
    )

    outer_canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    outer_canvas.configure(
        yscrollcommand=scrollbar.set
    )

    outer_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def _on_mousewheel(event):
        outer_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    outer_canvas.bind_all(
        "<MouseWheel>",
        _on_mousewheel
    )

    title = tk.Label(
        content,
        text=f"{plant_name} Scientific Profile",
        font=("Arial", 16, "bold")
    )

    title.pack(
        pady=10
    )

    summary = generate_executive_summary(
        selected_plant    )

    add_section_title(
        content,

        "=== EXECUTIVE SUMMARY ==="
    )

    executive_lines = [

        f"Plant : {summary['plant']}",

        f"Global Rank : #{summary['rank']}",

        f"Laser Color : {summary['laser_color']}",

        f"Emission Wavelength : {summary['wavelength']} nm",

        f"LRI Score : {summary['lri']}",

        f"Prototype Status : {summary['status']}",

        f"Confidence : {summary['confidence']}"    ]

    for line in executive_lines:

        add_info_line(
            content,
            line
        )

    intelligence_summary = selected_plant.get(
        "intelligence_summary",
        {}
    )

    add_section_title(
        content,
        "=== PLANT SCIENTIFIC PROFILE ==="
    )

    info = [
        f"Scientific Name      : {selected_plant.get('scientific_name', 'N/A')}",
        f"Origin               : {selected_plant.get('origin', 'N/A')}",
        f"Global Rank          : {selected_plant.get('global_rank', 'N/A')}",
        f"Material Score       : {selected_plant.get('material_score', 'N/A')}",
        f"Intelligence Score   : {intelligence_summary.get('intelligence_score', 'N/A')}",
        f"Patent Score         : {selected_plant.get('patent_potential_score', 'N/A')}",
        f"Thermal Score        : {selected_plant.get('thermal_score', 'N/A')}",
        f"Feasibility Score    : {selected_plant.get('feasibility_score', 'N/A')}",
        f"Q Factor Score       : {selected_plant.get('q_factor_score', 'N/A')}",
        f"Laser Color          : {selected_plant.get('laser_color', 'N/A')}",
        f"Absorption λ         : {selected_plant.get('lambda_abs', 'N/A')} nm",
        f"Emission λ           : {selected_plant.get('lambda_em', 'N/A')} nm",
        f"Fluorescence Region  : {selected_plant.get('fluorescence_region', 'N/A')}",
        f"Classification       : {selected_plant.get('classification', 'N/A')}",
        f"Governor Decision    : {selected_plant.get('governor_decision', 'N/A')}",
    ]

    for line in info:

        add_info_line(
            content,
            line
        )

    laser_output = selected_plant.get(
        "laser_output",
        {}
    )

    if not laser_output and predict_laser_output is not None:

        laser_output = predict_laser_output(
            selected_plant
        )

    add_section_title(
        content,
        "=== PREDICTED LASER OUTPUT ==="
    )

    laser_info = [
        f"Active Medium  : {laser_output.get('active_medium', selected_plant.get('name', 'N/A'))}",
        f"Wavelength     : {laser_output.get('emission_wavelength_nm', selected_plant.get('lambda_em', 'N/A'))} nm",
        f"Frequency      : {format_frequency(laser_output.get('frequency_hz', 'N/A'))}",
        f"Laser Color    : {laser_output.get('laser_color', selected_plant.get('laser_color', 'N/A'))}",
        f"Spectral Region: {laser_output.get('spectral_region', selected_plant.get('fluorescence_region', 'N/A'))}",
        f"Estimated Power: {laser_output.get('estimated_power', 'N/A')}",
        f"Laser Class    : {laser_output.get('proposed_laser_class', 'N/A')}",
        f"Validation     : {laser_output.get('validation_status', 'Theoretical Prediction - Requires Prototype Validation')}",
    ]

    for item in laser_info:

        add_info_line(
            content,
            item
        )

    architecture = generate_architecture_profile(
        selected_plant
    )

    add_section_title(
        content,
        "=== LASER SYSTEM ARCHITECTURE ==="
    )

    architecture_info = [
        f"Architecture : {architecture.get('architecture', 'N/A')}",
        f"Pump Source  : {architecture.get('pump_source', 'N/A')}",
        f"Cavity       : {architecture.get('cavity', 'N/A')}",
        f"Mirror 1     : {architecture.get('mirror_1', 'N/A')}",
        f"Mirror 2     : {architecture.get('mirror_2', 'N/A')}",
        f"Cooling      : {architecture.get('cooling', 'N/A')}",
        f"Validation   : {architecture.get('validation', 'N/A')}",
    ]

    for item in architecture_info:

        add_info_line(
            content,
            item
        )

    draw_digital_laser_twin(
        content,
        selected_plant,
        laser_output,
        architecture
    )

    add_laser_readiness_section(
        content,
        selected_plant
    )

    add_scientific_evidence_section(
        content,
        selected_plant
    )

    add_prototype_roadmap_section(
        content
    )

def generate_scientific_reasoning(plant):
        trace = []
        material_score = plant.get(
        "material_score",   0    )
        thermal_score = plant.get(
        "thermal_score",  0    )

        feasibility_score = plant.get(
        "feasibility_score",
        0    )

        q_factor_score = plant.get(
        "q_factor_score",
        0    )

        lri_score = plant.get(
        "lri_score",
        None    )

        if lri_score is None:

            lri_score = round(   (
                material_score
                + thermal_score
                + feasibility_score
                + q_factor_score
            ) / 4,
            2   )
            trace.append(
        "Scientific Evaluation Summary"    )
            if material_score >= 70:

              trace.append( "→ Material performance supports laser generation."
        )
              if thermal_score >= 80:
                  trace.append(
            "→ Thermal stability is excellent."        )

        if feasibility_score >= 80:
            trace.append( "→ Laser feasibility is high."   )

        if q_factor_score >= 80:

           trace.append(
            "→ Resonator quality potential is strong."     )
           trace.append(f"Combined LRI Score = {lri_score}"   )

        if lri_score >= 85:
            trace.append("→ FINAL DECISION: READY FOR PROTOTYPE"      )

        elif lri_score >= 60:

            trace.append(
            "→ FINAL DECISION: RESEARCH STAGE"    )
        else:

            trace.append( "→ FINAL DECISION: NEEDS OPTIMIZATION"        )

        return trace
