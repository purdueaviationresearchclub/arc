---
id: LLR-001                
title: Altitude Computation
status: draft             
owner: Quincey Johnson
parents: [L2-001]               
children: [None]              
---

# LLR-001: Altitude Computation

## Statement

The Air Data Computer shall compute **AirDataComputer:altitude** per the following: 
- $h = 44330 * (1-(\frac{P_{static}}{P_0})^{0.19026})$, where
  - $P_{static}$ is equal to **PitotStaticInputSignals:staticPressure**.
  -   $P_{0}$ is equal to Sea-level standard atmospheric reference pressure (29.92 inHg or 1013.25 hPa).
  -   h is equal to altitude in feet.

