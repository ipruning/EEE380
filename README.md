# EEE380

## 0. Table of Contents

- [EEE380](#eee380)
    - [0. Table of Contents](#0-table-of-contents)
    - [1. Background](#1-background)
        - [1.0 Install](#10-install)
        - [1.1 Usage of the algorithm part](#11-usage-of-the-algorithm-part)
        - [1.2 Usage of the hardware part](#12-usage-of-the-hardware-part)
        - [1.3 Name Convention](#13-name-convention)
    - [2. Architecture](#2-architecture)
        - [2.0 Overview](#20-overview)
        - [2.1 Class](#21-class)
    - [3. License](#3-license)
    - [4. External Link](#4-external-link)
    - [5. ChangeLog](#5-changelog)

## 1. Background

### 1.0 Install

- Clone GitHub Repository `git clone git@github.com:Spehhhhh/EEE380.git`
- Switch to the directory `cd EEE231`

### 1.1 Usage of the algorithm part

```bash
# This project uses pipenv to manage the virtual environment.

# Install Poetry
$ curl -sSL https://install.python-poetry.org | python3 -

# Set environment variables
$ echo 'export PATH="$HOME/.poetry/bin:$PATH"' >> ~/.zshrc

# Install package
$ poetry install

# Activate the virtual environment for the current project
$ poetry shell

# Generate lockfile
$ poetry lock --no-update

# Run the main program
$ poetry run python <files>
```

```bash
# MacBook M1 Only
# install pyaudio
brew install portaudio
python -m pip install --global-option='build_ext' --global-option='-I/opt/homebrew/Cellar/portaudio/19.7.0/include' --global-option='-L/opt/homebrew/Cellar/portaudio/19.7.0/lib' pyaudio
# install vosk-api
./scripts/vosk-macos.sh 
```

```python
# python3.10/site-packages/speech_recognition/__init__.py
# install vosk-api
def recognize_vosk(self, audio_data, language='en'):
    from vosk import KaldiRecognizer, Model

    assert isinstance(audio_data, AudioData), "Data must be audio data"

    if not hasattr(self, 'vosk_model'):
        if not os.path.exists("model"):
            return "Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder."
            exit (1)
        self.vosk_model = Model("model")

    rec = KaldiRecognizer(self.vosk_model, 16000);

    rec.AcceptWaveform(audio_data.get_raw_data(convert_rate=16000, convert_width=2));
    finalRecognition = json.loads(rec.FinalResult())
    if finalRecognition['text'] == '' :
        return ''
    else:
        return finalRecognition['text']
```

### 1.2 Usage of the hardware part

1. Install PlatformIO Core `http://docs.platformio.org/page/core.html`
2. Download development platform with examples `https://github.com/platformio/platform-atmelavr/archive/develop.zip>`
3. Extract ZIP archive
4. Run these commands:

```bash

# Change directory
$ cd <path>

# Build project
$ platformio run

# Upload firmware
$ platformio run --target upload

# Build specific environment
$ platformio run -e uno

# Upload firmware for the specific environment
$ platformio run -e uno --target upload

# Clean build files
$ platformio run --target clean
```

### 1.3 Name Convention

- Class Naming Convention: `CapWords`
- Class Member Convention: `lower_with_under_`
- Function Naming Convention: `lower_with_under()`
- Variables Naming Convention: `lower_with_under`

## 2. Architecture

### 2.0 Overview

TODO

### 2.1 Class

TODO

## 3. License

[GNU General Public License v3.0](LICENSE)

## 4. External Link

TODO

## 5. ChangeLog

- 220109 init
