import os
from collections import Counter

import project_registry as project_registry_module

PROJECT_REGISTRY = project_registry_module.PROJECT_REGISTRY


# ============================================================
# LASERSTONE AUTHORITATIVE REGISTRY AUTO BUILDER
# G-1 SOURCE-OF-TRUTH ENABLED
# ============================================================

REGISTRY_BUILDER_VERSION = "2.0"

ACTIVE_ROOT = os.path.realpath(
    os.path.dirname(os.path.abspath(__file__))
)

EXPECTED_ACTIVE_PROJECT_NAME = "project 1"

ENGINE_SUFFIX = "_engine.py"

EXCLUDED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "env",
    "backup",
    "backups",
    "archive",
    "archives",
    "history",
    "historical",
}

EXCLUDED_FILE_MARKERS = (
    ".bak",
    "_before_",
    "_backup",
    "_old",
    "_copy",
)

KNOWN_NON_ENGINE_COMPONENTS = {
    "intelligence_hub",
    "laser_sources",
    "spectral_analysis",
    "spectral_region",
}

REQUIRED_OPERATIONAL_FIELDS = {
    "status",
    "category",
    "standardized",
    "dashboard_visible",
    "inputs",
    "outputs",
}

SCIENTIFIC_METADATA_FIELDS = {
    "evidence_status",
    "source",
    "doi",
    "experimental_condition",
    "units",
    "uncertainty",
    "equation",
    "validity_domain",
    "value_origin",
}


# ============================================================
# 1. PATH / SOURCE-OF-TRUTH UTILITIES
# ============================================================

def normalize_path(path):
    if not path:
        return None

    return os.path.normcase(
        os.path.realpath(
            os.path.abspath(path)
        )
    )


def is_inside_active_root(path):
    if not path:
        return False

    try:
        normalized_path = normalize_path(path)
        normalized_root = normalize_path(ACTIVE_ROOT)

        return os.path.commonpath(
            [normalized_path, normalized_root]
        ) == normalized_root

    except (ValueError, TypeError):
        return False


def is_excluded_directory(directory_name):
    name = directory_name.lower()

    if name in EXCLUDED_DIRECTORIES:
        return True

    if "backup" in name:
        return True

    if "archive" in name:
        return True

    if "historical" in name:
        return True

    return False


def is_excluded_file(file_name):
    lower_name = file_name.lower()

    for marker in EXCLUDED_FILE_MARKERS:
        if marker in lower_name:
            return True

    return False


# ============================================================
# 2. G-1 SOURCE-OF-TRUTH GATE
# ============================================================

def source_of_truth_gate():
    """
    Mandatory G-1 gate.

    Normal runtime/discovery is restricted to ACTIVE_ROOT.
    Historical and backup copies are never automatic fallbacks.
    """

    checks = []
    critical_failures = []

    active_root_exists = os.path.isdir(ACTIVE_ROOT)

    checks.append(
        (
            "Active root exists",
            active_root_exists,
            ACTIVE_ROOT,
        )
    )

    active_project_name = os.path.basename(ACTIVE_ROOT)

    project_identity_ok = (
        active_project_name.lower()
        == EXPECTED_ACTIVE_PROJECT_NAME.lower()
    )

    checks.append(
        (
            "Authoritative project identity",
            project_identity_ok,
            active_project_name,
        )
    )

    builder_path = normalize_path(__file__)

    builder_inside_root = is_inside_active_root(
        builder_path
    )

    checks.append(
        (
            "registry_auto_builder.py inside Active Root",
            builder_inside_root,
            builder_path,
        )
    )

    registry_path = normalize_path(
        getattr(
            project_registry_module,
            "__file__",
            None,
        )
    )

    registry_inside_root = is_inside_active_root(
        registry_path
    )

    checks.append(
        (
            "project_registry.py resolved inside Active Root",
            registry_inside_root,
            registry_path,
        )
    )

    registry_available = isinstance(
        PROJECT_REGISTRY,
        dict,
    )

    checks.append(
        (
            "PROJECT_REGISTRY available",
            registry_available,
            type(PROJECT_REGISTRY).__name__,
        )
    )

    if not active_root_exists:
        critical_failures.append(
            "ACTIVE_ROOT_NOT_FOUND"
        )

    if not project_identity_ok:
        critical_failures.append(
            "PROJECT_IDENTITY_MISMATCH"
        )

    if not builder_inside_root:
        critical_failures.append(
            "REGISTRY_BUILDER_OUTSIDE_ACTIVE_ROOT"
        )

    if not registry_inside_root:
        critical_failures.append(
            "SHADOW_PROJECT_REGISTRY_IMPORT"
        )

    if not registry_available:
        critical_failures.append(
            "PROJECT_REGISTRY_INVALID"
        )

    gate_status = (
        "RED"
        if critical_failures
        else "GREEN"
    )

    return {
        "gate": "G-1",
        "name": "SOURCE OF TRUTH",
        "status": gate_status,
        "active_root": ACTIVE_ROOT,
        "checks": checks,
        "critical_failures": critical_failures,
        "historical_fallback": False,
    }


