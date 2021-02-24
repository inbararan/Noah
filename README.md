# Noah

Welcome to the Noah READNE page!

The Noah project contains two components.
1. The Hazanot-O-mat
2. The CSVfy

## Paths
The Noah Github repo misses a single special Python file, which is paths.py.  
You should create it yourself, locally (in the project directory), if you want to run the Noah project.  
Do not upload it it Github, though.

It should contain string constants holding important paths (e.g. input/output directories).
```python
# These must be there:
INPUT = r'<path/to/input/directory/where/all/evaluation/files/are>'
MASTER = r'<path/to/master/file>'
# These should be there only if you plan to use the Hazanot-O-mat
HAZANOTOMAT_TEMPLATE = r'<path/to/hazanotomat/template/file>'
HAZANOTOMAT_OUTPUT = r'<path/to/directory/where/you/want/the/output/files>'
# These should be there only if you plan to use the CSVfy
CSV_OUTPUT = r'<desired/path/to/output/csv>'
```

### Master
The master file is used by the Noah project to identify candidates, to verify names were written correctly, etc.  
It should be a csv with following columns:  
ID (תעודת זהות)  
Team (צוות, למשל א או ג)  
Full name (שם מלא)

### Template
The Hazanot-O-mat module is using a template file to create its Excel outputs.
