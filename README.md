# improved-roomba
A cheap mechanical cleaner with wifi, object detection, and space mapping.

Background:
A friend of mine bought a Roomba-like product for floor cleaning and was very dissatisfied with its performance. 
It did not clean the entire floor area, often missing large areas, and ended up cleaning areas that it had already cleaned. 
It also broke down a few years after service. I was donated the corpse of the mechanical cleaner since I had some ideas of how 
I could enhance its performance without driving up the cost. The one that my friend purchased was around $50. 

Purpose:
The purpose of this project was to provide a proof of concept that a good mechanical floor cleaner does not need to cost hundreds
or thousands of dollars like most high end Roombas. This can be done by creatively using cheap sensors and offloading any heavy
computation to the user’s personal computer. 

Details:
Since the Roomba I received was broken, I discarded all of its internal circuitry and sensors, leaving only the 2 brush motors,
the 2 wheel motors, and the vacuum motor. I bought an ESP-8266 for wireless communication with my PC which cost $2.2, 
two HC-SR04 Distance Sensors which cost $2.12 each, a 5V to 3.3V regulator which cost $0.9, a 400 point solderless breadboard which
cost $1.75, 4 SPDT relays which cost about $10 total. The most expensive part was my Arduino uno which cost $20. So in total, 
about an extra $39, minus the cost of all the sensors and circuitry I ripped out of the original. 

The plan is to get the roomba to explore the room and send the exploration data back to the computer. 
The computer can then generate a space map that determines where the roomba has gone and where it can go. 
This results in a two phase approach. The first phase is exploration; the roomba explores the room/rooms without worrying about where
it need to clean, instead being more interested in where to go to maximize exploration knowledge to better understand the geometry of the
room. Once all the data is collected, the PC will do all of the heavy computing to generate a functional space map of the rooms, and a
path for the roomba to take to clean as much of the room as possible in a timely manner. I preface 'as much as possible' since there
are physical size constraints that make small nooks and crannies impossible to clean with a roomba. This sequence is then saved and
communicated to the roomba whenever the room needs to be cleaned. The second phase consists of the roomba following the instructions
given by the sequence and actually cleaning the room. 

The pathing I used is similar is form to the pathing used by the original roomba, which more or less navigate the outer perimeter of the room 
and slowly makes its way toward the center. The main difference is tht the original method left holes that were uncleaned and often cleaned the
same area several times. By incorporating a space map, my algorithm find a reasonable path to clean all of the space that the mechanical 
cleaner has found to be traversable. 

I have tested my code on a segment of my hallways which works quite well. Further testing is difficult since there are many parts of
my home that are not conducive to using a roomba, ie pets, rugs, small nooks and crannies, and slightly raised protrusions in the doorways. 
The outputs and visuals included in the repository are from the tests I have conducted. 
