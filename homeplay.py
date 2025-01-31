from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import os
import sys

import pyautogui
import asyncio
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.media.control import GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER

HTML_FILE:str = "index.html"

class var:
    def __init__(self, type, data):
        self._type = type
        self._data = data
    
    def set(self, data):
        if isinstance(data, self._type):
            self._data = data
            
    def get(self):
        return self._data

def read_file(path:str) -> str:
    with open(os.path.join(os.getcwd(), path), "r", encoding="utf-8") as f:
        return f.read()

class HomeplayHandler(BaseHTTPRequestHandler):
    def _set_html_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def _set_json_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
    def _success(self):
        self._set_json_response()
        self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
        
    def _error(self, msg:str):
        self._set_json_response()
        self.wfile.write(json.dumps({"success": False, "message": msg}).encode('utf-8'))

    def do_GET(self):
        match self.path:
            case "/":
                content:str = read_file(HTML_FILE)
                self._set_html_response()
                self.wfile.write(content.encode('utf-8'))
            case "/current-track":
                try:
                    content:str = json.dumps({
                        "success": True,
                        "track": asyncio.run(get_current_song()),
                        "isPlaying": asyncio.run(get_playback_status()) == PlaybackStatus.PLAYING,
                        "volume": get_audio_info()
                    })
                    self._set_json_response()
                    self.wfile.write(content.encode('utf-8'))
                except:
                    self._error("Failed to collect data")
            case "/shutdown":
                running.set(False)
                self._success()
                print("Received shutdown command")
            case _:
                self._set_html_response()
                self.wfile.write(f"This site doesn't exist: '{self.path}'!".encode('utf-8'))
                

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(content_length))
        if not data:
            self._error("Invalid json data!")
            return
        match self.path:
            case "/":
                if "action" not in data:
                    self._error("No action provided!")
                    return 
                match data["action"]:
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
                        return self._error(f"Unsupported action: '{data['action']}'")
                self._success()
                return
            case _:
                self._set_json_response()
                self.wfile.write(json.dumps({"success": False, "message": "Invalid path!"}).encode('utf-8'))
        

running:var = var(bool, True)

def run(port=9187):
    server_address = (socket.gethostbyname(socket.gethostname()), port)
    print(f"Serving at http://{server_address[0]}:{server_address[1]}")
    httpd = HTTPServer(server_address, HomeplayHandler)
    try:
        while running.get():
            httpd.handle_request()
    except KeyboardInterrupt:
        print("Server interrupted")
    except Exception as e:
        print(f"An exception occured: {e}")
    print("Exiting..")
    httpd.server_close()
    
async def get_current_song():
    try:
        manager = await MediaManager.request_async()    
        session = manager.get_current_session()
        if session:
            media_properties = await session.try_get_media_properties_async()
            
            title = media_properties.title
            artist = media_properties.artist
            return {"title": title, "artist": artist}
        else:
            return None
    except:
        return None
        
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
    except Exception as e:
        return {"volume": 50, "isMute": False}

if __name__ == '__main__':
    if len(sys.argv) == 2:
        run(port=int(sys.argv[1]))
    else:
        run()