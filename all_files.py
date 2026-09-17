import rasterio as rio

file = r"E:\Sakshi\lab4\sentinel\T44PMV_20260901T045701_B02.tif"

with rio.open(file) as src:
    print("Dimensions:", src.width, "x", src.height)
    print("Total Bands:", src.count)
    print("CRS:", src.crs)
    
    #Q2
    import rasterio
import matplotlib.pyplot as plt
import numpy as np

# Open the stacked TIFF file
file = r"E:\Sakshi\lab4\sentinel\stacked.tif"

with rasterio.open(file) as src:

    # Calculate statistics for all bands
    for i in range(1, src.count + 1):
        band = src.read(i)

        print("Band", i)
        print("Minimum:", np.min(band))
        print("Maximum:", np.max(band))
        print("Mean:", np.mean(band))
        print("------------------")

    # Histogram of Band 2
    band2 = src.read(2)

    plt.figure()
    plt.hist(band2.flatten(), bins=50)
    plt.title("Histogram of Band 2")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    # Histogram of Band 3
    band3 = src.read(3)

    plt.figure()
    plt.hist(band3.flatten(), bins=50)
    plt.title("Histogram of Band 3")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()

    # Histogram of Band 4
    band4 = src.read(4)

    plt.figure()
    plt.hist(band4.flatten(), bins=50)
    plt.title("Histogram of Band 4")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.show()
    
    #Q3
    import rasterio as rio
from rasterio.warp import reproject, Resampling
import numpy as np
import os

file_path= r"E:\Sakshi\lab4\sentinel"

# B01 to B12
files = [
    os.path.join(folder, "T44PMV_20260901T045701_B01.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B02.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B03.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B04.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B05.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B06.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B07.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B08.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B09.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B10.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B11.tif"),
    os.path.join(folder, "T44PMV_20260901T045701_B12.tif")
]

# Use B02 as reference
with rio.open(files[1]) as src:
    profile = src.profile.copy()
    height = src.height
    width = src.width
    transform = src.transform
    crs = src.crs

profile.update(count=12)

# Create stacked image
with rio.open("stacked.tif", "w", **profile) as dst:

    for i, file in enumerate(files, start=1):

        with rio.open(file) as src:

            data = np.empty((height, width), dtype=src.dtypes[0])

            reproject(
                source=rio.band(src, 1),
                destination=data,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=crs,
                resampling=Resampling.bilinear
            )

            dst.write(data, i)

            print("Stacked B", i)

print("Band stacking completed!")

# Check the result
with rio.open("stacked.tif") as src:
    print("Dimensions:", src.width, "x", src.height)
    print("Total Bands:", src.count)
    print("CRS:", src.crs)
    
#Q4
import rasterio as rio
from rasterio.warp import reproject, Resampling
from rasterio.windows import Window
import matplotlib.pyplot as plt

import numpy as np
import os

folder = r"E:\Sakshi\lab4\sentinel"

with rio.open("stacked.tif") as src:
    data = src.read()
    
def normalize(band):
    band = band.astype(float)
    return (band - band.min()) / (band.max() - band.min())

# TRUE COLOR COMPOSITE 
nir = data[4]       # Band 5
red = data[3]       # Band 4
green = data[2]     # Band 3
blue = data[1]      # Band 2

true_color = np.dstack((
    normalize(red),
    normalize(green),
    normalize(blue)
))

plt.imshow(true_color)
plt.title("True Color Composite - sentinel")
plt.axis("off")
plt.show()

# FALSE COLOR COMPOSITE 
false_color = np.dstack((
    normalize(nir),
    normalize(red),
    normalize(green)
))

plt.imshow(false_color)
plt.title("False Color Composite - sentinel")
plt.axis("off")
plt.show()

#Q5
import rasterio
from rasterio.windows import Window

# 1. Define paths
input_raster =  r"E:\Sakshi\lab4\sentinel\stacked.tif"
output_raster = "clipped_aoi.tif"

