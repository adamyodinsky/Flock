def set_dry_run(dry_run):
    """Set dry run mode"""

    if dry_run is not None and dry_run is not False:
        return "All"

    return None
