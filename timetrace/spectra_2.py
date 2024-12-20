from nasu import get_d3d, system
import matplotlib.pyplot as plt # type: ignore
import os

def main():
	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "120329_spectra", 
		"output_filename": "mmspc4_120329_spectra_around2020ms", 
		"pointname" : "mmspc4", 
		"shot" : 120329, 
		"idx_startdomain" : 9, 
		"N_domain" : 1, 
		"tstart1" : 2.0155, 
		"tend1" : 2.0205, 
		"tstart2" : 2.0205, 
		"tend2" : 2.0255, 
		"NFFT" : 512
	}
	"""
	#############

	# main # EDIT HERE !!
	highk = get_d3d.timetrace_multidomains(inputs['pointname'], inputs["shot"], inputs["idx_startdomain"], inputs["N_domain"])

	sp1 = get_d3d.raw(highk).spectrum(inputs["tstart1"], inputs["tend1"], NFFT=inputs["NFFT"])
	sp2 = get_d3d.raw(highk).spectrum(inputs["tstart2"], inputs["tend2"], NFFT=inputs["NFFT"])

	# plot # EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot(sp1.f, sp1.psd, label=f"{inputs['tstart1']} - {inputs['tend1']} s")
	ax.plot(sp2.f, sp2.psd, label=f"{inputs['tstart2']} - {inputs['tend2']} s")
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("PSD [V^2/Hz]")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.legend()
	fig.suptitle(f"{inputs['pointname']} {inputs['shot']}")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		'f1': sp1.f, 
		'psd1': sp1.psd, 
		'f2': sp2.f, 
		'psd2': sp2.psd
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()