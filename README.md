# Speed & Red Light Camera Notifier
### By: David Zhong

## Description
In-car device that fetches daily camera locations and uses GPS to track user’s position, alerting them via speaker when nearing speed or red light camera.

## Features
- Scrapes camera locations daily (since camera location is subject to change every few months) in the Halton region (currently inoperable due to Town site maintenance), and records the coordinates in cameras.json.
- A Raspberry Pi Zero 2 W is in the car and constantly tracks your location and current road to alert if there may be a speed/red light camera within your proximity.
- A verbal warning is emitted from the Pi.

## Technologies
- Raspberry Pi
- Python
- GeoJSON

## Future Features
- Visual warning (LED)
- Better practices to sustain Raspberry Pi health
