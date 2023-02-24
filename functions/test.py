import pychromecast

chromecasts, browser = pychromecast.get_chromecasts() # type: ignore # Get all Chromecast stations in the current WiFi network
cast = chromecasts[0] # Set current cast to first in list. TODO: Allow chromecast selection
cast.wait() # Wait for further instructions before quit

mc = cast.media_controller # Get the media controller for the current cast device
mc.play_media('http://192.168.3.31:8000/media/m.wav', 'audio/+wav') # Play song from local server (see video_manager)
mc.block_until_active() # Block the media controller from changing status until the song is playing