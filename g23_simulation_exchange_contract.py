"""G23 simulation exchange contract, inventory and explicit SCAPS GUI invocation.

Standard-library-only validation of a transport envelope. Passing this
contract does not validate the underlying physics or provenance claims.
No external simulator is invoked unless --launch-scaps is explicitly selected.
"""
import math
import subprocess

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


# File exchange is a synthetic benchmark, not a scientific readiness certificate.
import json
import re
import uuid
from pathlib import Path

MODEL_ID = 'vacuum-frequency-benchmark-v1'


def _finite_positive(value):
    try:
        return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value) and value > 0 and math.isfinite(299792458 / value)
    except (OverflowError, ZeroDivisionError):
        return False


def validate_matlab_request(request):
    if not isinstance(request, dict):
        raise ValueError('Request must be an object')
    for key, expected in [('schema', 'G23_REQUEST_V1'), ('simulator', 'matlab'), ('model_id', MODEL_ID)]:
        if request.get(key) != expected:
            raise ValueError('Invalid request ' + key)
    if not isinstance(request.get('run_id'), str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', request['run_id']):
        raise ValueError('Unsafe run_id')
    if not isinstance(request.get('request_token'), str) or not re.fullmatch(r'[a-f0-9]{32}', request['request_token']):
        raise ValueError('Invalid request token')
    inputs = request.get('inputs')
    if not isinstance(inputs, dict) or set(inputs) != {'wavelength'}:
        raise ValueError('Expected wavelength input')
    datum = inputs['wavelength']
    if not isinstance(datum, dict) or set(datum) != {'value', 'unit'} or datum['unit'] != 'm' or not _finite_positive(datum['value']):
        raise ValueError('Wavelength must be positive finite metres')
    if request.get('conditions') != {'medium': 'vacuum'}:
        raise ValueError('Expected vacuum conditions')
    return request


MATLAB_SCRIPT = """function run_g23_matlab
% Synthetic benchmark only. Upload this file and request.json together.
root = fileparts(mfilename('fullpath'));
r = jsondecode(fileread(fullfile(root, 'request.json')));
assert(strcmp(r.schema, 'G23_REQUEST_V1') && strcmp(r.simulator, 'matlab'));
assert(strcmp(r.model_id, 'vacuum-frequency-benchmark-v1'));
assert(~isempty(regexp(r.run_id, '^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$', 'once')));
assert(~isempty(regexp(r.request_token, '^[a-f0-9]{32}$', 'once')));
w = r.inputs.wavelength;
assert(isnumeric(w.value) && isscalar(w.value) && isfinite(w.value) && w.value > 0);
assert(strcmp(w.unit, 'm') && strcmp(r.conditions.medium, 'vacuum'));
f = 299792458 / w.value;
assert(isfinite(f) && f > 0);
result = struct('simulator', 'matlab', 'simulator_version', version, ...
    'model_id', r.model_id, 'run_id', r.run_id, 'request_token', r.request_token, ...
    'inputs', r.inputs, 'conditions', r.conditions);
result.outputs = struct('frequency', struct('value', f, 'unit', 'Hz'));
result.provenance = struct('origin', 'synthetic exchange test', ...
    'environment', 'MATLAB file exchange', 'equation', 'frequency = c / wavelength');
output = fullfile(root, 'g23_result.json');
assert(~isfile(output) && ~isfolder(output), 'Result already exists; use a new run.');
fid = fopen(output, 'w');
assert(fid ~= -1, 'Cannot create result file');
cleanup = onCleanup(@() fclose(fid));
fprintf(fid, '%s', jsonencode(result));
disp(output);
end
"""


def _write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def export_matlab_request(output_root=None, run_id=None, wavelength_nm=620):
    if not _finite_positive(wavelength_nm):
        raise ValueError('Invalid wavelength_nm')
    request = {'schema': 'G23_REQUEST_V1', 'simulator': 'matlab', 'model_id': MODEL_ID,
               'run_id': run_id or 'G23-MATLAB-' + uuid.uuid4().hex,
               'request_token': uuid.uuid4().hex,
               'inputs': {'wavelength': {'value': wavelength_nm * 1e-9, 'unit': 'm'}},
               'conditions': {'medium': 'vacuum'},
               'provenance': {'origin': 'synthetic exchange test'}}
    validate_matlab_request(request)
    root = Path(output_root) if output_root is not None else Path(__file__).resolve().parent / 'simulation_exchange'
    root.mkdir(parents=True, exist_ok=True)
    folder = root / request['run_id']
    folder.mkdir()  # Collision is an error; previous runs are preserved.
    _write_json(folder / 'request.json', request)
    with (folder / 'run_g23_matlab.m').open('x', encoding='utf-8') as stream:
        stream.write(MATLAB_SCRIPT)
    return {'status': 'REQUEST_EXPORTED', 'run_id': request['run_id'],
            'request': str((folder / 'request.json').resolve()),
            'matlab_script': str((folder / 'run_g23_matlab.m').resolve()),
            'expected_result': str((folder / 'g23_result.json').resolve())}


def _read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('Nonfinite JSON constant: ' + value)
    with Path(path).open('rb') as stream:
        data = stream.read(1048577)
    if len(data) > 1048576:
        raise ValueError('JSON exceeds 1 MiB')
    return json.loads(data.decode('utf-8-sig'), object_pairs_hook=pairs, parse_constant=invalid)


def verify_matlab_result(request, result):
    validate_matlab_request(request)
    contract = validate_simulation_envelope(result)
    errors = dict(contract['errors'])
    if contract['valid']:
        for key in ('simulator', 'model_id', 'run_id', 'request_token', 'inputs', 'conditions'):
            if result.get(key) != request[key]:
                errors[key] = 'Result does not match request'
        expected = 299792458 / request['inputs']['wavelength']['value']
        outputs = result['outputs']
        datum = outputs.get('frequency', {})
        if set(outputs) != {'frequency'} or datum.get('unit') != 'Hz':
            errors['outputs'] = 'Expected frequency in Hz'
        elif not math.isclose(datum['value'], expected, rel_tol=1e-12, abs_tol=0):
            errors['frequency'] = 'Reference mismatch'
    return {'valid': not errors, 'errors': errors,
            'status': 'BENCHMARK_MATCH_ONLY' if not errors else 'BLOCKED',
            'scope': 'SYNTHETIC_BENCHMARK_ONLY', 'run_id': request['run_id'],
            'physical_validation': 'NOT_ESTABLISHED', 'execution_authenticity': 'NOT_VERIFIED'}


def import_matlab_result(request_path, result_path):
    import hashlib
    request, result = _read_json(request_path), _read_json(result_path)
    report = verify_matlab_result(request, result)
    report['sources'] = {name: {'path': str(Path(path).resolve()),
                              'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest()}
                         for name, path in [('request', request_path), ('result', result_path)]}
    output = Path(request_path).resolve().parent / ('verification_' + uuid.uuid4().hex + '.json')
    _write_json(output, report)
    report['report_path'] = str(output)
    return report



# Parsing an export does not certify its numerical convergence or physics.
_SCAPS_NUMBER = r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eEdD][+-]?\d+)?'


