### MADE BY ANGAROS - CREATIVE COMMONS : 08/10/2022 (DD/MM/YYY)
### Libraries used were not made by me, but brought to use by free licenses

# Imports
from os import kill, system
import sys
import chromecast_functions
import download_manager
import config
import tkinter
import trackQueue
import customtkinter
from threading import Thread
import time
import misc
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()

def initialise_window(c, queue):
    global pb, url_entry, total_length, current_length, pause_button, queueFrame
    player = customtkinter.CTkFrame(master=root, width=800)
    player.grid(column=0, row=0, pady=12, padx=10)

    queueFrame = customtkinter.CTkFrame(master=root, width=600)
    queueFrame.grid(column=1, row=0, pady=12, padx=10)

    url_label = customtkinter.CTkLabel(master=player, text="Enter Song URL: ")
    url_label.configure(wraplength=200, justify="center")
    url_label.grid(pady=12, padx=10)

    url_entry = customtkinter.CTkEntry(master=player, width=780, placeholder_text="https://youtube.com/example")
    url_entry.configure()
    url_entry.bind('<Return>', lambda x: initiate_process(url_entry.get()))
    url_entry.grid(pady=12, padx=10)

    playback = customtkinter.CTkFrame(master=player)
    playback.grid(pady=12, padx=10)

    stop_button = customtkinter.CTkButton(playback, text = "Stop",command=stop_media,
    border_width=2,
    corner_radius=20,
    border_color= c.getAccent(),
    hover_color=c.getAccent(),
    bg_color='transparent',
    fg_color='transparent')
    stop_button.grid(row=0, column=0, pady=12, padx=10)

    pause_button = customtkinter.CTkButton(playback, text = "Pause",command=pause_media,
    border_width=2,
    corner_radius=20,
    border_color= c.getAccent(),
    hover_color=c.getAccent(),
    bg_color='transparent',
    fg_color='transparent')
    pause_button.grid(row=0, column=1, pady=12, padx=10)

    play_button = customtkinter.CTkButton(playback, text = "Play",
    border_width=2,
    corner_radius=20,
    border_color= c.getAccent(),
    hover_color=c.getAccent(),
    bg_color='transparent',
    fg_color='transparent',
    command = lambda : play_media(url_entry.get(), queue))
    play_button.grid(row=0, column=2, pady=12, padx=10)

    volume = customtkinter.CTkFrame(master=player)
    volume.grid(pady=12, padx=10)
    
    volume_down_button = customtkinter.CTkButton(volume, text = "VDOWN",command=volume_down,
    border_width=2,
    corner_radius=20,
    border_color= c.getAccent(),
    hover_color=c.getAccent(),
    bg_color='transparent',
    fg_color='transparent')
    volume_down_button.grid(row=0, column=0, pady=12, padx=10)

    volume_up_button = customtkinter.CTkButton(volume, text = "VUP",command=volume_up,
    border_width=2,
    corner_radius=20,
    border_color= c.getAccent(),
    hover_color=c.getAccent(),
    bg_color='transparent',
    fg_color='transparent')
    volume_up_button.grid(row=0, column=1, padx=10)

    status = customtkinter.CTkFrame(master=player)
    status.grid(pady=12, padx=10)

    current_length=customtkinter.CTkLabel(status, text="00:00")
    current_length.grid(row=0, column=0, pady=12, padx=5)

    separator=customtkinter.CTkLabel(status, text="/")
    separator.grid(row=0, column=1, pady=12)

    total_length=customtkinter.CTkLabel(status, text="00:00")
    total_length.grid(row=0, column=2, pady=12, padx=5)

    pb = customtkinter.CTkProgressBar(player, mode='determinate', progress_color=c.getAccent())
    pb.set(0)
    pb.grid(pady=12, padx=10)

def volume_up():
    chromecast_functions.volume_up()

def volume_down():
    chromecast_functions.volume_down()

def play_media(entry, queue):
    initiate_process(entry)

def pause_media():
    global paused
    if (paused):
        paused = not paused
        pause_button.configure(text="Pause")
        chromecast_functions.play()
    else:
        paused = not paused
        pause_button.configure(text="Resume")
        chromecast_functions.pause()

def stop_media():
    global id, kill_threads, queue, queueFrame
    id += 1
    kill_threads = True
    if not queue.isEmpty():
        for i in range(queue.getQueueLength()):
            download_manager.delete_video(queue.getItems()[i].getTrackFilename())
            queue.removeItemByIndex(i)
        for widget in queueFrame.winfo_children():
            widget.destroy()
    reset_visuals()
    chromecast_functions.stop()

