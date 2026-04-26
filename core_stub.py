# core_stub.py (public version)
print("USING CORE_STUB:", __file__)
def run_aoi(golden_path, test_path, mask=None, smart=True):
    """
    Demo-only stub.
    Returns simulated defects to showcase UI and workflow.
    """

    if smart:
        # fewer defects (Smart AOI)
        defects = [
            (300, 250, 60, 40),
            (900, 500, 80, 60)
        ]
    else:
        # more defects (Wave AOI)
        defects = [
            (300, 250, 60, 40),
            (900, 500, 80, 60),
            (100, 100, 40, 40),
            (500, 200, 30, 30),
        ]

    return None, defects
