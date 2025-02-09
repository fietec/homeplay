# homeplay.py

A simple python http server for allowing media control via the home network. This project is sadly Windows-only.

## Installation
To install the required packages, navigate to the root directory of `homeplay` and run the following command:
```console
pip install -r requirements.txt
```

## Usage
To run the server, simply run in the terminal:
```console
python homeplay.py [<PORT>]
```
`homeplay` will thereafter serve a simple website on the home network to allow users to iteract with the currently playing media.

The address of the website will be printed to the console on startup, but it should generally look something like this:
```
http://192.168.178.22:9187
```
Simply open this website in your browser and control the media! (the one on your computer)