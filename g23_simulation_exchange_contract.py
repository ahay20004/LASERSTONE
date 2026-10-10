"""G23 simulation exchange contract; no external simulator is invoked.

Standard-library-only validation of a transport envelope. Passing this
contract does not validate the underlying physics or provenance claims.
"""
import math

SUPPORTED = frozenset({"python", "matlab", "scaps-1d", "comsol", "zemax", "lumerical"})
REQUIRED = ("simulator", "simulator_version", "model_id", "run_id",
            "inputs", "outputs", "conditions", "provenance")


def validate_simulation_envelope(envelope):
    errors = {}
    if not isinstance(envelope, dict):
        return {"valid": False, "errors": {"envelope": "Expected dictionary"},
                "status": "CONTRACT_ONLY"}
    for key in REQUIRED:
        if key not in envelope:
            errors[key] = "Missing required field"
    if errors:
        return {"valid": False, "errors": errors, "status": "CONTRACT_ONLY"}
    if (not isinstance(envelope["simulator"], str)
            or envelope["simulator"] not in SUPPORTED):
        errors["simulator"] = "Unknown simulator identifier"
    for key in ("simulator_version", "model_id", "run_id"):
        if not isinstance(envelope[key], str) or not envelope[key].strip():
            errors[key] = "Required nonempty string"
    for key in ("inputs", "outputs"):
        items = envelope[key]
        if not isinstance(items, dict) or not items:
            errors[key] = "Expected nonempty mapping"
            continue
        for name, datum in items.items():
            if not isinstance(name, str) or not name.strip():
                errors[key] = "Variable names must be nonempty strings"
                continue
            if not isinstance(datum, dict):
                errors[f"{key}.{name}"] = "Expected value/unit record"
                continue
            value, unit = datum.get("value"), datum.get("unit")
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                errors[f"{key}.{name}.value"] = "Expected finite numeric scalar"
            else:
                try:
                    finite = math.isfinite(value)
                except (ValueError, TypeError, OverflowError):
                    finite = False
                if not finite:
                    errors[f"{key}.{name}.value"] = "Expected finite numeric scalar"
            if not isinstance(unit, str) or not unit.strip():
                errors[f"{key}.{name}.unit"] = "Explicit unit required (use '1' if dimensionless)"
    for key in ("conditions", "provenance"):
        if not isinstance(envelope[key], dict) or not envelope[key]:
            errors[key] = "Expected nonempty mapping"
    return {"valid": not errors, "errors": errors, "status": "CONTRACT_ONLY"}


def inspect_simulator_runtimes(executable_paths=None):
    """Read-only availability check; never launch a simulator or claim readiness.

    Explicit paths are useful for Windows installations absent from PATH.
    Finding an executable does not verify its version, license, model or connector.
    SUPPORTED names describe envelope identifiers, not implemented adapters.
    """
    import os
    import platform
    import shutil
    import sys
    from pathlib import Path

    configured = {} if executable_paths is None else executable_paths
    if not isinstance(configured, dict):
        raise ValueError("Executable configuration must be a dictionary")
    if any(name not in SUPPORTED or name == "python" for name in configured):
        raise ValueError("Configure only recognized external simulator identifiers")
    for path in configured.values():
        if not isinstance(path, (str, os.PathLike)) or not os.fspath(path).strip():
            raise ValueError("Executable paths must be nonempty paths")

    commands = {"matlab": ("matlab",), "scaps-1d": ("scaps", "scaps1d"),
                "comsol": ("comsol",), "zemax": ("OpticStudio",),
                "lumerical": ("fdtd-solutions", "mode-solutions")}
    records = {"python": {
        "availability": "RUNNING_INTERPRETER", "executable": sys.executable,
        "runtime_version": platform.python_version(),
        "integration_status": "NOT_VERIFIED", "simulation_execution": "NOT_TESTED"}}
    for name, candidates in sorted(commands.items()):
        if name in configured:
            requested = Path(configured[name]).expanduser()
            found = str(requested.resolve()) if requested.is_file() else None
            availability = "EXPLICIT_FILE_FOUND" if found else "EXPLICIT_PATH_MISSING"
        else:
            found = next((result for command in candidates
                          if (result := shutil.which(command))), None)
            availability = "PATH_FOUND" if found else "NOT_FOUND_ON_PATH"
        records[name] = {"availability": availability, "executable": found,
                         "runtime_version": "NOT_VERIFIED",
                         "integration_status": "NOT_VERIFIED",
                         "simulation_execution": "NOT_TESTED"}
    return {"status": "INVENTORY_ONLY", "active_root": str(Path(__file__).resolve().parent),
            "all_simulators_ready": False, "simulators": records,
            "note": "Executable discovery does not prove integration or physical validation."}


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Inspect simulator availability without execution")
    parser.add_argument("--inventory", action="store_true", required=True)
    parser.add_argument("--executable", action="append", default=[], metavar="SIMULATOR=PATH",
                        help="Explicit external executable path; repeat for each simulator")
    args = parser.parse_args()
    configured = {}
    for item in args.executable:
        name, separator, path = item.partition("=")
        if not separator or name in configured:
            parser.error("Use one SIMULATOR=PATH entry per simulator")
        configured[name] = path
    try:
        inventory = inspect_simulator_runtimes(configured)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(inventory, indent=2, ensure_ascii=False))

