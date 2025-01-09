import nbformat
from nbformat.v4 import new_notebook, new_code_cell

# List of .py files to merge
python_files = ["scripts/fetch_data.py", "scripts/process_data.py", "scripts/analyze_openings.py", "scripts/analyze_outcomes.py", "scripts/analyze_time_management.py", "scripts/visualize.py"]

# Create a new notebook
notebook = new_notebook()

for py_file in python_files:
    with open(py_file, 'r') as f:
        code = f.read()
        # Add the code as a new cell
        notebook.cells.append(new_code_cell(code))

# Save the notebook
with open("merged_notebook.ipynb", 'w') as f:
    nbformat.write(notebook, f)

print("Notebook created: merged_notebook.ipynb")
