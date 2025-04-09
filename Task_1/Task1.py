import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
sheet = pd.read_excel('SFS_Screening_SFDBMD.xlsx')

# Extract relevant columns
x = sheet['Distance (m)']
sfd = sheet['SF (kN)']
bmd = sheet['BM (kN-m)']

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# --- Shear Force Diagram ---
axs[0].bar(x, sfd, width=0.05, color='blue', edgecolor='black')
axs[0].set_title('Shear Force Diagram ', fontsize=12)
axs[0].set_xlabel('Distance (m)')
axs[0].set_ylabel('Shear Force (kN)')
axs[0].grid(True)

# Annotate Max and Min SF values
sf_max_idx = sfd.idxmax()
sf_min_idx = sfd.idxmin()
axs[0].annotate(f'Max: {sfd[sf_max_idx]:.3f} kN',
                xy=(x[sf_max_idx], sfd[sf_max_idx]),
                xytext=(x[sf_max_idx]+0.2, sfd[sf_max_idx]+5),
                arrowprops=dict(arrowstyle="->"))

axs[0].annotate(f'Min: {sfd[sf_min_idx]:.3f} kN',
                xy=(x[sf_min_idx], sfd[sf_min_idx]),
                xytext=(x[sf_min_idx]+0.2, sfd[sf_min_idx]-10),
                arrowprops=dict(arrowstyle="->"))

# --- Bending Moment Diagram ---
axs[1].bar(x, bmd, width=0.05, color='red', edgecolor='black')
axs[1].set_title('Bending Moment Diagram ', fontsize=12)
axs[1].set_xlabel('Distance (m)')
axs[1].set_ylabel('Bending Moment (kN-m)')
axs[1].grid(True)

# Annotate Max and Min BM values
bm_max_idx = bmd.idxmax()
bm_min_idx = bmd.idxmin()
axs[1].annotate(f'Max: {bmd[bm_max_idx]:.3f} kN-m',
                xy=(x[bm_max_idx], bmd[bm_max_idx]),
                xytext=(x[bm_max_idx]+0.2, bmd[bm_max_idx]+5),
                arrowprops=dict(arrowstyle="->"))

axs[1].annotate(f'Min: {bmd[bm_min_idx]:.3f} kN-m',
                xy=(x[bm_min_idx], bmd[bm_min_idx]),
                xytext=(x[bm_min_idx]+0.2, bmd[bm_min_idx]-10),
                arrowprops=dict(arrowstyle="->"))

plt.suptitle('Bending Moment Diagram (Right) & Shear Force Diagram (Left)', fontsize=14, y=0.95)
plt.tight_layout()
plt.show()
