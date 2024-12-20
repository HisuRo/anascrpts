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
		"outdirname" : "120329_spectra", 
		"output_filename": "mmspc4_120329_spectra", 
		"sn" : 174070, 
		"sub" : 1, 
		"tstart" : 2.5, 
		"tend" : 8.5, 
		"diag_name" : "radm"
	}
	"""
	#############

	# main # EDIT HERE !!
	ece = get_eg.ece(sn=inputs["sn"], sub=inputs["sub"], tstart=inputs["tstart"], tend=inputs["tend"])

	# plot # EDIT HERE !!
	def plot_columns_with_subplots(time, data, group_size, labels, fignum):
		num_cols = data.shape[1]
		num_groups = (num_cols + group_size - 1) // group_size	
		fig, axes = plt.subplots(num_groups, 1, figsize=(10, 2 * num_groups), sharex=True, num=fignum)
		if num_groups == 1:
			axes = [axes]  # axesが1つのときはリスト化	
		for i, ax in enumerate(axes):
			start_idx = i * group_size
			end_idx = min((i + 1) * group_size, num_cols)
			cols = range(start_idx, end_idx)
			for col in cols:
				ax.plot(time, data[:, col], label=f"{labels[col]}")
			ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., ncol=2)
		ax.set_xlabel("Time [s]")
		fig.suptitle(f"ece_fast {inputs['diag_name']}\n"
					f"{inputs['sn']}-{inputs['sub']}")
		fig.tight_layout()

		return fig


	if inputs["diag_name"] == "RADH": 
		dobj = ece.radh
	elif inputs["diag_name"] == "RADL":
		dobj = ece.radl
	elif inputs['diag_name'] == "RADM":
		dobj = ece.radm


	labels = [f"ch{dobj.ADC_ch[i]:.0f} R={dobj.R[i]:.2f}" for i in range(len(dobj.ADC_ch))]
	fignum = f"{inputs['output_filename']}_Te"
	fig = plot_columns_with_subplots(ece.t, dobj.Te, 10, labels, fignum)

	fignum2 = f"{inputs['output_filename']}_rho"
	fig2, ax2 = plt.subplots(num=fignum2)
	ax2.scatter(dobj.R, dobj.rho_vacuum, color='blue', s=5)
	for i, ch in enumerate(dobj.ADC_ch):
		ax2.text(dobj.R[i], dobj.rho_vacuum[i], f"{int(ch)}", fontsize=12, ha='right', va='bottom', color='black')
	ax2.set_xlabel("R [m]")
	ax2.set_ylabel("$r_{\\rm{eff}}/a_{99}$ vacuum")

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		't' : ece.t, 
		'd' : dobj.Te, 
		'ch': dobj.ADC_ch, 
		'R' : dobj.R, 
		'fig2': fig2, 
		'rho': dobj.rho_vacuum
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now, suffix="_Te")
	system.output_fig(fig2, outdir, inputs, output_filepath, now, suffix="_rho")
	print("DONE !!")

if __name__ == "__main__":
	main()