def show_source_of_truth_gate():
    result = source_of_truth_gate()

    print(
        "\n=== G-1 SOURCE OF TRUTH GATE ===\n"
    )

    print(
        f"Registry Builder Version : "
        f"{REGISTRY_BUILDER_VERSION}"
    )

    print(
        f"Active Root              : "
        f"{result['active_root']}"
    )

    print(
        f"Gate Status              : "
        f"{result['status']}"
    )

    print(
        "Historical Fallback      : DISABLED"
    )

    print()

    for name, passed, detail in result["checks"]:

        state = "PASS" if passed else "FAIL"

        print(
            f"[{state}] {name}"
        )

        if detail is not None:
            print(
                f"       {detail}"
            )

    if result["critical_failures"]:

        print(
            "\nCritical Failures:"
        )

        for failure in result[
            "critical_failures"
        ]:
            print(
                f"  - {failure}"
            )

    else:
        print(
            "\nAuthoritative project identity verified."
        )

    print(
        "\nPolicy:"
    )

    print(
        "  Normal discovery is restricted "
        "to the Active Root."
    )

    print(
        "  Backup / Alpha / historical copies "
        "are not runtime fallbacks."
    )

    print(
        "  Missing active components remain "
        "missing until explicitly repaired."
    )

    return result


# ============================================================
# 3. ACTIVE ENGINE DISCOVERY
# ============================================================

def discover_engine_files():
    """
    Discover engine files inside ACTIVE_ROOT only.

    Backup/history-like files and directories are excluded.
    """

    discovered_files = {}

    for folder, directories, files in os.walk(
        ACTIVE_ROOT
    ):

        directories[:] = [
            directory
            for directory in directories
            if not is_excluded_directory(
                directory
            )
        ]

        if not is_inside_active_root(folder):
            continue

        for file_name in files:

            if not file_name.endswith(
                ENGINE_SUFFIX
            ):
                continue

            if is_excluded_file(file_name):
                continue

            file_path = os.path.join(
                folder,
                file_name,
            )

            if not is_inside_active_root(
                file_path
            ):
                continue

            engine_name = file_name[:-3]

            discovered_files.setdefault(
                engine_name,
                [],
            ).append(
                normalize_path(file_path)
            )

    return discovered_files


def discover_engines():
    return sorted(
        discover_engine_files().keys()
    )


def detect_active_duplicate_engines():
    duplicates = {}

    for engine_name, paths in (
        discover_engine_files().items()
    ):

        unique_paths = sorted(
            set(paths)
        )

        if len(unique_paths) > 1:
            duplicates[
                engine_name
            ] = unique_paths

    return duplicates


def show_discovered_engines():
    gate = source_of_truth_gate()

    print(
        "\n=== ACTIVE ENGINE DISCOVERY ===\n"
    )

    if gate["status"] != "GREEN":

        print(
            "Discovery blocked by G-1."
        )

        print(
            "No historical fallback attempted."
        )

        return []

    engines = discover_engines()

    print(
        f"Active Root: {ACTIVE_ROOT}\n"
    )

    for engine in engines:
        print(
            f"  {engine}"
        )

    print(
        "\n----------------------------"
    )

    print(
        f"Total Active Engine Files: "
        f"{len(engines)}"
    )

    duplicates = (
        detect_active_duplicate_engines()
    )

    if duplicates:

        print(
            "\nWARNING: duplicate active engine "
            "names detected:"
        )

        for engine_name, paths in (
            duplicates.items()
        ):

            print(
                f"\n  {engine_name}"
            )

            for path in paths:
                print(
                    f"    {path}"
                )

    else:
        print(
            "Active duplicate engine names: 0"
        )

    return engines


