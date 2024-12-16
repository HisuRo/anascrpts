from nasu import get_labcom, system
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore

# initial setting and input
config, wd = system.check_working_directory()
input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
inputs, outdir = system.load_input(input_filepath, outdir_base)
now, logs = system.get_logs(wd)

### input file template ### EDIT HERE !!
""" 
{
	"outdirname" : "174070_specgram", 
	"output_filename": "highk_ch3_174070_spectrogram", 
	"sn" : 174070,
    "subsn" : 1, 
    "tstart" : 2.5, 
    "tend" : 8.5, 
    "diagname" : "MWRM-PXI", 
    "ch" : 1, 
    "NFFT" : 1024
}
"""
#############

# main # EDIT HERE !!
tt = get_labcom.timetrace(sn=inputs["sn"], subsn=inputs["subsn"], tstart=inputs["tstart"], tend=inputs["tend"], diagname=inputs["diagname"], ch=inputs["ch"])
tt.raw.specgram(NFFT=inputs["NFFT"])

# plot # EDIT HERE !!
fig, ax = plt.subplots()
pcm = ax.pcolormesh(tt.raw.spg.t, tt.raw.spg.f, tt.raw.spg.psd.T)
cbar = fig.colorbar(pcm, ax=ax)
cbar.set_label("PSD [V$^2$/Hz]")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Frequency [Hz]")
fig.suptitle(f"{inputs['diagname']} {inputs['ch']}\n"
			f"{inputs['sn']}-{inputs['subsn']}")
fig.tight_layout()

# output # EDIT HERE !!
outputs = {
	'fig': fig, 
    'pcm' : pcm, 
    'cbar' : cbar, 
    't' : tt.raw.spg.t, 
    'f' : tt.raw.spg.f, 
    'd' : tt.raw.spg.psd
}

# systematic output and close
output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
system.output_fig(fig, outdir, inputs, output_filepath, now)
print("DONE !!")
