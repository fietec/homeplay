# homeplay

A simple `Flask` server for sharing media control over the home network.

**Warning**: There currently is an error where the program terminates at random times because of 
> COM method call without VTable

This is due to be fixed in the near future.

## How to use
I have no idea how python's fancy build systems work (maybe i am also refusing to learn them). I created a `requirements.txt`, please just figure out how get everything to work :/.

Anyway, after that simply run:
```terminal
python3 homeplay.py [<PORT>]
```
`homeplay` will thereafter serve a simple website on the home network to allow users to iteract with the currently playing media.

The address of the website will be printed in the console by Flask but it should generally look like this:
```
http://192.168.178.22:<PORT>
```
