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
about an extra $39, minus the cost of all the sensors and circuitry I ripped out of the original. The battery was also unuseable 
so I replaced it with several lower voltage batteries to get the same voltage and current output of the original. This was an additonal 
expense since the batteries combined cost me about $20 but one that I do not think should count toward the total expense of the new roomba
since I would have used the original battery had it not been broken. A picture of the modified roomba is included, named 
'modified_roomba_batteries_disconnected'. The circuit diagram detailing the electrical connections between each component is also included, 
named 'Circuit diagram'. 

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

Code details:

  ESP-8266: This is just the wifi module meant to connect my PC and the arduino. The code is really simple, just relay what one side says to
  the other side. There are multiple ways that this module can work, the original intent was to connect the ESP-8266 to the household wifi
  and then connect to the PC. However, after the most recent upgrade to my household wifi, the ESP-8266 can no longer connect to it, so I changed
  it to connect directly with the PC instead. 
  
  Arduino: Accepts instructions from the PC as a 7 digit code, and interprests it to control the motors and sensors of the modified roomba. 
  The first two digits correspond with the two wheels of the roomba, 0 is to go forward, 1 is to do nothing, 2 is to go backwards, 3 is a 
  special instruction. The third digit specifies what kind of response to give (received, distance from both sensors, etc). The last four 
  digits are the number of milliseconds the instruction should be carried out for, or in some cases the distance for an instruction. The 
  arduino is also used to perform basic computations not worth sending to the PC. 
  
  PC_python: First, I would like to preface that this code would likely be much faster if I wrote it in a language like C, but as this is just a 
  proof of concept, and since this code is only being run once (for the most part), python is just a much more convenient option. 
  
    Mode 0: The search and explore option. 
    The roomba will remain a certain distance away from the right wall and navigate the perimeter of the room in a counterclockwise fashion. 
    Once the outer perimeter is defined, it will make its way inward until either it is surrounded by areas that it has already explored or 
    the new space that it finds is not enough to justify further exploration (both are parameters that can be changed). The space map is updated 
    and saved after each movement. Each space in the spacemap corresponds with a 1cm x 1cm area in the room. An example of the output of this 
    segment of code is included, named 'data_room_example'. This will be used in mode 3. A visual representation of this data is also included, 
    named 'data_room_example_visual'.
    
    Mode 1: Direct communication.
    The PC will allow the user to input movement commands to the roomba. This was used primarily to test out snippets of code. 
    
    Mode 2: Plot.
    This plots a spacemap for the user to see. This was also primarily used to check code. 
    
    Mode 3: Smooth spacemap.
    A fairly computationally heavy program to smooth and manifest the spacemap made from mode 0 into something that can be used for navigation.
    Removes extra 'walls' that are not connected to anything, trims existing walls without affecting the interior area to reduce the size of the
    spacemap, finds all cleanable areas. For the new spacemap, spaces are labeled 0 if they are outside the cleanable area, 1 if they are a cleanble
    space, and 3 if they are a wall. The output for this segment of code is included, named 'data_room_smoothed_example'. This will be used in mode 4.
    A visual representation of this data is also included, named 'data_room_smoothed_visual'.
    
    Mode 4: Compute a path for cleaning.
    A very computationally heavy program to find a path for the roomba to take to clean the cleanable area. Follows a similar scheme as mode 1. 
    Makes its way around the perimeter of the room and slowly makes its way toward the center. Once it no longer sees any cleanable spaces around it, 
    it will call a searching progrom which parses through the entire spacemap looking for a 1. If one is found, a pathing program will be called to 
    direct the roomba to the uncleaned space where normal operations will continue. This will loop until the searching program parses through the 
    entire spacemap. At this point, all reasonable spaces will be cleaned. The cumulative path will be recorded and the spacemap which shows the
    path generated will be shown. Each new instruction is a slightly different color than the last to show progression of movement. The output for 
    this segment of code is included, named 'data_room_sequence_example'. This is used in mode 5. A visual representation of this data in also 
    included, named 'data_room_pathing_visual'. 
    
    Mode 5: Execute the list of instructions. 
    First, the roomba must make it to the starting corner, so a series of pre-made code snippets are executed to ensure that the roomba starts where 
    the program thinks it is starting. Then the instructions are read from the txt document and relayed to the roomba to execute. 
