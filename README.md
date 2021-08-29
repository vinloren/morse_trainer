# morse_trainer
 Exercise morse ability via Python client to TCP keyer server

### Brief description
This application should work in tandem with the github/vinloren/morse_keyer to drive the keyer with this suited python client instead of using a general purpose Telnet client such as Putty.

By using this client the keyer can be configured either regarding the morse wpm speed and the tone frequency as well. This latter feature actually produces different volume levels dpending on the frequency value set for the tone. The max volume using my ordinary 3.5-5Vdc passive buzzer is gotten at 800Hz, lower volume results for any other frequency. Maybe using other passive buzzer the result could be different.

### morse_trainer features
1) Play text entered in the xmit pane window
2) Play a group of 10 random text/numbers/special characters displayed in the transmit window as all of them are played. This way the user can test his ability and trained to improve it comparing the data detected in morse with the final display of what was actually sent. The codes values interpreted listening to the buzzer can be written in the CHECK TEST text box and the response regarding its correctness can be gotten clicking the push button. Each sequence can be easyly repeated since it is kept in the transmit window.
3) Continuosly send 10 groups of 5 random chars every two minutes or continuosly send what is in the transmit pane if the "Repeat send" checkbox is checked. 
4) Continuously play what is there in the xmit pane window (the last sentence comprised between the net to last new line and last one) with two second silence between data played.


### standar time spacing between morse sounds
The standard time spacing between dit / dah is 1 dit, the spacing between characters is 3xdit, the spacing between words is 7xdit. The application provides the possibility to double those spacing time just checking the "Double space between chars" checkbox to instruct the conpanion TCP keyer server. This is an additional feature aimed to ease the learnig curve of the morse code.
 
