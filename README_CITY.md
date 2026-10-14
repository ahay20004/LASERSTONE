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
heuristic pipeline completed, not physical validation. SCAPS inventory and explicit GUI invocation are available; read-only saved I-V import is available; automatic calculation and physical
validation remain unimplemented. MATLAB file exchange remains
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


## Saved SCAPS I-V import for review

In the university, open `Research Laboratories` and choose `READ SAVED SCAPS I-V`.
Select one explicit `.iv` file inside the active project root. The selected file
is read, never overwritten; results stay in the session for review and are not
mixed into the plant database or certified as physically valid. No model or run
is selected based on its filename. All concatenated runs are retained separately.

The CLI alternative is:

```powershell
python g23_simulation_exchange_contract.py --inspect-scaps-iv --result "reports\G23_SCAPS_mesh130_run4.iv"
```

This example path must exist; the importer does not guess its location. It records
an exact-byte source SHA-256, original units and parameter strings, simulated curve
points, SCAPS-derived solar parameters and reported conditions. The conversion
from mW/cm2 to W/m2 is labeled as derived. Definition/spectrum paths in export
headers are reported metadata only; no external files are followed or verified.
IV exports alone do not establish solver convergence, numerical settings or
physical validity. Incomplete runs, malformed rows, unknown units, nonfinite
values and duplicate run blocks block parsing rather than silently dropping data.
Warnings about scan direction or reported convergence failure require review.
The CLI omits the complete point matrix from console output; the in-memory API
retains it. Backup/historical sources and paths outside the active root are blocked.
