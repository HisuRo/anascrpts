# calculate 1st backward difference and detect  by arbitrary threshold

from nasu import get_d3d, system, proc
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
from scipy.signal import find_peaks # type: ignore


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
		"outdirname" : "120329_timetraces", 
		"output_filename": "ece27_drop_detection", 
		"pointname" : "ece27", 
		"shot" : 120329,
		"tstart" : 2.0, 
		"tend" : 3.2, 
		"rate_threshold" : 0.7, 
		"process_width : 0.010
	}
	"outdirname" : set output directory name
	"output_filename" : set output file name
	"pointname" : pointname of target signal S(t)
	"shot" : target shot
	"tstart" : start time of target period [s]
	"tend" : end time of target period [s]
	"rate_threshold" : threshold of rate of change in time over which the signal drops [S(t) unit / s] (absolute value)
	"process_width" : time width to calculate peak to peak value [s]. The center of process_width is t_drop event.
	"""
	#############

	# main # EDIT HERE !!
	tt = get_d3d.timetrace(inputs["pointname"], inputs["shot"])
	_, datlist = proc.getTimeIdxsAndDats(tt.t_s, inputs["tstart"], inputs["tend"], [tt.t_s, tt.d])
	t, d = datlist
	rate = np.diff(d) / np.diff(t)
	inverted_rate = - rate
	idx_drop, _ = find_peaks(inverted_rate, height=inputs["rate_threshold"])
	t_drop = t[1:][idx_drop]

	process_width = int(tt.Fs * inputs["process_width"])
	idxs_arounddrop = np.tile(idx_drop.reshape(idx_drop.size, 1), process_width) + np.arange(process_width) - process_width // 2
	d_process = d[idxs_arounddrop]
	drop_depth = d_process.max(axis=-1) - d_process.min(axis=-1)
	drop_center = (d_process.max(axis=-1) + d_process.min(axis=-1)) / 2
	rel_drop_depth = drop_depth / drop_center

	# plot # EDIT HERE !!
	fig, axs = plt.subplots(2, sharex=True)
	axs[0].plot(t, d)
	axs[1].plot(t[1:], rate)
	axs[0].vlines(t_drop, d.min(), d.max(), ls="--", color='grey')
	axs[1].vlines(t_drop, d.min(), d.max(), ls="--", color='grey')
	axs[1].set_xlabel("Time [s]")
	axs[0].set_ylabel(inputs["pointname"])
	axs[1].set_ylabel(f"d {inputs['pointname']} / dt")
	fig.suptitle(f"{inputs['shot']}")
	fig.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig': fig, 
		"t": t, 
		"d": d, 
		"d_rate": rate, 
		"t_event": t_drop, 
		"drop_depth" : drop_depth, 
		"drop_center" : drop_center, 
		"rel_drop_depth" : rel_drop_depth
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig, outdir, inputs, output_filepath, now)
	print("DONE !!")

if __name__ == "__main__":
	main()