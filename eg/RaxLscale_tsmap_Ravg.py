from nasu import get_eg, system
import matplotlib.pyplot as plt # type: ignore
import os

def main():

	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "", 
		"output_filename": "", 
		"sn" : 184509, 
		"subsn" : 1,
		"d_colnm" : "Te",
		"e_colnm" : "dTe",
		"tstart" : 4.25,
		"tend" : 4.75,
		"Rat" : 4.1,
		"dR" : 0.106,
		"polyN" : 10, 
		"rho_cut" : 0.9, 
		"include_outerside": false
	}
	"""
	#############

	# main # EDIT HERE !!
	tR_ts = get_eg.tsmap(inputs["sn"], inputs["subsn"], inputs["d_colnm"], inputs["e_colnm"], 
					  inputs["tstart"], inputs["tend"], rho_cut=inputs['rho_cut'], include_outerside=inputs['include_outerside'])
	tR_ts.tR.twin.polyfit(polyN=inputs["polyN"])
	tR_ts.tR.twin.pfit.Lscale(Rax=tR_ts.Rax)
	dat = tR_ts.tR.twin.pfit.RL.R_window(inputs["Rat"], dR=inputs["dR"], include_outerside=True)
	dat.average(axis=1, skipnan=True)

	# plot # EDIT HERE !!
	fig, ax = plt.subplots()
	ax.errorbar(dat.t_s, dat.avg.d, dat.avg.e, ecolor="grey")
	ax.set_xlabel("Time [s]")
	ax.set_ylabel(f"Rax/L{inputs['d_colnm']}")
	fig.suptitle(f"{inputs['sn']}-{inputs['subsn']}\n"
			     f"{inputs['Rat']} [m] dR={inputs['dR']}")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		't': dat.t_s, 
		'd': dat.avg.d, 
		'e': dat.avg.e
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, output_filepath, now)  # suffix="_0"
	print("DONE !!")

if __name__ == "__main__":
	main()
