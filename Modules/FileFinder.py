import sys, os


# Gets the resource path of a given file
# Used when file path is unknown (ex. in an EXE file)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
