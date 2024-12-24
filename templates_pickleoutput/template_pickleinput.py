# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system
import os

def main():
	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	data = system.load_pickle_data(inputs)
	# data_list = system.load_multiple_pickle_data(inputs, "input_datpaths")  # for multiple input paths

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