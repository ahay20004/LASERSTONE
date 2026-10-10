import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from plants_data import plants
from lsi_engine import calculate_lsi
from classifier import classify_lsi
from applications import predict_application
from display import display_plant_result
from code_repair_advisor import explain_runtime_error
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
CORE_DIR = os.path.join(ROOT_DIR, "core")
DATABASE_DIR = os.path.join(ROOT_DIR, "database")


if CORE_DIR not in sys.path:
    sys.path.insert(0, CORE_DIR)

if DATABASE_DIR not in sys.path:
    sys.path.insert(0, DATABASE_DIR)


from plants_data import plants
from laser_sources import laser_sources

from data_validator import validate_plant_data
from lsi_engine import calculate_lsi
from classifier import classify_lsi
from applications import predict_application
from color_predictor import predict_laser_color
from spectral_region import predict_spectral_region
from pump_predictor import predict_best_pump
from feasibility_engine import calculate_feasibility_score, classify_feasibility
from thermal_engine import evaluate_thermal_stability, classify_thermal_stability
from operation_mode_engine import evaluate_operation_mode
from photobleaching_engine import evaluate_photobleaching_stability, classify_photobleaching
from gain_ranking_engine import classify_gain_medium
from resonator_engine import recommend_resonator
from solvent_engine import recommend_solvent_environment
from spectral_analysis import analyze_spectrum
from gain_analysis import analyze_gain_medium
from spectral_quality_engine import calculate_spectral_quality
from global_ranking_engine import rank_plants
from qfactor_engine import evaluate_q_factor, classify_q_factor
from cavity_optimizer import optimize_laser_cavity
from beam_quality_engine import evaluate_beam_quality, classify_beam_quality
from efficiency_engine import evaluate_laser_efficiency, classify_laser_efficiency
from display import display_plant_result,display_plant_result,display_global_ranking
from interpretation_engine import generate_scientific_interpretation
from physics_model import (calculate_normalized_lsi, evaluate_gain_condition, estimate_laser_threshold)
from report_generator import save_all_reports
from material_score_engine import calculate_material_score, classify_material_score
from lri_engine import calculate_lri, classify_lri
from laser_architecture_engine import (recommend_laser_architecture)
from physics_consistency_engine import (evaluate_physics_consistency, classify_consistency )
from final_decision_engine import generate_final_decision
from scientific_recommendation_engine import (generate_scientific_recommendations)
from experimental_prediction_engine import (predict_experimental_success, classify_experimental_probability)
from research_novelty_engine import ( evaluate_research_novelty, classify_research_novelty )
from patent_potential_engine import (evaluate_patent_potential, classify_patent_potential)
from autonomous_discovery_engine import (discover_high_potential_patterns)
from laser_evolution_engine import (predict_material_evolution, classify_evolution_potential)
from hybrid_material_engine import (generate_hybrid_candidates)
from network_intelligence_engine import (build_material_network)
from scientific_confidence_engine import (calculate_scientific_confidence, classify_confidence)
from system_integrity_engine import (evaluate_system_integrity, classify_integrity)
from laserstone_governor import (laserstone_governor_decision)
from mission_control_engine import (generate_mission_control_summary)
from system_map import (LASERSTONE_SYSTEM_MAP)
from constants import MATERIAL_SCORE_WEIGHTS
from system_constants_validator import (run_configuration_validation)
from runtime_monitor_engine import (start_runtime_monitor, stop_runtime_monitor, generate_runtime_report )
from self_optimization_engine import (generate_self_optimization_report )
from audit_engine import (audit_plant) 
from system_health_engine import (generate_system_health_report, generate_system_health_summary )
from system_memory_engine import (generate_system_memory)
from strategic_advisor_engine import (generate_strategic_advice)
from platform_evolution_engine import (evaluate_platform_evolution)
from platform_evolution_engine import (evaluate_platform_evolution )
from final_snapshot_engine import (generate_final_snapshot)
from scientific_visualization_preparer import (prepare_visualization_data)
from chart_recommendation_engine import (recommend_scientific_charts)
from dashboard_layout_engine import (generate_dashboard_layout)
from gui_readiness_engine import (evaluate_gui_readiness)
from dashboard import launch_dashboard
from data_standardization_engine import (standardize_quality_value, classify_numeric_score )
from project_registry import (show_registered_engines,  registry_statistics, show_dependency_map, show_dependency_statistics, detect_unused_outputs )
from intelligence_hub import (generate_intelligence_summary, generate_system_health_report)
from laser_output_engine import predict_laser_output
from laserstone_master_roadmap import show_next_priority
from physics_evidence_engine import generate_physics_evidence
from project_diagnostic_engine import run_project_diagnostic
from plant_references import PLANT_REFERENCES
from plant_knowledge import PLANT_KNOWLEDGE
from plants_data import plants
from startup_diagnostic_engine import run_startup_diagnostic
from database.plant_identity import resolve_plant_name
from code_quality_guard import run_code_quality_guard








