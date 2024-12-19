from nasu import get_labcom, system
import matplotlib.pyplot as plt # type: ignore
import os

def main():

	# initial setting and input
	config, wd = system.check_working_directory()
	input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
	inputs, outdir = system.load_input(input_filepath, outdir_base)
	now, logs = system.get_logs(wd)

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "174070_spectra", 
		"output_filename": "mmwbs_ch3_174070_spectra", 
		"sn" : 174070, 
		"subsn" : 1, 
		"diagname" : MWRM-PXI, 
		"ch_i" : 1, 
		"ch_q" : 2, 
		"tstart_retrieve" : 3.,
		"tend_retrieve" : 6.,
		"tstart_list" : [4.3, 4.3335, 4.4335, 4.47, 4.5335, 4.6335], 
		"tend_list" : [4.3314, 4.4314, 4.47, 4.5314, 4.6314, 4.7], 
		"NFFT" : 1024
	}
	"""
	#############


	# main # EDIT HERE !!
	tt = get_labcom.timetrace_iq(inputs["sn"], inputs["subsn"], inputs["tstart_retrieve"], inputs["tend_retrieve"], inputs['diagname'], inputs["ch_i"], inputs["ch_q"])

	fig, ax = plt.subplots()

	Nsp = len(inputs["tstart_list"])
	psd_list = [0] * Nsp

	for i in range(Nsp):
		tstart = inputs["tstart_list"][i]
		tend = inputs["tend_list"][i]

		sp = tt.raw.spectrum(tstart, tend, NFFT=inputs["NFFT"])
		ax.plot(sp.f, sp.psd, label=f"{tstart} - {tend} s")

		psd_list[i] = sp.psd

	ax.set_xlabel("Frequency [Hz]")
	ax.set_ylabel("PSD [V^2/Hz]")
	ax.set_yscale("log")
	ax.legend()
	fig.suptitle(f"{inputs['diagname']} {inputs['ch_i']} {inputs['ch_q']}\n"
				f"{inputs['sn']}-{inputs['subsn']}")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		'f': sp.f, 
		'psd': psd_list
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()