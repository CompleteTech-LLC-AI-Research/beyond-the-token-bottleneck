---
type: moc
category: lens
title: "Safety, Interpretability & Auditability of Latent Systems"
created: "2026-04-06"
updated: "2026-04-08"
tags: [moc, safety, interpretability]
---

# Safety, Interpretability & Auditability of Latent Systems

Latent communication between agents creates a governance crisis. When models exchange continuous vectors instead of tokens, the entire safety infrastructure built around Chain-of-Thought monitoring --- reading what the model "says" to verify what the model "thinks" --- collapses. An agent sending a 512-byte slot-attention vector to a partner is performing computation that no human can read, no regex can filter, and no content policy can evaluate. The same property that makes latent communication powerful ([[continuous-vs-discrete-representation|continuous representations carry 4--2600x more information than discrete tokens]]) is what makes it dangerous: the channel is opaque by design.

This MOC traces the safety and interpretability problem from its origins through proposed solutions and forward to the fundamental tensions that remain unresolved. The question is not whether latent systems will be deployed --- they already outperform text-based alternatives by wide margins --- but whether they can be made auditable before deployment outpaces governance.

## Reading Path

![[safety-interpretability/reading-path]]

## The Three Layers of Latent Auditability

![[safety-interpretability/the-three-layers-of-latent-auditability]]

## Connections

![[safety-interpretability/connections]]
