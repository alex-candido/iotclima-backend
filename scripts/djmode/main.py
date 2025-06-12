# Inside ./scripts/djmode/main.py
import sys
import os

# Add the root project directory to sys.path
# This assumes main.py is in scripts/djmode/
# and the project root is two levels up from main.py
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from scripts.djmode.cli.commands import execute_from_command_line

if __name__ == '__main__':
    execute_from_command_line()