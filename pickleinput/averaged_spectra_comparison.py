import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, calc
import os

def main():
	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	data_list = system.load_multiple_pickle_data(inputs, "input_datpaths")

	### input ### EDIT HERE !!!
	""" template 
	{
		"outdirname" : "C:/python_data/24c_1125_ETG/spectra", 
		"output_filename" : "highk_ch3_184516_4.6-4.68s_184508_5-5.18s_NFFT4096",  
		"input_datpaths" : ["C:/python_data/24c_1125_ETG/spectra/highk_ch3_184516_4.6-4.68s_NFFT4096.pkl", 
							"C:/python_data/24c_1125_ETG/spectra/highk_ch3_184508_5-5.18s_NFFT4096.pkl"], 
		"labels" : ["low grad Te", "high grad Te"], 
		"data_unit" : "V", 
		"freq_ma_length" : 10
	}
	"""
	#############

	# main EDIT HERE !!

	# plot EDIT HERE !!
	fig, ax = plt.subplots()

	Nsp = len(inputs["input_datpaths"])
	psds = [0] * Nsp
	ma_psds = [0] * Nsp
	
	for i in range(Nsp):

		data = data_list[i]
		f = data["f"]
		psd = data["psd_avg"]
		ma_psd = calc.moving_average(psd, window_size=inputs["freq_ma_length"], mode="same")
		psds[i] = psd
		ma_psds[i] = ma_psd
		ax.plot(f, ma_psd, label=f"{inputs['labels'][i]}")
		ax.set_yscale("log")
		ax.set_ylabel(f"PSD [{inputs['data_unit']}$^2$/Hz]")
		ax.set_xlabel("Frequency [Hz]")
		ax.legend()

	fig.suptitle(f"{inputs['output_filename']}")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"fig": fig, 
		"f" : f, 
		"psds" : psds, 
		"ma_psds" : ma_psds
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()