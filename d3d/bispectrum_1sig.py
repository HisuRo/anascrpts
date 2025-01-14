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
		"output_filename" : "mmspc4_120329_bispectrum", 
		"pointname" : "mmspc4", 
		"shot" : 120329, 
		"idx_startdomain" : 9, 
		"N_domain" : 3, 
		"tstart_list" : [4.6335, 4.7335], 
		"tend_list" : [4.7314, 4.8], 
		"NFFT" : 512,
		"ovr" : 0.5, 
		"window" : "hann", 
		"flim" : 0
	}
	"""
	#############

	# main # EDIT HERE !!
	if inputs["flim"] == 0:
		inputs["flim"] = None
	tt = get_d3d.timetrace_multidomains(inputs["pointname"],inputs["shot"],inputs["idx_startdomain"],inputs["N_domains"])
	bs = tt.raw.bispectrum_multiwindows(inputs["tstart_list"], inputs["tend_list"], inputs["NFFT"], inputs["ovr"], inputs["window"], flim=inputs['flim'])
	noiselevel = 4. / bs.NEns

	# plot # EDIT HERE !!
	trange_str = ", ".join([f"{inputs['tstart_list'][i]}-{inputs['tend_list'][i]}s" for i in range(len(inputs["tstart_list"]))])
	figtitle = f"#{inputs['shot']}\n" \
				f"{trange_str}\n" \
				f"{inputs['pointname']}"
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