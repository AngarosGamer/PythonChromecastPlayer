import pychromecast
import config
import misc

def connect_chromecast():
    global cast
    chromecasts, browser = pychromecast.get_chromecasts() # type: ignore # Get all Chromecast stations in the current WiFi network
    cast = chromecasts[0] # Set current cast to first in list. TODO: Allow chromecast selection
    cast.wait() # Wait for further instructions before quit

def play_new_song(file, old = ""):
    global cast, mc
    c = config.config_setup()
    mc = cast.media_controller # Get the media controller for the current cast device
    mc.play_media(c.getLocation()+file, 'audio/+'+c.getFileType()) # Play song from local server (see video_manager)
    mc.block_until_active() # Block the media controller from changing status until the song is playing

def pause():
    global mc
    try:
        mc.pause() # Pause media output
    except:
        pass

def play():
    global mc
    try:
        mc.play() # Play / resume media output
    except:
        pass

def stop():
    global mc
    try:
        mc.stop() # Stop media output
    except:
        pass

def is_playing():
    global mc
    return (mc.status.player_state == 'playing') # Check if the media is currently playing

def volume_up():
    global cast
    cast.set_volume(cast.status.volume_level + 0.05)

def volume_down():
    global cast
    cast.set_volume(cast.status.volume_level - 0.05)