def parse_scaps_iv(text):
    """Parse illuminated SCAPS single-shot I-V exports without changing values.

    Supports concatenated runs and explicit units. Reject incomplete/ambiguous
    exports instead of silently skipping a run. Parameters remain SCAPS-derived;
    curve points remain simulated, never measured. No model is selected here.
    """
    import datetime
    import hashlib

    if not isinstance(text, str) or not text.lstrip('\ufeff').startswith('SCAPS '):
        raise ValueError('Expected a SCAPS I-V export header')
    text = text.lstrip('\ufeff').replace('\r\n', '\n')
    blocks = re.split(r'(?m)(?=^SCAPS )', text)
    runs = []
    fingerprints = set()

    def exactly(pattern, block, label, flags=re.MULTILINE):
        matches = list(re.finditer(pattern, block, flags))
        if len(matches) != 1:
            raise ValueError(f'Expected exactly one {label}')
        return matches[0]

    def finite(value):
        result = float(value.replace('D', 'e').replace('d', 'e'))
        if not math.isfinite(result):
            raise ValueError('Nonfinite SCAPS value')
        return result

    def quantity(label, block, unit, origin, alternatives=()):
        match = exactly(r'^\s*' + re.escape(label) + r'\s*=?\s+(' + _SCAPS_NUMBER + r')\s+(\S+)\s*$', block, label)
        raw_unit = match[2]
        if raw_unit not in (unit, *alternatives):
            raise ValueError(f'{label}: unsupported unit {raw_unit}')
        return {'value': finite(match[1]), 'unit': unit,
                'reported_unit': raw_unit, 'reported_value_text': match[1], 'value_origin': origin}

    for block in blocks:
        if not block.strip():
            continue
        digest = hashlib.sha256(block.strip().encode('utf-8')).hexdigest()
        if digest in fingerprints:
            raise ValueError('Duplicate SCAPS run block; no duplicate import performed')
        fingerprints.add(digest)
        version = exactly(r'^SCAPS\s+(\S+)\s+ELIS-UGent:.*$', block, 'version')[1]
        exactly(r'^Simulation of I-V curves\s*$', block, 'I-V calculation')
        number = int(exactly(r'^Single shot simulation #\s+(\d+)\s*$', block, 'shot number')[1])
        if number < 1:
            raise ValueError('Invalid SCAPS shot number')
        started = exactly(r'^Calculation started\s*:\s*(\d{2}-\d{2}-\d{4} at \d{1,2}:\d{2}:\d{2})\s*$', block, 'calculation time')[1]
        datetime.datetime.strptime(started, '%d-%m-%Y at %H:%M:%S')
        definition = exactly(r'^problem definition file[ \t]*:[ \t]*([^\n]+)$', block, 'reported problem definition')[1].strip()
        exactly(r'^Calculation under illumination\s*$', block, 'illumination')
        spectrum = exactly(r'^spectrum file[ \t]*:[ \t]*\n([^\n]+)$', block, 'spectrum')[1]
        spectrum = re.split(r'\s+last saved:', spectrum, maxsplit=1)[0].strip()
        if not definition or not spectrum:
            raise ValueError('Missing source definition or spectrum')
        conditions = {
            'illumination': 'LIGHT', 'spectrum_file_reported': spectrum,
            'temperature': quantity('Temperature', block, 'K', 'SIMULATION_SETTING'),
            'incident_power': quantity('Incident power on solar cell structure', block, 'mW/cm2', 'SIMULATION_SETTING'),
            'workpoint_bias': quantity('Workpoint bias voltage', block, 'V', 'SIMULATION_SETTING', ('Volt',)),
            'frequency': quantity('Frequency', block, 'Hz', 'SIMULATION_SETTING'),
        }
        # ND transmission is a unitless field in this SCAPS format.
        transmission = exactly(r'^Transmission of ND filter:\s*(' + _SCAPS_NUMBER + r')\s*$', block, 'ND transmission')
        conditions['nd_transmission'] = {'value': finite(transmission[1]), 'unit': '1', 'value_origin': 'SIMULATION_SETTING'}
        if (conditions['temperature']['value'] <= 0 or conditions['incident_power']['value'] <= 0
                or not math.isfinite(conditions['incident_power']['value'] * 10)):
            raise ValueError('Illuminated export requires positive temperature and power')
        conditions['incident_power_si'] = {
            'value': conditions['incident_power']['value'] * 10, 'unit': 'W/m2',
            'value_origin': 'DERIVED_UNIT_CONVERSION', 'conversion': '1 mW/cm2 = 10 W/m2',
        }
        current_convention = exactly(r'^Current reference convention:\s*(.+)$', block, 'current convention')[1].strip()
        voltage_convention = exactly(r'^Voltage reference convention:\s*(.+)$', block, 'voltage convention')[1].strip()
        power_convention = exactly(r'^Power generated by the cell:\s*(.+)$', block, 'power convention')[1].strip()
        header = exactly(r'^\s*v\(V\)\s+jtot\(mA/cm2\)[^\n]*$', block, 'curve table')
        summary = exactly(r'^solar cell parameters deduced from calculated IV-curve:\s*$', block, 'solar parameter summary')
        if summary.start() <= header.end():
            raise ValueError('SCAPS summary precedes curve table')
        columns = []
        for item in header[0].split():
            match = re.fullmatch(r'([^()\s]+)\(([^()\s]+)\)', item)
            if not match or match[2] not in ('V', 'mA/cm2'):
                raise ValueError('Unsupported curve column or unit')
            if match[2] != ('V' if not columns else 'mA/cm2'):
                raise ValueError('Current curve columns require mA/cm2')
            columns.append({'name': match[1], 'unit': match[2]})
        names = [c['name'] for c in columns]
        if len(set(names)) != len(names):
            raise ValueError('Duplicate curve column')
        rows = []
        for line in block[header.end():summary.start()].splitlines():
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) != len(columns):
                raise ValueError('Malformed or truncated SCAPS curve row')
            try:
                rows.append([finite(value) for value in parts])
            except (ValueError, OverflowError) as exc:
                raise ValueError('Invalid numeric SCAPS curve row') from exc
        if len(rows) < 2:
            raise ValueError('SCAPS curve requires at least two points')
        outputs = {}
        for label, key, unit, aliases in (
            ('Voc', 'voc', 'V', ('Volt',)), ('Jsc', 'jsc', 'mA/cm2', ()),
            ('FF', 'ff', '%', ()), ('eta', 'efficiency', '%', ()),
            ('V_MPP', 'v_mpp', 'V', ('Volt',)), ('J_MPP', 'j_mpp', 'mA/cm2', ())):
            outputs[key] = quantity(label, block[summary.end():], unit, 'SCAPS_DERIVED_FROM_SIMULATED_IV', aliases)
        voltages = [row[0] for row in rows]
        warnings = []
        if not all(a < b for a, b in zip(voltages, voltages[1:])):
            warnings.append('Voltage grid is not strictly increasing; review scan direction/order')
        if re.search(r'convergence\s+(failure|failed)|not\s+converged', block, re.IGNORECASE):
            warnings.append('Export contains a convergence failure message')
        runs.append({
            'run_index': len(runs) + 1, 'single_shot_number': number,
            'simulator': 'scaps-1d', 'simulator_version_reported': version,
            'calculation_started_reported': started, 'timezone': 'NOT_RECORDED_IN_EXPORT',
            'definition_file_reported': definition, 'definition_file_verified': False,
            'conditions': conditions, 'outputs': outputs,
            'curve': {'columns': columns, 'rows': rows, 'point_count': len(rows), 'value_origin': 'SIMULATED'},
            'conventions': {'current': current_convention, 'voltage': voltage_convention, 'power': power_convention},
            'run_fingerprint': digest, 'warnings': warnings,
            'solver_convergence': 'NOT_ESTABLISHED_FROM_IV_EXPORT',
            'numerical_settings': 'NOT_RECORDED_IN_IV_EXPORT',
            'physical_validation': 'NOT_ESTABLISHED',
            'status': 'REVIEW_REQUIRED' if warnings else 'PARSED_UNVALIDATED',
        })
    if not runs:
        raise ValueError('No SCAPS I-V runs found')
    return runs


