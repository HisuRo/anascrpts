# mask and linear fit to spectra, calculating powerlaw

import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
from nasu import system, get_d3d

# initial setting and input
config, wd = system.check_working_directory()
input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
inputs, outdir = system.load_input(input_filepath, outdir_base)
now, logs = system.get_logs(wd)
data_highk = system.load_pickle_data(inputs, "input_datpath_highk")
data_lowk = system.load_pickle_data(inputs, "input_datpath_lowk")

### input ### EDIT HERE !!!
""" template 
{
	"outdirname" : "120329_spectra", 
	"output_filename" : "mmspc3_mmspc4_120329_LPFed_amplitudes",  
	"input_datpath_highk" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc4_120329_LPFed_amplitude.pkl", 
	"input_datpath_lowk" : "/fusion/projects/xpsi/turbulence_and_transport/nasut/120329_spectra/mmspc3_120329_LPFed_amplitude.pkl", 
	"pointname1" : "echpwr", 
	"pointname2" : "pinj", 
	"pointname3" : "ece15", 
	"shot" : 120329, 
	"label_dat1" : "mmspc4 amplitude [a.u.]",
	"label_dat2" : "mmspc3 amplitude [a.u.]",
}
"""
#############

# main EDIT HERE !!
pech = get_d3d.timetrace(inputs["pointname1"], inputs["shot"])
pinj = get_d3d.timetrace(inputs["pointname2"], inputs["shot"])
ece = get_d3d.timetrace(inputs["pointname3"], inputs["shot"])

# plot EDIT HERE !!
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, sharex=True)
ax1.plot(data_highk["t"], data_highk["d"], c="blue")
ax1.set_ylabel(f"{inputs['label_dat1']}")
ax2.plot(data_lowk["t"], data_lowk["d"], c="red")
ax2.set_ylabel(f"{inputs['label_dat2']}")
ax3.plot(pech.t_s, pech.d, c="black")
ax3.set_ylabel(f"{inputs['pointname1']}")
ax4.plot(pinj.t_s, pinj.d, c="black")
ax4.set_ylabel(f"{inputs['pointname2']}")
ax5.plot(ece.t_s, ece.d, c="black")
ax5.set_ylabel(f"{inputs['pointname3']}")
fig.suptitle(f"{inputs['shot']}")
fig.tight_layout()

# output EDIT HERE !!
outputs = {
	"fig": fig, 
	"pt1_t" : pech.t_s, 
	"pt1_d" : pech.d, 
	"pt2_t" : pinj.t_s, 
	"pt2_d" : pinj.d, 
	"pt3_t" : ece.t_s, 
	"pt3_d" : ece.d
	}

# systematic output and close
output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
system.output_fig(fig, outdir, inputs, output_filepath, now)
print("DONE !!")
