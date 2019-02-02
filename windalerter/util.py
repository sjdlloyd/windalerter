import re
from pathlib2 import Path
def find_first_number(s): return float(re.findall(r'\d+\.?\d*', str(s))[0])

def append_csv(fields, filename):
    import csv
    p = Path(filename)
    if not p.exists():
        with open(filename, 'w+', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Wind speed', 'Wind direction', 'Time'])

    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(fields)