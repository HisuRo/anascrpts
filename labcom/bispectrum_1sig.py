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
		"output_filename": "lowk_ch8_highk_ch3_221_4.6335-4.7s_174070", 
		"sn" : 174070, 
		"subsn" : 1, 
		"tstart_retrieve" : 4.0, 
		"tend_retrieve" : 5.0, 
		"diagname1" : "MWRM-COMB", 
		"ch1_i" : 13, 
		"ch1_q" : 14, 
		"tstart" : 4.6335, 
		"tend" : 4.7, 
		"NFFT" : 4096,
		"ovr" : 0., 
		"window" : "hann", 
		"flim" : None, 
	}
	"""
	#############

	# main # EDIT HERE !!
	tt1 = get_labcom.timetrace_iq(inputs["sn"], inputs["subsn"], inputs["tstart_retrieve"], inputs["tend_retrieve"], inputs["diagname1"], inputs["ch1_i"], inputs["ch1_q"])
	tt2 = get_labcom.timetrace_iq(inputs["sn"], inputs["subsn"], inputs["tstart_retrieve"], inputs["tend_retrieve"], inputs["diagname2"], inputs["ch2_i"], inputs["ch2_q"])
	twsigs = get_labcom.twin_signals(tt1.t_s, tt2.t_s, tt1.d, tt2.d, tt1.Fs, tt2.Fs)
	bs = twsigs.bispectrum(inputs["tstart"], inputs["tend"], inputs["NFFT2"], inputs["ovr"], inputs["window"], inputs["mode"], interpolate=inputs["interpolate"])
	noiselevel = 4. / bs.NEns

	# plot # EDIT HERE !!
	figtitle = f"#{inputs['sn']}-{inputs['subsn']} {inputs['tstart']}-{inputs['tend']}s" \
				f"mode={inputs['mode']}\n" \
				f"1: {inputs['diagname1']} {inputs['ch1_i']} {inputs['ch1_q']}\n" \
				f"2: {inputs['diagname2']} {inputs['ch2_i']} {inputs['ch2_q']}"
	fig1, ax1 = plt.subplots()
	norm = Normalize(vmin=noiselevel, vmax=noiselevel*5)
	pcm1 = ax1.pcolormesh(bs.f1, bs.f2, bs.bicohsq, norm=norm, cmap="viridis")
	cbar1 = fig1.colorbar(pcm1, ax=ax1, label="bicoherence^2")
	ax1.set_xlabel("Frequency [Hz]")
	ax1.set_ylabel("Frequency [Hz]")
	# ax.set_xscale("")
	# ax.set_yscale("")
	# ax.legend()
	fig1.suptitle(figtitle)
	fig1.tight_layout()

	fig2, ax2 = plt.subplots()
	pcm2 = ax2.pcolormesh(bs.f1, bs.f2, bs.biphase, cmap="twilight_shifted")
	cbar2 = fig2.colorbar(pcm2, ax=ax2, label="biphase [rad]")
	ax2.set_xlabel("Frequency [Hz]")
	ax2.set_ylabel("Frequency [Hz]")
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
		'd1': bs.bicohsq, 
		'fig2': fig2, 
		'pcm2': pcm2, 
		'cbar2': cbar2, 
		'd2': bs.biphase
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig1, outdir, inputs, output_filepath, now, suffix="_bicohsq")
	system.output_fig(fig2, outdir, inputs, output_filepath, now, suffix="_biphase")
	print("DONE !!")

if __name__ == "__main__":
	main()