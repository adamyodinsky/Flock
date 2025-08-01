"""Check that all required environment variables are set"""

import logging
import os


class EnvVarNotSetError(Exception):
    """Raised when an environment variable is not set"""

    def __init__(self, var_name):
        self.var_name = var_name
        super().__init__(f"Environment variable '{self.var_name}' is not set")


def check_env_vars(required_vars, optional_vars=None):
    """Check that all required environment variables are set"""

    for var in required_vars:
        if var not in os.environ:
            logging.error("Environment variable %s is not set", var)
            raise EnvVarNotSetError(var)

    if optional_vars:
        for var in optional_vars:
            if var not in os.environ:
                logging.info("Optional environment variable %s is not set", var)