def inspect_scaps_iv(result_path):
    """Read one explicit source under the active root; never write or calculate."""
    import hashlib
    active_root = Path(__file__).resolve().parent
    if Path.cwd().resolve() != active_root:
        raise ValueError('Run SCAPS I-V inspection from the active project root')
    path = Path(result_path).resolve(strict=True)
    relative = path.relative_to(active_root)
    if any(part.lower() in ('backup', 'backups', 'alpha', 'historical', '.git') for part in relative.parts):
        raise ValueError('Historical or backup sources are excluded')
    if path.suffix.lower() != '.iv' or not path.is_file():
        raise ValueError('Expected one explicit .iv source file inside the active root')
    with path.open('rb') as stream:
        data = stream.read(2 * 1024 * 1024 + 1)
    if len(data) > 2 * 1024 * 1024:
        raise ValueError('SCAPS I-V export exceeds the supported 2 MiB size')
    try:
        text = data.decode('utf-8-sig')
        encoding = 'utf-8-sig'
    except UnicodeDecodeError:
        text = data.decode('cp1252')
        encoding = 'cp1252'
    runs = parse_scaps_iv(text)
    sha = hashlib.sha256(data).hexdigest()
    for run in runs:
        run['run_id'] = 'SCAPS-IV-' + sha[:16] + '-' + str(run['run_index'])
    return {'schema': 'G23_SCAPS_IV_REVIEW_V1', 'status': 'IMPORTED_FOR_REVIEW_ONLY', 'scope': 'SCAPS_SAVED_IV_IMPORT',
            'source': {'path': str(path), 'sha256': sha, 'size_bytes': len(data), 'encoding': encoding},
            'run_count': len(runs), 'runs': runs, 'new_simulation_executed': False,
            'physical_validation': 'NOT_ESTABLISHED', 'source_modified': False,
            'note': 'This reads saved simulated results; it does not certify convergence or physical validity.'}




