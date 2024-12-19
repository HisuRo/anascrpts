import numpy as np  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from scipy import signal  # type: ignore

def main():

    # FIRフィルタの設計
    fs = 10e6  # サンプリング周波数 (Hz)
    nyquist = fs / 2  # ナイキスト周波数
    low_cutoff = 150e3  # 低域カットオフ (Hz)
    high_cutoff = 1e6  # 高域カットオフ (Hz)
    num_taps = 1001  # フィルタのタップ数  filter order + 1
    # 群遅延サンプル数はfilter orderの半分

    # バンドパスFIRフィルタの設計 (firwinを使用)
    fir_filter = signal.firwin(num_taps, [low_cutoff / nyquist, high_cutoff / nyquist], pass_zero=False)

    # 周波数応答の計算
    w, h = signal.freqz(fir_filter, worN=2**14)
    freq = w * fs / (2 * np.pi)

    # 位相応答の計算
    phase = np.angle(h)

    # 群遅延の計算
    group_delay = -np.diff(np.unwrap(phase)) / np.diff(w)

    # プロット
    fig, axs = plt.subplots(3, sharex=True)
    ax1, ax2, ax3 = axs

    # 周波数応答のプロット
    ax1.plot(freq, 20 * np.log10(np.abs(h)), 'b')
    ax1.set_title('Frequency Response')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.set_ylabel('Magnitude (dB)')
    ax1.grid(True)
    ax1.set_xlim([0, fs / 2])

    # 位相応答のプロット
    ax2.plot(freq[:-1], phase[:-1], 'b')
    ax2.set_title('Phase Response')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Phase (radians)')
    ax2.grid(True)
    ax2.set_xlim([0, fs / 2])

    # 群遅延のプロット
    ax3.plot(freq[:-1], group_delay, 'b')
    ax3.set_title('Group Delay')
    ax3.set_xlabel('Frequency (Hz)')
    ax3.set_ylabel('Group Delay (samples)')
    ax3.grid(True)
    ax3.set_xlim([0, fs / 2])

    # プロットの表示
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
	main()