import click

CLI_HELP_BANNER = (
    """
▄▖  ▜ ▘▗ ▌     ▌ 
▚ ▛▌▐ ▌▜▘▛▌▛▌▛▌▙▘
▄▌▙▌▐▖▌▐▖▙▌▙▌▙▌▛▖
  ▌              
"""
    + click.style("       Audiobook chapter recognition tool", italic=True)
).replace("\n", "\b\n")
