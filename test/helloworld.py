from gsrc import system
import matplotlib.pyplot as plt # type: ignore
import os
import numpy as np # type: ignore

def main():

	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "text", 
		"output_filename": "helloworld", 
		"" : ""
	}
	"""
	#############

	# main # EDIT HERE !!
	print(inputs['text'])
		
	xx = np.arange(100) * 0.01
	yy = 2 * xx

	# plot # EDIT HERE !!
	fig, ax = plt.subplots()
	ax.plot(xx, yy)
	ax.set_xlabel("x")
	ax.set_ylabel("y")
	# ax.set_xscale("")
	# ax.set_yscale("")
	# ax.legend()
	fig.suptitle(f"test")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		'x': xx, 
		'y': yy
	}
	output_array = np.array([
		xx, 
		yy
	]).T
	colnm_list = ["x","y"]

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, output_filepath, now)  # suffix="_0"
	system.output_dat(output_array, colnm_list, outdir, output_filepath)
	print("DONE !!")

if __name__ == "__main__":
	main()