# 2. Define coordinates of your AOI (must match the image's coordinate system)
# Example: X (Longitude/Easting), Y (Latitude/Northing)
left_x, bottom_y = 500000, 4500000
right_x, top_y = 505000, 4505000

with rasterio.open(input_raster) as src:
    # Transform map coordinates to image pixel rows and columns
    top_row, left_col = src.index(left_x, top_y)
    bottom_row, right_col = src.index(right_x, bottom_y)
    
    # Calculate width and height in pixels
    width = right_col - left_col
    height = bottom_row - top_row
    
    # 3. Create the pixel window
    window = Window(left_col, top_row, width, height)
    
    # 4. Read data from the window
    clipped_data = src.read(window=window)
    
    # 5. Update metadata with new dimensions and spatial location
    kwargs = src.meta.copy()
    kwargs.update({
        "height": height,
        "width": width,
        "transform": rasterio.windows.transform(window, src.transform)
    })
    
    # 6. Write the new file
    with rasterio.open(output_raster, "w", **kwargs) as dst:
        dst.write(clipped_data)

print(f"Clipped image saved to: {output_raster}")

#Q6
import rasterio
import matplotlib.pyplot as plt

# -----------------------------
# 1. Open Sentinel-2 image
# -----------------------------
file_path = r"E:\Sakshi\lab4\sentinel\stacked.tif"

src = rasterio.open(file_path)

# -----------------------------
# 2. Sentinel-2 band wavelengths
# -----------------------------
wavelengths = [
    0.490,   # B2 Blue
    0.560,   # B3 Green
    0.665,   # B4 Red
    0.705,   # B5 Red Edge 1
    0.740,   # B6 Red Edge 2
    0.783,   # B7 Red Edge 3
    0.842,   # B8 NIR
    1.610,   # B11 SWIR 1
    2.190    # B12 SWIR 2
]

# Corresponding band numbers in the GeoTIFF
bands = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# -----------------------------
# 3. Select pixels
#    (row, column)
# -----------------------------
pixels = {
    "Vegetation": (500, 500),
    "Water":      (600, 600),
    "Urban":      (700, 700),
    "Built-up":   (800, 800)
}

# -----------------------------
# 4. Extract reflectance values
# -----------------------------
spectral_values = {}

for category, (row, col) in pixels.items():

    values = []

    for band in bands:
        value = src.read(band)[row, col]

        # If image is scaled by 10000
        value = value / 10000

        values.append(value)

    spectral_values[category] = values

# -----------------------------
# 5. Plot spectral signatures
# -----------------------------
plt.figure(figsize=(10, 6))

for category, values in spectral_values.items():
    plt.plot(
        wavelengths,
        values,
        marker='o',
        linewidth=2,
        label=category
    )

plt.xlabel("Wavelength (µm)")
plt.ylabel("Reflectance")
plt.title("Spectral Signature of Different Land-use Categories")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.show()

# -----------------------------
# 6. Print values
# -----------------------------
print("\nSpectral Reflectance Values:\n")

for category, values in spectral_values.items():
    print(category)
    for wavelength, value in zip(wavelengths, values):
        print(f"{wavelength:.3f} µm : {value:.4f}")
    print()

#Q7
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# FILE PATH
# =========================================================

file_path = r"E:\Sakshi\lab4\sentinel\stacked.tif"

# =========================================================
# SETTINGS
# =========================================================

# NDVI threshold
threshold = 0.3

# Band numbers in your stacked image
# B4 = Red
# B8 = NIR
RED_BAND = 3
NIR_BAND = 7

# =========================================================
# OPEN IMAGE
# =========================================================