def format_scaps_iv_summary(report):
    """Human-readable review of imported values; never a readiness certificate."""
    source = report['source']
    lines = ['SCAPS SAVED I-V REVIEW', f"Source: {source['path']}",
             f"SHA-256: {source['sha256']}", f"Runs: {report['run_count']}",
             'Curve points: simulated. Solar parameters: SCAPS-derived.',
             'Physical validation and solver convergence are not established by this import.', '']
    for run in report['runs']:
        lines.extend([f"Run {run['run_index']} | Shot {run['single_shot_number']} | SCAPS {run['simulator_version_reported']}",
                      f"Started (reported; timezone unknown): {run['calculation_started_reported']}",
                      f"Definition (reported, not verified): {run['definition_file_reported']}",
                      f"Curve points: {run['curve']['point_count']}"])
        for name in ('temperature', 'incident_power', 'incident_power_si'):
            datum = run['conditions'][name]
            lines.append(f"{name}: {datum.get('reported_value_text', datum['value'])} {datum['unit']}")
        for name, datum in run['outputs'].items():
            lines.append(f"{name}: {datum.get('reported_value_text', datum['value'])} {datum['unit']}")
        lines.append(f"Review status: {run['status']}")
        lines.extend(run['warnings'])
        lines.append('')
    return '\n'.join(lines)


