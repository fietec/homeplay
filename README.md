# homeplay.py

A simple python http server for allowing media control via the home network.

## How to use
I have no idea how python's fancy build systems work (maybe i am also refusing to learn them). I created a `requirements.txt`, please just figure out how get everything to work :/.

Anyway, after that simply run:
```terminal
python3 homeplay.py [<PORT>]
```
`homeplay` will thereafter serve a simple website on the home network to allow users to iteract with the currently playing media.

The address of the website will be printed to the console on startup, but it should generally look like this:
```
http://192.168.178.22:<PORT>
```
Simply open this website in your browser and control the media! (the one on your computer)