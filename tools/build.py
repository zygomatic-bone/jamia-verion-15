"""Rebuild the whole site into ../public, then check every link and asset.  Run:  python3 tools/build.py

Order matters: generate_site.py (Residential School + _redirects) first, then generate_portal.py (root pages), then
generate_forms_worker.py (the form service's rules, from the same schema the pages use).
The build stops with an error message if the link check finds a problem.
"""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent

# Fail early and plainly instead of with a traceback from the middle of the generator.
if sys.version_info < (3, 10):
    sys.exit(f'This build needs Python 3.10 or newer (this is {sys.version_info[0]}.{sys.version_info[1]}).')
try:
    import bs4  # noqa: F401  (generate_site.py reads the original school pages with it)
except ImportError:
    sys.exit('The build needs the Python package "beautifulsoup4", which is not installed for this Python.\n'
             'Install the build dependencies once (they are used only while building, never on the website):\n'
             '    python -m pip install --require-hashes -r tools/requirements.txt\n'
             '(if pip refuses a hash, "python -m pip install beautifulsoup4" is enough to build; then run both commands again).')

runpy.run_path(str(ROOT / "generate_site.py"), run_name="__main__")
runpy.run_path(str(ROOT / "generate_portal.py"), run_name="__main__")
runpy.run_path(str(ROOT / "generate_forms_worker.py"), run_name="__main__")
sys.exit(runpy.run_path(str(ROOT / "check_site.py"), run_name="check_site")["main"]())
