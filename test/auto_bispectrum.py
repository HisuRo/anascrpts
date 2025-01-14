import numpy as np
from nasu import timetrace, system
import matplotlib.pyplot as plt # type: ignore
import os


def makeTestIQInputForCrossBiSpectralAnalysis_v2(f1, f2, th1, th2, dth, dts, NFFTs, NEns, NOVs, sigma, isCoupling):

	dtx, dty, dtz = dts
	NFFTx, NFFTy, NFFTz = NFFTs
	NOVx, NOVy, NOVz = NOVs

	NSampx = NEns * NFFTx - (NEns - 1) * NOVx
	ttx = np.arange(0, NSampx) * dtx
	NSampy = NEns * NFFTy - (NEns - 1) * NOVy
	tty = np.arange(0, NSampy) * dty
	NSampz = NEns * NFFTz - (NEns - 1) * NOVz
	ttz = np.arange(0, NSampz) * dtz

	xITrue = np.cos(2 * np.pi * f1 * ttx + th1)
	xQTrue = np.sin(2 * np.pi * f1 * ttx + th1)
	yITrue = np.cos(2 * np.pi * f2 * tty + th2)
	yQTrue = np.sin(2 * np.pi * f2 * tty + th2)

	noisexI = np.random.normal(0, sigma, len(ttx))
	noisexQ = np.random.normal(0, sigma, len(ttx))
	noiseyI = np.random.normal(0, sigma, len(tty))
	noiseyQ = np.random.normal(0, sigma, len(tty))
	noisezI = np.random.normal(0, sigma, len(ttz))
	noisezQ = np.random.normal(0, sigma, len(ttz))

	if isCoupling:
		th3 = th1 + th2 - dth
	else:
		th3 = np.pi * (np.repeat(np.random.uniform(-1, 1, NEns), NFFTz))
	zz = np.cos(2 * np.pi * (f1 + f2) * ttz + th3) + noisezI \
	     + 1.j * (np.sin(2 * np.pi * (f1 + f2) * ttz + th3) + noisezQ)

	xx = xITrue + noisexI + 1.j * (xQTrue + noisexQ)
	yy = yITrue + noiseyI + 1.j * (yQTrue + noiseyQ)
	xx = xx[0:NSampx]
	yy = yy[0:NSampy]

	return ttx, xx, tty, yy, ttz, zz


def main():

	# initial setting and input
		
	script_path = os.path.abspath(__file__)
	inputs, tmpdir, outdir, logs, now = system.initial_setting(script_path=script_path)
		
		

	### input file template ### EDIT HERE !!
	""" 
	{
		"outdirname" : "test//auto_bispectrum", 
		"output_filename": "auto_bispectrum", 
		"f1" : 200e3, 
		"f2" : 10e3,
		"th1" : 0,
		"th2" : 0,
		"dth" : 0.7853981633974483,
		"dt" : 1e-6,
		"NFFT" : 256,
		"NEns" : 100,
		"NOV" : 128,
		"sigma" : 0.1,
		"isCoupling" : true
	}
	"""
	#############

	# main # EDIT HERE !!
	f1 = inputs["f1"]
	f2 = inputs["f2"]
	th1 = inputs["th1"]
	th2 = inputs["th2"]
	dth = inputs["dth"]
	dt = inputs["dt"]
	NFFT  = inputs["NFFT"]
	NEns = inputs["NEns"]
	NOV = inputs["NOV"]
	sigma = inputs["sigma"]	
	isCoupling = inputs["isCoupling"]

	ttx, xx, tty, yy, ttz, zz = makeTestIQInputForCrossBiSpectralAnalysis_v2(f1, f2, th1, th2, dth, [dt, dt, dt], [NFFT, NFFT, NFFT], NEns, [NOV, NOV, NOV], sigma, isCoupling)

	signal = xx + yy + zz

	sig = timetrace.signal(ttx, signal, 1 / dt)
	bs = sig.bispectrum(tstart=ttx[0], tend=ttx[-1], NFFT=NFFT, ovr=0.5, window="hamming", flim=None)
	bsat = sig.bispectum_at_f(f2, fix_var="f2")
		
	fig1, ax1 = plt.subplots()
	pcm1 = ax1.pcolormesh(bs.f1, bs.f2, bs.bicohsq)
	cbar1 = fig1.colorbar(pcm1, ax=ax1, label="bicoherence^2")
	ax1.set_xlabel("Frequency 1 [Hz]")
	ax1.set_ylabel("Frequency 2 [Hz]")
	fig1.tight_layout()
		
	fig2, ax2 = plt.subplots()
	pcm2 = ax2.pcolormesh(bs.f1, bs.f2, bs.biphase, cmap="twilight_shifted")
	cbar2 = fig2.colorbar(pcm2, ax=ax2, label="biphase [rad]")
	ax2.set_xlabel("Frequency 1 [Hz]")
	ax2.set_ylabel("Frequency 2 [Hz]")
	fig2.tight_layout()

	fig3, axs3 = plt.subplots(2, sharex=True)
	axs3[0].errorbar(bsat.f1, bsat.bicohsq, bsat.bicohsq_err, ecolor="grey")
	axs3[0].hlines(4 / NEns, bsat.f1[0], bsat.f1[-1], color="grey", linestyle="--")
	axs3[0].set_ylabel("Bi-coherence^2")

	axs3[1].errorbar(bsat.f1, bsat.biphase, bsat.biphase_err, ecolor="grey")
	axs3[1].set_ylim(-np.pi, np.pi)
	axs3[1].set_ylabel("Phase [rad]")
	axs3[1].set_xlabel("Frequency 1 [Hz]")

	fig3.suptitle(f"f2={f2} Hz")
	fig3.tight_layout()


	fig4, ax4 = plt.subplots()
	ax4.plot(ttx, np.real(xx * yy), label="x(f1) * y(f2)")
	ax4.plot(ttz, np.real(zz), label="z(f3)")
	ax4.set_xlabel("Time [s]")
	ax4.set_ylabel("Amplitude")
	ax4.legend()
	fig4.tight_layout()
		
	# output # EDIT HERE !!
	outputs = {
		'fig1': fig1, 
		'f1': bs.f1, 
		'f2': bs.f2, 
		'bicohsq': bs.bicohsq, 
		'fig2': fig2, 
		'biphase': bs.biphase, 
		'fig3': fig3, 
		'bicohsq_at': bsat.bicohsq,
		'bicohsq_err_at': bsat.bicohsq_err,
		'biphase_at': bsat.biphase,
		'biphase_err_at': bsat.biphase_err,
		'fig4': fig4, 
		't': ttx,
		'x': xx,
		'y': yy,
		'z': zz, 
	}

	# systematic output and close
	output_filepath = system.output_pickle_file(outputs, inputs, logs, outdir)
	system.output_fig(fig1, outdir, inputs, output_filepath, now, suffix="_bicohsq")
	system.output_fig(fig2, outdir, inputs, output_filepath, now, suffix="_biphase")
	system.output_fig(fig3, outdir, inputs, output_filepath, now, suffix="_at")
	system.output_fig(fig4, outdir, inputs, output_filepath, now, suffix="_signal")
	print("DONE !!")

if __name__ == "__main__":
    main()