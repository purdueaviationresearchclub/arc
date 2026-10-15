---
id: LLR-005                
title: Static Pressure Input Processing
status: draft             
owner: Gavin Siems
parents: [L2-004]               
children: [None]              
---

# LLR-005: Static Pressure Input Processing

## Statement
The Air Data Computer shall compute **AirDataComputerInputProcessing:staticPressurePa** per the following:
- *Static Pressure Pa* = *Static Pressure* * 6894.76 $\frac{Pa}{Psi}$, where:
  -  *Static Pressure Pa* equals **AirDataComputerInputProcessing:staticPressurePa**.
  -  *Static Pressure* equals **PitotStaticInputSignals:staticPressure** in Psi.
  -  Note: 6894.76 is the standard conversion factor from Psi to Pascals.



