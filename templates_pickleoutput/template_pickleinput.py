# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from gsrc import system
import os
import numpy as np # type: ignore

def main():
	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	data = system.load_pickle_data(inputs)
	# data_list = system.load_multiple_pickle_data(inputs, "input_datpaths")  # for multiple input paths

	### input ### EDIT HERE !!!
	""" template 
	{
		"outdirname" : "test", 
		"output_filename" : "test",  
		"input_datpath" : "", 
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
	output_array = np.array([
	])
	colnm_list = ["",""]

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, output_filepath, now)  # suffix="_0"
	system.output_dat(output_array, colnm_list, outdir, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()