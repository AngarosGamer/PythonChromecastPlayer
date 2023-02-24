### MADE BY ANGAROS - CREATIVE COMMONS : 08/10/2022 (DD/MM/YYY)
### Libraries used were not made by me, but brought to use by free licenses

# Imports
from os import kill, system
import chromecast_functions
import download_manager
import config
import tkinter
import customtkinter
from threading import Thread
import time
import misc

def initialise_window():
    global pb, url_entry, total_length, current_length, c, pause_button
    c = config.config_setup()

    url_label = customtkinter.CTkLabel(master=root, text="Enter Song URL: ")
    url_label.configure(wraplength=200, justify="center")
    url_label.grid(pady=12, padx=10)

    url_entry = customtkinter.CTkEntry(master=root, width=int(c.getWIN_X())-20, placeholder_text="https://youtube.com/example")
    url_entry.configure()
    url_entry.bind('<Return>', lambda x: initiate_process(url_entry.get()))
    url_entry.grid(pady=12, padx=10)

    playback = customtkinter.CTkFrame(master=root)
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
    command = lambda : play_media(url_entry.get()))
    play_button.grid(row=0, column=2, pady=12, padx=10)

    volume = customtkinter.CTkFrame(master=root)
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

    status = customtkinter.CTkFrame(master=root)
    status.grid(pady=12, padx=10)

    current_length=customtkinter.CTkLabel(status, text="00:00")
    current_length.grid(row=0, column=0, pady=12, padx=5)

    separator=customtkinter.CTkLabel(status, text="/")
    separator.grid(row=0, column=1, pady=12)

    total_length=customtkinter.CTkLabel(status, text="00:00")
    total_length.grid(row=0, column=2, pady=12, padx=5)

    pb = customtkinter.CTkProgressBar(root, mode='determinate', progress_color=c.getAccent())
    pb.set(0)
    pb.grid(pady=12, padx=10)

def volume_up():
    chromecast_functions.volume_up()

def volume_down():
    chromecast_functions.volume_down()

def play_media(entry):
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
    global id, kill_threads
    id += 1
    kill_threads = True
    if (len(songs) != 0):
        for i in range(len(songs)):
            download_manager.delete_video(songs[i])
            songs.remove(songs[i])
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
    global id, kill_threads, isPlaying
    id += 1
    kill_threads = True
    if (len(songs) != 0):
        for i in range(len(songs)):
            download_manager.delete_video(songs[i])
            songs.remove(songs[i])
    if (not ("youtube.com" in entry)):
        return # The link is invalid, do nothing
    if (entry == ''): # On initialisation, tkinter will run through button functions with no / null arguments. Prevent issues by checking if null / empty
        return
    filename, length = download_manager.download_ytvid_as_mp3(entry) # Retrieve the filename and video length, and download audio from given URL
    songs.append(filename)
    kill_threads = False
    t = Thread(target=update_visuals, args=(length,id,)) # New thread for visual aspects of the app 
    t.daemon = True 
    t.start()
    threads.append(t)
    isPlaying = True
    chromecast_functions.play_new_song(filename) # Play song on chromecast

def on_closing():
    stop_media()
    root.destroy()

def media_server():
    system('cmd /k "python -m http.server"')

# Setup for main variables
global c
global paused
threads = [] # threads
songs = [] # songs
paused = False
id = 0
kill_threads = False

# Start local storage server
t = Thread(target=media_server) # New thread for visual aspects of the app 
t.daemon = True 
t.start()
threads.append(t)

chromecast_functions.connect_chromecast() # Connect to the first chromecast of list. Not optimised, but good for single-chromecast households
c = config.config_setup() # the config class

customtkinter.set_appearance_mode(c.getColor())

root = customtkinter.CTk()
root.title(c.getAppName())
root.geometry(c.getWIN_X()+'x'+c.getWIN_Y())
root.protocol("WM_DELETE_WINDOW", on_closing)

initialise_window()

root.mainloop()