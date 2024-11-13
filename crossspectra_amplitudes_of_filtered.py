# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, get_d3d, check

# initial setting and input
config, wd = system.check_working_directory()
input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
inputs, outdir = system.load_input(input_filepath, outdir_base)
now, logs = system.get_logs(wd)
data1 = system.load_pickle_data(inputs, "input_datpath1")
data2 = system.load_pickle_data(inputs, "input_datpath2")

### input ### EDIT HERE !!!
""" template 
{
	"outdirname" : "120329_crossspectra", 
	"output_filename" : "mmspc4_mmspc3_120329_crossspectra_amplitudes_of_filtered",  
	"input_datpath1" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc4_120329_spectra_amplitude_of_filtered.pkl", 
	"input_datpath2" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc3_120329_spectra_amplitude_of_filtered.pkl", 
	"tstart1" : 2.0, 
	"tend1" : 2.3, 
	"tstart2" : 2.3, 
	"tend2" : 2.6, 
	"tstart3" : 2.6, 
	"tend3" : 2.9, 
	"tstart4" : 2.9, 
	"tend4" : 3.2, 
	"NFFT" : 131072
}
"""
#############

# main EDIT HERE !!
check.same_data(data1["t"], data2["t"])
tw = get_d3d.twin_signals(data1["t"], data1["d"], data2["d"], data1["Fs"])
cs1 = tw.cross_spectrum(inputs["tstart1"], inputs["tend1"], NFFT=inputs["NFFT"], ovr=0)
cs2 = tw.cross_spectrum(inputs["tstart2"], inputs["tend2"], NFFT=inputs["NFFT"], ovr=0)
cs3 = tw.cross_spectrum(inputs["tstart3"], inputs["tend3"], NFFT=inputs["NFFT"], ovr=0)
cs4 = tw.cross_spectrum(inputs["tstart4"], inputs["tend4"], NFFT=inputs["NFFT"], ovr=0)
noiselevel = 1. / cs1.NEns

# plot EDIT HERE !!
fig, axs = plt.subplots(3, sharex=True)
ax1, ax2, ax3 = axs
ax1.plot(cs1.f, cs1.cohsq, label=f"{inputs['tstart1']} - {inputs['tend1']} s")
ax1.plot(cs2.f, cs2.cohsq, label=f"{inputs['tstart2']} - {inputs['tend2']} s")
ax1.plot(cs3.f, cs3.cohsq, label=f"{inputs['tstart3']} - {inputs['tend3']} s")
ax1.plot(cs4.f, cs4.cohsq, label=f"{inputs['tstart4']} - {inputs['tend4']} s")
ax1.hlines(noiselevel, cs1.f.min(), cs1.f.max(), ls="--", colors="grey")
ax1.set_xscale("log")
# ax.set_yscale("")
ax1.set_ylabel("Coherence^2")
ax1.set_ylim(0, noiselevel * 10)
ax1.legend()

ax2.plot(cs1.f, cs1.phase, label=f"{inputs['tstart1']} - {inputs['tend1']} s")
ax2.plot(cs2.f, cs2.phase, label=f"{inputs['tstart2']} - {inputs['tend2']} s")
ax2.plot(cs3.f, cs3.phase, label=f"{inputs['tstart3']} - {inputs['tend3']} s")
ax2.plot(cs4.f, cs4.phase, label=f"{inputs['tstart4']} - {inputs['tend4']} s")
ax2.set_ylabel("Phase [rad]")

ax3.plot(cs1.f, cs1.psd, label=f"{inputs['tstart1']} - {inputs['tend1']} s")
ax3.plot(cs2.f, cs2.psd, label=f"{inputs['tstart2']} - {inputs['tend2']} s")
ax3.plot(cs3.f, cs3.psd, label=f"{inputs['tstart3']} - {inputs['tend3']} s")
ax3.plot(cs4.f, cs4.psd, label=f"{inputs['tstart4']} - {inputs['tend4']} s")
ax3.set_xlabel("Frequency [Hz]")
ax3.set_ylabel("ABS(CSD) [V^2/Hz]")

fig.suptitle(f"{inputs['output_filename']}")
fig.tight_layout()

# output EDIT HERE !!
outputs = {
	"fig": fig, 
	"f1" : cs1.f, 
	"cohsq1" : cs1.cohsq, 
	"phase1" : cs1.phase, 
	"f2" : cs2.f, 
	"cohsq2" : cs2.cohsq, 
	"phase2" : cs2.phase, 
	"f3" : cs3.f, 
	"cohsq3" : cs3.cohsq, 
	"phase3" : cs3.phase, 
	"f4" : cs4.f, 
	"cohsq4" : cs4.cohsq, 
	"phase4" : cs4.phase, 
}

# systematic output and close
output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
system.output_fig(fig, outdir, inputs, output_filepath, now)
print("DONE !!")