# Run startup diagnostic
if not run_startup_diagnostic():
    print("Startup diagnostic failed. Exiting.")
    exit(1)

def analyze_plant(plant):
    """Analyze a detached record; numeric gates do not certify physical validity."""
    import copy
    import math
    from g23_scientific_input_gate import validate_scientific_inputs
    from g23_checked_physics_consistency import assess_physics_consistency

    check = validate_scientific_inputs(plant)
    if not isinstance(plant, dict):
        return {"name": "Unknown", "valid": False, "missing_fields": [],
                "validation_status": "INVALID_INPUT", "validation_errors": check["errors"],
                "analysis_status": "BLOCKED", "analysis_stage": "INPUT"}
    plant = copy.deepcopy(plant)
    for field in ('analysis_stage', 'analysis_status', 'applications', 'audit_issues', 'audit_status', 'beam_quality_class', 'beam_quality_score', 'best_pump_laser', 'cavity_geometry', 'classification', 'cooling_system', 'cw_score', 'decision_basis', 'evolution_class', 'evolution_recommendations', 'evolution_score', 'experimental_success_class', 'experimental_success_score', 'feasibility_class', 'feasibility_score', 'final_decision', 'gain_class', 'gain_classification', 'gain_condition', 'gain_score', 'governor_decision', 'intelligence_summary', 'knowledge_info', 'laser_efficiency_class', 'laser_efficiency_score', 'laser_output', 'lri_class', 'lri_score', 'lsi', 'material_class', 'material_score', 'mirror_reflectivity', 'missing_fields', 'normalized_lsi', 'operation_mode', 'output_coupler', 'patent_potential_class', 'patent_potential_score', 'photobleaching_class', 'photobleaching_score', 'physical_validation_status', 'physics_consistency_class', 'physics_consistency_score', 'physics_consistency_status', 'predicted_color', 'predicted_region', 'pulsed_score', 'pump_efficiency', 'pump_source', 'q_factor_class', 'q_factor_score', 'recommended_length', 'recommended_resonator', 'recommended_solvent', 'reference_info', 'research_novelty_class', 'research_novelty_score', 'scientific_confidence_class', 'scientific_confidence_score', 'scientific_interpretation', 'scientific_recommendations', 'score_basis', 'solvent_reason', 'spectral_quality', 'spectral_quality_class', 'spectral_quality_score', 'stokes_shift', 'system_integrity_class', 'system_integrity_score', 'system_integrity_warnings', 'thermal_class', 'thermal_score', 'threshold_indicator', 'valid', 'validation_errors', 'validation_status'):
        plant.pop(field, None)
    raw = copy.deepcopy(plant)
    stage = "INPUT"

    def blocked(status, errors, missing=()):
        result = copy.deepcopy(raw)
        result.update(valid=False, missing_fields=list(missing),
                      validation_status=status, validation_errors=errors,
                      analysis_status="BLOCKED", analysis_stage=stage)
        return result

    def require_score(field, container=None):
        value = (plant if container is None else container).get(field)
        if (isinstance(value, bool) or not isinstance(value, (int, float))
                or not math.isfinite(value) or not 0 <= value <= 100):
            raise ValueError(f"{field}: required finite numeric score in [0, 100]")

    if not check["valid"]:
        return blocked("INVALID_INPUT", check["errors"])
    try:
        plant["name"] = resolve_plant_name(plant["name"])
        validation = validate_plant_data(plant)
        if not validation["valid"]:
            return blocked("INVALID_INPUT", {k: "Required field" for k in validation["missing"]}, validation["missing"])
        stage = "BASE_CALCULATIONS"
        lsi_result = calculate_lsi(plant['phi'], plant['tau'], plant['sigma_a'], plant['eta'], plant['knr'], plant['refractive_index'])
        pump_result = predict_best_pump(plant, laser_sources)
        spectral_result = analyze_spectrum(plant)
        gain_result = analyze_gain_medium(plant)
        plant['lsi'] = lsi_result
        plant['classification'] = classify_lsi(lsi_result)
        plant['normalized_lsi'] = calculate_normalized_lsi(plant)
        plant['gain_condition'] = evaluate_gain_condition(plant)
        plant['threshold_indicator'] = estimate_laser_threshold(plant)
        plant['applications'] = predict_application(lsi_result)
        plant['predicted_color'] = predict_laser_color(plant['lambda_em'])
        plant['predicted_region'] = predict_spectral_region(plant['lambda_em'])
        plant['pump_source'] = pump_result
        plant['best_pump_laser'] = pump_result['laser_name']
        plant['pump_efficiency'] = pump_result['estimated_efficiency']
        plant['spectral_quality'] = calculate_spectral_quality(plant)
        plant['stokes_shift'] = spectral_result['stokes_shift']
        plant['spectral_quality_score'] = standardize_quality_value(plant['spectral_quality'])
        require_score('spectral_quality_score')
        plant['spectral_quality_class'] = classify_numeric_score(plant['spectral_quality_score'])
        plant['gain_score'] = gain_result['gain_score']
        require_score('gain_score')
        plant['gain_classification'] = gain_result['gain_classification']
        plant['feasibility_score'] = calculate_feasibility_score(plant, lsi_result, pump_result)
        require_score('feasibility_score')
        plant['feasibility_class'] = classify_feasibility(plant['feasibility_score'])
        plant['thermal_score'] = evaluate_thermal_stability(plant)
        require_score('thermal_score')
        plant['thermal_class'] = classify_thermal_stability(plant['thermal_score'])
        operation_mode = evaluate_operation_mode(plant, plant['thermal_score'], plant['feasibility_score'])
        plant['operation_mode'] = operation_mode['mode']
        plant['cw_score'] = operation_mode['cw_score']
        require_score('cw_score')
        plant['pulsed_score'] = operation_mode['pulsed_score']
        require_score('pulsed_score')
        plant['photobleaching_score'] = evaluate_photobleaching_stability(plant, plant['thermal_score'], plant['feasibility_score'])
        require_score('photobleaching_score')
        plant['photobleaching_class'] = classify_photobleaching(plant['photobleaching_score'])
        plant['gain_class'] = classify_gain_medium(plant['gain_score'])
        plant['recommended_resonator'] = recommend_resonator(plant['gain_score'], plant['thermal_score'], plant['operation_mode'], plant['photobleaching_score'])
        solvent_data = recommend_solvent_environment(plant)
        plant['recommended_solvent'] = solvent_data['solvent']
        plant['solvent_reason'] = solvent_data['reason']
        plant['q_factor_score'] = evaluate_q_factor(plant, plant['gain_score'], plant['thermal_score'], plant['photobleaching_score'])
        require_score('q_factor_score')
        cavity_data = optimize_laser_cavity(plant['gain_score'], plant['q_factor_score'], plant['operation_mode'], plant['thermal_score'])
        plant['q_factor_class'] = classify_q_factor(plant['q_factor_score'])
        plant['mirror_reflectivity'] = cavity_data['mirror_reflectivity']
        plant['output_coupler'] = cavity_data['output_coupler']
        plant['cavity_geometry'] = cavity_data['geometry']
        plant['recommended_length'] = cavity_data['recommended_length']
        plant['cooling_system'] = cavity_data['cooling']
        plant['beam_quality_score'] = evaluate_beam_quality(plant['gain_score'], plant['q_factor_score'], plant['thermal_score'], cavity_data['geometry'], plant['operation_mode'])
        require_score('beam_quality_score')
        plant['beam_quality_class'] = classify_beam_quality(plant['beam_quality_score'])
        plant['laser_efficiency_score'] = evaluate_laser_efficiency(plant, plant['gain_score'], plant['q_factor_score'], plant['beam_quality_score'], plant['thermal_score'])
        require_score('laser_efficiency_score')
        plant['laser_efficiency_class'] = classify_laser_efficiency(plant['laser_efficiency_score'])
        plant['material_score'] = calculate_material_score(plant)
        require_score('material_score')
        plant['material_class'] = classify_material_score(plant['material_score'])
        stage = "LRI_AND_CONSISTENCY"
        plant["lri_score"] = calculate_lri(plant)
        require_score("lri_score")
        plant["lri_class"] = classify_lri(plant["lri_score"])
        consistency = assess_physics_consistency(plant)
        if consistency["status"] != "HEURISTIC_SCORE_ONLY":
            return blocked("INVALID_DERIVED_SCORES", consistency["errors"])
        plant["physics_consistency_score"] = consistency["score"]
        plant["physics_consistency_class"] = "Heuristic score only"
        plant["physics_consistency_status"] = consistency["status"]
        stage = "SECONDARY_SCORES"
        plant['experimental_success_score'] = predict_experimental_success(plant)
        require_score('experimental_success_score')
        plant['experimental_success_class'] = classify_experimental_probability(plant['experimental_success_score'])
        plant['research_novelty_score'] = evaluate_research_novelty(plant)
        require_score('research_novelty_score')
        plant['research_novelty_class'] = classify_research_novelty(plant['research_novelty_score'])
        plant['patent_potential_score'] = evaluate_patent_potential(plant)
        require_score('patent_potential_score')
        plant['patent_potential_class'] = classify_patent_potential(plant['patent_potential_score'])
        evolution_data = predict_material_evolution(plant)
        plant['evolution_score'] = evolution_data['score']
        require_score('evolution_score')
        plant['evolution_recommendations'] = evolution_data['recommendations']
        plant['evolution_class'] = classify_evolution_potential(plant['evolution_score'])
        plant['scientific_confidence_score'] = calculate_scientific_confidence(plant)
        require_score('scientific_confidence_score')
        plant['scientific_confidence_class'] = classify_confidence(plant['scientific_confidence_score'])
        integrity_data = evaluate_system_integrity(plant)
        plant['system_integrity_score'] = integrity_data['score']
        require_score('system_integrity_score')
        plant['system_integrity_warnings'] = integrity_data['warnings']
        plant['system_integrity_class'] = classify_integrity(plant['system_integrity_score'])
        intelligence_data = generate_intelligence_summary(plant)
        plant['intelligence_summary'] = intelligence_data
        require_score("intelligence_score", plant["intelligence_summary"])
        stage = "DECISION_SUPPORT"
        plant["score_basis"] = "HEURISTIC_MODEL_SCORES"
        plant["physical_validation_status"] = "NOT_ESTABLISHED_BY_THIS_PIPELINE"
        plant["decision_basis"] = "HEURISTIC_RESEARCH_TRIAGE_ONLY"
        plant["lri_class"] = "Heuristic tier: " + plant["lri_class"]
        plant["scientific_confidence_class"] = "Heuristic tier: " + plant["scientific_confidence_class"]
        plant["scientific_interpretation"] = ["Heuristic model interpretation: " + text for text in generate_scientific_interpretation(plant)]
        plant["scientific_recommendations"] = ["Heuristic research suggestion: " + text for text in generate_scientific_recommendations(plant)]
        plant["final_decision"] = "Heuristic research triage: " + generate_final_decision(plant)
        plant["governor_decision"] = "Heuristic research triage: " + laserstone_governor_decision(plant)
        plant["valid"] = True
        plant["missing_fields"] = []
        plant["validation_errors"] = {}
        plant["validation_status"] = "DOMAIN_SCREEN_PASSED"
        plant["analysis_status"] = "COMPLETE_HEURISTIC_ANALYSIS"
        plant["analysis_stage"] = "COMPLETE"
        return plant
    except Exception as exc:
        return blocked("ENGINE_ERROR", {stage: f"{type(exc).__name__}: {exc}"})


