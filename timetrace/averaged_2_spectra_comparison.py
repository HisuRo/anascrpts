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
	data1 = system.load_pickle_data(inputs, "input_datpath1")
	data2 = system.load_pickle_data(inputs, "input_datpath2")

	### input ### EDIT HERE !!!
	""" template 
	{
		"outdirname" : "120329_spectra_sawtooth", 
		"output_filename" : "mmspc4_120329_spectra_comparison_before_after_sawteeth_from2000-2300ms",  
		"input_datpath1" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra_sawtooth/mmspc4_120329_spectra_before_sawteeth_from2000-2300ms.pkl", 
		"input_datpath2" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra_sawtooth/mmspc4_120329_spectra_after_sawteeth_from2000-2300ms.pkl", 
		"label1" : "before", 
		"label2" : "after", 
		"xscale" : "linear"
	}
	"""
	#############

	# main EDIT HERE !!
	f = data1["f"]
	psd1 = data1["psd_avg"]
	psd2 = data2["psd_avg"]
	diff_psd = psd2 - psd1

	# plot EDIT HERE !!
	fig, axs = plt.subplots(2, sharex=True)
	ax, ax2 = axs
	ax.plot(f, psd1, label=f"{inputs['label1']}")
	ax.plot(f, psd2, label=f"{inputs['label2']}")
	ax.set_xscale(inputs['xscale'])
	ax.set_yscale("log")
	ax.set_ylabel("PSD [V^2/Hz]")
	ax.legend()

	ax2.plot(f, diff_psd, label=f"{inputs['label2']} - {inputs['label1']}")
	ax2.hlines(0, f.min(), f.max(), ls="--", colors="grey")
	ax2.set_xlabel("Frequency [Hz]")
	ax2.set_ylabel("PSD difference [V^2/Hz]")
	ax2.legend()

	fig.suptitle(f"{inputs['output_filename']}")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"fig": fig, 
		"f" : f, 
		"psd1" : psd1, 
		"psd2" : psd2, 
		"diff" : diff_psd, 
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()