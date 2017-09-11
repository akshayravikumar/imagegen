# Random Image Generator

This module creates random images using random.org's random number generator, and displays them using PyPlot. Note that random.org has a quota on the number/volume of requests, so sometimes this service might be unavailable (upon which an error will be displayed).

Requirements: `numpy (version 1.13.0), pyplot (version 1.5.1), requests (version 2.10.0)`

Usage: 
```
python imagegen.py HEIGHT WIDTH
Dimensions must be integers in [1, 200]. If WIDTH and HEIGHT aren't supplied, uses 128x128 by default.

```
