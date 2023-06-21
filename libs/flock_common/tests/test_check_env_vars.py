import os
import unittest
from unittest.mock import patch

from flock_common.env_checker import EnvVarNotSetError, check_env_vars


class TestCheckEnvVars(unittest.TestCase):
    """Test flock_common.env_checker.check_env_vars"""

    def test_required_vars_present(self):
        """Test that check_env_vars does not raise an exception when all required"""
        with patch.dict(os.environ, {"A": "value_a", "B": "value_b", "C": "value_c"}):
            try:
                check_env_vars(["A", "B", "C"])
            except EnvVarNotSetError:
                self.fail("check_env_vars raised EnvVarNotSetError unexpectedly!")

    def test_required_var_missing(self):
        """Test that check_env_vars raises an exception when a required var is missing"""
        with patch.dict(os.environ, {"A": "value_a", "B": "value_b"}):
            with self.assertRaises(EnvVarNotSetError):
                check_env_vars(["A", "B", "C"])

    def test_optional_vars_present(self):
        """Test that check_env_vars does not raise an exception when all optional vars are present"""

        with patch.dict(
            os.environ, {"A": "value_a", "B": "value_b", "C": "value_c", "D": "value_d"}
        ):
            try:
                check_env_vars(["A", "B", "C"], optional_vars=["D"])
            except EnvVarNotSetError:
                self.fail("check_env_vars raised EnvVarNotSetError unexpectedly!")

    def test_optional_var_missing(self):
        """Test that check_env_vars does not raise an exception when an optional var is missing"""

        with patch.dict(os.environ, {"A": "value_a", "B": "value_b", "C": "value_c"}):
            try:
                check_env_vars(["A", "B", "C"], optional_vars=["D"])
            except EnvVarNotSetError:
                self.fail("check_env_vars raised EnvVarNotSetError unexpectedly!")


if __name__ == "__main__":
    unittest.main()
