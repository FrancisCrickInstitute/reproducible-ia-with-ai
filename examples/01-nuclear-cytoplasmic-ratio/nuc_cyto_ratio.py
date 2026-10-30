"""
YAP/TAZ nuclear:cytoplasmic (N:C) ratio from 4-channel microscopy TIFs
======================================================================

WHAT THE SCRIPT DOES
  1. Loads a 4-channel TIF: 1 = DAPI, 2 = Tubulin, 3 = Actin, 4 = YAP/TAZ.
  2. Segments whole cells with the Cellpose 3 'cyto3' model (Actin + DAPI channels).
  3. Segments nuclei with the same 'cyto3' model (DAPI channel only).
     Only cyto3 is used because it is the one Cellpose 3 model with a backup
     copy on Hugging Face (the cellpose.org model server can fail with HTTP 500).
  4. Defines nucleus = nuclear pixels inside a cell, and
     cytoplasm = cell pixels outside the nucleus.
  5. Measures mean YAP/TAZ intensity in each compartment, pooled over all cells
     in the image, and calculates the N:C ratio.
  6. Saves an overlay PNG for each image and one CSV for all images.

HOW TO RUN (step by step)
  1. Install Miniconda (if you do not already have conda):
     https://docs.conda.io/en/latest/miniconda.html
  2. Open a terminal ("Anaconda Prompt" on Windows, "Terminal" on Mac/Linux).
  3. Create a fresh Python environment:
         conda create -n yap python=3.10 -y
  4. Activate it (repeat this step every time you open a new terminal):
         conda activate yap
  5. Install the required packages. Cellpose MUST be version 3: version 4
     changed the interface this script uses.
         pip install "cellpose>=3,<4" tifffile scikit-image matplotlib pandas
     (Optional, for speed: if you have an NVIDIA GPU, install the CUDA build
      of PyTorch first, following https://pytorch.org/get-started/locally/.
      Without a GPU the script still works on the CPU, just more slowly.)
  6. Save this script as "yap_taz_nc_ratio.py", e.g. in the folder with your images.
  7. In the terminal, move into that folder:
         cd path/to/your/folder
  8. Run the script on one image, several images, or a wildcard pattern:
         python yap_taz_nc_ratio.py my_image.tif
         python yap_taz_nc_ratio.py image1.tif image2.tif
         python yap_taz_nc_ratio.py "*.tif"
  9. The first run downloads the cyto3 model (~27 MB) from Hugging Face into
     Cellpose's model folder (~/.cellpose/models), so an internet connection
     is needed once. If that download is blocked, download it manually from
     https://huggingface.co/spaces/mouseland/cellpose/resolve/main/cyto3
     and save it as a file named "cyto3" (no extension) in that folder,
     e.g. C:\\Users\\<you>\\.cellpose\\models\\cyto3 on Windows.
  10. Outputs (written to the current folder):
         <image name>_overlay.png  - Actin (red), YAP/TAZ (green), DAPI (blue),
                                     cell outlines in white, nuclei in yellow
         yap_taz_results.csv       - one row per image
  11. IMPORTANT: before the first real run, set CELL_DIAMETER and NUC_DIAMETER
      in the SETTINGS section below to the typical diameter of a cell and of a
      nucleus in YOUR images, in pixels (measure a few with the line tool in
      Fiji/ImageJ). Cellpose cannot estimate these automatically here, because
      its size models are only available from the cellpose.org server.
      Open the overlay PNGs to check the segmentation; if cells or nuclei are
      split (diameter too small) or merged (too large), adjust and run again.

NOTE: the TIF must be a single 2D plane with 4 channels, stored either as
(channels, height, width) or (height, width, channels). For z-stacks, make a
maximum projection (e.g. in Fiji) first.
"""

import sys
import glob
import os
import urllib.request
import numpy as np
import pandas as pd
import tifffile
import matplotlib.pyplot as plt
from skimage.segmentation import find_boundaries, clear_border
from cellpose import models

# ----------------------------- SETTINGS ------------------------------------
# Channel positions in the file, counted from 0 (so channel 1 -> 0, etc.)
DAPI, TUBULIN, ACTIN, YAP = 0, 1, 2, 3

CELL_DIAMETER = 50     # typical cell diameter in pixels -> MEASURE AND SET FOR YOUR IMAGES
NUC_DIAMETER = 30      # typical nucleus diameter in pixels -> MEASURE AND SET FOR YOUR IMAGES
USE_GPU = True         # Cellpose falls back to the CPU automatically if no GPU is found
REMOVE_EDGE_CELLS = False     # ignore cells touching the image border (they are incomplete)
SUBTRACT_BACKGROUND = False   # subtract the median YAP/TAZ signal outside cells (camera offset etc.)
OUTPUT_CSV = "yap_taz_results.csv"
# ---------------------------------------------------------------------------


