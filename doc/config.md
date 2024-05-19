
<h2 align="center">Configuration</h2>

With your favorite editor, edit the config file found at ~/.config/pyamp/config.yaml.<br>

__song_format__:<br>
The order of the variables alters the order they're displayed, the available vars, for now, are:<br>
	 - title<br>
	 - album<br>
	 - artist<br>

__run_on_song_change__:<br>
the specified script is ran at every status change (play, pause, stop resume), and the status is passed as an argument.<br>
an [example script](https://pastebin.com/X1KveJi2) is located at .config/pyamp/onsongchange.sh after installation.<br>
remember to change the user in the default value to your actual user.

__theme__:<br>
you can change between the following themes:<br>
main<br>
midnight_pipe<br>
metal<br>

__Mpd Connection__:<br>
And also, if you changed mpd's host and/or port in mpd.conf, make sure to change it here too. <br>

[Go Back](../README.md)