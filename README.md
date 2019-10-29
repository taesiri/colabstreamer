# Colab Streamer

``colabsreamer`` is a Python module to allow you to create a virtual desktop inside a COLAB notebook and stream it to Twitch or Youtube.

## Usage

A colab notebook with GPU is needed.

```bash
!pip install git+https://github.com/taesiri/colabstraemer
import colabstraemer
colabstraemer.config_all()
colabstraemer.stream_to_twitch('twitch_secret')
```

## remocolab

This module is heavily influenced by [remocolab](https://github.com/demotomohiro/remocolab) and share many codes with it.
