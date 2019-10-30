# Colab Streamer

``colabsreamer`` is a Python module to allow you to create a virtual desktop inside a COLAB notebook and stream it to Twitch or Youtube.

## Disclaimer

⚠️ Still under development! Things Will Break! ⚠️

## Usage

A colab notebook with GPU is needed.

```bash
!pip install git+https://github.com/taesiri/colabstreamer
import colabstreamer
colabstreamer.config_all()
colabstreamer.stream_to_twitch('twitch_secret')
```

## remocolab

This module is heavily influenced by [remocolab](https://github.com/demotomohiro/remocolab) and share many codes with it.

## Screenshot

![glxgears](https://raw.githubusercontent.com/taesiri/colabstreamer/master/Screenshots/glxgears.png)