# ============================================================
# 4. REGISTRY RECONCILIATION
# ============================================================

def get_registry_reconciliation():
    gate = source_of_truth_gate()

    if gate["status"] != "GREEN":

        return {
            "gate_status": "RED",
            "discovered": [],
            "registered": [],
            "matched": [],
            "missing": [],
            "registered_without_engine_file": [],
            "known_non_engine": [],
            "unresolved_registered": [],
            "coverage": 0.0,
        }

    discovered = set(
        discover_engines()
    )

    registered = set(
        PROJECT_REGISTRY.keys()
    )

    matched = discovered & registered

    missing = discovered - registered

    registered_without_engine_file = (
        registered - discovered
    )

    known_non_engine = (
        registered_without_engine_file
        & KNOWN_NON_ENGINE_COMPONENTS
    )

    unresolved_registered = (
        registered_without_engine_file
        - KNOWN_NON_ENGINE_COMPONENTS
    )

    if discovered:
        coverage = (
            len(matched)
            / len(discovered)
        ) * 100.0
    else:
        coverage = 0.0

    return {
        "gate_status": "GREEN",
        "discovered": sorted(discovered),
        "registered": sorted(registered),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "registered_without_engine_file":
            sorted(
                registered_without_engine_file
            ),
        "known_non_engine":
            sorted(known_non_engine),
        "unresolved_registered":
            sorted(unresolved_registered),
        "coverage": coverage,
    }


def compare_with_registry():
    result = get_registry_reconciliation()

    print(
        "\n=== REGISTRY RECONCILIATION ===\n"
    )

    if result["gate_status"] != "GREEN":

        print(
            "Reconciliation blocked by G-1."
        )

        return result

    print(
        f"Discovered Active Engines : "
        f"{len(result['discovered'])}"
    )

    print(
        f"Registered Entries        : "
        f"{len(result['registered'])}"
    )

    print(
        f"Verified Name Matches     : "
        f"{len(result['matched'])}"
    )

    print(
        f"Awaiting Registry Audit   : "
        f"{len(result['missing'])}"
    )

    print(
        f"Registered Without "
        f"_engine.py Match : "
        f"{len(result['registered_without_engine_file'])}"
    )

    print(
        f"Known Non-Engine Entries  : "
        f"{len(result['known_non_engine'])}"
    )

    print(
        f"Unresolved Registered     : "
        f"{len(result['unresolved_registered'])}"
    )

    print(
        f"Discovery Coverage        : "
        f"{result['coverage']:.2f}%"
    )

    print(
        "\n--- MATCHED ---"
    )

    for engine in result["matched"]:
        print(
            f"  {engine}"
        )

    print(
        "\n--- AWAITING CODE AUDIT ---"
    )

    for engine in result["missing"]:
        print(
            f"  {engine}"
        )

    print(
        "\n--- KNOWN NON-ENGINE COMPONENTS ---"
    )

    for component in (
        result["known_non_engine"]
    ):
        print(
            f"  {component}"
        )

    if result[
        "unresolved_registered"
    ]:

        print(
            "\n--- UNRESOLVED REGISTERED ENTRIES ---"
        )

        for component in (
            result[
                "unresolved_registered"
            ]
        ):
            print(
                f"  {component}"
            )

    return result


# ============================================================
# 5. CATEGORY SUPPORT
# ============================================================

def suggest_category(engine_name):
    """
    Organizational suggestion only.
    This is not scientific verification.
    """

    name = engine_name.lower()

    if "audit" in name:
        return "System Audit"

    if "dashboard" in name:
        return "User Interface"

    if "gui" in name:
        return "User Interface"

    if "evidence" in name:
        return "Scientific Evidence"

    if "trace" in name:
        return "Scientific Traceability"

    if "physics" in name:
        return "Physics Core"

    if "laser" in name:
        return "Laser Engineering"

    if "prediction" in name:
        return "Scientific Prediction"

    if "recommendation" in name:
        return "Decision Support"

    if "decision" in name:
        return "Decision Support"

    if "dependency" in name:
        return "Dependency Intelligence"

    if "health" in name:
        return "System Health"

    if "memory" in name:
        return "System Memory"

    if "mission" in name:
        return "Mission Control"

    if "optimization" in name:
        return "System Optimization"

    if "discovery" in name:
        return "Scientific Discovery"

    if "hybrid" in name:
        return "Hybrid Materials"

    if "solvent" in name:
        return "Material Environment"

    if "resonator" in name:
        return "Laser Engineering"

    return "Requires Audit"