def main():

    if not run_startup_diagnostic():
        return
    if not run_code_quality_guard():
        return

        # بقية المشروع

  

       

    run_project_diagnostic()
    print("===================================")
    print("      LASERSTONE™ V1 SYSTEM")
    print("===================================")
    
    runtime_start = start_runtime_monitor()
    validation_report = (run_configuration_validation())
    print("\nCONFIGURATION VALIDATION")
    optimization_report = (generate_self_optimization_report() )
    print("\nSELF OPTIMIZATION REPORT")
    print(f"Optimization Status : " f"{optimization_report['optimization_status']}" )
    print("\nSuggestions:")
    for suggestion in (optimization_report["optimization_suggestions"] ):
        print(f"- {suggestion}")

    print(f"Material Weights : " f"{validation_report['material_weights']}")
    print(f"LRI Weights      : " f"{validation_report['lri_weights']}")
    print(f"Confidence Weights : " f"{validation_report['confidence_weights']}")
    print(f"Thresholds Valid : " f"{validation_report['thresholds_valid']}")
    print(f"System Valid     : " f"{validation_report['system_valid']}")






    analyzed_plants = []

    for plant in plants:
        analyzed_plant = analyze_plant(plant)

        if not analyzed_plant["valid"]:
            print("\nDATA VALIDATION ERROR")
            print(f"Plant: {analyzed_plant.get('name', 'Unknown')}")
            print("Validation errors:", analyzed_plant.get("validation_errors", {}))
            print("Missing Fields:")
            
            for field in analyzed_plant["missing_fields"]:
                print(f"- {field}")

            continue
        
        audit_data = audit_plant(analyzed_plant)
        analyzed_plant["audit_status"] = (audit_data["status"] )
        analyzed_plant["audit_issues"] = (audit_data["issues"] )

        analyzed_plants.append(analyzed_plant)
    
    if not analyzed_plants:
        print("No valid records; downstream analysis stopped.")
        return

    ranked_plants = rank_plants(analyzed_plants)

    autonomous_discoveries = (discover_high_potential_patterns(ranked_plants ))
    hybrid_candidates = (generate_hybrid_candidates(ranked_plants ))
    material_network = build_material_network(ranked_plants)



    print("\nNUMBER OF RANKED PLANTS:", len(ranked_plants))
    
    display_global_ranking(ranked_plants)

    for plant in ranked_plants:
        plant["laser_output"] = predict_laser_output(plant)
        plant_key = resolve_plant_name(
        plant.get("name")  )
        plant["reference_info"] = PLANT_REFERENCES.get( plant_key,  {}  )
        plant["knowledge_info"] = PLANT_KNOWLEDGE.get(
        plant_key,
        {}    )
        display_plant_result(plant)

    
    saved_reports = save_all_reports(ranked_plants)

    print("\nALL REPORTS GENERATED SUCCESSFULLY")
    print("\n--- GLOBAL MATERIAL ANALYSIS ---")
    print(f"Material Score      : {plant['material_score']} / 100")
    plant["laser_architecture"] = (recommend_laser_architecture(plant))
    
    print(f"Material Class      : {plant['material_class']}")
    print(f"LRI Score        : {plant.get('lri_score', 'NOT CALCULATED')} / 100")
    print(f"LRI Class        : {plant.get('lri_class', 'NOT CALCULATED')}")
    plant["mission_control"] = (generate_mission_control_summary(plant))
   
    
    for report_path in saved_reports:
        print(report_path)
    
    print("\n===================================")
    print("AUTONOMOUS DISCOVERY ENGINE")
    print("===================================")

    for discovery in autonomous_discoveries:
      print(f"- {discovery}")
      hybrid_candidates = (generate_hybrid_candidates(ranked_plants ))

      print("\n===================================")
      print("HYBRID LASER MATERIAL ANALYSIS")
      print("===================================")

    for hybrid in hybrid_candidates:

      print(f"{hybrid['hybrid']} " f"=> {hybrid['score']} / 100 " f"({hybrid['classification']})" )

    print("\n===================================")
    print("LASER MATERIAL NETWORK")
    print("===================================")

    for relation in material_network:
        print(f"{relation.get('source','UNKNOWN')} <-> " f"{relation.get('target','UNKNOWN')}" )

    print(f"Similarity : " f"{relation.get('similarity','UNKNOWN')}"     )

    print(f"Relationship : " f"{relation.get('relationship','UNKNOWN')}" )

    print("-----------------------------------")

    print("\n===================================")
    print("LASERSTONE MISSION CONTROL")
    print("===================================")
    
    for plant in ranked_plants:
       
       summary = plant.get("mission_control", {})
       print(f"Summary Name      : {summary.get('material_score', 'NOT CALCULATED')}")
       print(f"Risk              : {summary.get('risk', 'NOT CALCULATED')}")
       print(f"Final Pattern     : {summary.get('pattern', 'NOT CALCULATED')}")
       print(f"Decision          : {summary.get('decision', 'NOT CALCULATED')}")

    print("-----------------------------------")

    print("\n===================================")
    print("LASERSTONE SYSTEM MAP")
    print("===================================")
    for layer, engines in (
    LASERSTONE_SYSTEM_MAP.items()):
       print(f"\n{layer}")

    for engine in engines:

        print(f" - {engine}")
        
    runtime = stop_runtime_monitor(runtime_start)
    runtime_report = (generate_runtime_report(runtime, len(ranked_plants), len(LASERSTONE_SYSTEM_MAP) ))
    print("\n===================================")
    print("RUNTIME MONITOR")
    print("===================================")
    print(f"Runtime (s)      : " f"{runtime_report['runtime_seconds']}")
    print(f"Plants Processed : " f"{runtime_report['plants_processed']}")
    print(f"Active Layers    : " f"{runtime_report['engines_active']}" )
    print(f"System Status    : " f"{runtime_report['system_status']}")

    health_summary = generate_system_health_summary(ranked_plants, validation_report,
    optimization_report, runtime_report )
    system_memory = generate_system_memory(
    ranked_plants )
    strategic_advice = (generate_strategic_advice(ranked_plants) )
    platform_evolution = (evaluate_platform_evolution(ranked_plants) )
    final_snapshot = (generate_final_snapshot(ranked_plants, runtime_report, health_summary, platform_evolution    ) )
    visualization_data = (prepare_visualization_data(ranked_plants) )
    chart_recommendations = (recommend_scientific_charts(visualization_data ))
    dashboard_layout = (generate_dashboard_layout() )
    gui_readiness = evaluate_gui_readiness(visualization_data, chart_recommendations,
    dashboard_layout,  runtime_report,  health_summary )







    print("\n===================================")
    print("LASERSTONE SYSTEM HEALTH")
    print("===================================")
    print(f"Total Plants      : {health_summary['total_plants']}")
    print(f"PASS              : {health_summary['pass']}")
    print(f"WARNING           : {health_summary['warning']}")
    print(f"REVIEW REQUIRED   : {health_summary['review_required']}")
    print(f"Configuration OK  : {health_summary['configuration_valid']}")
    print(f"Optimization      : {health_summary['optimization_status']}")
    print(f"Runtime           : {health_summary['runtime_status']}")
    print(f"Platform Status   : {health_summary['platform_status']}")
    
    print("\n===================================")
    print("LASERSTONE SYSTEM MEMORY")
    print("===================================")
    print(f"Top Material        : " f"{system_memory['top_material']}" )
    print(f"Material Score      : " f"{system_memory['top_material_score']}")
    print(f"Top Intelligence    : " f"{system_memory['top_intelligence']}")
    print(f"Patent Potential    : " f"{system_memory['top_patent']}" )
    print(f"Governor Decision   : " f"{system_memory['top_decision']}" )
    
    print("\n===================================")
    print("STRATEGIC ADVISOR")
    print("===================================")
    
    for advice in strategic_advice:
        print(f"- {advice}")

    print("\n===================================")
    print("PLATFORM EVOLUTION STATUS")
    print("===================================")
    
    print(f"Evolution Index   : " f"{platform_evolution['evolution_index']}" )
    print(f"Platform Stage    : " f"{platform_evolution['stage']}" )

    print("\n===================================")
    print("LASERSTONE FINAL SNAPSHOT")
    print("===================================")
    print(f"Top Material      : " f"{final_snapshot['top_material']}" )
    print(f"Material Score    : " f"{final_snapshot['top_score']}" )
    print(f"Intelligence      : " f"{final_snapshot['top_intelligence']}" )
    print(f"Patent Potential  : " f"{final_snapshot['top_patent']}" )
    print(f"Governor Decision : " f"{final_snapshot['governor']}" )
    print(f"Platform Stage    : " f"{final_snapshot['platform_stage']}" )
    print(f"Runtime (s)       : " f"{final_snapshot['runtime']}")
    print(f"Platform Health   : " f"{final_snapshot['health']}" )

    print("\n===================================")
    print("VISUALIZATION DATA READY")
    print("===================================")

    print(f"Prepared Entries : " f"{len(visualization_data)}"  )

    print("\n===================================")
    print("SCIENTIFIC VISUALIZATION PLANNER")
    print("===================================")
    
    for chart in chart_recommendations:
        print(f"- {chart}")

    print("\n===================================")
    print("DASHBOARD LAYOUT ENGINE")
    print("===================================")
    
    for section, items in (dashboard_layout.items()  ):
        print(f"\n{section}")

    for item in items:

        print(f"- {item}")

    print("\n===================================")
    print("GUI READINESS ENGINE")
    print("===================================")
    
    print(f"GUI Readiness Score : {gui_readiness['score']} / 100")
    print(f"GUI Readiness Class : {gui_readiness['class']}")
    print("\nGUI Notes:")
    
    for note in gui_readiness["notes"]:
        print(f"- {note}")







    print("\n===================================")
    print("OPENING DASHBOARD NOW...")
    print("===================================")

    try:
        launch_dashboard(ranked_plants)
        print("DASHBOARD CLOSED SUCCESSFULLY")

    except Exception as error:
        print("\nDASHBOARD LAUNCH ERROR:")
        print(error)

    print("\n===================================")
    print("END LASERSTONE MAIN SYSTEM")
    print("===================================")


if __name__ == "__main__":

    try:
        main()

    except Exception as error:
        print("\nSYSTEM ERROR:")
        print(error)

    finally:
        print("\nRUNNING POST-SYSTEM DIAGNOSTICS...")

        try:
            generate_system_health_report()
        except Exception as error:
            print("Health report error:", error)

        try:
            show_next_priority()
        except Exception as error:
            print("Next priority error:", error)

        #show_registered_engines()
        #registry_statistics()
        #show_dependency_map()
        #show_dependency_statistics()
        #detect_unused_outputs()
        generate_system_health_report()
        show_next_priority()
    
