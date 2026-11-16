# Hearing Structure: Speech, Spectra, and Audio Learning

Source: https://ml-biomat.com/tutorials/machine-learning/m20/en/
Language: en

From a tone to an utterance: connect sampling, sound events, recognition, synthesis, and separation.

## 1. One recording can answer several different questions

When a doorbell rings, we identify the event before deciding whether to open the door. In a meeting, we need both the words and the identity of the speaker. In music, we follow melody, rhythm, and individual instruments. These activities begin with sound but correspond to different learning tasks. Audio classification labels an entire recording; sound event detection also locates its beginning and end. Automatic speech recognition produces text, speaker diarization asks who spoke when, and text-to-speech synthesis produces a waveform from text. Choosing the question first determines the required labels and what counts as a useful answer.

A microphone records a changing signal rather than directly reporting meanings such as “cat” or “turn left.” Sound passes through a room, reflections, background noise, and a recording device before being sampled and quantized. A change in the waveform may reflect the spoken content, but it may also reflect distance, volume, or microphone response. A model that recognizes training recordings in one room can lose its basis for prediction in another. Audio learning therefore combines a careful representation of signals with experiments that distinguish information about content from information about the recording conditions.

We start with generated sounds that can be heard, plotted, and checked numerically. A small spectrogram classifier tests the value of retaining temporal structure rather than averaging it away. Two signals in separate frequency bands are then mixed and separated with an explicit frequency rule, allowing listening to be compared with signal-to-noise measurements. Speech recognition, synthesis, and speaker analysis build on that signal-processing foundation. Their inputs, outputs, training information, and evaluation criteria are explained individually. The generated sweeps test these computational steps without requiring linguistic background or pretending that a tone classifier already recognizes speech.

## 2. Turn continuous vibration into a sequence of numbers

An analog signal changes continuously, while a digital recording measures it at regularly spaced instants. A sample rate of 8000 Hz means 8000 values per second, giving 16000 samples for two seconds of mono audio. A 440 Hz sinusoid completes 440 cycles per second; its amplitude describes the size of its oscillation. Frequency, sample rate, and amplitude answer different questions. Uncalibrated digital amplitudes are usually expressed relative to a numerical full-scale range. A recorded value of 0.5 therefore does not identify a universal sound pressure or perceived loudness.

