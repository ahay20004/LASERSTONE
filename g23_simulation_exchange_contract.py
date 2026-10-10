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


def _main():
    import argparse
    parser = argparse.ArgumentParser(description='Read-only inventory and synthetic MATLAB file exchange')
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--inventory', action='store_true')
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
        if args.inventory:
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
        return 0 if result.get('valid', True) else 1
    except (ValueError, OSError, TypeError, OverflowError) as exc:
        print(json.dumps({'status': 'ERROR', 'error': str(exc)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(_main())
