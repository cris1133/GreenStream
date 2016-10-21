# GreenStream
_Never wait at a red light again._

This was the project for my first-ever hackathon: hackNY Fall 2014.

You can find my teammate's github at: https://github.com/amelius15

The idea behind the project started with wanting to route the end-user around red lights with a prediction algorithm that will plot out the future state of the traffic lights in your route. Unfortunately, NYC's traffic infrastructure is really (really) old and hence there isn't an open API for even finding out the current state of a traffic light at a given intersection.

# Enter the computer vision component

To gather the data we desired, we in parallel would pull over 500 Manhattan & Brooklyn traffic camera feeds every few seconds and would analyze the traffic flow of each intersection using SimpleCV – a more pythonic wrapper around OpenCV. Our process was to take a few still shots, combine them together with a matix add operation, do some pre-processing (namely binarization), run a Hough transform and measure the angles of the lines.

We decided to do the extra step of adding multiple shots together before analysis because it makes the movement of traffic far more pronounced for the line detection algorithm, specifically after nightfall when the shots from the traffic cameras aren't too clear and when traffic is sparse.
