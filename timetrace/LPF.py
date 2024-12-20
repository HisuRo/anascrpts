# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, calc
import os

def main():
	# initial setting and input
	config, wd = system.check_working_directory()
	script_path = os.path.abspath(__file__)
	input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
	inputs, outdir = system.load_input(input_filepath, outdir_base)
	now, logs = system.get_logs(wd, script_path)
	data = system.load_pickle_data(inputs)

	### input ### EDIT HERE !!!
	""" template 
	{
		"outdirname" : "120329_spectra", 
		"output_filename" : "mmspc4_120329_LPFed_amplitude",  
		"input_datpath" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc4_120329_spectra_envelope_of_filtered.pkl", 
		"fpass" : 1e3, 
		"fstop" : 10e3, 
		"data_label" : "filtered amplitude [V]"
	}
	"""
	#############

	# main EDIT HERE !!
	d_filt = calc.lowpass(data["d"], data["Fs"], inputs["fpass"], inputs["fstop"])

	# plot EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot(data["t"], d_filt)
	# ax.set_xscale("")
	# ax.set_yscale("")
	ax.set_xlabel("Time [s]")
	ax.set_ylabel(f"{inputs['data_label']}")
	# ax.legend()
	fig.suptitle(f"{inputs['output_filename']}")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"fig": fig, 
		"t" : data["t"], 
		"d" : d_filt, 
		"Fs" : data["Fs"]
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()