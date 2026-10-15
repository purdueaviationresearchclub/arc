---
id: LLR-007              
title: Indicated Airspeed Knots
status: draft             
owner: Gavin Siems
parents: [L2-004]               
children: [None]              
---

# LLR-007: Indicated Airspeed Knots

## Statement
The Air Data Computer shall compute **AirDataComputerOutputProcessing:airspeedKnots** per the following:
- $IAS_{knots} = IAS_{m/s} * 1.94384 \frac{knots}{m/s}$, where:
  - $IAS_{knots}$ equals **AirDataComputerOutputProcessing:airspeedKnots**.
  - $IAS_{m/s}$ equals **AirDataComputer:airspeedMetersPerSec** in meters per second.
  - Note: 1.94384 is the standard conversion factor from speed in m/s to speed in knots. 

