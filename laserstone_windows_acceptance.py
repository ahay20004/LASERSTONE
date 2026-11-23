"""Windows workstation acceptance evidence collector; never self-certifies GUI usability."""
from __future__ import annotations
import datetime as dt
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "laserstone_windows_acceptance.json"

def run_check(name: str, args: list[str]) -> dict:
    try:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                                timeout=180, check=False)
        return {"name": name, "status": "PASS" if result.returncode == 0 else "FAIL",
                "exit_code": result.returncode,
                "output_tail": (result.stdout + "\n" + result.stderr)[-5000:]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"name": name, "status": "ERROR", "error": type(exc).__name__}

def collect() -> dict:
    host_is_windows = platform.system() == "Windows"
    checks = []
    if host_is_windows:
        checks = [
            run_check("agent_council_tests",
                      [sys.executable, "-m", "unittest", "discover", "-s", "tests",
                       "-p", "test_agent_*.py", "-v"]),
            run_check("paper2_synthetic_tests",
                      [sys.executable, "-m", "unittest", "discover", "-s",
                       "projects/paper2/tests", "-p", "test_*.py", "-v"]),
            run_check("local_agent_inventory",
                      [sys.executable, "agent_local_inventory.py"]),
        ]
    git = run_check("git_commit", ["git", "rev-parse", "HEAD"]) if host_is_windows else {
        "name": "git_commit", "status": "NOT_RUN"}
    all_passed = host_is_windows and all(x["status"] == "PASS" for x in checks)
    return {
        "schema": 1, "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "host_os": platform.system(), "host_is_windows": host_is_windows,
        "python_version": platform.python_version(), "git": git,
        "checks": checks,
        "synthetic_software_checks_passed": all_passed,
        "gui_runtime_verified": False,
        "scientific_validation_verified": False,
        "agent_runtime_verified": False,
        "operational_readiness": "NOT_ESTABLISHED",
        "next_gate": "Human-observed GUI launch, real input integration and scientific evidence audit",
    }

def main() -> int:
    report = collect()
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print("LASERSTONE workstation report:", REPORT)
    print("Software checks:", "PASS" if report["synthetic_software_checks_passed"] else "NOT_PASSED")
    print("Operational readiness: NOT_ESTABLISHED (GUI and scientific gates remain)")
    return 0 if report["synthetic_software_checks_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