def category_report():
    category_counts = Counter()

    for _, info in (
        PROJECT_REGISTRY.items()
    ):

        category = info.get(
            "category",
            "Unclassified",
        )

        category_counts[
            category
        ] += 1

    print(
        "\n=== CATEGORY ANALYSIS REPORT ===\n"
    )

    for category, count in sorted(
        category_counts.items()
    ):

        print(
            f"{category}: {count}"
        )

    print(
        "\n----------------------------"
    )

    print(
        f"Total Categories: "
        f"{len(category_counts)}"
    )

    print(
        f"Total Registered Engines: "
        f"{len(PROJECT_REGISTRY)}"
    )

    return dict(category_counts)


# ============================================================
# 6. SAFE REGISTRY CANDIDATE REPORT
# ============================================================

def suggest_missing_registry_entries():
    """
    Missing engines are audit candidates only.

    Inputs, outputs, equations and evidence are never fabricated.

    No PROJECT_REGISTRY mutation occurs here.
    """

    result = get_registry_reconciliation()

    print(
        "\n=== REGISTRY AUDIT CANDIDATES ===\n"
    )

    if result["gate_status"] != "GREEN":

        print(
            "Candidate analysis blocked by G-1."
        )

        return []

    missing_engines = result["missing"]

    if not missing_engines:

        print(
            "No missing active engine entries."
        )

        return []

    print(
        "These are audit candidates only."
    )

    print(
        "Inputs/outputs are NOT inferred."
    )

    print(
        "No PROJECT_REGISTRY mutation "
        "will be performed.\n"
    )

    candidates = []

    for engine in missing_engines:

        candidate = {
            "engine": engine,
            "suggested_category":
                suggest_category(engine),
            "inputs":
                "REQUIRES CODE AUDIT",
            "outputs":
                "REQUIRES CODE AUDIT",
            "equations":
                "REQUIRES CODE AUDIT",
            "evidence":
                "REQUIRES CODE AUDIT",
            "runtime_use":
                "REQUIRES CODE AUDIT",
            "status":
                "UNVERIFIED",
        }

        candidates.append(candidate)

        print(
            f"{engine}"
        )

        print(
            f"  Suggested Category : "
            f"{candidate['suggested_category']}"
        )

        print(
            "  Inputs             : "
            "REQUIRES CODE AUDIT"
        )

        print(
            "  Outputs            : "
            "REQUIRES CODE AUDIT"
        )

        print(
            "  Equations          : "
            "REQUIRES CODE AUDIT"
        )

        print(
            "  Evidence           : "
            "REQUIRES CODE AUDIT"
        )

        print(
            "  Runtime Use        : "
            "REQUIRES CODE AUDIT"
        )

        print(
            "  Status             : "
            "UNVERIFIED\n"
        )

    return candidates


# ============================================================
# 7. REGISTRY METADATA AUDIT
# ============================================================

def registry_metadata_audit():
    print(
        "\n=== REGISTRY METADATA AUDIT ===\n"
    )

    total_entries = len(
        PROJECT_REGISTRY
    )

    operational_complete = 0

    scientific_presence = {
        field: 0
        for field in (
            SCIENTIFIC_METADATA_FIELDS
        )
    }

    incomplete_operational = []

    for engine_name, info in (
        PROJECT_REGISTRY.items()
    ):

        missing_operational = [
            field
            for field in (
                REQUIRED_OPERATIONAL_FIELDS
            )
            if field not in info
        ]

        if not missing_operational:
            operational_complete += 1

        else:
            incomplete_operational.append(
                (
                    engine_name,
                    missing_operational,
                )
            )

        for field in (
            SCIENTIFIC_METADATA_FIELDS
        ):

            if field in info:
                scientific_presence[
                    field
                ] += 1

    print(
        f"Registry Entries: "
        f"{total_entries}"
    )

    print(
        f"Operational Metadata Complete: "
        f"{operational_complete}/"
        f"{total_entries}"
    )

    if incomplete_operational:

        print(
            "\nOperational Metadata Gaps:"
        )

        for engine_name, fields in (
            incomplete_operational
        ):

            print(
                f"  {engine_name}: "
                f"{', '.join(fields)}"
            )

    print(
        "\nScientific Metadata Presence:"
    )

    for field in sorted(
        SCIENTIFIC_METADATA_FIELDS
    ):

        print(
            f"  {field}: "
            f"{scientific_presence[field]}/"
            f"{total_entries}"
        )

    print(
        "\nImportant:"
    )

    print(
        "Scientific metadata presence "
        "does not prove scientific validity."
    )

    return {
        "total_entries": total_entries,
        "operational_complete":
            operational_complete,
        "incomplete_operational":
            incomplete_operational,
        "scientific_presence":
            scientific_presence,
    }


