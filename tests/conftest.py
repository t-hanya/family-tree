"""
Setup script for pytest framework.
"""


from pathlib import Path
import sys


project_root = Path(__file__).resolve().parent.parent
sys.path.append(project_root)
