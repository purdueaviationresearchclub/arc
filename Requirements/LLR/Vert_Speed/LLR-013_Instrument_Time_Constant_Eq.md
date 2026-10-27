---
id: L2-013                # L1-### | L2-### | LLR-###
title: Instrument Time Constant Equation
status: draft             # draft | review | approved | implemented | verified | deprecated
owner: Luke Galka
parents: []               # L1: none | L2: [L1-###] | LLR: [L2-###, L1-###]
children: []              # L1: [L2-###, LLR-###] | L2: [LLR-###] | LLR: none
---

# L2-013: Instrument Time Constant Equation

## Statement
The pneumatic time constant ($\tau$, in seconds) characterizing the instrument's lag filter shall be defined as:
$$\tau = \frac{V}{K R T}$$
where $V$ is the internal case volume ( $\text{ft}^3$ ), $R$ is the specific gas constant for air ( $1,716\text{ ft}\cdot\text{lbf}/(\text{slug}\cdot^\circ\text{R})$ ), and $T$ is the absolute air temperature inside the instrument ( $^\circ\text{R}$ ).
