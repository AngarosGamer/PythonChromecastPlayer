import pychromecast
import config
import misc
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

def connect_chromecast():
    global cast
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Getting chromecast")
    chromecasts, browser = pychromecast.get_chromecasts() # type: ignore # Get all Chromecast stations in the current WiFi network
    cast = chromecasts[0] # Set current cast to first in list. TODO: Allow chromecast selection
    cast.wait() # Wait for further instructions before quit

def play_new_song(file, old = ""):
    global cast, mc
    c = config.config_setup()
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Playing new song from file {file}")
    mc = cast.media_controller # Get the media controller for the current cast device
    mc.play_media(c.getLocation()+file, 'audio/+'+c.getFileType()) # Play song from local server (see video_manager)
    mc.block_until_active() # Block the media controller from changing status until the song is playing

def pause():
    global mc
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Trying to pause music")
    try:
        mc.pause() # Pause media output
    except:
        print(f"{Fore.YELLOW}Warning :{Style.RESET_ALL} Unable to pause music")
        pass

def play():
    global mc
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Trying to play music")
    try:
        mc.play() # Play / resume media output
    except:
        print(f"{Fore.YELLOW}Warning :{Style.RESET_ALL} Unable to play music")
        pass

def stop():
    global mc
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Trying to stop music")
    try:
        mc.stop() # Stop media output
    except:
        print(f"{Fore.YELLOW}Warning :{Style.RESET_ALL} Unable to stop music")
        pass

def is_playing():
    global mc
    return (mc.status.player_state == 'playing') # Check if the media is currently playing

def volume_up():
    global cast
    cast.set_volume(cast.status.volume_level + 0.05)
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Setting volume up to {cast.status.volume_level}")

def volume_down():
    global cast
    cast.set_volume(cast.status.volume_level - 0.05)
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Setting volume down to {cast.status.volume_level}")