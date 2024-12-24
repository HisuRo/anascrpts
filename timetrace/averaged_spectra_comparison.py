import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system
import os

def main():
	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)

	### input ### EDIT HERE !!!
	""" template 
	{
		"outdirname" : "C:/python_data/24c_1125_ETG/spectra", 
		"output_filename" : "highk_ch3_184516_4.6-4.68s_184508_5-5.18s_NFFT4096",  
		"input_datpaths" : ["C:/python_data/24c_1125_ETG/spectra/highk_ch3_184516_4.6-4.68s_NFFT4096.pkl", 
							"C:/python_data/24c_1125_ETG/spectra/highk_ch3_184508_5-5.18s_NFFT4096.pkl"], 
		"labels" : ["low grad Te", "high grad Te"], 
		"data_unit" : "V"
	}
	"""
	#############

	# main EDIT HERE !!

	# plot EDIT HERE !!
	fig, ax = plt.subplots()

	Nsp = len(inputs["input_datpaths"])
	psds_list = [0] * Nsp
	data_list = system.load_multiple_pickle_data(inputs, "input_datpaths")
	for i in range(Nsp):

		data = data_list[i]
		f = data["f"]
		psds_list[i] = data["psd_avg"]
		ax.plot(f, psds_list[i], label=f"{inputs['labels'][i]}")
		ax.set_yscale("log")
		ax.set_ylabel(f"PSD [{inputs['data_unit']}$^2$/Hz]")
		ax.legend()

	fig.suptitle(f"{inputs['output_filename']}")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"fig": fig, 
		"f" : f, 
		"psd" : psds_list
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()