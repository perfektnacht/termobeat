"""Predefined ASCII art assets for the visualizer.

The constants defined here represent the ASCII art used by the
visualization routines:

``HAND_FRAMES``
    Multiple poses of a metal hand (``\\m/``) used to reflect the current
    volume level.
``OMARCHY_BANNER``
    Text banner shown on a detected beat.
``WAVE_TEMPLATE``
    Small ring pattern used to draw expanding wave animations.
"""

# Simple representations of a metal hand (\m/) in different poses
HAND_FRAMES = [
    [
        "  \\m/  ",
        "   |   ",
        "  / \\  ",
    ],
    [
        "  \\m/  ",
        "   |   ",
        "  /\\   ",
    ],
    [
        "  \\m/  ",
        "   \\|  ",
        "  / \\  ",
    ],
]

# OMARCHY banner generated with ``pyfiglet`` using the ``ansi_shadow`` font.
# The strings do not include any indentation so the banner can be centered on
# the screen at runtime.
OMARCHY_BANNER = [
    " ██████╗ ███╗   ███╗ █████╗ ██████╗  ██████╗██╗  ██╗██╗   ██╗",
    "██╔═══██╗████╗ ████║██╔══██╗██╔══██╗██╔════╝██║  ██║╚██╗ ██╔╝",
    "██║   ██║██╔████╔██║███████║██████╔╝██║     ███████║ ╚████╔╝",
    "██║   ██║██║╚██╔╝██║██╔══██║██╔══██╗██║     ██╔══██║  ╚██╔╝",
    "╚██████╔╝██║ ╚═╝ ██║██║  ██║██║  ██║╚██████╗██║  ██║   ██║",
    " ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝",
]

# Template for simple wave ring layers
WAVE_TEMPLATE = [
    "   ~    ",
    " ~   ~  ",
    "~     ~",
    " ~   ~  ",
    "   ~    ",
]
