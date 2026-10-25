"""Rebuild the whole site into ../public, then check every link and asset.  Run:  python3 tools/build.py

Order matters: generate_site.py (Residential School + _redirects) first, then generate_portal.py (root pages).
The build stops with an error message if the link check finds a problem.
"""
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
runpy.run_path(str(ROOT / "generate_site.py"), run_name="__main__")
runpy.run_path(str(ROOT / "generate_portal.py"), run_name="__main__")
sys.exit(runpy.run_path(str(ROOT / "check_site.py"), run_name="check_site")["main"]())
