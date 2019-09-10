# ESP8266-micropython-breakout
micropython code for brick.py written for ESP8266 micropython (not circuit python).
The soruce file is too big to be imported directly. It will run out of the 32K dynamic memory in ESP8266.
You need to use micropython mpy-cross (precompiler) to complie that to the byte-code breakout.mpy
Then import breakout to run.

Don't copy both breakout.py and breakout.mpy to your ESP8266 micropython board.
Otherwise, it'll only run breakout.py and runs out of memory.
Only copy breakout.mpy to your ESP8266 micropython board.
