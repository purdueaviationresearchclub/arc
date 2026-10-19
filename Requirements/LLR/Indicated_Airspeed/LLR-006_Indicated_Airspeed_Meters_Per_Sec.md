---
id: LLR-006               
title: Indicated Airspeed Meters Per Sec
status: draft             
owner: Gavin Siems
parents: [L2-004]               
children: [None]              
---

# LLR-006: Indicated Airspeed Meters Per Sec

## Statement
The Air Data Computer shall compute AirDataComputer:airspeedMetersPerSec per the following:
- *IAS* = $\sqrt{\frac{2(P_{Total}-P_{Static})}{\rho_0}}$, where:
  - $P_{Total}$  is equal to **AirDataComputerInputProcessing:pitotPressurePa** in Pascals.
  - $P_{Static}$ is equal to **AirDataComputerInputProcessing:staticPressurePa** in Pascals.
  - $\rho_0$  1.225 kg/m³ (standard sea-level air density).
  - *IAS*  is indicated airspeed in meters per second.

