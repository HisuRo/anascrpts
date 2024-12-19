from nasu import get_labcom, system
import matplotlib.pyplot as plt # type: ignore
from matplotlib.gridspec import GridSpec # type: ignore
import numpy as np # type: ignore

def main():
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
    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 2, width_ratios=[20, 2], height_ratios=[1, 4], hspace=0.1, wspace=0.1)

    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(tt.raw.t_s, tt.raw.d, lw=0.1)
    ax1.set_ylabel("Signal [V]")

    ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
    pcm = ax2.pcolormesh(tt.raw.spg.t, tt.raw.spg.f, tt.raw.spg.psd.T)
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Frequency [Hz]")

    cax = fig.add_subplot(gs[1, 1])
    cbar = fig.colorbar(pcm, cax=cax, ax=ax2, label="PSD [V$^2$/Hz]")

    plt.setp(ax1.get_xticklabels(), visible=False)

    fig.suptitle(f"{inputs['diagname']} {inputs['ch']}\n"
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