$$
t_n=\frac{n}{f_s},\qquad x[n]=A\sin(2\pi f_0t_n+\phi),\qquad N=f_sT
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/c5fb7428d211201250c2723f.svg) | Integer sample index starting at zero. |
| ![Formula](https://ml-biomat.com/static/agent-math/a7fe25f77889bee1430ff4c0.svg) | Sample rate in Hz, or samples per second. |
| ![Formula](https://ml-biomat.com/static/agent-math/af73c71154f6f0e1e155cc73.svg) | Time of sample n and recording duration, in seconds. |
| ![Formula](https://ml-biomat.com/static/agent-math/4137d12b0e3cd75eb27ad555.svg) | Sample and amplitude, in common relative amplitude units. |
| ![Formula](https://ml-biomat.com/static/agent-math/36617854c069c6f283a50186.svg) | Sinusoid frequency, in Hz. |
| ![Formula](https://ml-biomat.com/static/agent-math/e8ea4606e878cd1dc5ff695b.svg) | Initial phase in radians; trigonometric arguments are dimensionless. |
| ![Formula](https://ml-biomat.com/static/agent-math/54c5f8946c55301722df6f6e.svg) | Integer sample count; duration times sample rate is assumed integral. |

Sampling f_s times per second gives an interval 1/f_s. Substituting these instants into a continuous sinusoid produces its digital sequence. At 8000 Hz the interval is 0.125 ms and a two-second recording has 16000 samples. With frequency 1000 Hz, amplitude one, and phase zero, the first five samples are 0, sqrt(2)/2, 1, sqrt(2)/2, and 0: eight samples per cycle. Frequency times time is dimensionless, and multiplication by 2π expresses the accumulated phase.

Under band-limiting and related reconstruction conditions, the sample rate must exceed twice the highest signal frequency to identify the signal uniquely within the band. Sampling at 8000 Hz folds components above 4000 Hz into lower frequencies. For example, samples of a 5000 Hz cosine at that rate are identical to samples of a 3000 Hz cosine. The numbers alone no longer reveal which analog signal was present. Before reducing a sample rate, an antialiasing filter removes components outside the new supported band. Merely dropping selected samples does not perform correct resampling.

These constraints have been central to telephone and recording technology: transmission and storage bandwidth are limited, while listeners still need sufficient information to understand speech. Digital signal processing made sound a repeatable computational object and enabled systematic comparisons of features and recognition methods. End-to-end networks can now accept raw waveforms, but sample rate, bandwidth, and quantization still determine what they receive. Playing a recording made at 16 kHz as though it were sampled at 8 kHz changes both duration and pitch. Editing the sample-rate label is not the same operation as resampling the signal.

Channels also carry information. Stereo recordings can contain spatial cues, and arrival-time differences between microphones can help locate a source. Averaging channels produces one signal but can weaken out-of-phase components and discard spatial structure. Decide whether the task needs that information and record channel order and synchronization. Our single-channel examples isolate temporal and spectral structure. Amplitudes use a common relative scale, and the exported listening examples share the same playback gain, preserving their amplitude relationships instead of normalizing each processed result independently.

## 3. A spectrogram unfolds frequency through time

A Fourier transform of a whole recording describes which frequencies are present but mixes together their order of occurrence. The short-time Fourier transform, or STFT, analyzes a short window and then moves that window through the recording. Its output is a complex matrix indexed by frequency and window position. Each entry contains magnitude and phase. Displaying magnitude or power as color produces a spectrogram. A rising sweep makes an upward-sloping bright trace, while a falling sweep makes a downward-sloping trace. Averaging over time can make their frequency distributions similar while removing the direction that distinguishes them.

$$
X_{k,m}=\frac{1}{S_w}\sum_{n=0}^{N_w-1}x[n+mH]w[n]e^{-2\pi\mathrm{i}kn/N_w},\qquad S_w=\sum_{n=0}^{N_w-1}w[n],\qquad f_k=\frac{kf_s}{N_w}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/d0993be952e6f796d152c613.svg) | Input samples in relative amplitude units; zeros extend the boundaries. |
| ![Formula](https://ml-biomat.com/static/agent-math/c098f70b11f917194ff6ac69.svg) | Dimensionless Hann-window weights and their sum. |
| ![Formula](https://ml-biomat.com/static/agent-math/166403f5e6eb7bbd6158cb63.svg) | Window length and hop in sample counts; positive integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/e5657cfd582d156d8f6302a7.svg) | Within-window sample index, frequency-bin index, and frame index; integers. |
| ![Formula](https://ml-biomat.com/static/agent-math/f30e943e4d67119e11eb027d.svg) | Imaginary unit with square −1; the complex exponential combines sine and cosine projections. |
| ![Formula](https://ml-biomat.com/static/agent-math/b46603b01976eb1afd77ef4f.svg) | Complex coefficient at bin k and frame m, normalized by the window sum and in input amplitude units. |
| ![Formula](https://ml-biomat.com/static/agent-math/05efcb9156fe14780eed3c07.svg) | Sample rate and frequency of bin k, both in Hz. |

Window the segment and project it onto oscillating basis functions to obtain local frequency content. Real signals need only nonnegative frequencies, so 256 samples give 129 bins. At 8000 Hz the spacing is 31.25 Hz and bin 16 is 500 Hz. A hop of 64 analyzes the signal every 8 ms. The code pads half a window on both sides, aligning frame timestamps with original-signal centers; sample indexing in this expression refers to the padded array. Dividing by the window sum separates coefficient amplitude from window length.

Window length determines the observation scale. At 8000 Hz, a 256-sample window covers 32 ms and gives a frequency-bin spacing of 31.25 Hz. Moving the window by 64 samples gives an 8 ms hop. A longer window helps distinguish nearby frequencies but spreads brief changes over a longer interval. A shorter hop samples the time axis more densely without shortening the underlying analysis window. Zero padding draws the spectrum on a denser frequency grid but does not create new resolving power. A Hann window softens the edges to reduce spectral leakage caused by abrupt truncation, while also affecting the main-lobe width.

$$
D_{k,m}=20\log_{10}\frac{|X_{k,m}|}{A_{\rm ref}},\qquad P_{b,m}=\sum_k B_{b,k}|X_{k,m}|^2,\qquad \operatorname{mel}(f)=2595\log_{10}\left(1+\frac{f}{700\,\mathrm{Hz}}\right)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b46603b01976eb1afd77ef4f.svg) | Complex STFT coefficient; its magnitude is in relative amplitude units. |
| ![Formula](https://ml-biomat.com/static/agent-math/89d8b2e252400f4fafdbec52.svg) | Integer frequency-bin, frame, and Mel-band indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/6cfa31659fe18d2711f8738c.svg) | Positive reference amplitude, in the same units as X. |
| ![Formula](https://ml-biomat.com/static/agent-math/2171c3b4ff2a63fc599e89e0.svg) | Level relative to the reference amplitude, in dB. |
| ![Formula](https://ml-biomat.com/static/agent-math/a1e55881cda008514a87fa9a.svg) | Dimensionless weight of Mel filter b at bin k. |
| ![Formula](https://ml-biomat.com/static/agent-math/b9733ff69a26642e8c62ed40.svg) | Aggregated squared magnitude, in squared relative amplitude units. |
| ![Formula](https://ml-biomat.com/static/agent-math/3fc10fc0b5bd7fa3b82fd22f.svg) | Physical frequency f is in Hz; Mel is the HTK perceptual coordinate used here. |

A logarithm acts on a dimensionless ratio, so amplitude is divided by a reference with matching units. An amplitude ratio of one half gives about −6.02 dB; 10 log10 of the corresponding squared-amplitude ratio one quarter gives the same result. Mel aggregation weights nearby powers: values 4 and 1 with weights 0.5 and 1 produce a band value 3. A frequency of 1000 Hz is approximately 1000 mel. Network features use a natural logarithm after a numerical floor, whereas plotted decibels use base-ten logarithms.

A decibel display compresses large intensity differences so that weaker harmonics remain visible, but its reference must be stated. An amplitude ratio uses 20 times a logarithm; a power ratio uses 10 times a logarithm. Halving amplitude gives approximately −6.02 dB. If every spectrogram is normalized to its own maximum, colors compare internal structure but do not compare absolute strength across recordings. Our classification examples use individual peak references. The separation experiment uses one shared reference. Colorbars and captions preserve that distinction, identifying exactly which comparisons the display supports.

A Mel filter bank aggregates linear-frequency power into perceptually arranged bands that are denser at low frequencies and wider at high frequencies. Each triangular filter takes a weighted sum of nearby spectral powers; taking logarithms gives the familiar log-Mel representation. It retains spectral envelopes useful for speech, but it is not lossless: frequency aggregation discards detail, and power discards phase. The code constructs 32 continuous triangular filters with apex value one, sampled directly at discrete frequency bins without renormalizing their sampled peaks or areas. When comparing implementations, check the Mel convention, normalization, window settings, and reference values together. Equal array shapes do not establish equal representations.

![Waveforms and linear-frequency spectra for three held-out examples. Each spectrum uses its own peak as 0 dB, with 256-sample windows, 64-sample hops, and 8000 Hz sampling. Trace direction distinguishes rising and falling sweeps.](https://ml-biomat.com/static/tutorials/machine-learning/figures/e3ebb96541e8e0f472d5d9a0.svg?v=e3ebb96541e8)

Figure 1Waveforms and linear-frequency spectra for three held-out examples. Each spectrum uses its own peak as 0 dB, with 256-sample windows, 64-sample hops, and 8000 Hz sampling. Trace direction distinguishes rising and falling sweeps.

## 4. Classify a recording, then locate events inside it

A clip classifier can process a log-Mel spectrogram with convolutions that detect harmonics, frequency slopes, or short bursts before combining them into class probabilities. Our three classes are a steady tone, a rising sweep, and a falling sweep. Each recording lasts 0.6 seconds, with variation in frequency, initial phase, and noise. Recordings within one condition group share a simple device gain and adjacent-sample response. Training, validation, and testing use different condition groups, preventing an identical device profile from appearing in both training and testing. These groups represent generated recording conditions; they are not described as real human speakers.

Event detection adds temporal localization. If a ten-second recording contains speech and two doorbell events, the label “contains a doorbell” is insufficient. A model can output probabilities for several events at each short-time frame, then apply thresholds, minimum durations, and interval merging to produce event segments. Overlapping sounds require independent multilabel outputs rather than forcing every frame into exactly one class. Weak supervision provides only recording-level labels and requires a mechanism for pooling local evidence into a clip decision. Event boundaries that were never supplied during training should not be treated as available reference annotations.

Streaming introduces an additional constraint: delay. A prediction using two seconds of future context requires waiting two seconds before producing the corresponding result. Causal convolutions, limited right context, and chunked attention offer different accuracy and latency tradeoffs. Event-detection evaluation should state onset and offset tolerances, missed events, false alarms, and duration-matching rules. For monitoring alarms in long recordings, false alarms per hour may describe operational cost better than clip accuracy. These definitions belong in the task design because they determine which kind of error the model should reduce.

## 5. Speech and text do not arrive with frame-by-frame alignment

Two people can say the same greeting at different speeds, and either may prolong the final sound. Speech-recognition datasets often contain recordings and transcripts without exact labels for the acoustic frames corresponding to each character. Earlier hidden Markov model systems represented pronunciation through states and temporal transitions, combining acoustic likelihoods, pronunciation dictionaries, and language models. Alignment became part of probabilistic inference. Neural networks later took over much of acoustic modeling, and end-to-end methods learned increasingly direct mappings from sound to symbol sequences. The alignment problem remained; new objectives expressed it in different ways.

CTC predicts a character or subword at each input frame and adds a special blank symbol. To turn a frame path into a transcript, first merge adjacent repeated symbols and then remove blanks. For example, A, A, blank, A becomes AA. Removing blanks before merging would incorrectly produce just A. Training does not select one required alignment: it sums the probabilities of all paths that collapse to the correct transcript. Output order advances monotonically with input time, and repeated output characters require an intervening blank. Dynamic programming accumulates shared prefixes efficiently rather than enumerating exponentially many complete paths.

$$
p(Y\mid X)=\sum_{\pi:\,\mathcal B(\pi)=Y}\prod_{t=1}^{T}p_t(\pi_t\mid X),\qquad \mathcal L_{\rm CTC}=-\log p(Y\mid X)
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/a28e27b5a4ff6fb1a8387994.svg) | Input acoustic-frame sequence and target token sequence; the token sequence is usually shorter. |
| ![Formula](https://ml-biomat.com/static/agent-math/4130b90d370e23b5f3efe091.svg) | Frame count and integer frame index. |
| ![Formula](https://ml-biomat.com/static/agent-math/4c7b7b1118bfe7ed2694035e.svg) | Length-T frame path including blanks, and its token at frame t. |
| ![Formula](https://ml-biomat.com/static/agent-math/bad201494f63e5f5cf85c962.svg) | Collapse operation: merge adjacent repeats first, then remove blanks. |
| ![Formula](https://ml-biomat.com/static/agent-math/af9a87107fc3edc86391c888.svg) | Dimensionless token probability at frame t conditioned on the acoustic input. |
| ![Formula](https://ml-biomat.com/static/agent-math/1ac183623433bd322ce4dd9d.svg) | Transcript probability and negative natural-log loss; probability is dimensionless and loss is in nats. |

Multiply frame probabilities within a path under the CTC factorization, then sum mutually exclusive paths. With A probabilities 0.6,0.5,0.7, AA has just the path A–blank–A and probability 0.21. The empty transcript has probability 0.4×0.5×0.3=0.06. The remaining six paths collapse to A, totaling 0.73 and giving loss −ln(0.73), approximately 0.315. The acoustic encoder can use temporal context; this output factorization does not assert that raw acoustic frames are independent.

The greedy path, obtained by choosing the largest probability at each frame, can differ from the most likely transcript. Our example has just three frames and two symbols, blank and A, so all eight paths can be listed. The greedy path collapses to AA, but the combined probability of paths collapsing to A is 0.73, exceeding the probability 0.21 for AA. The second frame has a tie, and the script consistently selects the first symbol, blank, making the greedy procedure explicit. This demonstrates why decoding is more than selecting the largest number in each column. Beam search preserves several candidate prefixes to approximate more of the sequence probability.

![Frame-token probabilities and transcript probabilities after summing all eight paths. Greedy decoding chooses blank at the second-frame tie and outputs AA, while A has the largest complete transcript probability, 0.73.](https://ml-biomat.com/static/tutorials/machine-learning/figures/20d8daf3e92f5eabcff1c589.svg?v=20d8daf3e92f)

Figure 2Frame-token probabilities and transcript probabilities after summing all eight paths. Greedy decoding chooses blank at the second-frame tie and outputs AA, while A has the largest complete transcript probability, 0.73.

## Eight acoustic paths, three possible transcripts

Set the probability of A at each frame; the blank probability is its complement. Each path merges adjacent repeats before dropping blanks. The right panel sums paths with the same transcript, comparing greedy decisions with sequence-level decisions. Greedy ties select blank.

[Figure: Eight CTC paths and summed transcript probabilities](https://ml-biomat.com/tutorials/machine-learning/m20/en/#M20-svg)

An encoder–decoder recognizer organizes the problem differently. An encoder represents the acoustic sequence, and a decoder generates text using both previously emitted text and attention to the acoustic representation. CTC's factorization across frame outputs differs from an autoregressive decoder's dependence on text history, affecting alignment, streaming, and linguistic constraints. The original Whisper study trained a system on large quantities of multilingual, multitask audio with transcripts, illustrating the effect of supervision breadth on transfer. When using such models, evaluate transcription, translation, timestamps, and silence separately rather than combining different output tasks into one score.

$$
\mathrm{WER}=\frac{S+D+I}{N_{\rm ref}}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/1e2e153d47e5fe74ff1b2e08.svg) | Substitution, deletion, and insertion counts in a minimum-edit alignment from reference to recognized transcript. |
| ![Formula](https://ml-biomat.com/static/agent-math/28343a0bbc49a01e2b8450a5.svg) | Positive reference word count. |
| ![Formula](https://ml-biomat.com/static/agent-math/506ac9a8622bbafd87956531.svg) | Dimensionless word error rate; multiply by 100 for percent. Many insertions can make it exceed one. |

For reference “turn left at next street” and recognition “turn right at the next street,” left is substituted by right and the is inserted. The five-word reference gives WER=(1+0+1)/5=0.4. The denominator remains the reference length rather than changing to the recognized length after insertions. Corpus WER commonly sums edits and reference words before division; this differs from an unweighted average of sentence-level WERs because sentences have different lengths.

Word error rate first finds a minimum-edit alignment between the reference and recognized transcript, then counts substitutions, deletions, and insertions. Character error rate is often appropriate for character-based comparisons, including some Chinese settings, but segmentation rules must still be stated. Normalizing case, punctuation, and number spellings changes the score. Speaker-disjoint evaluation tests new speakers, whereas recording-environment splits test devices and noise conditions. Adjacent chunks from one long recording should remain in the same partition. Useful error analysis returns to individual utterances to distinguish proper names, accent variation, noise, and clipped audio boundaries.

## 6. Generate speech through pronunciation, prosody, and a vocoder

Text-to-speech begins with text, but the text does not specify every property of the sound. Ambiguous pronunciations, abbreviation expansion, pauses, and emphasis all affect the result. A text front end can normalize numbers and symbols and convert text to characters or phonemes. An acoustic model then predicts representations such as duration, fundamental frequency, energy, or a Mel spectrogram. Two versions of a sentence may contain the same phonemes while placing different emphasis on its message. Prosody is therefore part of how the acoustic sequence unfolds through time, not an optional decoration added after synthesis.

The original Tacotron 2 work connected a character-to-Mel sequence predictor with a WaveNet vocoder that generates waveforms from those spectrograms. The first stage specifies the evolving acoustic envelope and alignment; the second supplies the detailed waveform needed for playback. A Mel power representation does not retain full phase, so reversing the colors of a spectrogram cannot recover the original signal. A vocoder learns a conditional waveform distribution. Other synthesis systems explicitly predict phoneme durations or use diffusion and flow methods to generate acoustic representations, while still addressing the relationship between text, timing, and sound.

HiFi-GAN combines waveform generation with multiple discriminators, including discriminators that examine structure at different periods. Voiced speech contains recurring, approximately periodic patterns, and a smooth average spectrum alone may not preserve their natural detail. Adversarial, feature-matching, and spectral objectives constrain different aspects of the output while the generator upsamples its Mel conditioning into a high-rate waveform. Vocoder evaluation should report quality, speed, and the relationship between test conditioning and training conditioning. Processing a measured spectrogram and processing one predicted by an upstream acoustic model can expose the vocoder to different error distributions.

Listening studies require stable comparison conditions. Sentence content, playback level, headphones, and presentation order affect judgments; randomized ordering and anonymous samples reduce some of those influences. Mean opinion scores summarize ratings but should be accompanied by the rating scale, listener count, language experience, and sample composition. Scores from two studies need not represent the same listening test. Spectral distances or intelligibility metrics can help locate errors but do not fully replace listening for naturalness, pronunciation, and prosody. Multispeaker synthesis should also distinguish content accuracy, voice similarity, and prosodic control rather than treating them as one attribute.

## 7. Extract a target from a mixture and inspect what was removed

A microphone usually receives several sources together. Denoising aims to retain a target while suppressing interference; source separation seeks multiple individual outputs. If target and interference occupy separate frequency bands, a frequency mask demonstrates the mechanism directly: retain the target band, suppress other bands, and reconstruct a waveform. Our target contains components at 440 Hz and 880 Hz, while interference sweeps upward from 1300 Hz. Retaining frequencies below 1000 Hz therefore has an explicit basis. Two real speakers commonly overlap in the same bands, where this rule cannot separate their contributions.

$$
\hat S_{k,m}=M_{k,m}X_{k,m},\qquad \hat s=\operatorname{ISTFT}(\hat S),\qquad \mathrm{SNR}=10\log_{10}\frac{\sum_n s[n]^2}{\sum_n(\hat s[n]-s[n])^2}
$$

| Symbol | Meaning and units |
| --- | --- |
| ![Formula](https://ml-biomat.com/static/agent-math/b46603b01976eb1afd77ef4f.svg) | Complex mixture spectrum, in amplitude units. |
| ![Formula](https://ml-biomat.com/static/agent-math/60e1d12d4350594a5b98bbbc.svg) | Dimensionless frequency or time-frequency mask; one at frequencies up to 1000 Hz and zero elsewhere here. |
| ![Formula](https://ml-biomat.com/static/agent-math/b162864974e72484bd9eaf9d.svg) | Estimated target spectrum, in amplitude units. |
| ![Formula](https://ml-biomat.com/static/agent-math/ecbd8a3ba1b2757fa6521b98.svg) | Integer frequency-bin, frame, and sample indices. |
| ![Formula](https://ml-biomat.com/static/agent-math/ef3728d51aa7279137439047.svg) | Inverse short-time transform using matching windows and overlap weights. |
| ![Formula](https://ml-biomat.com/static/agent-math/72e299742b02f1bf993be8a6.svg) | Known target and estimated waveform, in amplitude units, with aligned time and sample rate. |
| ![Formula](https://ml-biomat.com/static/agent-math/33105f45313029a217dc86e7.svg) | Target-to-error energy ratio expressed in dB. |

A zero mask suppresses a coefficient, while a value one retains the mixture coefficient. Inverse frames are windowed, overlap-added, and normalized by the corresponding sum of squared windows. Target energy 100 and error energy 10 give SNR 10 dB; reducing error energy to one gives 20 dB. Matching squared-amplitude units cancel before taking the logarithm. This reference-waveform calculation penalizes both residual interference and target loss; it is not scale-invariant SI-SDR.

A learned separator can predict time-frequency masks, complex spectra, or time-domain waveforms. Training must state how reference sources were obtained. When several output sources have no fixed ordering, permutation-invariant training chooses the lowest loss across assignments between outputs and references, avoiding a penalty for correctly separated sources returned in a different order. Reusing mixture phase makes mask reconstruction straightforward but introduces phase-related limits. Complex-spectrum or waveform prediction takes on more of the reconstruction problem. Multiple microphones additionally provide arrival-time and spatial-covariance information that can combine spatial filtering with learned representations.

Music also benefits from representations matched to its structure. The uniformly spaced STFT supports straightforward signal calculations. A constant-Q representation uses approximately logarithmic frequency spacing that relates naturally to musical intervals. Chroma pools the same pitch class across octaves, helping some harmony tasks while discarding octave information. Beat and onset analysis concern when energy changes; melody and multipitch estimation concern which fundamental frequencies are present together. Instrument separation should inspect residual interference, missing target components, and newly introduced artifacts rather than relying only on overall amplitude error. A representation should preserve the distinctions required by the task.

The three examples below are two-second, 8000 Hz, 16-bit mono WAV files written with a shared gain. The first contains a two-frequency target with a smooth envelope. The second adds a sweeping interferer and white noise. The third retains STFT coefficients below 1000 Hz and reconstructs the signal. Listen for the interference, then locate its retained and suppressed regions in the spectrogram. Shared gain preserves amplitude relationships across processing stages. Keeping player volume consistent makes the numerical comparison easier to relate to the audible difference.

Target: generated 440 Hz and 880 Hz components, 8000 Hz sample rate, 2 seconds.

Target audio

Mixture: target, an interferer rising from 1300 Hz, and white noise, with shared playback gain.

Mixed audio

Band estimate: retain STFT coefficients below 1000 Hz and reconstruct by overlap-add.

Estimated target audio

![Top: waveform detail from 0.80–0.84 seconds with a shared amplitude range. Bottom: full two-second spectra with a shared decibel reference. Targets are 440 and 880 Hz; interference lies above 1300 Hz. The mask also retains noise inside the target band.](https://ml-biomat.com/static/tutorials/machine-learning/figures/4665298e82a18d24cba6117a.svg?v=4665298e82a1)

Figure 3Top: waveform detail from 0.80–0.84 seconds with a shared amplitude range. Bottom: full two-second spectra with a shared decibel reference. Targets are 440 and 880 Hz; interference lies above 1300 Hz. The mask also retains noise inside the target band.

## 8. Run the experiment, then connect it to speaker representations

The script implements sampling, Hann-window STFT, a 32-band Mel filter bank, convolutional classification, frequency masking, inverse reconstruction, and an exactly enumerable CTC example. Recording-condition groups provide 120 training clips, 36 validation clips, and 48 test clips. A small two-convolution network selects its checkpoint by validation cross entropy. A second baseline averages log-Mel features over time and fits logistic regression. Both use the same partitions, creating a specific comparison: after temporal structure is removed, how reliably can a predictor still identify sweep direction?

### From waveforms to classification, separation, and CTC probabilities

Generates short audio without downloading weights. Saves playable WAV files, numerical arrays, four bilingual figure groups, and summary.json using two CPU threads.

```
"""Generated audio: time-frequency analysis, classification, masks, and exact CTC."""
import argparse,copy,itertools,json
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix
import torch
from torch import nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

torch.set_num_threads(2)
FS=8000;NFFT=256;HOP=64;DURATION=.6

def stft(x,nfft=NFFT,hop=HOP):
    window=np.hanning(nfft+1)[:-1]
    padded=np.pad(x,(nfft//2,nfft//2+(-len(x))%hop))
    frames=np.lib.stride_tricks.sliding_window_view(padded,nfft)[::hop]
    return np.fft.rfft(frames*window,axis=1).T/window.sum()

def istft(z,length,nfft=NFFT,hop=HOP):
    window=np.hanning(nfft+1)[:-1];frames=np.fft.irfft(z.T,n=nfft,axis=1)*window.sum()
    out=np.zeros((len(frames)-1)*hop+nfft);weight=np.zeros_like(out)
    for i,frame in enumerate(frames):
        out[i*hop:i*hop+nfft]+=frame*window;weight[i*hop:i*hop+nfft]+=window**2
    out=np.divide(out,weight,out=np.zeros_like(out),where=weight>1e-12)
    return out[nfft//2:nfft//2+length]

def mel_filters(count=32):
    hz=np.fft.rfftfreq(NFFT,1/FS)
    mel=lambda x:2595*np.log10(1+x/700)
    points=700*(10**(np.linspace(mel(0),mel(FS/2),count+2)/2595)-1)
    filters=[]
    for left,mid,right in zip(points[:-2],points[1:-1],points[2:]):
        filters.append(np.maximum(0,np.minimum((hz-left)/(mid-left),(right-hz)/(right-mid))))
    return np.array(filters),points[1:-1]

BANK,CENTERS=mel_filters()
def feature(x):return np.log(np.maximum(BANK@abs(stft(x))**2,1e-8)).astype(np.float32)

def dataset(groups,snr=None):
    signals=[];labels=[];groupids=[]
    time=np.arange(int(FS*DURATION))/FS
    for group in groups:
        profile=np.random.default_rng(2000+group);echo=profile.uniform(-.25,.25);gain=profile.uniform(.7,1.3)
        for label in range(3):
            for repeat in range(4):
                rng=np.random.default_rng(10000+group*100+label*10+repeat)
                low=rng.uniform(300,600);high=rng.uniform(1200,1700);phase=rng.uniform(0,2*np.pi)
                if label==0:f0=f1=rng.uniform(650,950)
                elif label==1:f0,f1=low,high
                else:f0,f1=high,low
                phase_t=2*np.pi*(f0*time+(f1-f0)/(2*DURATION)*time**2)+phase
                clean=np.sin(phase_t)*np.sin(np.pi*time/DURATION)**2
                clean=gain*(clean+echo*np.r_[0,clean[:-1]])
                level=rng.uniform(5,25) if snr is None else snr
                noise=np.random.default_rng(90000+group*100+label*10+repeat).normal(size=len(clean))
                noise*=np.sqrt(np.mean(clean**2)/(10**(level/10)*np.mean(noise**2)))
                signals.append(clean+noise);labels.append(label);groupids.append(group)
    return np.array(signals),np.array(labels),np.array(groupids)

class AudioCNN(nn.Module):
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Conv2d(1,8,3,padding=1),nn.ReLU(),nn.MaxPool2d(2),nn.Conv2d(8,16,3,padding=1),nn.ReLU(),nn.AdaptiveAvgPool2d((4,4)),nn.Flatten(),nn.Linear(256,3))
    def forward(self,x):return self.net(x)

def collapse(path):
    return ''.join(c for i,c in enumerate(path) if c!='_' and (i==0 or c!=path[i-1]))

def edit_distance(ref,hyp):
    d=np.zeros((len(ref)+1,len(hyp)+1),int);d[:,0]=np.arange(len(ref)+1);d[0,:]=np.arange(len(hyp)+1)
    for i in range(1,len(ref)+1):
        for j in range(1,len(hyp)+1):d[i,j]=min(d[i-1,j]+1,d[i,j-1]+1,d[i-1,j-1]+(ref[i-1]!=hyp[j-1]))
    return int(d[-1,-1])

def run(out,language):
    out.mkdir(parents=True,exist_ok=True);zh=language=='zh';text=lambda z,e:z if zh else e
    plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','axes.unicode_minus':False})
    save=lambda fig,name:(fig.savefig(out/f'{name}-{language}.svg',bbox_inches='tight'),fig.savefig(out/f'{name}-{language}.png',dpi=140,bbox_inches='tight'),plt.close(fig))
    waves,y,g=dataset(range(17));features=np.array([feature(w) for w in waves]);train=g<10;valid=(g>=10)&(g<13);test=g>=13
    mean=features[train].mean();std=features[train].std();inputs=torch.tensor((features-mean)/std)[:,None];targets=torch.tensor(y)
    torch.manual_seed(20);model=AudioCNN();optimizer=torch.optim.Adam(model.parameters(),lr=.002);trace=[];best=float('inf');selected=0
    trainids=np.flatnonzero(train)
    for epoch in range(35):
        model.train();order=torch.randperm(len(trainids));total=0
        for ids in order.split(24):
            ix=trainids[ids.numpy()];optimizer.zero_grad();loss=nn.functional.cross_entropy(model(inputs[ix]),targets[ix]);loss.backward();optimizer.step();total+=loss.item()*len(ix)
        model.eval()
        with torch.no_grad():vl=nn.functional.cross_entropy(model(inputs[valid]),targets[valid]).item()
        trace.append((total/train.sum(),vl))
        if vl<best:best=vl;weights=copy.deepcopy(model.state_dict());selected=epoch+1
    model.load_state_dict(weights);model.eval()
    torch.save({'model':model.state_dict(),'mean':float(mean),'std':float(std)},out/'audio-model.pt')
    (out/'model.json').write_text(json.dumps({'class':'AudioCNN','classes':['steady','rising','falling'],'sample_rate_hz':FS,'window_samples':NFFT,'hop_samples':HOP,'mel_filters':32,'selected_epoch':selected,'mean':float(mean),'std':float(std)},indent=2),encoding='utf-8')
    saved=torch.load(out/'audio-model.pt',weights_only=True);reloaded=AudioCNN();reloaded.load_state_dict(saved['model']);reloaded.eval()
    restored_inputs=torch.tensor((features[test]-saved['mean'])/saved['std'])[:,None]
    with torch.no_grad():reload_error=float((model(inputs[test])-reloaded(restored_inputs)).abs().max())
    with torch.no_grad():prob=model(inputs[test]).softmax(1).numpy()
    pred=prob.argmax(1);cm=confusion_matrix(y[test],pred,labels=range(3))
    baseline=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000));baseline.fit(features[train].mean(2),y[train]);baseline_accuracy=float(baseline.score(features[test].mean(2),y[test]))
    levels=[20,5,-5];noise_acc=[]
    for level in levels:
        ww,yy,_=dataset(range(13,17),level);ff=np.array([feature(w) for w in ww]);xx=torch.tensor((ff-mean)/std)[:,None]
        with torch.no_grad():pp=model(xx).argmax(1).numpy()
        noise_acc.append(float(np.mean(pp==yy)))
    t=np.arange(2*FS)/FS;envelope=np.sin(np.pi*t/2)**2
    clean=envelope*(.65*np.sin(2*np.pi*440*t)+.2*np.sin(2*np.pi*880*t));interference=.65*envelope*np.sin(2*np.pi*(1300*t+250*t*t))
    noise=np.random.default_rng(77).normal(0,.12,len(t));mixture=clean+interference+noise
    z=stft(mixture);freq=np.fft.rfftfreq(NFFT,1/FS);mask=(freq<=1000).astype(float)[:,None]
    estimate=istft(z*mask,len(t));reconstructed=istft(z,len(t));reconstruction_error=float(abs(reconstructed-mixture).max())
    snr=lambda estimate:float(10*np.log10(np.sum(clean**2)/np.sum((estimate-clean)**2)))
    shared_gain=.85/max(np.max(abs(x)) for x in [clean,mixture,estimate])
    for name,w in [('clean',clean),('mixture',mixture),('filtered',estimate)]:wavfile.write(out/(name+'.wav'),FS,np.int16(np.clip(w*shared_gain,-1,1)*32767))
    ctc_prob=np.array([[.4,.6],[.5,.5],[.3,.7]]);sequences={}
    for path in itertools.product(range(2),repeat=3):
        output=collapse(''.join('_A'[k] for k in path));p=float(np.prod([ctc_prob[i,k] for i,k in enumerate(path)]));sequences[output]=sequences.get(output,0)+p
    greedy=collapse(''.join('_A'[k] for k in ctc_prob.argmax(1)))
    ref='turn left at next street'.split();hyp='turn right at the next street'.split();ed=edit_distance(ref,hyp)
    summary={'sample_rate_hz':FS,'window_samples':NFFT,'hop_samples':HOP,'frequency_bin_hz':FS/NFFT,'split_clips':[int(train.sum()),int(valid.sum()),int(test.sum())],'group_overlap':len(set(g[train])&set(g[test])),'selected_epoch':selected,'cnn_test_accuracy':float(np.mean(pred==y[test])),'time_averaged_baseline_accuracy':baseline_accuracy,'confusion_matrix':cm.tolist(),'noise_levels_db':levels,'noise_accuracy':noise_acc,'stft_reconstruction_max_error':reconstruction_error,'input_snr_db':snr(mixture),'filtered_snr_db':snr(estimate),'ctc_sequence_probabilities':sequences,'ctc_greedy_output':greedy,'wer_edit_distance':ed,'wer_reference_words':len(ref),'wer':ed/len(ref),'audio_duration_seconds':len(t)/FS,'audio_shared_gain':float(shared_gain)}
    summary['reload_logits_error']=reload_error
    (out/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    np.savez_compressed(out/'data.npz',waveforms=waves,labels=y,groups=g,features=features,probabilities=prob,trace=trace,clean=clean,mixture=mixture,estimate=estimate,ctc_prob=ctc_prob)
    assert reconstruction_error<1e-10;assert abs(sum(sequences.values())-1)<1e-12;assert abs(sequences['AA']-.21)<1e-12;assert ed==2
    names=[text('恒定音调','Steady tone'),text('上升扫频','Rising sweep'),text('下降扫频','Falling sweep')]
    fig,axs=plt.subplots(2,3,figsize=(12,5.6),gridspec_kw={'height_ratios':[.7,1.4]},layout='constrained')
    for c in range(3):
        idx=np.flatnonzero((y==c)&test)[0];wave=waves[idx];spec=stft(wave);db=20*np.log10(np.maximum(abs(spec),1e-8)/np.max(abs(spec)))
        axs[0,c].plot(np.arange(len(wave))/FS,wave,lw=.35,color='#4d6575');axs[0,c].set(title=names[c],xlabel=text('时间 / s','Time / s'),ylabel=text('振幅','Amplitude'))
        im=axs[1,c].pcolormesh(np.arange(spec.shape[1])*HOP/FS,freq,db,cmap='magma',vmin=-65,vmax=0,shading='auto',rasterized=True);axs[1,c].set(ylim=(0,2500),xlabel=text('时间 / s','Time / s'),ylabel=text('频率 / Hz','Frequency / Hz'))
    fig.colorbar(im,ax=axs[1,:],label=text('相对峰值 / dB','Relative to each peak / dB'));save(fig,'representations')
    fig,axs=plt.subplots(1,3,figsize=(12,3.7),layout='constrained');tr=np.array(trace)
    axs[0].plot(np.arange(1,36),tr[:,0],label=text('训练','Train'),color='#176b91');axs[0].plot(np.arange(1,36),tr[:,1],label=text('验证','Validation'),color='#bc5549');axs[0].set(xlabel=text('轮数','Epoch'),ylabel=text('交叉熵','Cross entropy'));axs[0].legend()
    im=axs[1].imshow(cm,cmap='Blues',vmin=0,vmax=16);axs[1].set(xticks=range(3),yticks=range(3),xticklabels=names,yticklabels=names,xlabel=text('预测类别','Predicted'),ylabel=text('实际类别','True'));axs[1].tick_params(axis='x',labelrotation=25)
    for i in range(3):
        for j in range(3):axs[1].text(j,i,str(cm[i,j]),ha='center',va='center',color='white' if cm[i,j]>8 else '#18384d')
    axs[2].plot(levels,noise_acc,'o-',color='#176b91');axs[2].axhline(1/3,color='#8e9ba3',ls='--',label=text('随机机会 1/3','Chance 1/3'));axs[2].set(xticks=levels,ylim=(0,1.05),xlabel=text('输入信噪比 / dB','Input SNR / dB'),ylabel=text('正确率','Accuracy'));axs[2].legend();save(fig,'classification')
    fig,axs=plt.subplots(2,3,figsize=(12,5.8),layout='constrained');refamp=max(abs(stft(w)).max() for w in [clean,mixture,estimate])
    for j,(name,w)in enumerate([(text('目标声','Target'),clean),(text('混合声','Mixture'),mixture),(text('频带估计','Band estimate'),estimate)]):
        segment=(t>=.8)&(t<.84)
        axs[0,j].plot(t[segment],w[segment],lw=.8,color=['#176b91','#8c6e99','#2b897a'][j]);axs[0,j].set(title=name,xlabel=text('时间 / s','Time / s'),ylabel=text('振幅','Amplitude'),ylim=(-1.5,1.5))
        zz=stft(w);im=axs[1,j].pcolormesh(np.arange(zz.shape[1])*HOP/FS,freq,20*np.log10(np.maximum(abs(zz),1e-8)/refamp),vmin=-65,vmax=0,cmap='magma',shading='auto',rasterized=True);axs[1,j].set(xlabel=text('时间 / s','Time / s'),ylabel=text('频率 / Hz','Frequency / Hz'),ylim=(0,2500))
    fig.colorbar(im,ax=axs[1,:],label=text('共享参考 / dB','Shared reference / dB'));save(fig,'separation')
    fig,axs=plt.subplots(1,2,figsize=(10,3.2),layout='constrained');im=axs[0].imshow(ctc_prob.T,cmap='Blues',vmin=0,vmax=1,aspect='auto')
    axs[0].set(xticks=range(3),xticklabels=[1,2,3],yticks=[0,1],yticklabels=[text('空白','Blank'),'A'],xlabel=text('声学帧','Acoustic frame'),title=text('每帧输出概率','Frame probabilities'))
    for i in range(3):
        for j in range(2):axs[0].text(i,j,f'{ctc_prob[i,j]:.1f}',ha='center',va='center',color='white' if ctc_prob[i,j]>.55 else '#18384d')
    axs[1].bar([text('空序列','Empty'),'A','AA'],[sequences[''],sequences['A'],sequences['AA']],color=['#9daab1','#176b91','#bf7444']);axs[1].set(ylim=(0,1),ylabel=text('所有路径求和后的概率','Probability summed over paths'),title=text('最可能的路径不等于最可能的转写','Best path differs from best transcript'));save(fig,'ctc')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('output'));p.add_argument('--language',choices=['zh','en'],default='en');a=p.parse_args();run(a.output,a.language)
```

The audio-model.pt checkpoint stores the selected CNN weights and training-set mean and standard deviation; model.json records sampling and feature settings. Normalizing test features with those saved values and loading a fresh AudioCNN reproduces logits exactly, preserving the training input scale for subsequent inference.

In this seeded run, the convolutional classifier correctly labels all 48 test recordings, while the time-averaged baseline reaches accuracy 0.6875. Keeping test signal parameters fixed and adding noise at 20, 5, and −5 dB gives CNN accuracies 1.0, 1.0, and 0.3333. The strong low-noise result and deterioration under stronger noise should be read together. Training noise ranges from 5 to 25 dB, whereas −5 dB changes the input conditions. This controlled experiment shows when the spectral traces supporting the prediction become obscured by noise.

![Measured training and validation cross entropy, count confusion matrix for 48 test clips from held-out condition groups, and accuracy with changed noise SNR on fixed test signal parameters. The dashed line is chance for three balanced classes.](https://ml-biomat.com/static/tutorials/machine-learning/figures/81de55a240bf2da045e225e8.svg?v=81de55a240bf)

Figure 4Measured training and validation cross entropy, count confusion matrix for 48 test clips from held-out condition groups, and accuracy with changed noise SNR on fixed test signal parameters. The dashed line is chance for three balanced classes.

The separation example has input SNR approximately −0.329 dB and an estimated-target SNR approximately 13.869 dB. These values compare each output against the known target waveform using samplewise error energy, answering how well this particular frequency-band example recovers its target. Reconstructing the unmasked STFT gives a maximum error of about 6.66×10⁻¹⁶, checking the window and overlap-add implementation. The script also verifies that all CTC transcript probabilities sum to one and computes a transcript with one substitution and one insertion, giving WER 2/5=0.4.

For measured speech, self-supervised representations can learn from recordings without transcripts. Wav2vec 2.0 masks parts of a latent acoustic representation and uses a contrastive task with quantized targets before adapting to recognition with transcribed examples. Speaker representations instead emphasize properties that persist across different utterances by one person. Embedding distances support verification, while clustering can organize segments from a long recording. Identification asks who a person is, verification asks whether two recordings match, and diarization also recovers speaking times and handles overlapping speech. Their reference labels and error counts are different.

A diarization pipeline often combines voice-activity detection, local embeddings, clustering, and temporal-boundary refinement. Its evaluation should state whether overlapping speech is counted, whether boundary collars allow timing tolerance, and how missed speech, false speech detections, and speaker confusion contribute. Splitting by person, removing duplicates by recording source, and preserving sample-rate, preprocessing, and model versions connects results to genuinely new recording conditions. Waveforms, spectra, text, and identity representations now form a coherent chain. The next model choice becomes clearer when its retained information and required reference answers are specified first.

[Download complete code and data](https://ml-biomat.com/static/tutorials/machine-learning/downloads/M20.zip)

Extract and follow the README; the code matches this chapter.

## References and further reading

1. [librosa — Using display.specshow](https://librosa.org/doc-playground/main/auto_examples/plot_display.html)

   Displaying time, frequency, and decibel references.
2. [SciPy STFT documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.stft.html)

   Windows, boundaries, amplitude scaling, and reconstruction conditions.
3. [Connectionist Temporal Classification](https://www.cs.toronto.edu/~graves/icml_2006.pdf)

   Original CTC paper: alignment marginalization and training.
4. [Sequence Modeling With CTC](https://distill.pub/2017/ctc/)

   Open visual explanation of collapsing, dynamic programming, and decoding.
5. [SpeechBrain — Speech Recognition From Scratch](https://speechbrain.readthedocs.io/en/latest/tutorials/tasks/speech-recognition-from-scratch.html)

   Open pipeline from acoustic input to encoder–decoder models and beam search.
6. [Robust Speech Recognition via Large-Scale Weak Supervision](https://arxiv.org/abs/2212.04356)

   Original Whisper study of multilingual and multitask supervision.
7. [Natural TTS Synthesis by Conditioning WaveNet on Mel Spectrogram Predictions](https://arxiv.org/abs/1712.05884)

   Acoustic prediction and vocoding in Tacotron 2.
8. [HiFi-GAN](https://arxiv.org/abs/2010.05646)

   Original waveform generation research emphasizing periodic structure.
9. [wav2vec 2.0](https://arxiv.org/abs/2006.11477)

   Masked latent representations and contrastive pretraining.
