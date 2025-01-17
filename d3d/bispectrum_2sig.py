from nasu import get_d3d, system
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
		"outdirname" : "120329_bispectrum", 
		"output_filename" : "mmspc4_mmspc3_120329_bispectrum_after_sawteeth_1ms_NFFT2=512", 
		"pointname1" : "mmspc4", 
		"pointname2" : "mmspc3", 
		"shot" : 120329, 
		"idx_startdomain_1" : 9, 
		"idx_startdomain_2" : 9, 
		"N_domains_1" : 3, 
		"N_domains_2" : 3, 
		"carrier_freq_2" : 2e6,
		"downsampling_factor_2" : 20,
		"tstart_list" : [2.0205,2.0495,2.0715,2.0905,2.1255,2.156,2.179,2.198,2.218,2.243,2.265,2.285], 
		"tend_list" : [2.0215,2.0505,2.0725,2.0915,2.1265,2.157,2.18,2.199,2.219,2.244,2.266,2.286], 
		"NFFT2" : 512,
		"ovr" : 0.5, 
		"window" : "hann", 
		"mode" : "112",
		"flim1" : 2e6, 
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
	tt1 = get_d3d.timetrace_multidomains(inputs["pointname1"],inputs["shot"],inputs["idx_startdomain_1"],inputs["N_domains_1"])
	tt2 = get_d3d.timetrace_multidomains(inputs["pointname2"], inputs["shot"], inputs["idx_startdomain_2"], inputs["N_domains_2"])
	tt2.produce_virtual_IQ_signal(inputs["carrier_freq_2"], inputs["downsampling_factor_2"])

	tw = get_d3d.twin_signals(tt1.raw.t_s, tt2.virtIQ.t_s, tt1.raw.d, tt2.virtIQ.d, tt1.raw.Fs, tt2.virtIQ.Fs)

	bs = tw.bispectrum_multiwindows(inputs["tstart_list"], inputs["tend_list"], inputs["NFFT2"], inputs["ovr"], inputs["window"], inputs['mode'], 
								 flim1=inputs['flim1'], flim2=inputs['flim2'], interpolate=inputs["interpolate"])
	noiselevel = 4. / bs.NEns

	# plot # EDIT HERE !!
	trange_str = ", ".join([f"{inputs['tstart_list'][i]}-{inputs['tend_list'][i]}s" for i in range(len(inputs["tstart_list"]))])
	figtitle = f"#{inputs['shot']}\n" \
				f"{trange_str}\n" \
				f"1: {inputs['pointname1']}\n" \
				f"2: {inputs['pointname2']}"
	fig1, ax1 = plt.subplots()
	norm = Normalize(vmin=noiselevel, vmax=noiselevel*4)
	pcm1 = ax1.pcolormesh(bs.f1, bs.f2, bs.bicohsq, norm=norm, cmap="viridis", shading="auto")
	cbar1 = fig1.colorbar(pcm1, ax=ax1, label="bicoherence^2")
	ax1.set_xlabel("Frequency [Hz]")
	ax1.set_ylabel("Frequency [Hz]")
	# ax.set_xscale("")
	# ax.set_yscale("")
	# ax.legend()
	fig1.suptitle(figtitle)
	fig1.tight_layout()

	fig2, ax2 = plt.subplots()
	pcm2 = ax2.pcolormesh(bs.f1, bs.f2, bs.biphase, cmap="twilight_shifted", shading="auto")
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