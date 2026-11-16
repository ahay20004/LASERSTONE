"""Generic equation contract regression tests with synthetic data."""
import unittest

from cloud.equation_contract import Quantity
from cloud.universal_equation_protocol import (
    EquationSpec, VariableSpec, validate_equation_inputs,
)


def q(value, unit, source="synthetic test input", state="DERIVED"):
    return Quantity(value, unit, source, state)


SPEC = EquationSpec(
    equation_id="synthetic_velocity_v1",
    variables=(
        VariableSpec("distance", "m", minimum=0),
        VariableSpec("time", "s", minimum=0),
    ),
    assumptions=("Constant velocity",),
    relation_checks=(lambda v: v["time"].value > 0,),
)


class UniversalEquationProtocolTests(unittest.TestCase):
    def test_complete_valid_snapshot(self):
        values = {"distance": q(10, "m"), "time": q(2, "s")}
        self.assertEqual(validate_equation_inputs(SPEC, values), values)

    def test_unit_mismatch_and_missing_variable(self):
        for values in (
            {"distance": q(10, "cm"), "time": q(2, "s")},
            {"distance": q(10, "m")},
            {"distance": q(10, "m"), "time": q(2, "s"), "extra": q(1, "m")},
        ):
            with self.assertRaises(ValueError):
                validate_equation_inputs(SPEC, values)

    def test_domain_and_relations(self):
        for values in (
            {"distance": q(-1, "m"), "time": q(2, "s")},
            {"distance": q(10, "m"), "time": q(0, "s")},
            {"distance": q(float("nan"), "m"), "time": q(2, "s")},
            {"distance": q(10, "m", source=""), "time": q(2, "s")},
        ):
            with self.assertRaises(ValueError):
                validate_equation_inputs(SPEC, values)

    def test_evidence_policy(self):
        spec = EquationSpec(
            equation_id="measured_only",
            variables=(VariableSpec("x", "m", required_evidence=("MEASURED",)),),
            assumptions=("Input must be measured",),
        )
        with self.assertRaises(ValueError):
            validate_equation_inputs(spec, {"x": q(1, "m", state="PREDICTED")})

    def test_invalid_contract_rejected(self):
        invalid = EquationSpec("duplicate", (
            VariableSpec("x", "m"), VariableSpec("x", "m")
        ), ("synthetic",))
        with self.assertRaises(ValueError):
            validate_equation_inputs(invalid, {"x": q(1, "m")})


if __name__ == "__main__":
    unittest.main()
