---
name: academic-standards
description: Enforce rigorous academic standards for research and writing, specifically prioritizing Finance, AI, and Quantitative Finance domains. Defines mandatory citation styles, language, and output formats.
allowed-tools: [Read]
---

# Academic Standards & Rigor

## Purpose
This skill serves as the **SINGLE SOURCE OF TRUTH** for quality, style, and methodology across all research and writing tasks. All other skills (`literature-review`, `research-paper-writer`) must adhere to these standards.

## Domain Focus
**Prioritize research in:**
- Finance (Quantitative Finance, Asset Pricing, Market Microstructure)
- Artificial Intelligence (Machine Learning, Deep Learning, NLP)
- Algorithmic Trading & Financial Technology
- Economics & Law (where relevant to Finance)

## Core Rules

### 1. Source Quality
- **Peer-Reviewed Priority**: Use ONLY peer-reviewed journal articles (Q1/Q2 rankings), academic books, and reputable scholarly sources.
- **ArXiv/Preprints**: Use **strictly** for latest cutting-edge papers (last 1-2 years) where peer review is pending. For established topics, referenced peer-reviewed versions are mandatory.
- **Excluded**: Do not use non-academic blogs, generic news sites, or unverified preprints unless they are from renowned authors in the field.

### 2. Tone and Language
- **British English**: Use formal, academic British English (e.g., "analyse", "behaviour", "modelling").
- **Precision**: Use PhD-level vocabulary and sentence structure. Avoid colloquialisms.
- **Objectivity**: Ensure arguments are critical, evidence-based, and balanced. Compare differing viewpoints.

### 3. Citation Style (Harvard)
- **All** citations must use **Harvard Style**.
- **In-text**: (Smith, 2023) or (Smith and Jones, 2024).
- **Reference List**: Must be included at the end of every output.
- **BibTeX**: Always providing a corresponding BibTeX entry or `references.bib` file.

## Mandatory Output Format

When providing a list of papers or literature summary, you **MUST** use the following table format:

| Paper Name with Authors | Summary (Concise) | Reference (Harvard) |
|-------------------------|-------------------|---------------------|
| **Attention Is All You Need**<br>Vaswani et al. | Introduces the Transformer architecture, replacing RNNs with self-attention mechanisms for sequence modeling tasks. | Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł. and Polosukhin, I. (2017) 'Attention Is All You Need', *Advances in Neural Information Processing Systems*, 30. |

## Analysis Guidelines
- **Theoretical Framework**: Situating discussions within recognised theoretical and methodological frameworks (e.g., Efficient Market Hypothesis, Modern Portfolio Theory).
- **Critical Depth**: Do not just summarize; evaluate methodological strengths/weaknesses.
- **Verification**: Ensure all sources are accurate and verifiable. **NO HALLUCINATIONS**.

## Integration
- **literature-review**: Apply these source filters during search.
- **research-paper-writer**: Apply these style rules during drafting.
- **citation-management**: Use these rules for formatting.
