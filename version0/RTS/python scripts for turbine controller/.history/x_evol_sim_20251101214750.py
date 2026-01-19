import numpy as np
import re
from pathlib import Path

JT = 1

def _parse_numbers(text):
    return np.array([float(x) for x in re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", text)])

# adjust path if necessary
file_path = Path("IEA-22-280-RWT_Cp_Ct_Cq.txt")

with file_path.open("r", encoding="utf-8") as f:
    raw_lines = [ln.rstrip() for ln in f.readlines()]

# get first two non-empty lines -> betas and lambdas
non_empty = [ln for ln in raw_lines if ln.strip() != ""]
if len(non_empty) < 2:
    raise ValueError("File must contain at least two non-empty lines for betas and lambdas.")

betas = _parse_numbers(non_empty[0])
lambdas = _parse_numbers(non_empty[1])

# collect the remaining lines (preserve original order) after the two header lines
# find indices of the first two non-empty lines in raw_lines
idxs = []
count = 0
for i, ln in enumerate(raw_lines):
    if ln.strip() != "":
        idxs.append(i)
        count += 1
        if count == 2:
            break
rest_lines = raw_lines[idxs[-1]+1 :]

# split rest_lines into groups separated by one or more blank lines
tables = []
current = []
for ln in rest_lines:
    if ln.strip() == "":
        if current:
            tables.append(current)
            current = []
    else:
        current.append(ln)
if current:
    tables.append(current)

if len(tables) < 3:
    raise ValueError("Expected 3 tables after beta/lambda lines; found {}".format(len(tables)))

def _parse_table(table_lines):
    rows = []
    for ln in table_lines:
        nums = _parse_numbers(ln)
        if nums.size == 0:
            continue
        rows.append(nums)
    if not rows:
        return np.empty((0, 0))
    arr = np.vstack(rows)
    return arr

cp = _parse_table(tables[0])
ct = _parse_table(tables[1])
ctau = _parse_table(tables[2])

print(ctau)

# optional sanity checks
if cp.shape != (len(lambdas), len(betas)):
    raise ValueError(f"cp shape {cp.shape} does not match (len(lambdas)={len(lambdas)}, len(betas)={len(betas)})")
if ct.shape != (len(lambdas), len(betas)):
    raise ValueError(f"ct shape {ct.shape} does not match expected dimensions")
if ctau.shape != (len(lambdas), len(betas)):
    raise ValueError(f"ctau shape {ctau.shape} does not match expected dimensions")
def ctau(beta, lambda_):
    return beta * lambda_

def tau_aero(ctau, rho = 1.225, A = 1, V =1):
    return ctau * 0.5 * rho * A * V**2

def omega_dot(tau, J = JT):
    return tau / J