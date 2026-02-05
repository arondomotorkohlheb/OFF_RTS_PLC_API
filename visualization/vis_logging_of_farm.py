import numpy as np
import matplotlib.pyplot as plt
file_path = r'C:\Users\akohlheb\working_files\visualization\visual_data.npy'

data = np.load(file_path)
data = data[:, :, :]

labels = [r'$\beta_ref$', r'$\gamma_{ref}$', r'$\omega_{ref}$', r'$\beta$', r'$\gamma$', r'$\omega$', r'$c_p$', r'$P_{ref}$', r'$P_{gen}$' , r'$c_p$', r'c_t']


# Signal indices
IDX_BETA_REF  = 0
IDX_OMEGA_REF = 2
IDX_BETA      = 3
IDX_OMEGA     = 5
IDX_P_REF     = 7
IDX_P_GEN     = 8

t = range(data.shape[0])

fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
 
# --- β vs β_ref ---
for k in range(data.shape[1]):
    line, = axs[0].plot(t, data[:, k, IDX_BETA])        # achieved (solid)
    axs[0].plot(
        t,
        data[:, k, IDX_BETA_REF],
        linestyle='--',
        color=line.get_color()                          # same color
    )

axs[0].set_ylabel(r'$\beta$')
axs[0].set_title(r'$\beta$ vs $\beta_{ref}$')
axs[0].grid(True)


# --- ω vs ω_ref ---
for k in range(data.shape[1]):
    line, = axs[1].plot(t, data[:, k, IDX_OMEGA])       # achieved (solid)
    axs[1].plot(
        t,
        data[:, k, IDX_OMEGA_REF],
        linestyle='--',
        color=line.get_color()                          # same color
    )

axs[1].set_ylabel(r'$\omega$')
axs[1].set_title(r'$\omega$ vs $\omega_{ref}$')
axs[1].grid(True)
# --- Summed power over all turbines ---
P_ref_sum = data[:, :, IDX_P_REF].sum(axis=1)
P_gen_sum = data[:, :, IDX_P_GEN].sum(axis=1)
# --- Summed power over all turbines ---
line, = axs[2].plot(t, P_gen_sum, label=r'$\sum P_{gen}$')   # achieved (solid)
axs[2].plot(
    t,
    P_ref_sum,
    linestyle='--',
    color=line.get_color(),                                 # same color
    label=r'$\sum P_{ref}$'
)

axs[2].set_ylabel(r'Total Power')
axs[2].set_title(r'Total Power (All Turbines)')
axs[2].set_xlabel(r'Time [s]')
axs[2].legend()
axs[2].grid(True)

plt.show()
