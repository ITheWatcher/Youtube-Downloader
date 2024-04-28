import pytube
from pytube import YouTube, Playlist, Channel
import tkinter as tk
from tkinter import filedialog
import os, sys


def remove_forbidden_chars(title):
    forbidden_chars = "|/\\*?<>:"
    translation_table = str.maketrans("", "", forbidden_chars)
    return title.translate(translation_table)


def download_video(url, path, quality):
    try:
        yt = YouTube(url)
        print(f"[-] Downloading video: {yt.title}")
        video = yt.streams.filter(progressive=True , file_extension="mp4").get_by_resolution(resolution=quality).download(path)
        print(f"[-] Video downloaded succesfully to {path}/{remove_forbidden_chars(yt.title)}")
    
    except Exception as e:
        print(f"[!] Error {e}")


def download_audio(url, path):
    try:
        yt = YouTube(url)
        print(f"[-] Downloading audio: {yt.title}")
        audio = yt.streams.filter(only_audio=True, file_extension="mp4").order_by('abr').desc().first().download(path)
        print(f"[-] Audio downloaded succesfully to {path}/{remove_forbidden_chars(yt.title)}")
    
    except Exception as e:
        print(f"[!] Error {e}")


def download_playlist(url, type_, res, playlist_folder):
    try:
        pl = Playlist(url)
        for amount, urls in enumerate(pl.video_urls, 1):
            for video in pl.videos:
                yt = YouTube(urls)
                if type_:
                    video = video.streams.filter(only_audio=type_, file_extension="mp4").order_by('abr').desc().first()
                    
                else:
                    video = yt.streams.filter(only_audio=type_, progressive=True, file_extension='mp4').get_by_resolution(resolution=res)

            video.download(rf"{playlist_folder}")
            print(f"[-] Download completed for {amount}/{len(pl.video_urls)} to diractory {playlist_folder}/{yt.title}")
        print(f"[-] Playlist [ {pl.title} ] downloaded successfully.")
                    
            
    except Exception as e:
        print(f"[!] Error {e}")
        
        
def playlist_info_etc(url, path):
    pl = Playlist(url)
    channel_id = pl.owner_id
    channel = Channel(f"https://www.youtube.com/channel/{channel_id}")
    channel_name = channel.channel_name

    print(f"[-] Downloading playlist [ {pl.title} ] by channel [ {channel_name} ].....")
    

    playlist_folder = f"{path}/{remove_forbidden_chars(pl.title)}"

    if os.path.exists(f"{playlist_folder}"):
        while True:
            folder_choice = input("[!] Folder with this name already exists, do you want to download at same diractory Y/N (q to quit):  ").capitalize()
            
            if folder_choice in ["Y", "N", "Q"]:
                break
            
            else:
                print("[!] Invalid choice. Please enter 'Y' to download in the same directory, 'N' to back the first.")

        if folder_choice == "Y":
            return playlist_folder
        elif folder_choice == "N":
            if os.name == "nt":
                _ = os.system("cls")
                
            else:
                _ = os.system("clear")
            return folder_choice
        elif folder_choice == "Q":
            print("[!] Quitting programe")
            sys.exit()
            
    else:
        os.mkdir(f"{playlist_folder}")
                    
    return playlist_folder

                    
def get_res(url):
    try:
            yt = YouTube(url)
            resolutions = sorted(
                    {stream.resolution for stream in yt.streams if stream.resolution},
                    key=lambda x: int(x[:-1]),
                )
            print(f"[-] Available Resolutions:")
            for res in resolutions:
                print(res)
    except Exception as e:
        print(f"[!] Error can't get all resolution type it manually. [{e}]")
        
        
####################################################################################
        # if ask == "P":
            # pl = Playlist(url)
            # for urls in pl.video_urls:
            #     a = urls.index[1]
            # yt = YouTube(a)
            # resolutions = sorted(
            #         {stream.resolution for stream in yt.streams if stream.resolution},
            #         key=lambda x: int(x[:-1]),
            #     )
            # print(f"[-] Available Resolutions:")
            # for res in resolutions:
            #     print(res)
################# Get resolution not avilable now for playlist#######################
            
            

def main():
    while True:
        ask = input("[-] Do you need to download | Video | Audio | Playlist | (q to quit): ").capitalize().strip()
        if ask == "Q":
            break
        
        elif ask == "Video":
            video_url = input("[-] Enter video url: ")
            get_res(video_url)
            quality = input("[-] What resolution do you want to download the video: ")
            downloade_path = filedialog.askdirectory()
            download_video(video_url, downloade_path, quality)
            
        elif ask == "Audio":
            video_url = input("[-] Enter video url: ")
            downloade_path = filedialog.askdirectory()
            download_audio(video_url, downloade_path)
            
        elif ask == "Playlist":
            playlist_url = input("[-] Enter playlist url: ")
            playlist_type = input("[-] Do you want to download playlist as Video or Audio:  ").capitalize().strip()
            downloade_path = filedialog.askdirectory()
            quality = input("[-] What resolution do you want to download the video: ")
            folder_choice = playlist_info_etc(playlist_url, downloade_path)
            if folder_choice == "N":
                continue
            
            if playlist_type == "Video":
                download_playlist(playlist_url, False, quality, folder_choice)
                
            elif playlist_type == "Audio":
                download_playlist(playlist_url, True, quality, folder_choice)
            
            else:
                print("[!] Invalid please choose Video or Audio: ")         
                

if __name__ == "__main__":
    
    root = tk.Tk()
    root.withdraw()
    main()
     
   
    
###Telegram: https://t.me/hh8cc | Github: 