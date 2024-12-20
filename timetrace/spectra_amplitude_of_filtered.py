# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, calc, get_d3d

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
		"output_filename" : "mmspc4_120329_spectra_envelope_of_filtered",  
		"input_datpath" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc4_120329_filtered_spectra.pkl"
		"NFFT" : 2**17
	}
	"""
	#############

	# main EDIT HERE !!
	amp = calc.amplitude(data["d"])
	amp_obj = get_d3d.signal(data["t"], amp, data["Fs"])
	sp1 = amp_obj.spectrum(data['tstart1'], data['tend1'], NFFT=inputs["NFFT"])
	sp2 = amp_obj.spectrum(data['tstart2'], data['tend2'], NFFT=inputs["NFFT"])
	sp3 = amp_obj.spectrum(data['tstart3'], data['tend3'], NFFT=inputs["NFFT"])
	sp4 = amp_obj.spectrum(data['tstart4'], data['tend4'], NFFT=inputs["NFFT"])
	# plot EDIT HEE !
	fig, ax = plt.subplots()
	ax.plot(sp1.f, sp1.psd, label=f"{data['tstart1']} - {data['tend1']} s")
	ax.plot(sp2.f, sp2.psd, label=f"{data['tstart2']} - {data['tend2']} s")
	ax.plot(sp3.f, sp3.psd, label=f"{data['tstart3']} - {data['tend3']} s")
	ax.plot(sp4.f, sp4.psd, label=f"{data['tstart4']} - {data['tend4']} s")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("PSD [V^2/Hz]")
	ax.legend()
	fig.suptitle(f"{data['pointname']} {data['shot']}")
	fig.tight_layout()

	fig2, ax2 = plt.subplots()
	ax2.plot(data["t"], amp)
	ax2.set_xlabel("Time [s]")
	ax2.set_ylabel("envelope [V]")
	fig2.suptitle(f"{data['pointname']} {data['shot']}")
	fig2.tight_layout()

	# output EDIT HERE !!
	outputs = {
		'fig': fig, 
		'f1': sp1.f, 
		'psd1': sp1.psd, 
		'f2': sp2.f, 
		'psd2': sp2.psd, 
		'f3': sp3.f, 
		'psd3': sp3.psd, 
		'f4': sp4.f, 
		'psd4': sp4.psd, 
		"fig2": fig2, 
		"t": data["t"], 
		"d": amp, 
		"Fs": data["Fs"]
	}


	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()