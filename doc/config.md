## Configuration
Pyamp's configuration file is located at `~/.config/pyamp/config.yaml`.

### `song_format`:
The order of the variables determines how they are displayed. The available variables, for now, are:
- `title`
- `album`
- `artist`

### `run_on_song_change`:
The specified script is executed on every status change (play, pause, stop, resume), and the current status is passed as an argument.  
An [example script](../src/resources/onsongchange.sh) can be found at `.config/pyamp/onsongchange.sh` after installation.

### `theme`:
You can choose from the following themes:
- `main`
- `midnight_pipe`
- `metal`

### `host` and `port`:
If you’ve changed MPD's host and/or port in `mpd.conf`, or if you're interacting with a remote machine, make sure to update the `host` and `port` values in the configuration file as well.  
<br>

[Go Back](../README.md)