def load_image(path):
    """Read the TIF and return it as a float array shaped (4, height, width)."""
    img = tifffile.imread(path).squeeze()      # squeeze removes empty dimensions
    if img.ndim == 3 and img.shape[0] != 4:    # channels stored last -> move them first
        img = np.moveaxis(img, -1, 0)
    if img.ndim != 3 or img.shape[0] != 4:
        raise ValueError(f"{path}: expected a 2D image with 4 channels, got shape {img.shape}")
    return img.astype(np.float32)


def normalise(channel):
    """Stretch a channel to 0-1 for display (1st to 99.8th percentile)."""
    lo, hi = np.percentile(channel, (1, 99.8))
    return np.clip((channel - lo) / (hi - lo + 1e-9), 0, 1)


# Make sure the cyto3 model file is in Cellpose's model folder. Cellpose would
# normally fetch it from cellpose.org; we fetch it from the Hugging Face copy
# instead. Once the file is there, Cellpose uses it without downloading.
CYTO3_URL = "https://huggingface.co/spaces/mouseland/cellpose/resolve/main/cyto3"
cyto3_file = models.MODEL_DIR / "cyto3"
if not cyto3_file.exists():
    print(f"Downloading cyto3 model to {cyto3_file} ...")
    cyto3_file.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(CYTO3_URL, cyto3_file)

# Load the model once; it is used for both cells and nuclei in every image.
# CellposeModel (rather than models.Cellpose) is used because it does not need
# the separate size-estimation model, which only exists on cellpose.org.
model = models.CellposeModel(gpu=USE_GPU, model_type="cyto3")

# Expand wildcards ourselves so "*.tif" also works on Windows
files = [f for pattern in sys.argv[1:] for f in sorted(glob.glob(pattern))]
if not files:
    sys.exit("Usage: python yap_taz_nc_ratio.py image.tif [more images or *.tif]")

results = []
for path in files:
    print(f"Processing {path} ...")
    img = load_image(path)

    # --- 1. Segmentation ---------------------------------------------------
    # Cellpose numbers channels from 1, with 0 meaning "none".
    # channels=[cytoplasm channel, nucleus channel]; channel_axis=0 says the
    # channels are the first dimension of the array.
    # eval() returns (masks, flows, styles); we only need masks, which are
    # label images: 0 = background, 1, 2, 3... = individual objects.
    # Cells: Actin as the cytoplasm channel, DAPI as the nucleus channel.
    cells = model.eval(img, channels=[ACTIN + 1, DAPI + 1],
                       channel_axis=0, diameter=CELL_DIAMETER)[0]
    # Nuclei: DAPI on its own (cyto3 was also trained on nuclear images).
    nuclei = model.eval(img, channels=[DAPI + 1, 0],
                        channel_axis=0, diameter=NUC_DIAMETER)[0]

    if REMOVE_EDGE_CELLS:
        cells = clear_border(cells)   # drop cells cut off by the image edge

    in_cell = cells > 0              # True for every pixel belonging to a cell
    nuclei[~in_cell] = 0             # keep only nuclei (parts) that lie inside cells

    # --- 2. Define compartments --------------------------------------------
    nuc_px = nuclei > 0                  # nucleus: nuclear pixels inside cells
    cyt_px = in_cell & (nuclei == 0)     # cytoplasm: cell pixels outside nuclei

    if not nuc_px.any() or not cyt_px.any():
        print(f"  WARNING: no cells/nuclei found in {path}, skipping.")
        continue

    # --- 3. Measure YAP/TAZ -------------------------------------------------
    yap = img[YAP]
    # Background = median signal outside cells. Removing it matters because an
    # offset added to both compartments pushes the ratio towards 1.
    background = np.median(yap[~in_cell]) if SUBTRACT_BACKGROUND and (~in_cell).any() else 0.0
    mean_nuc = yap[nuc_px].mean() - background
    mean_cyt = yap[cyt_px].mean() - background
    ratio = mean_nuc / mean_cyt

    print(f"  {cells.max()} labelled cells | nucleus {mean_nuc:.1f} | "
          f"cytoplasm {mean_cyt:.1f} | N:C ratio {ratio:.2f}")

    results.append({
        "Input filename": os.path.basename(path),
        "Mean Intensity of YAP/TAZ in Nuclei": mean_nuc,
        "Mean Intensity of YAP/TAZ in Cytoplasm": mean_cyt,
        "Nuclear:Cytoplasmic ratio of YAP/TAZ intensity": ratio,
    })

    # --- 4. Overlay image ---------------------------------------------------
    # RGB composite: Actin = red, YAP/TAZ = green, DAPI = blue
    rgb = np.dstack([normalise(img[ACTIN]), normalise(yap), normalise(img[DAPI])])
    rgb[find_boundaries(cells, mode="inner")] = [1, 1, 1]    # cell outlines: white
    rgb[find_boundaries(nuclei, mode="inner")] = [1, 1, 0]   # nucleus outlines: yellow
    overlay_name = os.path.splitext(os.path.basename(path))[0] + "_overlay.png"
    plt.imsave(overlay_name, rgb)

# --- 5. Save all results to one CSV -------------------------------------------
pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
print(f"Done. Results saved to {OUTPUT_CSV}")