# ============================================================
# 8. FROZEN ARCHITECTURAL POLICY
# ============================================================

def audit_summary():
    result = get_registry_reconciliation()
    gate = source_of_truth_gate()

    print(
        "\n=== LASERSTONE REGISTRY AUDIT SUMMARY ===\n"
    )

    print(
        f"G-1 Source-of-Truth : "
        f"{gate['status']}"
    )

    print(
        f"Active Root         : "
        f"{ACTIVE_ROOT}"
    )

    print(
        "Historical Fallback : DISABLED"
    )

    if result["gate_status"] == "GREEN":

        print(
            f"Physical Engines    : "
            f"{len(result['discovered'])}"
        )

        print(
            f"Registry Entries    : "
            f"{len(result['registered'])}"
        )

        print(
            f"Verified Matches    : "
            f"{len(result['matched'])}"
        )

        print(
            f"Awaiting Audit      : "
            f"{len(result['missing'])}"
        )

        print(
            f"Known Non-Engine    : "
            f"{len(result['known_non_engine'])}"
        )

        print(
            f"Unresolved Entries  : "
            f"{len(result['unresolved_registered'])}"
        )

        print(
            f"Coverage            : "
            f"{result['coverage']:.2f}%"
        )

    print(
        "\n=== FROZEN SAFETY POLICY ===\n"
    )

    policies = [
        (
            "1. Active Root is the only normal "
            "runtime/discovery source."
        ),
        (
            "2. Backup, Alpha and historical copies "
            "are excluded by default."
        ),
        (
            "3. Missing active component does not "
            "authorize historical fallback."
        ),
        (
            "4. File existence does not prove "
            "scientific validity."
        ),
        (
            "5. Registry presence does not prove "
            "runtime use."
        ),
        (
            "6. Missing registry entry does not "
            "mean inactive."
        ),
        (
            "7. Inputs and outputs must be verified "
            "from source code."
        ),
        (
            "8. Equations must be verified from "
            "implementation."
        ),
        (
            "9. Scientific evidence must remain "
            "traceable."
        ),
        (
            "10. Missing is not Zero."
        ),
        (
            "11. Measured, Derived and Predicted "
            "values remain distinct."
        ),
        (
            "12. Multiple engines do not constitute "
            "independent evidence when assumptions "
            "are shared."
        ),
        (
            "13. No automatic PROJECT_REGISTRY "
            "mutation is performed here."
        ),
        (
            "14. GREEN means structural gate pass, "
            "not automatic scientific verification."
        ),
    ]

    for policy in policies:
        print(
            policy
        )

    print(
        "\nRegistry Builder Role:"
    )

    print(
        "  Authoritative Registry / Reconciliation"
    )

    print(
        "  G-1 Source-of-Truth Control"
    )

    print(
        "\nMaster Audit Role:"
    )

    print(
        "  project_audit_engine.py"
    )

    print(
        "\nDecision Architecture:"
    )

    print(
        "  G-1 -> G0 -> G1 -> G2 -> G3 "
        "-> G4 -> G5 -> G6 -> G7"
    )

    print(
        "\nExecution States:"
    )

    print(
        "  GREEN : execute / verify / record"
    )

    print(
        "  AMBER : investigate / gather evidence"
    )

    print(
        "  RED   : isolate affected branch"
    )

    return {
        "gate": gate,
        "reconciliation": result,
    }


# ============================================================
# 9. MAIN
# ============================================================

def main():
    gate = show_source_of_truth_gate()

    if gate["status"] != "GREEN":

        print(
            "\nLASERSTONE REGISTRY CONTROL STOPPED."
        )

        print(
            "Reason: G-1 Source-of-Truth failure."
        )

        print(
            "No fallback to backup/history "
            "has been attempted."
        )

        return

    show_discovered_engines()

    compare_with_registry()

    category_report()

    registry_metadata_audit()

    suggest_missing_registry_entries()

    audit_summary()


if __name__ == "__main__":
    main()