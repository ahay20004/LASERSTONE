LASERSTONE INTERNATIONAL SCIENTIFIC UNIVERSITY

CITY ARCHITECTURE

The Scientific City is built as an independent academic campus.

Every building is developed independently.

Every building has:

• Mission
• Interface
• Scientific Engines
• Documentation

No direct modifications are allowed outside the architectural plan.

The city grows by complete buildings, never by temporary patches.

## G23 checked runtime entry points

`main.prepare_runtime()` is the shared preparation path for the console,
checked dashboard launcher and scientific city. It runs startup and syntax
checks, configuration validation, immutable heuristic analysis, audit, ranking,
and the existing discovery, network, strategy and visualization preparation
once. Every material receives its own mission and architecture summaries.
A failed or incomplete record blocks the batch; no raw-record fallback is used.
Preparation does not export reports or launch external simulators.

Run from the authoritative active project root on `g23/stage13-integration`:

```powershell
python -m unittest discover -p "test_g23*.py" -v
python -B safe_dashboard_launcher.py --check
python safe_dashboard_launcher.py
```

The gateway and chosen view reuse the prepared session. `--check` prepares it
without opening a GUI or writing reports. `python main.py --no-gui` explicitly
exports reports, preserving existing reports rather than overwriting them.

UI engine counts and connections come from registry declarations. They are not
execution counts or maturity certificates. `ANALYSIS_READY` means the checked
heuristic pipeline completed, not physical validation. SCAPS inventory and explicit GUI invocation are available; automatic calculation
and scientific result import remain unimplemented. MATLAB file exchange remains
a synthetic benchmark. Windows GUI rendering and external simulator execution
require a separate local test; repository tests do not prove them.


## Project and university views

`OPEN DASHBOARD` opens the project control center, including all 16 gateway
buttons, the ranked-material table, material profiles and charts. The content
scrolls vertically and horizontally on smaller screens.

`OPEN SCIENTIFIC CITY` opens the city view; its `OPEN UNIVERSITY PLAZA` button
opens the seven-building campus. Building callbacks open the existing material,
physics, engineering, intelligence, expertise, repository and simulator-inventory
views. Missing callbacks are disabled. The laboratories show simulator inventory;
they do not claim unimplemented simulator execution.

The university plaza can open `OPEN PROJECT DASHBOARD` as a child window using
the same prepared session and Tk event loop. This does not re-run analysis or
create a second database. For direct university entry, run from the active root:

```powershell
python -m city.plaza_launcher
```

Importing the campus launcher no longer opens a GUI. Tests construct both views
with mocked Tk widgets and exercise gateway/building callbacks; visual rendering
on Windows remains a local verification step.


## Explicit SCAPS GUI invocation

From the active project root, use the existing G23 exchange tool:

```powershell
python g23_simulation_exchange_contract.py --launch-scaps --executable "scaps-1d=C:\Program Files (x86)\Scaps3312\scaps3312.exe"
```

This Windows-only operation reads the executable SHA-256 and size, checks the
process list by image name, and opens SCAPS with no calculation arguments. It
starts no additional process when the image name is already running; a name match
alone does not verify that process's executable path. Missing files, wrong roots,
failed process listing and immediate process exit do not count as readiness.
A process ID is not proof of a visible GUI, valid physics or result integration.
No calculation is selected and no scientific result is imported by this command.
