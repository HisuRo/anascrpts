# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, get_d3d, check

def main():
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
		"downsampling_factor" : 100, 
		"tstart_list" : [2.0, 2.3, 2.6, 2.9], 
		"tend_list" : [2.3, 2.6, 2.9, 3.2], 
		"NFFT" : 1024, 
		"xscale" : "log"
	}
	"""
	#############

	# main EDIT HERE !!
	check.same_data(data1["t"], data2["t"])
	sig1 = get_d3d.signal(data1["t"], data1["d"], data1["Fs"])
	sig2 = get_d3d.signal(data2["t"], data2["d"], data2["Fs"])
	sig1.decimate(downsampling_factor=inputs["downsampling_factor"])
	sig2.decimate(downsampling_factor=inputs["downsampling_factor"])

	tw = get_d3d.twin_signals(sig1.dec.t_s, sig1.dec.d, sig2.dec.d, sig1.dec.Fs)

	fig, axs = plt.subplots(3, sharex=True)
	ax1, ax2, ax3 = axs

	Nsp = len(inputs["tstart_list"])
	cohsq_list = [0] * Nsp
	phase_list = [0] * Nsp
	csdamp_list = [0] * Nsp

	for i in range(Nsp):
		tstart = inputs["tstart_list"][i]
		tend = inputs["tend_list"][i]
		cs = tw.cross_spectrum(tstart, tend, NFFT=inputs["NFFT"], ovr=0.5)
		noiselevel = 4. / cs.NEns

		cohsq_list[i] = cs.cohsq
		phase_list[i] = cs.phase
		csdamp_list[i] = cs.csdamp

		ax1.plot(cs.f, cs.cohsq, label=f"{tstart} - {tend} s")
		ax1.hlines(noiselevel, cs.f.min(), cs.f.max(), ls="--", colors="grey")
		ax2.plot(cs.f, cs.phase, label=f"{tstart} - {tend} s")
		ax3.plot(cs.f, cs.csdamp, label=f"{tstart} - {tend} s")

	ax1.set_ylabel("Coherence^2")
	ax1.set_ylim(0, noiselevel * 5)
	ax1.legend(loc="upper left", bbox_to_anchor=(1, 1))
	ax1.text(0.95, 0.95, 'noiselevel = 4/NEns', transform=ax1.transAxes, ha='right', va='top')

	ax2.set_ylabel("Phase [rad]")

	ax3.set_xscale(inputs["xscale"])
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

if __name__ == "__main__":
	main()