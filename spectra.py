import os
from nasu import get_d3d, proc, system
import pickle
import matplotlib.pyplot as plt # type: ignore
import sys
from datetime import datetime

wd = "~/analysis_scripts"
cwd = os.getcwd()
if cwd != wd:
	raise Exception("change working directory to analysis_scripts!!")

now = datetime.now()

tmpdir = "/local-scratch/nasut"
proc.ifNotMake(tmpdir)

### input ###
inputs = {
	'pointname': "mmspc4", 
	'shot': 120329, 
	'idx_startdomain': 9, 
	'N_domain': 8, 
	"tstart1": 2.0, 
	"tend1": 2.3, 
	"tstart2": 2.3, 
	"tend2": 2.6, 
	"tstart3": 2.6, 
	"tend3": 2.9, 
	"tstart4": 2.9, 
	"tend4": 3.2
}
#############

### log #####
logs = {
	'script': {sys.argv[0]}, 
	'analsis_scripts_gitid': {system.get_commit_id(wd)}, 
	'nasu_gitid': {system.get_commit_id("nasu")}, 
	'datetime': {now}
}
#############

highk = get_d3d.timetrace_multidomains(inputs['pointname'], inputs["shot"], inputs["idx_startdomain"], inputs["N_domain"])

sp1 = highk.raw(highk).spectrum(inputs["tstart1"], inputs["tend1"])
sp2 = highk.raw(highk).spectrum(inputs["tstart2"], inputs["tend2"])
sp3 = highk.raw(highk).spectrum(inputs["tstart3"], inputs["tend3"])
sp4 = highk.raw(highk).spectrum(inputs["tstart4"], inputs["tend4"])

# plot
fig, ax = plt.subplots()
ax.plot(sp1.f, sp1.psd, label=f"{inputs["tstart1"]} - {inputs["tend1"]} s")
ax.plot(sp2.f, sp2.psd, label=f"{inputs["tstart2"]} - {inputs["tend2"]} s")
ax.plot(sp3.f, sp3.psd, label=f"{inputs["tstart3"]} - {inputs["tend3"]} s")
ax.plot(sp4.f, sp4.psd, label=f"{inputs["tstart4"]} - {inputs["tend4"]} s")
ax.set_xlabel("Frequency [Hz]")
ax.set_ylabel("PSD [dB]")
ax.set_xscale("log")
ax.set_yscale("log")
ax.legend()
fig.suptitle(f"{inputs["pointname"]} {inputs["shot"]}")
fig.tight_layout()

# output
outputs = {
	'fig': fig, 
	'f1': sp1.f, 
	'psd1': sp1.psd, 
	'f2': sp2.f, 
	'psd2': sp2.psd, 
	'f3': sp3.f, 
	'psd3': sp3.psd, 
	'f4': sp4.f, 
	'psd4': sp4.psd
}
outputs.update(inputs)
outputs.update(logs)

with open("mmspc4_120329_spectra.pkl", "wb") as f:
	pickle.dump(outputs, f)

with open("mmspc4_120329_spectra.pkl", "rb") as f:
	loaded_fig = pickle.load(f)

loaded_fig.show()
