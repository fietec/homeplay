# homeplay.py

A simple python http server for allowing media control via the home network. This project is sadly Windows-only.

## How to use
To install the required packages, navigate to the root directory of `homeplay` and run the following command:
```terminal
pip install -r requirements.txt
```

After that, simply run:
```terminal
python3 homeplay.py [<PORT>]
```
`homeplay` will thereafter serve a simple website on the home network to allow users to iteract with the currently playing media.

The address of the website will be printed to the console on startup, but it should generally look like this:
```
http://192.168.178.22:9187
```
Simply open this website in your browser and control the media! (the one on your computer)