def launch_scaps_gui(executable):
    """Explicit GUI invocation only; no calculation or scientific import.

    Read a binary snapshot for traceability, check process names before launch,
    and keep simulator resources relative to its own installation directory.
    A PID is process evidence, not proof of a visible GUI or valid calculation.
    """
    import csv
    import hashlib
    import io
    import platform
    import subprocess

    active_root = Path(__file__).resolve().parent
    if Path.cwd().resolve() != active_root:
        raise ValueError("Run SCAPS invocation from the active project root")
    if platform.system() != "Windows":
        raise ValueError("SCAPS GUI invocation requires Windows")
    if not isinstance(executable, (str, Path)) or not str(executable).strip():
        raise ValueError("Explicit SCAPS executable path required")
    path = Path(executable).expanduser()
    if not path.is_absolute():
        raise ValueError("SCAPS executable path must be absolute")
    path = path.resolve(strict=True)
    if not re.fullmatch(r"scaps[0-9]+\.exe", path.name, re.IGNORECASE):
        raise ValueError("Expected a versioned SCAPS executable")
    if not path.is_file():
        raise ValueError("SCAPS executable is not a file")
    with path.open('rb') as stream:
        header = stream.read(2)
        if header != b'MZ':
            raise ValueError("Expected a Windows executable header")
        digest = hashlib.sha256()
        digest.update(header)
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    snapshot = path.stat()
    process_list = subprocess.run(
        ['tasklist.exe', '/FI', f'IMAGENAME eq {path.name}', '/FO', 'CSV', '/NH'],
        capture_output=True, text=True, check=True, timeout=10,
    )
    matching = []
    for row in csv.reader(io.StringIO(process_list.stdout)):
        if row and row[0].casefold() == path.name.casefold():
            if len(row) < 2 or not row[1].isdigit():
                raise ValueError("Cannot verify existing SCAPS process listing")
            matching.append(int(row[1]))
    report = {
        'scope': 'GUI_INVOCATION_ONLY', 'active_root': str(active_root),
        'executable': str(path), 'sha256': digest.hexdigest(),
        'size_bytes': snapshot.st_size, 'simulator_version': 'NOT_VERIFIED',
        'gui_visibility': 'NOT_VERIFIED', 'simulation_execution': 'NOT_TESTED',
        'result_import': 'NOT_REQUESTED', 'physical_validation': 'NOT_ESTABLISHED',
    }
    if matching:
        report.update(status='IMAGE_NAME_ALREADY_RUNNING', process_ids=matching,
                      new_process_started=False, existing_process_path='NOT_VERIFIED')
        return report
    process = subprocess.Popen([str(path)], cwd=str(path.parent), shell=False)
    # This does not wait for simulation or manipulate the native application.
    exit_code = process.poll()
    report.update(status='PROCESS_STARTED' if exit_code is None else 'PROCESS_EXITED_EARLY',
                  process_ids=[process.pid], new_process_started=True, exit_code=exit_code)
    return report

