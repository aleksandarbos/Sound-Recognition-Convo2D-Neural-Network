# Sound Recognition
## Using Neural Networks - Convolution2D

### Technical specs
Python + OpenCV 3.0 + Keras lib for Neural Networks

### Summary
The main goal this project is to recognize *(fingerprint)* short audio samples, such as short speech command, whistle, 
or any other sound from nature and map them to specific action.

### Motivation

Using sound samples for reaching your goal:
    - Sound recognition of songs *(music)* , sounds from nature, human voice
    - Using human voice for commanding smarthpone, smart vehicle during the ride
    - Can be of great use to people with major disability.

### Implemented:
    - So far, software is trained to recognize whistle melodies and short audio samples. 
    It can be easly upgraded to recognize specific types of sound.

### Further implemenation:
     - Sound recognition in real-time (not from audio samples, live recording from mic)
     - New data-sets and new training

### Screenshots:
- Main frame: <br />
 ![Alt text](/images/screenshots/mainframe.png?raw=true "Sound Recognition - GUI")

#### Simple whistle ASCENDING test:
- Application output: <br />
![Simple whistle ASC test](/images/screenshots/ascending_whistle_test.png?raw=true "Simple whistle ASC test")
- Test analyze - FFT: <br />
![Simple whistle test analyte - FFT](/images/screenshots/ascending_whistle_fft.png?raw=true "Simple whistle test analyte - FFT")
- Test analyze - Waveform: <br />
![Test analyze - Waveform](/images/screenshots/ascending_whistle_waveform.png?raw=true "Test analyze - Waveform")
- Test analyze - Spectrogram: <br />
![Simple whistle test analyte - Spectrogram](/images/screenshots/ascending_whistle_spectrogram.png?raw=true "Simple whistle test analyte - Spectrogram")
- Test analyze - Spectrogram - Black and White (ready as Neural Network input): <br />
![Simple whistle test analyte - Spectrogram BW ANN ready input](/images/screenshots/ascending_whistle_spectrogram_bw.png?raw=true "Simple whistle test analyte - Spectrogram BW ANN ready input")

### Instalation

### Licence
    - MIT

### References
[Great spectrogram article](http://www.frank-zalkow.de/en/code-snippets/create-audio-spectrograms-with-python.html) <br/ >
[University Of Novi Sad, Faculty Of Techical Scieces, AI-lab](https://github.com/ftn-ai-lab/sc-2015)