"""Visual aspects of the app such as progress bar, video length and current timestamp are reset to 0 here"""
def reset_visuals():
    global pb, current_length, total_length
    # Reset the values
    current_time = 0
    total_length.configure(text=misc.beautify_time(current_time))
    current_length.configure(text=misc.beautify_time(current_time)) # Set on to tkinter window
    pb.set(0)

"""Visual aspects of the app such as progress bar, video length and current timestamp are updated here"""
def update_visuals(length, item_id):
    global pb, url_entry, current_length, total_length, kill_threads
    # Reset the values
    current_time = 0
    total_length.configure(text=misc.beautify_time(length))
    pb.set(0)
    current_time = 0
    while int(length) >= current_time: # Stop when the song ends
        if (kill_threads and item_id != id):
            return
        pb.set(current_time/int(length))
        current_length.configure(text=misc.beautify_time(current_time)) # Set on to tkinter window
        current_time += 1 # Increment current song timestamp by one
        time.sleep(1) # Wait a second

"""Initiate a new listening session from url (entry parameter). Downloads a song, starts a thread for visual updates, and plays on chromecast station"""
def initiate_process(entry):
    global id, kill_threads, queue, queueFrame
    id += 1
    kill_threads = True
    if not queue.isEmpty():
        for i in range(len(queue.getItems())):
            download_manager.delete_video(queue.getItems()[i].getTrackFilename())
            queue.removeItemByIndex(i)
        for widget in queueFrame.winfo_children():
            widget.destroy()
    if (not ("youtube.com" in entry)):
        return # The link is invalid, do nothing
    if (entry == ''): # On initialisation, tkinter will run through button functions with no / null arguments. Prevent issues by checking if null / empty
        return
    newQueueObject(entry, queueFrame)
    filename, length = download_manager.download_ytvid_as_mp3(entry, queue) # Retrieve the filename and video length, and download audio from given URL
    queue.createQueueItem(filename, entry)
    kill_threads = False
    t = Thread(target=update_visuals, args=(length,id,)) # New thread for visual aspects of the app 
    t.daemon = True 
    t.start()
    threads.append(t)
    chromecast_functions.play_new_song(filename) # Play song on chromecast

def newQueueObject(url, queueFrame):
    global c
    itemFrame = customtkinter.CTkFrame(master=queueFrame, width=(600-20))
    itemFrame.grid(pady=12, padx=10)
    queueItem = customtkinter.CTkLabel(master=itemFrame, text=url)
    queueItem.configure(justify="left")
    queueItem.grid(row=0, column=0, pady=12, padx=10)
    button = customtkinter.CTkButton(master=itemFrame, text="Current Song",
        border_width=2,
        corner_radius=20,
        border_color= c.getAccent(),
        hover_color=c.getAccent(),
        bg_color='transparent',
        fg_color='transparent')
    button.grid(row=0, column=1, pady=12, padx=10)

def on_closing():
    stop_media()
    print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Visual closing down")
    root.destroy()

def media_server():
    system('cmd /k "python -m http.server"')

# Setup for main variables
global c
global paused
threads = [] # threads
paused = False
id = 0
kill_threads = False

# Start local storage server
print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Starting app thread")
try:
    t = Thread(target=media_server) # New thread for visual aspects of the app 
    t.daemon = True 
    t.start()
    threads.append(t)
except:
    print(f"{Fore.RED}Error :{Style.RESET_ALL} Error while statring app thread. Quitting")
    sys.exit()

print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Connecting to chromecast player")
try:
    chromecast_functions.connect_chromecast() # Connect to the first chromecast of list. Not optimised, but good for single-chromecast households
except:
    print(f"{Fore.RED}Error :{Style.RESET_ALL} Error while connecting to Chromecast. Quitting")
    sys.exit()

c = config.config_setup() # the config class

try:
    customtkinter.set_appearance_mode(c.getColor())
except:
    customtkinter.set_appearance_mode('system')

print(f"{Fore.BLUE}Info :{Style.RESET_ALL} Setting up visual window")
try:
    root = customtkinter.CTk()
    root.title(c.getAppName())
    root.geometry(c.getWIN_X()+'x'+c.getWIN_Y())
    root.protocol("WM_DELETE_WINDOW", on_closing)
    queue = trackQueue.queue({})
    initialise_window(c, queue)

except:
    print(f"{Fore.RED}Error :{Style.RESET_ALL} Error while connecting to start window. Quitting")
    sys.exit()

root.mainloop()