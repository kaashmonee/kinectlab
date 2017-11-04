# Flappy Bird Kinect Lab

Flappy bird on the Kinect

## Getting Started

This is a flappy bird game on the Kinect. Wave your arms up and down to have the bird fly. Used code base from Microsoft's Kinect Flappy Bird demonstration at Carnegie Mellon University.

### Prerequisites

What things you need to install the software and how to install them

```
pip install <library>
```

### Installing

Install the following libraries:
* pykinect2
* ctypes
* _ctypes
* pygame
* sys
* math


### Misc. Notes

Error in this line of code...please refer to original microsoft documentation here:
<<link>>

```
def drawBird(self):
        pygame.draw.circle(self.frameSurface, (200, 200, 0), int(self.screenWidth/2), int(self.screenHeight - self.birdHeight), 40)
```

## Built With

* Microsoft Kinect

## Acknowledgments

* Microsoft documentation
* Updated comments to update readability
