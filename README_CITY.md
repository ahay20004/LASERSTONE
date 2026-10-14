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
heuristic pipeline completed, not physical validation. SCAPS is still an
inventory/contract identifier: its direct invocation and scientific result
import are not implemented by this runtime repair. MATLAB file exchange remains
a synthetic benchmark. Windows GUI rendering and external simulator execution
require a separate local test; repository tests do not prove them.
