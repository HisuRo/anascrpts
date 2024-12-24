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
		"outdirname" : "24c_1125_ETG/spectra", 
		"output_filename" : "highk_ch3_24c_1125_ETG_6conditions_NFFT4096_ma11_intratio_200kHz_50kHz",  
		"input_datpath" : "C:/python_data/24c_1125_ETG/spectra/highk_ch3_24c_1125_ETG_6conditions_NFFT4096_ma11.pkl", 
		"lower_freq" : 50e3, 
		"higher_freq" : 200e3
	}
	"""
	#############

	# main EDIT HERE !!
	f = data["f"]
	ma_psds = np.array(data["ma_psds"])
	idx_low = np.argmin(np.abs(f - inputs["lower_freq"]))
	idx_high = np.argmin(np.abs(f - inputs["higher_freq"]))
	S_low = ma_psds[:, idx_low]
	S_high = ma_psds[:, idx_high]
	ratio = 10 * np.log10(S_low / S_high)

	# plot EDIT HERE !!

	# output EDIT HERE !!
	outputs = {
		"S_low" : S_low, 
		"S_high" : S_high, 
		"ratio" : ratio, 
		"labels" : data["labels"]
	}

	# systematic output and close
	system.output_pickle_file(outputs, inputs, logs, outdir)
	print("DONE !!")

if __name__ == "__main__":
	main()