with rasterio.open(file_path) as src:

    print("Number of bands:", src.count)
    print("Image size:", src.width, "x", src.height)
    print("CRS:", src.crs)

    # Pixel size
    pixel_width = abs(src.transform.a)
    pixel_height = abs(src.transform.e)

    pixel_area = pixel_width * pixel_height

    print("\nPixel size:")
    print(pixel_width, "m x", pixel_height, "m")

    print("Pixel area:", pixel_area, "m²")

    # =====================================================
    # CREATE SMALL ARRAYS ONLY FOR DISPLAY
    # =====================================================

    display_size = 1000

    scale = max(
        src.width // display_size,
        src.height // display_size
    )

    out_height = src.height // scale
    out_width = src.width // scale

    # Read RED and NIR as downsampled arrays
    red_small = src.read(
        RED_BAND,
        out_shape=(1, out_height, out_width),
        resampling=rasterio.enums.Resampling.average
    ).astype(np.float32)

    nir_small = src.read(
        NIR_BAND,
        out_shape=(1, out_height, out_width),
        resampling=rasterio.enums.Resampling.average
    ).astype(np.float32)

    # =====================================================
    # NDVI FOR DISPLAY
    # =====================================================

    denominator = nir_small + red_small

    ndvi_small = np.zeros_like(red_small)

    valid = denominator != 0

    ndvi_small[valid] = (
        (nir_small[valid] - red_small[valid])
        / denominator[valid]
    )

    # =====================================================
    # PLOT NDVI MAP
    # =====================================================

    plt.figure(figsize=(10, 7))

    plt.imshow(
        ndvi_small,
        cmap="RdYlGn",
        vmin=-1,
        vmax=1
    )

    plt.colorbar(label="NDVI")

    plt.title("NDVI Map")

    plt.xlabel("Column")
    plt.ylabel("Row")

    plt.tight_layout()

    plt.savefig(
        "NDVI_map.png",
        dpi=200
    )

    plt.show()

    # =====================================================
    # FULL RESOLUTION VEGETATION AREA
    # =====================================================

    vegetation_pixels = 0

    total_valid_pixels = 0

    print("\nCalculating vegetation area...")
    print("Please wait...")

    # Process image in blocks
    for _, window in src.block_windows(RED_BAND):

        red = src.read(
            RED_BAND,
            window=window
        ).astype(np.float32)

        nir = src.read(
            NIR_BAND,
            window=window
        ).astype(np.float32)

        denominator = nir + red

        valid = denominator != 0

        ndvi = np.zeros_like(red)

        ndvi[valid] = (
            (nir[valid] - red[valid])
            / denominator[valid]
        )

        # Count valid pixels
        total_valid_pixels += np.sum(valid)

        # Count vegetation pixels
        vegetation_pixels += np.sum(
            (ndvi >= threshold) & valid
        )

    # =====================================================
    # VEGETATION AREA
    # =====================================================

    vegetation_area_m2 = (
        vegetation_pixels * pixel_area
    )

    vegetation_area_hectares = (
        vegetation_area_m2 / 10000
    )

    vegetation_area_km2 = (
        vegetation_area_m2 / 1000000
    )

    print("\n===================================")
    print("VEGETATION RESULTS")
    print("===================================")

    print("NDVI threshold:", threshold)

    print("Vegetation pixels:",
          vegetation_pixels)

    print("Vegetated area:",
          vegetation_area_m2,
          "m²")

    print("Vegetated area:",
          vegetation_area_hectares,
          "hectares")

    print("Vegetated area:",
          vegetation_area_km2,
          "km²")

    # =====================================================
    # VEGETATION MAP FOR DISPLAY
    # =====================================================

    vegetation_small = np.where(
        ndvi_small >= threshold,
        1,
        0
    )

    plt.figure(figsize=(10, 7))

    plt.imshow(
        vegetation_small,
        cmap="gray",
        vmin=0,
        vmax=1
    )

    cbar = plt.colorbar(
        ticks=[0, 1]
    )

    cbar.ax.set_yticklabels([
        "No Vegetation (0)",
        "Vegetation (1)"
    ])

    plt.title(
        "Vegetated Landcover Map"
    )

    plt.xlabel("Column")
    plt.ylabel("Row")

    plt.tight_layout()

    plt.savefig(
        "vegetation_map.png",
        dpi=200
    )

    plt.show()

    print("\n===================================")
    print("FILES CREATED")
    print("===================================")

    print("NDVI map:")
    print("NDVI_map.png")

    print("\nVegetation map:")
    print("vegetation_map.png")