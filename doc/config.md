<h2 align="center">Configuration</h2>

To configure Pyamp, open the config file located at `~/.config/pyamp/config.yaml` using your favorite editor.  
<br>

### `song_format`:
The order of the variables determines how they are displayed. The available variables, for now, are:
- `title`
- `album`
- `artist`

### `run_on_song_change`:
The specified script is executed on every status change (play, pause, stop, resume), and the current status is passed as an argument.  
An [example script](https://pastebin.com/X1KveJi2) can be found at `.config/pyamp/onsongchange.sh` after installation.

### `theme`:
You can choose from the following themes:
- `main`
- `midnight_pipe`
- `metal`

### mpd connection:
If you’ve changed MPD's host and/or port in `mpd.conf`, or if you're interacting with a remote machine, make sure to update the `host` and `port` values in the configuration file as well.  
<br>

[Go Back](../README.md)
