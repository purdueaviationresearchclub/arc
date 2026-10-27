---
id: L2-011                # L1-### | L2-### | LLR-###
title: Hydrostatic Equation Measurement
status: draft             # draft | review | approved | implemented | verified | deprecated
owner: Luke Galka
parents: []               # L1: none | L2: [L1-###] | LLR: [L2-###, L1-###]
children: []              # L1: [L2-###, LLR-###] | L2: [LLR-###] | LLR: none
---

# L2-001: Hydrostatic Equation Measurement

## Statement
The system shall relate the time rate of change of ambient static pressure to vertical speed using the hydrostatic equation:
$$\frac{dp}{dh} = -\rho(h) \cdot g$$

where $\rho(h)$ is local air density ($\text{slug/ft}^3$), $g = 32.174\text{ ft/s}^2$, and $h$ is geometric altitude ($\text{ft}$)
