# GreenStream
_Never wait at a red light again._

This was the project for my first hackathon: hackNY Fall 2014.

You can find my teammate's github at: https://github.com/amelius15

The idea behind the project started with wanting to route the end-user around red lights with a prediction algorithm that will plot out the future state of the traffic lights in your route. Unfortunately, NYC's traffic infrastructure is old and doesn't have an open API for finding the current state of a traffic light at a given intersection.

# Enter the computer vision component

To gather the data we needed, we're pulling over 500 Manhattan & Brooklyn traffic camera feeds in parallel every few seconds and analyzing the direction of traffic for each intersection to infer the state of the traffic lights. 

Our process was to take a few still shots, add them together to create an elongated motion shot, binarize the resulting image, run a Hough transform and measure the angles of the lines.
