"""Unified knowledge and calculation payload for future local UI."""
from scientific_knowledge import knowledge_card
from scientific_pathways import build_pathways, PATHWAYS

def build_workspace(identifier, inputs, *, language="ar", pathway="student",
                    uncertainties=None, independent=False, correlation=None,
                    output_unit=None):
    if pathway not in PATHWAYS:
        raise ValueError("Unknown scientific pathway")
    card = knowledge_card(identifier, language)
    shared = build_pathways(identifier, inputs, uncertainties=uncertainties,
                            independent=independent, correlation=correlation,
                            output_unit=output_unit)
    focus = shared["pathways"][pathway]["focus"]
    return {"language":language, "pathway":pathway, "knowledge":card,
            "shared_result":shared["shared_result"], "focus":focus,
            "scientific_validation":False, "release_authorized":False}
