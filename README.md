[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/SudoFoundry/Aura) [![License: GPL](https://img.shields.io/badge/License-GPL-green.svg)](https://opensource.org/licenses/GPL-3.0)

# Aura

![decoded image](https://i.imgur.com/ieySLgV.png)

Aura is a lightweight python script that decodes analog Automatic Picture Transmission (APT) signals from the National Oceanic and Atmospheric Administration's (NOAA) weather satellites.

## Nature of NOAA Satellite Broadcast

NOAA satellite broadcast transmissions are composed of two image channels, telemetry information, and synchronization data, with the image channels typically referred to as Video A and Video B. All this data is transmitted as a horizontal scan line. A complete line is 2080 pixels long, with each image using 909 pixels and the remainder going to the telemetry and synchronization. Lines are transmitted at 2 per second, which equates to a 4160 words per second, or 4160 baud.

On NOAA Polar-orbiting Operational Environmental Satellite (POES) system satellites, the two images are 4 km/pixel smoothed 8-bit images derived from two channels of the advanced very-high-resolution radiometer (AVHRR) sensor. The images are corrected for nearly constant geometric resolution prior to being broadcast; as such, the images are free of distortion caused by the curvature of the Earth.

Of the two images, one is typically long-wave infrared (10.8 micrometers) with the second switching between near-visible (0.86 micrometers) and mid-wave infrared (3.75 micrometers) depending on whether the ground is illuminated by sunlight. However, NOAA can configure the satellite to transmit any two of the AVHRR's image channels.

Included in the transmission are a series of synchronization pulses, minute markers, and telemetry information.

The synchronization information, transmitted at the start of each video channel, allows the receiving software to align its sampling with the baud rate of the signal, which can vary slightly over time. The minute markers are four lines of alternating black then white lines which repeat every 60 seconds (120 lines).

The telemetry section is composed of sixteen blocks, each 8 lines long, which are used as reference values to decode the image channels. The first eight blocks, called "wedges," begin at 1/8 max intensity and successively increase by 1/8 to full intensity in the eighth wedge, with the ninth being zero intensity. Blocks ten through fifteen each encode a calibration value for the sensor. The sixteenth block identifies which sensor channel was used for the preceding image channel by matching the intensity of one of the wedges one through six. Video channel A typically matches either wedge two or three, channel B matches wedge four.

The first fourteen blocks should be identical for both channels. The sixteen telemetry blocks repeat every 128 lines, and these 128 lines are referred to as a frame.

The signal itself is a 256-level amplitude modulated 2400Hz subcarrier, which is then frequency modulated onto the 137 MHz-band RF carrier. Maximum subcarrier modulation is 87% (±5%), and overall RF bandwidth is 34 kHz. On NOAA POES vehicles, the signal is broadcast at approximately 37dBm (5 watts) effective radiated power.

An APT signal is continuously broadcast, with reception beginning at the start of the next line when the receiver is within radio range. Images can be received in real-time by relatively unsophisticated, inexpensive receivers during the time the satellite is within radio range, which typically lasts 8 to 15 minutes.

## Pre-requisites

- This repository
- Python 3.7.7
- NumPy
- SciPy
- Pillow (Python Imaging Library)

## Useage

Clone or download this repository and execute the following command in the terminal with this repository being the current working directory.

```bash
python decoder.py [path to wav file — relative to the script] [path to output image file — relative to the script]
```

## Tested Operating Systems

- macOS 10.15
- macOS 10.14
- macOS 10.13.6

## License

Licensed under [GNU General Public License v3.0](https://github.com/SudoFoundry/Aura/blob/master/LICENSE).
