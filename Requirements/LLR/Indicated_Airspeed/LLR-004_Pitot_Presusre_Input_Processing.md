---
id: LLR-004                
title: Pitot Pressure Input Processing
status: draft             
owner: Gavin Siems
parents: [L2-004]               
children: [None]              
---

# LLR-004: Pitot Pressure Input Processing

## Statement
The Air Data Computer shall compute **AirDataComputerInputProcessing:pitotPressurePa** per the following:
- *Pitot Pressure Pa* = *Pitot Pressure* * 6894.76 $\frac{Pa}{Psi}$, where:
  - *Pitot Pressure Pa* equals **AirDataComputerInputProcessing:pitotPressurePa** in Pascals. 
  - *Pitot Pressure* equals **PitotStaticInputSignals:pitotPressure** in Psi.
  - Note: 6894.76 is the standard conversion factor from Psi to Pascals.
