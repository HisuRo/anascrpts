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
		"fit_colnm" : "Te_fit", 
		"fiterr_colnm" : "Te_fit_err", 
		"tstart" : 4.0,
		"tend" : 5.,
		"polyN" : 10
	}
	"""
	#############

	# main # EDIT HERE !!
	tR_ts = get_eg.tsmap(inputs["sn"], inputs["subsn"], inputs["d_colnm"], inputs["e_colnm"], inputs["tstart"], inputs["tend"])
	tR_tsfit = get_eg.tsmap(inputs["sn"], inputs["subsn"], inputs["fit_colnm"], inputs["fiterr_colnm"], inputs["tstart"], inputs["tend"])
	tR_ts.tR.twin.polyfit(polyN=inputs["polyN"])

	for i, tat in enumerate(tR_ts.tR.twin.t_s):

		# plot # EDIT HERE !!
		fig, ax = plt.subplots(num="test")
		ax.errorbar(tR_ts.tR.twin.rho[i], tR_ts.tR.twin.d[i], tR_ts.tR.twin.e[i], fmt=".", ecolor="grey", color="black", label=inputs['d_colnm'])
		ax.plot(tR_tsfit.tR.twin.rho[i], tR_tsfit.tR.twin.d[i], color="blue", label=inputs['fit_colnm'])
		ax.fill_between(tR_tsfit.tR.twin.rho[i], tR_tsfit.tR.twin.d[i] + tR_tsfit.tR.twin.e[i], tR_tsfit.tR.twin.d[i] - tR_tsfit.tR.twin.e[i], color="blue", alpha=0.3)
		ax.plot(tR_ts.tR.twin.pfit.rho[i], tR_ts.tR.twin.pfit.d[i], color="green", label=f"{inputs['d_colnm']} polyfit deg={inputs['polyN']}")
		ax.fill_between(tR_ts.tR.twin.pfit.rho[i], tR_ts.tR.twin.pfit.d[i] + tR_ts.tR.twin.pfit.e[i], tR_ts.tR.twin.pfit.d[i] - tR_ts.tR.twin.pfit.e[i], color="green", alpha=0.3)
		ax.set_xlabel("reff/a99")
		ax.set_ylabel(f"{inputs['d_colnm']}")
		# ax.set_xscale("")
		# ax.set_yscale("")
		ax.legend()
		fig.suptitle(f"{inputs['sn']}-{inputs['subsn']}\n" \
					f"{tat} s")
		fig.tight_layout()

		# output # EDIT HERE !!
		outputs = {
			'fig': fig, 
			'rho_d': tR_ts.tR.twin.rho[i], 
			'd': tR_ts.tR.twin.d[i], 
			'e': tR_ts.tR.twin.e[i], 
			'rho_fit': tR_tsfit.tR.twin.rho[i], 
			'fit': tR_tsfit.tR.twin.d[i], 
			'fit_err': tR_tsfit.tR.twin.e[i], 
			'rho_pfit': tR_ts.tR.twin.pfit.rho[i], 
			'pfit': tR_ts.tR.twin.pfit.d[i], 
			'pfit_err': tR_ts.tR.twin.pfit.e[i]
		}

		# systematic output and close
		output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir, suffix=f"_{tat}s")
		system.output_fig(fig, outdir, output_filepath, now)  # suffix="_0"

	print("DONE !!")

if __name__ == "__main__":
	main()