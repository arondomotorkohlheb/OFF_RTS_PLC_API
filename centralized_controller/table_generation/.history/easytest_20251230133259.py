from tqdm import tqdm
import time

outer = range(3)
inner = range(5)

for i in tqdm(outer, desc="Outer loop"):
    for j in tqdm(inner, desc="Inner loop", leave=False):
        time.sleep(0.1)