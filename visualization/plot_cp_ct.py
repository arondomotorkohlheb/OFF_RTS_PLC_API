labels = [r'$\beta_ref$', r'$\gamma_{ref}$', r'$\omega_{ref}$', r'$\beta$', r'$\gamma$', r'$\omega$', r'$c_p$', r'$P_{ref}$', r'$P_{gen}$' , r'$c_p$', r'c_t']
import numpy as np
import matplotlib.pyplot as plt


file_path = r'C:\Users\akohlheb\working_files\visualization\visual_data.npy'
data = np.load(file_path)

# Signal indices
IDX_CP = 6
IDX_CT = 10

t = np.arange(data.shape[0])

# Sum over all turbines (axis = 1)
cp_sum = data[:, :, IDX_CP].sum(axis=1)
ct_sum = data[:, :, IDX_CT].sum(axis=1)

# Single canvas
fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(t, cp_sum, label=r'$\sum c_p$')
ax.plot(t, ct_sum, label=r'$\sum c_t$')

ax.set_xlabel(r'Time [s]')
ax.set_ylabel(r'Summed Coefficients')
ax.set_title(r'Summed $c_p$ and $c_t$ (All Turbines)')
ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()
