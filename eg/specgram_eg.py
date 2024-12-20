from nasu import get_eg_timetrace, system
import matplotlib.pyplot as plt # type: ignore
from matplotlib.gridspec import GridSpec # type: ignore
import numpy as np # type: ignore
import os

def main():
    # initial setting and input
    config, wd = system.check_working_directory()
    script_path = os.path.abspath(__file__)
    input_filepath, tmpdir, outdir_base = system.define_input_tmp_output_directories(script_path, config)
    inputs, outdir = system.load_input(input_filepath, outdir_base)
    now, logs = system.get_logs(wd, script_path)

    ### input file template ### EDIT HERE !!
    """ 
    {
        "outdirname" : "174070_specgram", 
        "output_filename": "fir_nel_fast_4119_174070_spectrogram", 
        "sn" : 174070,
        "subsn" : 1, 
        "tstart" : 4, 
        "tend" : 5, 
        "diagname" : "fir_nel_fast", 
        "name" : "nL(4119)", 
        "dim" : 0, 
        "other_idxs" : [0],
        "NFFT" : 1024
    }
    """
    #############

    # main # EDIT HERE !!
    tt = get_eg_timetrace.timetrace(sn=inputs["sn"], subsn=inputs["subsn"], tstart=inputs["tstart"], tend=inputs["tend"], diagname=inputs["diagname"], name=inputs["name"], dim=inputs["dim"], other_idxs=inputs["other_idxs"])
    tt.raw.specgram(NFFT=inputs["NFFT"])

    # plot # EDIT HERE !!
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 2, width_ratios=[20, 2], height_ratios=[1, 4], hspace=0.1, wspace=0.1)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(tt.raw.t_s, tt.raw.d, lw=0.1)
    ax1.set_ylabel("Signal")

    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
    pcm = ax2.pcolormesh(tt.raw.spg.t, tt.raw.spg.f, tt.raw.spg.psd.T)
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Frequency [Hz]")

    cax = fig.add_subplot(gs[1, 1])
    cbar = fig.colorbar(pcm, cax=cax, ax=ax2, label="PSD [/Hz]")

    plt.setp(ax1.get_xticklabels(), visible=False)

    fig.suptitle(f"{inputs['diagname']} {inputs['name']}\n"
                f"{inputs['sn']}-{inputs['subsn']}")
    # fig.tight_layout()

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

if __name__ == "__main__":
	main()