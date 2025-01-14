# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, calc
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
		"outdirname" : "174070_bispectrum", 
		"output_filename" : "highk_ch3_4.6-4.8s_174070_NFFT256_hamming_300kHz_vsf2",  
		"input_datpath" : "C:python_data/174070_bispectrum/highk_ch3_4.6-4.8s_174070_NFFT256_hamming_300kHz.pkl", 
		"fix_var" : "f2"
	}
	"""
	#############

	# main EDIT HERE !!
	bsst = calc.bispectral_stat(data["fx"], data["fy"], data["fz"], data["d1"], data["e1"], data["d2"], data["e2"], inputs["fix_var"])
	noiselevel = 1 / data["NEns"]

	# plot EDIT HERE !!
	fig, (ax1, ax2) = plt.subplots(2, figsize=(6, 8), sharex=True)
	ax1.errorbar(bsst.f, bsst.bicohsq_avg, bsst.bicohsq_ste, ecolor="grey")
	ax1.hlines(noiselevel, bsst.f[0], bsst.f[-1], color="grey", linestyle="--")
	ax1.set_ylabel("Bi-coherence^2")

	ax2.errorbar(bsst.f, bsst.biphase_avg, bsst.biphase_ste, ecolor="grey")
	ax2.set_ylabel("Phase [rad]")
	ax2.set_xlabel("Frequency [Hz]")
	fig.suptitle(f"{inputs['outdirname']}\n{inputs['output_filename']}")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"fig": fig, 
		"f": bsst.f, 
		"d1": bsst.bicohsq_avg,
		"e1": bsst.bicohsq_ste,
		"d2": bsst.biphase_avg,
		"e2": bsst.biphase_ste, 
		"NEns": data["NEns"]
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now, suffix="")
	print("DONE !!")

if __name__ == "__main__":
	main()