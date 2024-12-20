# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system
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
		"output_filename" : "mmspc4_120329_spectra_powerlaw",  
		"input_datpath" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc4_120329_spectra.pkl", 
		"" : 
	}
	"""
	#############

	# main EDIT HERE !!

	# plot EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot()
	ax.set_xscale("")
	ax.set_yscale("")
	ax.set_xlabel("")
	ax.set_ylabel("")
	ax.legend()
	fig.suptitle("")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"fig": fig
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()