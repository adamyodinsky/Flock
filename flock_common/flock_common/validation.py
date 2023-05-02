import os

import yaml


def validation_iterator(dir_path, validation_function):
    """
    Load YAML files into a dictionary object for all YAML files in
    a directory and its numbered subdirectories.

    Args:
        dir_path (str): Path to directory containing YAML files.

    Returns:
        None.

    """
    # get list of subdirectories in directory
    subdirs = [
        x for x in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, x))
    ]

    subdirs = sorted(subdirs)

    # loop through subdirectories
    for subdir in subdirs:
        subdir_path = os.path.join(dir_path, subdir)

        # loop through YAML files in subdirectory
        for yaml_file in os.listdir(subdir_path):
            if yaml_file.endswith(".yaml"):
                yaml_path = os.path.join(subdir_path, yaml_file)

                # load YAML into dictionary
                with open(yaml_path, "r", encoding="utf-8") as file:
                    data = yaml.safe_load(file)

                print(f"Validating {yaml_path} - ", end="", flush=True)
                kind = data["kind"]

                try:
                    validation_function(data)
                except Exception as error:  # pylint: disable=broad-except
                    print(f"Error validating {yaml_file}:")
                    print(f"Full Path: {yaml_path}")
                    print(str(error))

                print(f"{kind} - OK")
