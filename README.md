# homeplay

A simple `Flask` server for sharing media control over the home network.

## How to use
Simply run:
```terminal
python3 homeplay.py [<PORT>]
```
`homeplay` will thereafter serve a simple website on the home network to allow users to iteract with the currently playing media.

The address of the website will be printed in the console by Flask but it should generally look like this:
```
http://192.168.178.22:<PORT>
```
