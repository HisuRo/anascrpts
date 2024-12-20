from nasu import get_d3d, system
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore

def main():
	# initial setting and input
	config, wd = system.check_working_directory()
	script_path = os.path.abspath(__file__)
	input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
	inputs, outdir = system.load_input(input_filepath, outdir_base)
	now, logs = system.get_logs(wd, script_path)

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "120329_spectra", 
		"output_filename": "mmspc4_120329_spectra_after_sawteeth_from2000-2300ms", 
		"pointname" : "mmspc4", 
		"shot" : 120329, 
		"idx_startdomain" : 9, 
		"N_domain" : 3, 
		"tstart_list" : [2.0205, 2.0495, 2.0715, 2.0905, 2.1255, 2.156, 2.179, 2.198, 2.218, 2.243, 2.265, 2.285], 
		"tend_list" : [2.0255, 2.0545, 2.0765, 2.0955, 2.1305, 2.161, 2.184, 2.203, 2.223, 2.248, 2.27, 2.29], 
		"NFFT" : 512
	}
	"""
	#############

	# main # EDIT HERE !!
	N_sp = len(inputs["tstart_list"])
	tt = get_d3d.timetrace_multidomains(inputs['pointname'], inputs["shot"], inputs["idx_startdomain"], inputs["N_domain"])
	psds = [0]*N_sp

	for i in range(N_sp):
		sp = get_d3d.raw(tt).spectrum(inputs["tstart_list"][i], inputs["tend_list"][i], NFFT=inputs["NFFT"])
		psds[i] = sp.psd
	psds = np.array(psds)
	psd_avg = np.average(psds, axis=0)
	f = sp.f

	# plot # EDIT HERE !!
	fig, ax = plt.subplots()
	for i in range(N_sp):
		ax.plot(f, psds[i], ".", label=f"{inputs['tstart_list'][i]} - {inputs['tend_list'][i]} s")
	ax.plot(f, psd_avg, label=f"averaged", c="black")
	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("PSD [V^2/Hz]")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.legend()
	fig.suptitle(f"{inputs['pointname']} {inputs['shot']}\n"
				f"{inputs['output_filename']}")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		'f': f, 
		'psds': psds, 
		'psd_avg': psd_avg
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()