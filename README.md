# CE-BL: Cross-Sensor Extraction & Blending of Lunar Imagery

## Smart India Hackathon 2026

**Problem Statement ID:** 26166

**Problem Statement Title:**  
Multi-modal, Sun Angle and Scale Invariant Image Correspondence using Chandrayaan-2 Optical Images (OHRC, TMC and IIRS)

**Theme:** Space Technology  
**Category:** Software  
**Team Name:** CE-BL

---

## 🌙 Problem Overview

Lunar image registration involves aligning images of the same region captured under different imaging conditions or by different sensors into a common coordinate system.

Chandrayaan-2 optical instruments such as **OHRC, TMC and IIRS** capture lunar imagery with differences in:

- Sun illumination and shadow conditions
- Viewing geometry
- Spatial resolution and scale
- Sensor characteristics and image appearance

These variations make it difficult to identify reliable corresponding points between a source image and a reference image.

The objective of this project is to develop a generic software approach for finding accurate image correspondences and registering Chandrayaan-2 optical imagery with sub-pixel precision.

---

## 🎯 Proposed Solution

CE-BL is a prototype for cross-sensor lunar image correspondence and registration.

The system follows a multi-stage approach designed to handle difficult matching conditions caused by illumination, scale and viewpoint variations.

Our prototype combines:

1. Image normalization and preprocessing
2. Multi-stage image correspondence
3. Geometric transformation and registration
4. Outlier rejection using RANSAC
5. Spatial distribution analysis of match points
6. Solar geometry and shadow analysis
7. Quantitative evaluation using registration metrics

The objective is to provide an auditable registration workflow that can evaluate correspondence quality across different lunar image sensors.

---

## 🛰️ Three-Tier Correspondence Architecture

CE-BL uses a fallback-based architecture for image correspondence.

### Layer 1 — Detector-Free Matching

The primary stage explores detector-free matching approaches for identifying correspondences under challenging illumination and appearance variations.

### Layer 2 — Classical Feature Matching

If the primary matching approach does not produce sufficient reliable correspondences, classical feature-based methods such as SIFT or AKAZE can be used as a fallback.

### Layer 3 — Spatial Uniformity Resampling

The final stage focuses on improving the spatial distribution of correspondences across the image and reducing clustering of match points in a limited region.

---

## 🌗 Illumination and Shadow Analysis

Lunar surface appearance changes significantly depending on solar illumination.

CE-BL incorporates solar geometry information to analyze:

- Sun azimuth
- Sun elevation
- Solar incidence
- Potential shadow-affected regions

This information can help interpret correspondence failures caused by large illumination differences between sensor observations.

---

## 🔄 Image Registration Workflow

The general workflow of the prototype is:

```text
Input Lunar Images
        │
        ▼
Image Preprocessing & Normalization
        │
        ▼
Layer 1: Primary Correspondence
        │
        ▼
Layer 2: Classical Fallback
        │
        ▼
Layer 3: Spatial Distribution Improvement
        │
        ▼
Outlier Rejection using RANSAC
        │
        ▼
Geometric Transformation
        │
        ▼
Registered Image
        │
        ▼
Evaluation & Confidence Metrics