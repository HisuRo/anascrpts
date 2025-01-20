from nasu import get_labcom, system
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import os

def main():
	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "24c_1125_ETG/spectra", 
		"output_filename": "highk_ch3_184508_5-5.18s_NFFT1024", 
		"sn" : 184508, 
		"subsn" : 1, 
		"diagname" : "MWRM-COMB2",
		"ch_i" : 19, 
		"ch_q" : 20, 
		"tstart_retrieve" : 4.5, 
		"tend_retrieve" : 5.5, 
		"tstart_list" : [5.0, 5.057553, 5.157552], 
		"tend_list" : [5.055554, 5.155554, 5.18], 
		"NFFT" : 1024
	}
	"""
	#############

	# main # EDIT HERE !!
	N_sp = len(inputs["tstart_list"])
	tt = get_labcom.timetrace_iq(inputs['sn'], inputs["subsn"], inputs["tstart_retrieve"], inputs["tend_retrieve"], inputs["diagname"], inputs["ch_i"], inputs["ch_q"])
	psds = [0]*N_sp

	for i in range(N_sp):
		sp = tt.raw.spectrum(inputs["tstart_list"][i], inputs["tend_list"][i], NFFT=inputs["NFFT"])
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
	ax.set_ylabel("PSD [/Hz]")
	ax.set_xscale("log")
	ax.set_yscale("log")
	ax.legend()
	fig.suptitle(f"{inputs['diagname']} {inputs['ch_i']} {inputs['ch_q']}\n"
				f"{inputs['sn']}-{inputs['subsn']}")
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
	system.output_fig(fig, outdir, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()