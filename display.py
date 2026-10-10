def display_plant_result(plant):

    print("\n" + "=" * 50)

    print(f"Analysis Basis: {plant.get('score_basis', 'UNSPECIFIED')}")
    print(f"Physical Validation: {plant.get('physical_validation_status', 'NOT ESTABLISHED')}")
    print(f"Decision Basis: {plant.get('decision_basis', 'UNSPECIFIED')}")
    if plant.get('valid') is False or plant.get('analysis_status') == 'BLOCKED':
        print("Analysis blocked:", plant.get('validation_errors', {}))
        return
    print(f"Plant: {plant.get('name', 'Unknown')}")
    print(f"Scientific Name: {plant.get('scientific_name', 'N/A')}")
    print(f"Origin: {plant.get('origin', 'N/A')}")

    print("-" * 50)

    print(f"Global Rank: #{plant.get('global_rank', 'N/A')}")
    print(f"Material Score: {plant.get('material_score', 'N/A')} / 100")
    print(f"Material Class: {plant.get('material_class', 'N/A')}")

    print("-" * 50)

    print(f"LSI Value: {plant.get('lsi', 'N/A')}")
    print(f"Classification: {plant.get('classification', 'N/A')}")
    print(f"Normalized LSI: {plant.get('normalized_lsi', 'N/A')} / 100")
    print(f"Gain Condition: {plant.get('gain_condition', 'N/A')}")
    print(f"Threshold Indicator: {plant.get('threshold_indicator', 'N/A')}")

    print("-" * 50)

    print(f"Feasibility Score: {plant.get('feasibility_score', 'N/A')} / 100")
    print(f"Feasibility Class: {plant.get('feasibility_class', 'N/A')}")
    print(f"Thermal Score: {plant.get('thermal_score', 'N/A')} / 100")
    print(f"Thermal Class: {plant.get('thermal_class', 'N/A')}")
    print(f"Photobleaching Score: {plant.get('photobleaching_score', 'N/A')} / 100")
    print(f"Photobleaching Class: {plant.get('photobleaching_class', 'N/A')}")
    
    print("-" * 50)

    print(f"Absorption λ: {plant.get('lambda_abs', 'N/A')} nm")
    print(f"Emission λ: {plant.get('lambda_em', 'N/A')} nm")
    print(f"Stokes Shift: {plant.get('stokes_shift', 'N/A')} nm")
    print(f"Predicted Laser Color: {plant.get('predicted_color', 'N/A')}")
    print(f"Spectral Region: {plant.get('predicted_region', 'N/A')}")
    print(f"Spectral Quality: {plant.get('spectral_quality', 'N/A')}")
    print(f"Spectral Quality Score: " f"{plant.get('spectral_quality_score', 'N/A')} / 100" )
    print(f"Spectral Quality Class: " f"{plant.get('spectral_quality_class', 'N/A')}" )
    print("-" * 50)

    print(f"Gain Score: {plant.get('gain_score', 'N/A')} / 100")
    print(f"Gain Classification: {plant.get('gain_classification', 'N/A')}")
    print(f"Gain Medium Class: {plant.get('gain_class', 'N/A')}")
    print(f"Best Pump Laser: {plant.get('best_pump_laser', 'N/A')}")
    print(f"Pump Efficiency: {plant.get('pump_efficiency', 'N/A')} %")

    print("-" * 50)
    print("--- LASER SYSTEM ARCHITECTURE ---")
    print(f"Recommended Architecture: {plant.get('laser_architecture', 'N/A')}")
    print(f"Recommended Resonator: {plant.get('recommended_resonator', 'N/A')}")
    print(f"Recommended Solvent: {plant.get('recommended_solvent', 'N/A')}")
    print(f"Solvent Reason: {plant.get('solvent_reason', 'N/A')}")

    print("-" * 50)

    print(f"Q-Factor Score: {plant.get('q_factor_score', 'N/A')} / 100")
    print(f"Q-Factor Class: {plant.get('q_factor_class', 'N/A')}")
    print(f"Mirror Reflectivity: {plant.get('mirror_reflectivity', 'N/A')}")
    print(f"Output Coupler: {plant.get('output_coupler', 'N/A')}")
    print(f"Cavity Geometry: {plant.get('cavity_geometry', 'N/A')}")
    print(f"Recommended Length: {plant.get('recommended_length', 'N/A')}")
    print(f"Cooling System: {plant.get('cooling_system', 'N/A')}")

    print("-" * 50)

    print(f"Beam Quality Score: {plant.get('beam_quality_score', 'N/A')} / 100")
    print(f"Beam Quality Class: {plant.get('beam_quality_class', 'N/A')}")
    print(f"Laser Efficiency: {plant.get('laser_efficiency_score', 'N/A')} / 100")
    print(f"Efficiency Class: {plant.get('laser_efficiency_class', 'N/A')}")

    print("\n--- LASER READINESS INDEX ---")
    print(f"LRI Score: {plant.get('lri_score', 'N/A')} / 100")
    print(f"LRI Classification: {plant.get('lri_class', 'N/A')}")

    print("\nApplications:")
    for app in plant.get("applications", []):
        print(f"- {app}")

    print("\n--- PHYSICS CONSISTENCY ---")
    print(f"Consistency Score: {plant.get('physics_consistency_score', 'N/A')} / 100")
    print(f"Consistency Class: {plant.get('physics_consistency_class', 'N/A')}")

    print("\n--- FINAL LASER DEVELOPMENT DECISION ---")
    print(f"Decision: {plant.get('final_decision', 'N/A')}")

    print("\n--- SCIENTIFIC RECOMMENDATIONS ---")
    for recommendation in plant.get("scientific_recommendations", []):
        print(f"- {recommendation}")

    print("\n--- EXPERIMENTAL PREDICTION ---")
    print(f"Experimental Success: {plant.get('experimental_success_score', 'N/A')} / 100")
    print(f"Prediction Class: {plant.get('experimental_success_class', 'N/A')}")

    print("\n--- RESEARCH NOVELTY ANALYSIS ---")
    print(f"Novelty Score: {plant.get('research_novelty_score', 'N/A')} / 100")
    print(f"Novelty Class: {plant.get('research_novelty_class', 'N/A')}")

    print("\n--- PATENT POTENTIAL ANALYSIS ---")
    print(f"Patent Potential: {plant.get('patent_potential_score', 'N/A')} / 100")
    print(f"Patent Classification: {plant.get('patent_potential_class', 'N/A')}")

    print("\n--- LASER EVOLUTION ANALYSIS ---")
    print(f"Evolution Potential: {plant.get('evolution_score', 'N/A')} / 100")
    print(f"Evolution Class: {plant.get('evolution_class', 'N/A')}")
    print("Evolution Recommendations:")
    for rec in plant.get("evolution_recommendations", []):
        print(f"- {rec}")

    print("\n--- SCIENTIFIC CONFIDENCE ---")
    print(f"Confidence Score: {plant.get('scientific_confidence_score', 'N/A')} / 100")
    print(f"Confidence Class: {plant.get('scientific_confidence_class', 'N/A')}")

    print("\n--- SYSTEM INTEGRITY ---")
    print(f"Integrity Score: {plant.get('system_integrity_score', 'N/A')} / 100")
    print(f"Integrity Class: {plant.get('system_integrity_class', 'N/A')}")
    print("Integrity Warnings:")
    for warning in plant.get("system_integrity_warnings", []):
        print(f"- {warning}")

    print("\n--- CENTRAL INTELLIGENCE HUB ---")
    intelligence = plant.get("intelligence_summary", {})
    print(f"Unified Intelligence: {intelligence.get('intelligence_score', 'N/A')} / 100")
    print(f"Intelligence Class: {intelligence.get('classification', 'N/A')}")

    print("\n--- LASERSTONE AI GOVERNOR ---")
    print(f"Governor Decision: {plant.get('governor_decision', 'N/A')}")

    print("\n--- AUDIT MODE ---")
    print(f"Audit Status: {plant.get('audit_status', 'N/A')}")
    print("Audit Notes:")
    for note in plant.get("audit_issues", []):
        print(f"- {note}")

    print("\nScientific Interpretation:")
    for line in plant.get("scientific_interpretation", []):
        print(f"- {line}")

    print("=" * 50)

      
    physics_keys = [
        "emission_strength",
        "absorption_strength",
        "optical_quality",
        "loss_indicator"
    ]
       
    print("\n=== PHYSICS EVIDENCE ===")

    if all(key in plant for key in physics_keys):
        print(f"Emission Strength : {plant.get('emission_strength')}")
        print(f"Absorption Strength : {plant.get('absorption_strength')}")
        print(f"Optical Quality : {plant.get('optical_quality')}")
        print(f"Loss Indicator : {plant.get('loss_indicator')}")
    else:
        print("Physics Evidence Status: NOT CALCULATED")
        print("Required: generate_physics_evidence(plant) before display_plant_result(plant)")

    print("=" * 50)

    print("\n--- REFERENCE DATA ---")
    ref = plant.get("reference_info", {})
    knowledge = plant.get("knowledge_info", {})

    print(f"Reference ID: {ref.get('reference_id', 'N/A')}")
    print(f"Confidence: {ref.get('confidence', 'N/A')}")
    print(f"Source Type: {ref.get('source_type', 'N/A')}")

    print("\n--- KNOWLEDGE PROFILE ---")
    print(f"Application: {knowledge.get('application', 'N/A')}")
    print(f"Research Status: {knowledge.get('research_status', 'N/A')}")
    print(f"Confidence Score: {knowledge.get('confidence_score', 'N/A')}")
    print(f"Country: {knowledge.get('country', 'N/A')}")
    print(f"Notes: {knowledge.get('notes', 'N/A')}")

    
def display_global_ranking(ranked_plants):

    print("\n===================================")
    print("        GLOBAL LASER RANKING")
    print("===================================")

    for plant in ranked_plants:

        print(
            f"#{plant.get('global_rank', 'N/A')} "
            f"{plant.get('name', 'Unknown')} "
            f"→ Material Score: {plant.get('material_score', 'N/A')} "
            f"→ Class: {plant.get('material_class', 'N/A')}"
        )

    print("===================================")
