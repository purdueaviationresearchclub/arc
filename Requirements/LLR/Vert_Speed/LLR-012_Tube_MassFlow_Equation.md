---
id: L2-012                # L1-### | L2-### | LLR-###
title: Tube Mass Flow Equation
status: draft             # draft | review | approved | implemented | verified | deprecated
owner: Luke Galka
parents: []               # L1: none | L2: [L1-###] | LLR: [L2-###, L1-###]
children: []              # L1: [L2-###, LLR-###] | L2: [LLR-###] | LLR: none
---

# L2-012: Tube Mass Flow Equation

## Statement
The mass flow rate ($\dot{m}$, in $\text{slugs/s}$) through the instrument's calibrated metering restriction shall adhere to the linear orifice flow relation:
$$\dot{m} = K (p - p_c)$$
where $K$ is the pneumatic conductance of the capillary tube ( $\text{slugs} / (\text{psf}\cdot\text{s})$ ), $p$ is ambient static pressure ( $\text{psf}$ ), and $p_c$ is internal case pressure ($\text{psf}$).
