from flask import Flask, request, send_file, jsonify
import pyautogui
import os
import socket
import sys
import asyncio
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

PORT:int = 9187
SUCCESS:dict = {"success": True}
HTML:str = "index.html"

app = Flask(__name__)

def error(msg:str)->str:
    return {"success": False, "message": msg}

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return send_file(HTML)
    elif request.method == 'POST':
        json = request.json
        if json != None:
            if "action" not in json:
                return error("No action provided!")
            try:
                match json["action"]:
                    case "vol-low":
                        for _ in range(3):
                            pyautogui.press("volumedown")
                    case "vol-high":
                        for _ in range(3):
                            pyautogui.press("volumeup")
                    case "vol-mute":
                        pyautogui.press("volumemute")
                    case "track-next":
                        pyautogui.press("nexttrack")
                    case "track-prev":
                        pyautogui.press("prevtrack")
                    case "track-play":
                        pyautogui.press("playpause")
                    case _:
                        return error(f"Unsupported action: '{json['action']}'")
                return SUCCESS
            except:
                return error("Internal error")
        return error("Bad request!")
    return error(f"Unsupported request method: '{request.method}'")

@app.route('/current-track', methods=['GET'])
def get_current_track():
    try:
        return jsonify({
            "success": True,
            "track": {
                "title": asyncio.run(get_current_song())
            },
            "isPlaying": asyncio.run(get_playback_status()) == PlaybackStatus.PLAYING,
            "audio": get_audio_info()
        })
    except:
        return "{}"
        
@app.route("/shutdown")
def shutdown():
    return SUCCESS
    
async def get_current_song():
    try:
        manager = await MediaManager.request_async()    
        session = manager.get_current_session()
        if session:
            media_properties = await session.try_get_media_properties_async()
            
            title = media_properties.title
            artist = media_properties.artist
            return f"'{title}' by {artist}"
        else:
            return "No media is currently playing."
    except:
        return ""
        
async def get_playback_status():
    try:
        manager = await MediaManager.request_async()
        session = manager.get_current_session()
        if session:
            return session.get_playback_info().playback_status
        return None
    except:
        return None
    
def get_audio_info():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 1, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return {"volume": volume.GetMasterVolumeLevelScalar()*100, "isMuted": volume.GetMute()}
    except:
        return {"volume": 50, "isMute": False}

if (len(sys.argv) > 1):
    port:int = int(sys.argv[1])
else:
    port:int = PORT
app.run(socket.gethostbyname(socket.gethostname()), port)