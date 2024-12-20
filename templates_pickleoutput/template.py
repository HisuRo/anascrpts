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
		"output_filename": "mmspc4_120329_spectra", 
		"" : ""
	}
	"""
	#############

	# main # EDIT HERE !!

	# plot # EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot()
	ax.set_xlabel("")
	ax.set_ylabel("")
	ax.set_xscale("")
	ax.set_yscale("")
	ax.legend()
	fig.suptitle(f"")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()