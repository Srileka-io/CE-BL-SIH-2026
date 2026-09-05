import streamlit as st
import pandas as pd
import numpy as np
import cv2
import os
import sys
os.environ['OPENCV_IO_MAX_IMAGE_PIXELS'] = str(pow(2, 40))
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

st.set_page_config(page_title="CE-BL Registration Dashboard", layout="wide")

# ---------------------------------------------------------------------------
# GLOBAL STYLE: colorful 3D clay-glassmorphism
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background: linear-gradient(-45deg, #1a1240, #3a1c5c, #0f2a4a, #4a1942, #12203f, #2d0a4e);
    background-size: 400% 400%;
    animation: gradientShift 20s ease infinite;
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp::before {
    content: "";
    position: fixed;
    top: -15%; left: -10%;
    width: 45%; height: 45%;
    background: radial-gradient(circle, rgba(255,60,180,0.30), transparent 70%);
    filter: blur(70px);
    z-index: 0;
    pointer-events: none;
    animation: floatBlob 14s ease-in-out infinite alternate;
}
.stApp::after {
    content: "";
    position: fixed;
    bottom: -15%; right: -10%;
    width: 50%; height: 50%;
    background: radial-gradient(circle, rgba(0,220,255,0.28), transparent 70%);
    filter: blur(70px);
    z-index: 0;
    pointer-events: none;
    animation: floatBlob 18s ease-in-out infinite alternate-reverse;
}
@keyframes floatBlob {
    0%   { transform: translate(0px, 0px) scale(1); }
    100% { transform: translate(30px, -20px) scale(1.15); }
}

h1 {
    background: linear-gradient(90deg, #ff6ec4, #ffd166, #7873f5, #4ade80, #38bdf8);
    background-size: 300% 300%;
    animation: gradientShift 8s ease infinite;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    filter: drop-shadow(0 3px 0 rgba(0,0,0,0.25)) drop-shadow(0 6px 14px rgba(120,60,255,0.35));
}

h2 {
    color: #f5f5ff !important;
    font-weight: 700 !important;
    letter-spacing: -0.2px;
}

[data-testid="stCaptionContainer"] p, .stCaption {
    color: #cfcfef !important;
}

.section-chip {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.3px;
    margin-bottom: 10px;
    color: #fff;
    box-shadow:
        3px 3px 8px rgba(0,0,0,0.30),
        -2px -2px 6px rgba(255,255,255,0.08);
}
.chip-pink   { background: linear-gradient(135deg, #ff6ec4, #b5179e); }
.chip-cyan   { background: linear-gradient(135deg, #38bdf8, #0e7490); }
.chip-orange { background: linear-gradient(135deg, #fb923c, #c2410c); }
.chip-green  { background: linear-gradient(135deg, #4ade80, #15803d); }
.chip-purple { background: linear-gradient(135deg, #a78bfa, #6d28d9); }

[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-radius: 28px !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    box-shadow:
        10px 10px 28px rgba(0, 0, 0, 0.35),
        -8px -8px 24px rgba(255, 255, 255, 0.05),
        inset 1px 1px 1px rgba(255, 255, 255, 0.25),
        inset -2px -2px 8px rgba(0, 0, 0, 0.15) !important;
    padding: 1.6rem 1.8rem !important;
    margin-bottom: 1.6rem;
    transition: transform 0.35s ease, box-shadow 0.35s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-5px);
    box-shadow:
        14px 14px 34px rgba(0, 0, 0, 0.4),
        -8px -8px 26px rgba(255, 255, 255, 0.06),
        inset 1px 1px 1px rgba(255, 255, 255, 0.3),
        inset -2px -2px 8px rgba(0, 0, 0, 0.15) !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.10), rgba(255,255,255,0.03));
    border-radius: 18px;
    padding: 14px 18px;
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow:
        6px 6px 16px rgba(0,0,0,0.30),
        -4px -4px 12px rgba(255,255,255,0.05);
}
[data-testid="stMetricLabel"] { color: #c3c3ec !important; }
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    text-shadow: 0 2px 6px rgba(120,60,255,0.5);
}
[data-testid="stMetricDelta"] { color: #4ade80 !important; }

[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.14);
    box-shadow: 6px 6px 18px rgba(0,0,0,0.28);
}

[data-testid="stImage"] {
    padding: 10px;
    background: rgba(255,255,255,0.05);
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.14);
}
[data-testid="stImage"] img {
    border-radius: 16px;
    box-shadow: 0 6px 26px rgba(120, 60, 255, 0.40);
}

[data-testid="stAlert"] {
    background: linear-gradient(145deg, rgba(56,189,248,0.16), rgba(56,189,248,0.06)) !important;
    border: 1px solid rgba(56,189,248,0.35) !important;
    border-radius: 18px !important;
    color: #e0f2fe !important;
    box-shadow: 5px 5px 16px rgba(0,0,0,0.25), inset 1px 1px 2px rgba(255,255,255,0.15) !important;
}

div[data-baseweb="notification"] {
    border-radius: 18px !important;
}

hr { border-color: rgba(255,255,255,0.15) !important; }

.footer-caption {
    text-align: center;
    color: #a5a5d8;
    padding-top: 0.5rem;
}

.custom-notice {
    background: linear-gradient(145deg, rgba(167,139,250,0.16), rgba(167,139,250,0.06));
    border: 1px solid rgba(167,139,250,0.35);
    border-radius: 18px;
    padding: 16px 20px;
    color: #ede9fe;
    box-shadow: 5px 5px 16px rgba(0,0,0,0.25), inset 1px 1px 2px rgba(255,255,255,0.15);
}
.custom-notice code {
    background: rgba(255,255,255,0.12);
    padding: 1px 6px;
    border-radius: 6px;
    color: #fff;
}

/* --- Sidebar navigation styling --- */
[data-testid="stSidebar"] {
    background: rgba(20, 12, 45, 0.55) !important;
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.10);
}
[data-testid="stSidebar"] h2 {
    background: linear-gradient(90deg, #ff6ec4, #a78bfa, #38bdf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #cfcfef !important;
}
div[role="radiogroup"] > label {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 14px;
    padding: 10px 14px;
    margin-bottom: 8px;
    transition: all 0.2s ease;
    width: 100%;
}
div[role="radiogroup"] > label:hover {
    background: rgba(167,139,250,0.18);
    border-color: rgba(167,139,250,0.45);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Registration + evaluation helper functions (used by Stage 5)
# ---------------------------------------------------------------------------

STAGE5_MAX_DIM = 2048


def load_image_any(path):
    if not os.path.exists(path):
        return None
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    return img


def downsample_for_registration(img, max_dim=STAGE5_MAX_DIM):
    h, w = img.shape[:2]
    scale = max_dim / max(h, w)
    if scale >= 1.0:
        return img.copy(), 1.0
    new_w, new_h = int(round(w * scale)), int(round(h * scale))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, scale


def register_and_evaluate(src_img_full, ref_img_full, pts_src_full, pts_ref_full):
    src_small, scale_src = downsample_for_registration(src_img_full)
    ref_small, scale_ref = downsample_for_registration(ref_img_full)

    pts_src = (np.float32(pts_src_full) * scale_src).reshape(-1, 1, 2)
    pts_ref = (np.float32(pts_ref_full) * scale_ref).reshape(-1, 1, 2)

    H, mask = cv2.findHomography(pts_src, pts_ref, cv2.RANSAC, ransacReprojThreshold=3.0)

    if H is None:
        return None, {
            "Total Matches": len(pts_src),
            "Inlier Count": 0,
            "Inlier Ratio": 0.0,
            "RMSE (pixels, downsampled space)": "N/A",
        }, None, src_small, ref_small

    inlier_mask = mask.ravel().astype(bool)

    h, w = ref_small.shape[:2]
    warped_img = cv2.warpPerspective(src_small, H, (w, h))

    inlier_count = int(inlier_mask.sum())
    total_matches = len(pts_src)
    inlier_ratio = inlier_count / total_matches if total_matches > 0 else 0.0

    src_inliers = pts_src[inlier_mask]
    ref_inliers = pts_ref[inlier_mask]
    projected = cv2.perspectiveTransform(src_inliers, H)
    errors = np.linalg.norm(projected - ref_inliers, axis=2).ravel()
    rmse = float(np.sqrt(np.mean(errors ** 2))) if len(errors) > 0 else None

    metrics = {
        "Total Matches": total_matches,
        "Inlier Count": inlier_count,
        "Inlier Ratio": round(inlier_ratio, 4),
        "RMSE (pixels, downsampled space)": round(rmse, 4) if rmse is not None else "N/A",
    }

    checker = make_checkerboard(warped_img, ref_small)
    return warped_img, metrics, checker, src_small, ref_small


def make_checkerboard(img_a, img_b, block_size=40):
    if img_a.shape != img_b.shape:
        img_b = cv2.resize(img_b, (img_a.shape[1], img_a.shape[0]))
    h, w = img_a.shape[:2]
    checker = np.zeros_like(img_a)
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = img_a if ((x // block_size) + (y // block_size)) % 2 == 0 else img_b
            checker[y:y+block_size, x:x+block_size] = block[y:y+block_size, x:x+block_size]
    return checker


# ---------------------------------------------------------------------------
# Page render functions — one per stage
# ---------------------------------------------------------------------------

def page_overview():
    st.title("CE-BL: Cross-Sensor Extraction & Blending of Lunar Imagery")
    st.caption("SIH 2026 — Problem Statement ID 26166 — Live Confidence Dashboard")
    st.markdown("Use the sidebar to navigate between pipeline stages.")


def page_stage1():
    st.markdown('<span class="section-chip chip-pink">🎯 STAGE 1</span>', unsafe_allow_html=True)
    st.header("1. Three-Tier Fallback: Evaluation Summary")
    csv_path = "data/evaluation_summary.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        st.dataframe(df, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        best_layer = df.loc[df["inlier_ratio"].idxmax()]
        col1.metric("Best Inlier Ratio", f"{best_layer['inlier_ratio']:.3f}", best_layer["layer"])
        if df["rmse"].notna().any():
            best_rmse_row = df.dropna(subset=["rmse"]).loc[df.dropna(subset=["rmse"])["rmse"].idxmin()]
            col2.metric("Best RMSE (px)", f"{best_rmse_row['rmse']:.3f}", best_rmse_row["layer"])
        col3.metric("Total Matches (Layer 1)", int(df[df["layer"].str.contains("Layer 1")]["total_matches"].values[0]))
    else:
        st.markdown('<div class="custom-notice">No evaluation summary found. Run <code>src/evaluate.py</code> first.</div>', unsafe_allow_html=True)


def page_stage2():
    st.markdown('<span class="section-chip chip-cyan">🌗 STAGE 2</span>', unsafe_allow_html=True)
    st.header("2. Registered Image Pair (Cropped Overlap Region)")
    img_col1, img_col2 = st.columns(2)
    if os.path.exists("data/ohrc_crop.png"):
        img_col1.image("data/ohrc_crop.png", caption="OHRC (cropped overlap)", use_container_width=True)
    if os.path.exists("data/tmc2_crop.png"):
        img_col2.image("data/tmc2_crop.png", caption="TMC-2 (cropped overlap)", use_container_width=True)


def page_stage3():
    st.markdown('<span class="section-chip chip-orange">🌑 STAGE 3</span>', unsafe_allow_html=True)
    st.header("3. Predictive Shadow-Modeling Output")
    shadow_col1, shadow_col2 = st.columns(2)
    if os.path.exists("data/ohrc_shadow_mask.png"):
        shadow_col1.image("data/ohrc_shadow_mask.png", caption="OHRC predicted shadow mask (sun elev. 2.4°)", use_container_width=True)
    if os.path.exists("data/tmc2_shadow_mask.png"):
        shadow_col2.image("data/tmc2_shadow_mask.png", caption="TMC-2 predicted shadow mask (sun elev. 52.7°)", use_container_width=True)


def page_stage4():
    st.markdown('<span class="section-chip chip-green">☀️ STAGE 4</span>', unsafe_allow_html=True)
    st.header("4. Extracted Solar Geometry (from PDS4 Metadata)")
    if os.path.exists("data/sun_angles.csv"):
        sun_data = pd.read_csv("data/sun_angles.csv")
        sun_data = sun_data.rename(columns={
            "scene": "Scene",
            "sun_azimuth": "Sun Azimuth (°)",
            "sun_elevation": "Sun Elevation (°)",
            "solar_incidence": "Solar Incidence (°)",
        })
        st.dataframe(sun_data, use_container_width=True)
    else:
        st.markdown('<div class="custom-notice">data/sun_angles.csv not found. Run <code>src/extract_sun_angles.py</code> first.</div>', unsafe_allow_html=True)
    st.info("OHRC's near-horizon sun elevation (2.4°) explains the extreme illumination mismatch with TMC-2 and the resulting Layer 2 (classical) matching failure.")


def page_stage5():
    st.markdown('<span class="section-chip chip-purple">🛰️ STAGE 5</span>', unsafe_allow_html=True)
    st.header("5. Registration Output & Alignment Verification")
    st.caption("This is the PS-required deliverable: the registered image, plus RMSE / inlier count / inlier ratio.")
    st.caption(f"Note: for performance/stability, warping and RMSE are computed on images downsampled to max {STAGE5_MAX_DIM}px on the long side, not full native resolution.")

    matches_csv = "data/matches_subpixel.csv" if os.path.exists("data/matches_subpixel.csv") else "data/matches.csv"
    src_path = "data/ohrc_crop.png"
    ref_path = "data/tmc2_crop.png"

    if os.path.exists(matches_csv) and os.path.exists(src_path) and os.path.exists(ref_path):
        matches_df = pd.read_csv(matches_csv)
        pts_src = matches_df[["src_x", "src_y"]].to_numpy()
        pts_ref = matches_df[["ref_x", "ref_y"]].to_numpy()

        src_img_full = load_image_any(src_path)
        ref_img_full = load_image_any(ref_path)

        if len(pts_src) < 4:
            st.markdown(
                f'<div class="custom-notice">Only {len(pts_src)} match points found in {matches_csv} — need at least 4 to compute a homography.</div>',
                unsafe_allow_html=True,
            )
        else:
            warped_img, metrics, checker, src_small, ref_small = register_and_evaluate(
                src_img_full, ref_img_full, pts_src, pts_ref
            )

            if warped_img is None:
                st.markdown(
                    '<div class="custom-notice">Homography estimation failed (cv2.findHomography returned None). '
                    'Check that matches points are correctly ordered (src_x/src_y from the OHRC crop, ref_x/ref_y from the TMC-2 crop) '
                    'and not degenerate (all collinear, etc).</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.subheader("Evaluation Metrics")
                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                metric_col1.metric("Total Matches", metrics["Total Matches"])
                metric_col2.metric("Inlier Count", metrics["Inlier Count"])
                metric_col3.metric("Inlier Ratio", metrics["Inlier Ratio"])
                metric_col4.metric("RMSE (px)", metrics["RMSE (pixels, downsampled space)"])

                if "subpixel_residual_px" in matches_df.columns:
                    valid_residuals = matches_df["subpixel_residual_px"].dropna()
                    if len(valid_residuals) > 0:
                        st.caption(f"Mean sub-pixel refinement residual: {valid_residuals.mean():.4f} px across {len(valid_residuals)} refined points.")

                st.subheader("Before / After Registration")
                b_col1, b_col2, b_col3 = st.columns(3)
                with b_col1:
                    st.image(cv2.cvtColor(src_small, cv2.COLOR_BGR2RGB), caption="Source (before, downsampled)", use_container_width=True)
                with b_col2:
                    st.image(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB), caption="Warped (registered)", use_container_width=True)
                with b_col3:
                    st.image(cv2.cvtColor(ref_small, cv2.COLOR_BGR2RGB), caption="Reference (downsampled)", use_container_width=True)

                st.subheader("Checkerboard Alignment Check")
                st.image(cv2.cvtColor(checker, cv2.COLOR_BGR2RGB),
                          caption="Alternating blocks: registered vs. reference — visible seams indicate misalignment",
                          use_container_width=True)

                st.subheader("Blend / Swipe Comparison")
                blend_alpha = st.slider("Slide to compare warped ↔ reference", 0.0, 1.0, 0.5)
                blended = cv2.addWeighted(warped_img, blend_alpha, ref_small, 1 - blend_alpha, 0)
                st.image(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB), caption="Blend slider", use_container_width=True)
    else:
        st.markdown("""
        <div class="custom-notice">
            Missing <code>data/matches.csv</code> / <code>data/matches_subpixel.csv</code> (columns: <code>src_x, src_y, ref_x, ref_y</code>, in FULL-RES crop pixel coordinates) or the cropped images.
            Export your Layer 1 matcher's keypoint pairs to populate this section.
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------

PAGES = {
    "🏠 Overview": page_overview,
    "🎯 Stage 1 — Evaluation Summary": page_stage1,
    "🌗 Stage 2 — Cropped Imagery": page_stage2,
    "🌑 Stage 3 — Shadow Modeling": page_stage3,
    "☀️ Stage 4 — Solar Geometry": page_stage4,
    "🛰️ Stage 5 — Registration Output": page_stage5,
}

with st.sidebar:
    st.markdown("## CE-BL Navigator")
    selection = st.radio("Go to:", list(PAGES.keys()), label_visibility="collapsed")

with st.container(border=True):
    PAGES[selection]()

st.divider()
st.markdown('<p class="footer-caption">CE-BL prototype — Team CE-BL — SIH 2026</p>', unsafe_allow_html=True)