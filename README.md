# morse_trainer
 Exercise morse ability via Python client to TCP keyer server

### Brief description
This application should work in tandem with the github/vinloren/morse_keyer to drive the keyer with this suited python client instead of using a general purpose Telnet client such as Putty.

By using this client the keyer can be configured either regarding the morse wpm speed and the tone frequency as well. This latter feature actually produces different volume levels dpending on the frequency value set for the tone. The max volume using my ordinary 3.5-5Vdc passive buzzer is gotten at 800Hz, lower volume results for any other frequency. Maybe using other passive buzzer the result could be different.

### morse_trainer features
Basically the text entered in the transmit window is sent to the keyer to be played, in addition to this a set of 10 groups of 5 random characters can be generated and displayed to the transmit window upon transmission completion. 

This way the user can test his ability and trained to improve it comparing the data detected in morse with the final display of what was actually sent.
Each tsequence cam be easyly repeated since it is kept in the transmit window.

Another added feature is the possibility to continuosly send, at a pace of 2 minutes, 10 groups of 5 random chars
