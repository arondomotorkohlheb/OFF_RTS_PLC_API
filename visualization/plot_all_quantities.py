import numpy as np
import matplotlib.pyplot as plt

file_path = r'C:\Users\akohlheb\working_files\OFF_RTS_PLC_API\visualization\visual_data_pc.npy'

data = np.load(file_path)
data = data[:, :, :]

labels = [r'$\beta_ref$', r'$\gamma_{ref}$', r'$\omega_{ref}$', r'$\beta$', r'$\gamma$', r'$\omega$', r'$c_p$', r'$P_{ref}$', r'$P_{gen}$', r'$c_p$', r'c_t']

t = range(data.shape[0])
num_quantities = data.shape[2]

# Create subplots for each label/quantity
fig, axs = plt.subplots(num_quantities, 1, figsize=(10, 3*num_quantities), sharex=True)

# Plot each quantity for all turbines
for idx, label in enumerate(labels):
    for k in range(data.shape[1]):
        axs[idx].plot(t, data[:, k, idx], label=f'Turbine {k+1}')
    
    axs[idx].set_ylabel(label)
    axs[idx].set_title(f'{label} (All Turbines)')
    axs[idx].grid(True)
    if idx == 0:
        axs[idx].legend(loc='upper right', fontsize='small')

axs[-1].set_xlabel(r'Time [s]')
plt.tight_layout()
plt.show()
