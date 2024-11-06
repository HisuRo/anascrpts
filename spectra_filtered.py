from nasu import get_d3d, system, calc
import matplotlib.pyplot as plt # type: ignore

# initial setting and input
config, wd = system.check_working_directory()
input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(wd, config)
inputs, outdir = system.load_input(input_filepath, outdir_base)
now, logs = system.get_logs(wd)

### input file template ### EDIT HERE !!
""" 
{
	"outdirname" : "120329_spectra", 
	"output_filename": "mmspc4_120329_filtered_spectra", 
	"pointname" : "mmspc4", 
	"shot" : 120329, 
	"idx_startdomain" : 9, 
	"N_domain" : 8, 
	"tstart1" : 2.0, 
	"tend1" : 2.3, 
	"tstart2" : 2.3, 
	"tend2" : 2.6, 
	"tstart3" : 2.6, 
	"tend3" : 2.9, 
	"tstart4" : 2.9, 
	"tend4" : 3.2, 
	"fpass_low" : 150e3, 
	"fpass_high" : 1e6, 
	"fstop_low" : 100e3, 
	"fstop_high" : 2e6
}
"""
#############

# main # EDIT HERE !!
highk = get_d3d.timetrace_multidomains(inputs['pointname'], inputs["shot"], inputs["idx_startdomain"], inputs["N_domain"])
highk_filt = calc.bandPass(highk.d, highk.Fs, fp=[inputs["fpass_low"], inputs["fpass_high"]], fs=[inputs["fstop_low"], inputs["fstop_high"]])

sp1 = calc.spectrum(highk.t_s, highk_filt, highk.Fs, inputs["tstart1"], inputs["tend1"], NFFT=2**14)
sp2 = calc.spectrum(highk.t_s, highk_filt, highk.Fs, inputs["tstart2"], inputs["tend2"], NFFT=2**14)
sp3 = calc.spectrum(highk.t_s, highk_filt, highk.Fs, inputs["tstart3"], inputs["tend3"], NFFT=2**14)
sp4 = calc.spectrum(highk.t_s, highk_filt, highk.Fs, inputs["tstart4"], inputs["tend4"], NFFT=2**14)

# plot # EDIT HERE !!
fig, ax = plt.subplots()
ax.plot(sp1.f, sp1.psd, label=f"{inputs['tstart1']} - {inputs['tend1']} s")
ax.plot(sp2.f, sp2.psd, label=f"{inputs['tstart2']} - {inputs['tend2']} s")
ax.plot(sp3.f, sp3.psd, label=f"{inputs['tstart3']} - {inputs['tend3']} s")
ax.plot(sp4.f, sp4.psd, label=f"{inputs['tstart4']} - {inputs['tend4']} s")
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("PSD [V^2/Hz]")
ax.set_xscale("log")
ax.set_yscale("log")
ax.legend()
fig.suptitle(f"{inputs['pointname']} {inputs['shot']}")
fig.tight_layout()

fig2, ax2 = plt.subplots()
ax2.plot(highk.t_s, highk_filt)
ax2.set_xlabel("Time [s]")
ax2.set_ylabel("Obsrerved electric field [V]")
fig2.suptitle(f"{inputs['pointname']} {inputs['shot']}")
fig2.tight_layout()

# output # EDIT HERE !!
outputs = {
	'fig': fig, 
	'f1': sp1.f, 
	'psd1': sp1.psd, 
	'f2': sp2.f, 
	'psd2': sp2.psd, 
	'f3': sp3.f, 
	'psd3': sp3.psd, 
	'f4': sp4.f, 
	'psd4': sp4.psd, 
	"fig2": fig2, 
	"t": highk.t_s, 
	"highk_filt": highk_filt
}

# systematic output and close
output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
system.output_fig(fig, outdir, inputs, output_filepath, now)
print("DONE !!")