# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system

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
		"fmin_mask" : 130e3, 
		"fmax_mask" : 370e3
	}
	"""
	#############

	# main EDIT HERE !!
	fidxs = np.where((data["f1"] > inputs["fmin_mask"]) & (data["f1"] < inputs["fmax_mask"]))[0]
	masked_f = data["f1"][fidxs]
	masked_psd1 = data["psd1"][fidxs]
	masked_psd2 = data["psd2"][fidxs]
	masked_psd3 = data["psd3"][fidxs]
	masked_psd4 = data["psd4"][fidxs]

	popts1, pcovs1 = np.polyfit(np.log10(masked_f), np.log10(masked_psd1), 1, cov=True)
	popts2, pcovs2 = np.polyfit(np.log10(masked_f), np.log10(masked_psd2), 1, cov=True)
	popts3, pcovs3 = np.polyfit(np.log10(masked_f), np.log10(masked_psd3), 1, cov=True)
	popts4, pcovs4 = np.polyfit(np.log10(masked_f), np.log10(masked_psd4), 1, cov=True)

	a1, b1 = popts1
	a2, b2 = popts2
	a3, b3 = popts3
	a4, b4 = popts4

	da1, db1 = np.sqrt(np.diagonal(pcovs1))
	da2, db2 = np.sqrt(np.diagonal(pcovs2))
	da3, db3 = np.sqrt(np.diagonal(pcovs3))
	da4, db4 = np.sqrt(np.diagonal(pcovs4))

	print(f"a1 = {a1:.2f} +- {da1:.2f}\n"
		f"a2 = {a2:.2f} +- {da2:.2f}\n"
		f"a3 = {a3:.2f} +- {da3:.2f}\n"
		f"a4 = {a4:.2f} +- {da4:.2f}\n")

	# plot EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot(masked_f, masked_psd1, label=f"{data['tstart1']} - {data['tend1']} s")
	ax.plot(masked_f, masked_psd2, label=f"{data['tstart2']} - {data['tend2']} s")
	ax.plot(masked_f, masked_psd3, label=f"{data['tstart3']} - {data['tend3']} s")
	ax.plot(masked_f, masked_psd4, label=f"{data['tstart4']} - {data['tend4']} s")
	ax.plot(masked_f, 10**b1 * masked_f**a1, ls="--", c="black")
	ax.plot(masked_f, 10**b2 * masked_f**a2, ls="--", c="black")
	ax.plot(masked_f, 10**b3 * masked_f**a3, ls="--", c="black")
	ax.plot(masked_f, 10**b4 * masked_f**a4, ls="--", c="black")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("PSD [V^2/Hz]")
	ax.legend()
	fig.suptitle("mmspc4 120329")
	fig.tight_layout()

	# output EDIT HERE !!
	outputs = {
		"a1": a1, 
		"da1": da1, 
		"b1": b1, 
		"db1": db1,
		"a2": a2, 
		"da2": da2, 
		"b2": b2, 
		"db2": db2,
		"a3": a3,
		"da3": da3,
		"b3": b3,
		"db3": db3,
		"a4": a4, 
		"da4": da4, 
		"b4": b4, 
		"db4": db4,
		"fig": fig, 
		"masked_f": masked_f, 
		"masked_psd1": masked_psd1, 
		"masked_psd2": masked_psd2, 
		"masked_psd3": masked_psd3, 
		"masked_psd4": masked_psd4
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()