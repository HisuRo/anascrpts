import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import numpy as np # type: ignore
from nasu import calc
import matplotlib.pyplot as plt # type: ignore
from scipy import stats # type: ignore

### input ###
Fs = int(1e6)
T = 10000  # [ms]
randomscale_x = 1.0
randomscale_y = 1.0
tstart = 0.1
tend = 0.4
NFFT = 2**16
#############

size = T*Fs // 1000 + 1
print(size)

t = np.linspace(0, T / 1000, size)
x = np.random.normal(loc=0., scale=randomscale_x, size=size)
y = np.random.normal(loc=0., scale=randomscale_y, size=size)

cs = calc.cross_spectrum(t_s=t, d1=x, d2=y, Fs_Hz=Fs, tstart=tstart, tend=tend, NFFT=NFFT, ovr=0.5, window="hann", detrend="constant", unwrap_phase=False)

noiselevel = 1. / cs.NEns
mean_level = np.average(cs.cohsq)
std_cohsq = np.std(cs.cohsq, ddof=1)

beta_params = stats.beta.fit(cs.cohsq)
alpha, beta = beta_params[0], beta_params[1]
print(
	f"alpha: {alpha}\n"
	f"beta : {beta}\n"
	)

fig, ax1 = plt.subplots(1, sharex=True)

ax1.plot(cs.f, cs.cohsq, alpha=0.6)
ax1.hlines(noiselevel, cs.f.min(), cs.f.max(), ls="--", colors="grey", label="1/NEns")
ax1.hlines(mean_level, cs.f.min(), cs.f.max(), ls="-.", colors="red", label="mean coherence^2")

ax1.set_ylabel("Coherence^2")
# ax1.set_ylim(0, noiselevel * 10)
ax1.legend()

# ax1.set_xscale("log")
ax1.set_xlabel("Frequency [Hz]")

fig.suptitle(f"Coherence of random signals following normal distributions")
fig.tight_layout()

fig2, ax2 = plt.subplots(1)
ax2.hist(cs.cohsq, bins=1000, density=True, alpha=0.6)

x = np.linspace(0, 1, 1001)
pdf_fitted = stats.beta.pdf(x, alpha, beta)
ax2.plot(x, pdf_fitted, c="red", label=f"Beta Fit\nα={alpha:.2f}, β={beta:.2f}")
ax2.vlines(noiselevel, 0, 7, ls="--", colors="grey", label="1/NEns")
ax2.vlines(mean_level, 0, 7, ls="-.", colors="red", label="mean coherence^2")

ax2.set_xlabel("Coherence^2")
ax2.legend()
fig2.suptitle("PDF Histogram of Coherence^2")

plt.show()
