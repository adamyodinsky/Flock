import logging


def set_dry_run(dry_run):
    """Set dry run mode"""

    if dry_run is not None and dry_run is not False:
        dry_run = "All"
    else:
        dry_run = None

    dry_print = "enabled" if dry_run else "disabled"
    logging.debug("Dry run mode: %s", dry_print)

    return dry_run
