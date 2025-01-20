from nasu import get_labcom, system
import matplotlib.pyplot as plt # type: ignore
import os

def main():

	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "24c_1125_ETG/bsmod", 
		"output_filename": "bsmod_timing_184508_4-5s", 
		"sn" : 184508, 
		"subsn" : 1, 
		"tstart" : 4.0, 
		"tend" : 5.0, 
		"diagname" : "MWRM-PXI", 
		"ch" : 4, 
		"rate_threshold" : 10000, 
		"t_process_width" : 1e-5
	}
	"""
	#############

	# main # EDIT HERE !!
	bsmod = get_labcom.timetrace(inputs["sn"], inputs["subsn"], inputs["tstart"], inputs["tend"], inputs["diagname"], inputs["ch"])
	rise = bsmod.raw.detect_event(rate_threshold=inputs['rate_threshold'], t_process_width=inputs['t_process_width'], type="rise")
	drop = bsmod.raw.detect_event(rate_threshold=inputs['rate_threshold'], t_process_width=inputs['t_process_width'], type="drop")

	# plot # EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot(bsmod.t_s, bsmod.d)
	ax.set_xlabel("Time [s]")
	ax.set_ylabel("Signal [V]")
	fig.suptitle(f"{inputs['sn']}-{inputs['subsn']}\n")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig' : fig, 
		't' : bsmod.t_s, 
		'd' : bsmod.d,
		't_offstart': rise.t_s, 
		't_offend' : drop.t_s
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()