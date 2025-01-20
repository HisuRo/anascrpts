from nasu import get_labcom, system
import matplotlib.pyplot as plt # type: ignore
from matplotlib.colors import Normalize # type: ignore
import os

def main():

	# initial setting and input
	
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
	
	

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "174070_bispectrum", 
		"output_filename" : "highk_lowk_", 
		"sn" : 174070, 
		"subsn" : 1, 
		"tstart_retrieve" : 4.0, 
		"tend_retrieve" : 5.0, 
		"diagname_1" : "MWRM-PXI", 
		"ch_i_1" : 1, 
		"ch_q_1" : 2, 
		"diagname_2" : "MWRM-COMB", 
		"ch_i_2" : 13, 
		"ch_q_2" : 14, 
		"tstart_list" : [4.6, 4.6335, 4.7335], 
		"tend_list" : [4.6314, 4.7314, 4.8], 
		"NFFT2" : 512,
		"ovr" : 0.5, 
		"window" : "hann", 
		"mode" : "112",
		"flim1" : 300e3, 
		"flim2" : 200e3,
		"interpolate" : false
	}
	"""
	#############

	# main # EDIT HERE !!
	if inputs["flim1"] == 0:
		inputs["flim1"] = None
	if inputs["flim2"] == 0:
		inputs["flim2"] = None
	tt1 = get_labcom.timetrace_iq(inputs["sn"], inputs["subsn"], inputs["tstart_retrieve"], inputs["tend_retrieve"], inputs["diagname_1"], inputs["ch_i_1"], inputs["ch_q_1"])
	tt2 = get_labcom.timetrace_iq(inputs["sn"], inputs["subsn"], inputs["tstart_retrieve"], inputs["tend_retrieve"], inputs["diagname_2"], inputs["ch_i_2"], inputs["ch_q_2"])

	tw = get_labcom.twin_signals(tt1.raw.t_s, tt2.raw.t_s, tt1.raw.d, tt2.raw.d, tt1.raw.Fs, tt2.raw.Fs)

	bs = tw.bispectrum_multiwindows(inputs["tstart_list"], inputs["tend_list"], inputs["NFFT2"], inputs["ovr"], inputs["window"], inputs['mode'], 
								 flim1=inputs['flim1'], flim2=inputs['flim2'], interpolate=inputs["interpolate"])
	noiselevel = 4. / bs.NEns

	# plot # EDIT HERE !!
	trange_str = ", ".join([f"{inputs['tstart_list'][i]}-{inputs['tend_list'][i]}s" for i in range(len(inputs["tstart_list"]))])
	figtitle = f"#{inputs['sn']}\n" \
				f"{trange_str}\n" \
				f"mode={inputs['mode']}\n" \
				f"1: {inputs['diagname_1']} {inputs['ch_i_1']} {inputs['ch_q_1']}\n" \
				f"2: {inputs['diagname_2']} {inputs['ch_i_2']} {inputs['ch_q_2']}"
	fig1, ax1 = plt.subplots()
	norm = Normalize(vmin=noiselevel, vmax=noiselevel*4)
	pcm1 = ax1.pcolormesh(bs.f1, bs.f2, bs.bicohsq, norm=norm, cmap="viridis", shading="auto")
	cbar1 = fig1.colorbar(pcm1, ax=ax1, label="bicoherence^2")
	ax1.set_xlabel("Frequency x [Hz]")
	ax1.set_ylabel("Frequency y [Hz]")
	# ax.set_xscale("")
	# ax.set_yscale("")
	# ax.legend()
	fig1.suptitle(figtitle)
	fig1.tight_layout()

	fig2, ax2 = plt.subplots()
	pcm2 = ax2.pcolormesh(bs.f1, bs.f2, bs.biphase, cmap="twilight_shifted", shading="auto")
	cbar2 = fig2.colorbar(pcm2, ax=ax2, label="biphase [rad]")
	ax2.set_xlabel("Frequency x [Hz]")
	ax2.set_ylabel("Frequency y [Hz]")
	# ax.set_xscale("")
	# ax.set_yscale("")
	# ax.legend()
	fig2.suptitle(figtitle)
	fig2.tight_layout()

	# output # EDIT HERE !!
	outputs = {
		'fig1': fig1, 
		'pcm1': pcm1, 
		'cbar1': cbar1, 
		'fx': bs.f1, 
		'fy': bs.f2, 
		'fz': bs.f3, 
		'd1': bs.bicohsq, 
		'e1': bs.bicohsq_err,
		'fig2': fig2, 
		'pcm2': pcm2, 
		'cbar2': cbar2, 
		'd2': bs.biphase, 
		'e2': bs.biphase_err, 
		'NEns': bs.NEns
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig1, outdir, inputs, output_filepath, now, suffix="_bicohsq")
	system.output_fig(fig2, outdir, inputs, output_filepath, now, suffix="_biphase")
	print("DONE !!")

if __name__ == "__main__":
	main()