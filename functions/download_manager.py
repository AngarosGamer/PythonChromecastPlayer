import yt_dlp
import spotify_dl
import os
import misc
import config

def download_ytvid_as_mp3(video_url):
    video_info = yt_dlp.YoutubeDL().extract_info(url = video_url,download=False) # Extract the video info from parsed URL
    filename = f"{clean_name(video_info['title'])}.wav" # type: ignore # Select the file name
    length = f"{video_info['duration']}" # type: ignore # Select video file duration
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':'./media/'+filename, # Output file name is just the video name followed by .mp3
        'limit-rate':'100M', # Download rate limiter to 100MBytes/s
        'no-part':True, # No partitions
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']]) # type: ignore # Download requested information into current folder
    return filename, length # return the file name and the video length
    
def delete_video(name):
    os.remove('./media/'+name) # Remove a song in current directory

def clean_name(name):
    name = str(name)
    return hash(name)