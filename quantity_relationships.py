"""Read-only relationship discovery from registered equations; no inferred causality."""
from physical_quantities import get_quantity
from physical_constants import get_record
from equation_registry import REGISTRY, check_equation

def describe_quantity(identifier):
    quantity = get_quantity(identifier)
    produced_by = []
    used_by = []
    for key, eq in REGISTRY.items():
        if eq.output == identifier:
            produced_by.append(key)
        if any(kind == "quantity" and name == identifier
               for kind, name, power in eq.factors):
            used_by.append(key)
    return {"identifier": identifier, "symbol": quantity.symbol,
            "unit": quantity.unit, "dimensions": quantity.dimensions,
            "produced_by": tuple(produced_by), "used_by": tuple(used_by)}

def describe_equation(identifier):
    eq = REGISTRY[identifier]
    return {"identifier": identifier, "expression": eq.expression,
            "output": describe_quantity(eq.output),
            "inputs": tuple((name, power, describe_quantity(name))
                            for kind, name, power in eq.factors if kind == "quantity"),
            "constants": tuple((name, power, get_record(name))
                               for kind, name, power in eq.factors if kind == "constant"),
            "conditions": eq.conditions,
            "dimensional_assessment": check_equation(identifier),
            "scientific_validation": False}


def export_graph():
    """Return JSON-compatible nodes and directed dependency edges."""
    nodes = {}
    edges = []
    for identifier, eq in sorted(REGISTRY.items()):
        equation_id = "equation:" + identifier
        nodes[equation_id] = {"id": equation_id, "kind": "equation",
                              "label": eq.expression, "conditions": eq.conditions}
        for kind, name, power in eq.factors:
            node_id = kind + ":" + name
            record = get_record(name) if kind == "constant" else get_quantity(name)
            nodes[node_id] = {"id": node_id, "kind": kind, "label": record.symbol,
                              "unit": record.unit, "dimensions": list(record.dimensions)}
            edges.append({"source": node_id, "target": equation_id,
                          "relation": "input", "power": power})
        output_id = "quantity:" + eq.output
        record = get_quantity(eq.output)
        nodes[output_id] = {"id": output_id, "kind": "quantity", "label": record.symbol,
                            "unit": record.unit, "dimensions": list(record.dimensions)}
        edges.append({"source": equation_id, "target": output_id, "relation": "output"})
    return {"nodes": list(nodes.values()), "edges": edges,
            "scientific_validation": False}
