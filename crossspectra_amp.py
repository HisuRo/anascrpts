# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, get_d3d, check, calc

# initial setting and input
config, wd = system.check_working_directory()
input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
inputs, outdir = system.load_input(input_filepath, outdir_base)
now, logs = system.get_logs(wd)

### input ### EDIT HERE !!!
""" template 
{
	"outdirname" : "120329_crossspectra", 
	"output_filename" : "mmspc4_mmspc3_120329_crossspectra_amplitudes", 
	"pointname1" : "mmspc4", 
	"pointname2" : "mmspc3", 
	"shot" : 120329, 
	"idx_startdomain" : 9, 
	"N_domain" : 3, 
	"carrier_freq" : 2e6, 
	"downsampling_factor" : 20, 
	"tstart_list" : [2.0], 
	"tend_list" : [2.3], 
	"NFFT" : 1024
}
"""
#############

# main EDIT HERE !!

highk = get_d3d.timetrace_multidomains(inputs["pointname1"], inputs["shot"], inputs["idx_startdomain"], inputs["N_domain"])
lowk = get_d3d.timetrace_multidomains(inputs["pointname2"], inputs["shot"], inputs["idx_startdomain"], inputs["N_domain"])
lowk.produce_virtual_IQ_signal(inputs["carrier_freq"], inputs["downsampling_factor"])

highk.amplitude.decimate(inputs["downsampling_factor"])

check.same_data(highk.amplitude.dec.t_s, lowk.virtIQamp.t_s)
tw = get_d3d.twin_signals(highk.amplitude.dec.t_s, highk.amplitude.dec.d, lowk.virtIQamp.t_s, highk.amplitude.dec.Fs)


# plot EDIT HERE !!
fig, axs = plt.subplots(3, sharex=True)
ax1, ax2, ax3 = axs

Nsp = len(inputs["tstart_list"])
cohsq_list = [0] * Nsp
phase_list = [0] * Nsp
csdamp_list = [0] * Nsp

for i in range(Nsp):
	tstart = inputs["tstart_list"][i]
	tend = inputs["tend_list"][i]
	cs = tw.cross_spectrum(tstart, tend, NFFT=inputs["NFFT"], ovr=0)
	noiselevel = 4. / cs.NEns

	cohsq_list[i] = cs.cohsq
	phase_list[i] = cs.phase
	csdamp_list[i] = cs.csdamp

	ax1.plot(cs.f, cs.cohsq, label=f"{tstart} - {tend} s")
	ax1.hlines(noiselevel, cs.f.min(), cs.f.max(), ls="--", colors="grey")
	ax2.plot(cs.f, cs.phase, label=f"{tstart} - {tend} s")
	ax3.plot(cs.f, cs.csdamp, label=f"{tstart} - {tend} s")

ax1.set_ylabel("Coherence^2")
ax1.set_ylim(0, noiselevel * 10)
ax1.legend()

ax2.set_ylabel("Phase [rad]")

ax3.set_xscale("log")
ax3.set_xlabel("Frequency [Hz]")
ax3.set_ylabel("ABS(CSD) [V^2/Hz]")
ax3.set_yscale("log")

fig.suptitle(f"{inputs['output_filename']}")
fig.tight_layout()

# output EDIT HERE !!
outputs = {
	"fig": fig, 
	"f" : cs.f, 
	"cohsq" : cohsq_list, 
	"phase" : phase_list, 
	"csdamp" : csdamp_list, 
}

# systematic output and close
output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
system.output_fig(fig, outdir, inputs, output_filepath, now)
print("DONE !!")
