## Development

### Set up

``` js
pip2 install vamp
pip2 install midiutil
pip2 install jams
```


- You will need to install Melodia Vamp Plugin

1. Download from https://www.upf.edu/web/mtg/melodia?p=Download%20and%20installation
2. for Mac OS: Copy all files in "MTG-MELODIA 1.0 (OSX universal).zip" to: /Library/Audio/Plug-Ins/Vamp

- Also install python-midi-master

See [experiments/README.md](experiments/README.md)

# Download Youtube Files

## as wav

``` youtube-dl https://www.youtube.com/watch?v=7Bz2E8KxedM -x --audio-format wav ```

# Harmtrace

[https://hackage.haskell.org/package/ListLike](https://hackage.haskell.org/package/ListLike)

## Haskell and Cabal

Install Haskall Platform. Note that harmtrace requires an old version of ghc

[https://www.haskell.org/platform/download/7.10.3/Haskell%20Platform%207.10.3%2064bit.pkg](https://www.haskell.org/platform/download/7.10.3/Haskell%20Platform%207.10.3%2064bit.pkg)
[https://www.haskell.org/platform/prior.html](https://www.haskell.org/platform/prior.html)

## Installation


``` sh
brew install stack
```

Make sure /Users/<user>/.stack/global-project/stack.yaml has correct resolver
```
flags: {}
extra-package-dbs: []
packages: []
extra-deps: []
resolver: ghc-7.10.3
```

``` sh
cd <harmtrace source folder>
stack solver --update-config
stack build
```

# Converting to MIDI

There are two ways to convert to MIDI
1. Waon
2. melodia

## Scripts

Scripts will convert all wav files in data/ to mid files

``` sh
python convert_wavs_to_midi.py
python convert_wavs_to_midi_waon.py
```

# Test

```
python test_midi_properties.py
```