def _main():
    import argparse
    parser = argparse.ArgumentParser(description='Inventory, synthetic MATLAB exchange and explicit SCAPS GUI invocation')
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--inventory', action='store_true')
    modes.add_argument('--launch-scaps', action='store_true')
    modes.add_argument('--inspect-scaps-iv', action='store_true')
    modes.add_argument('--export-matlab', action='store_true')
    modes.add_argument('--verify-matlab', action='store_true')
    parser.add_argument('--executable', action='append', default=[])
    parser.add_argument('--output-root')
    parser.add_argument('--run-id')
    parser.add_argument('--wavelength-nm', type=float)
    parser.add_argument('--request')
    parser.add_argument('--result')
    args = parser.parse_args()
    try:
        if args.inspect_scaps_iv:
            if (not args.result or args.executable or any(x is not None for x in
                    (args.output_root, args.run_id, args.wavelength_nm, args.request))):
                raise ValueError("SCAPS I-V inspection requires only --result PATH")
            result = inspect_scaps_iv(args.result)
            # Keep console output short; the API retains the complete curve.
            for run in result['runs']:
                run['curve'].pop('rows')
        elif args.launch_scaps:
            if (len(args.executable) != 1 or any(x is not None for x in
                    (args.output_root, args.run_id, args.wavelength_nm, args.request, args.result))):
                raise ValueError("SCAPS invocation requires only --executable scaps-1d=ABSOLUTE_PATH")
            name, sep, path = args.executable[0].partition('=')
            if name != 'scaps-1d' or not sep or not path:
                raise ValueError("Use --executable scaps-1d=ABSOLUTE_PATH")
            result = launch_scaps_gui(path)
        elif args.inventory:
            if any(x is not None for x in (args.output_root, args.run_id, args.wavelength_nm, args.request, args.result)):
                raise ValueError('Exchange arguments require an exchange mode')
            paths = {}
            for item in args.executable:
                name, sep, path = item.partition('=')
                if not sep or name in paths:
                    raise ValueError('Use unique SIMULATOR=PATH entries')
                paths[name] = path
            result = inspect_simulator_runtimes(paths)
        elif args.export_matlab:
            if args.executable or args.request or args.result:
                raise ValueError('Unexpected arguments for export')
            result = export_matlab_request(args.output_root, args.run_id, 620 if args.wavelength_nm is None else args.wavelength_nm)
        else:
            if args.executable or args.output_root or args.run_id or args.wavelength_nm is not None or not args.request or not args.result:
                raise ValueError('Verification requires --request and --result only')
            result = import_matlab_result(args.request, args.result)
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result.get('valid', True) and result.get('status') != 'PROCESS_EXITED_EARLY' else 1
    except (ValueError, OSError, TypeError, OverflowError, UnicodeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'ERROR', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(_main())
