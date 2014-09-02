LaserTunnel
===========

pygame code for the amazing Bloominglabs/Wonderlab laser tunnel project

##Overview
This code was written to run on a Raspberry Pi communicating via serial port w/ an Arduino that sends it 'commands':

'a' - arm system<br/>
'd' - disarm system<br/>
1-8 - which sensor was triggered<br/>
'r' - quits program

In the event there is no Arduino attached there is a 'debug' mode where you can just type those things on the keyboard.

##Pre-requisites
Really aside from PyGame (installed on most RasPi images out-of-the-box) and PySerial, this doesn't use any special modules.
