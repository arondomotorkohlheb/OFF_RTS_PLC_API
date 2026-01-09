from itertools import product
from tqdm import tqdm
import time

outer = range(3)
inner = range(5)

for i, j in tqdm(product(outer, inner), total=len(outer)*len(inner), desc="All iterations"):
    time.sleep(0.1)