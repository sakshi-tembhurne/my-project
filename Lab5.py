import os
import zipfile
import geopandas as gpd
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Setup & Unzipping
# -----------------------------------------------------------------------------
# Define working directories and unzip files
extract_dir = r"C:\Users\jothi\OneDrive\Desktop\sakshi\data"
os.makedirs(extract_dir, exist_ok=True)

for zip_file in ["meghalaya.zip", "NE_states.zip"]:
    if os.path.exists(zip_file):
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

# Identify extracted shapefile paths
meghalaya_shp = None
ne_states_shp = None

for root, _, files in os.walk(extract_dir):
    for file in files:
        if file.endswith(".shp"):
            full_path = os.path.join(root, file)
            if "meghalaya" in file.lower():
                meghalaya_shp = full_path
            elif "ne" in file.lower() or "state" in file.lower():
                ne_states_shp = full_path

# Fallback in case naming differs inside zip
if not meghalaya_shp or not ne_states_shp:
    all_shps = [os.path.join(r, f) for r, d, fs in os.walk(extract_dir) for f in fs if f.endswith('.shp')]
    meghalaya_shp = all_shps[0]
    ne_states_shp = all_shps[1]

gdf_meghalaya = gpd.read_file(meghalaya_shp)
gdf_ne = gpd.read_file(ne_states_shp)


# -----------------------------------------------------------------------------
# Question 1: Print the projection of all shapefiles
# -----------------------------------------------------------------------------
print("--- Question 1: CRS Information ---")
print("Meghalaya Shapefile CRS:", gdf_meghalaya.crs)
print("NE States Shapefile CRS:", gdf_ne.crs)
print()


# -----------------------------------------------------------------------------
# Question 2: Check whether the shapefiles have missing attributes
# -----------------------------------------------------------------------------
print("--- Question 2: Missing Attributes ---")
print("Meghalaya Missing Values:\n", gdf_meghalaya.isnull().sum())
print("\nNE States Missing Values:\n", gdf_ne.isnull().sum())
print()


# -----------------------------------------------------------------------------
# Question 3: Reproject CRS to EPSG:4326, plot (highlight NE states), & save
# -----------------------------------------------------------------------------
print("--- Question 3: Reprojection & Export ---")
# Reproject
gdf_meghalaya_4326 = gdf_meghalaya.to_crs(epsg=4326)
gdf_ne_4326 = gdf_ne.to_crs(epsg=4326)

# Save as new shapefiles
gdf_meghalaya_4326.to_file("Meghalaya_EPSG4326.shp")
gdf_ne_4326.to_file("NE_states_EPSG4326.shp")

# Plot NE States with highlighted boundaries/colors
fig, ax = plt.subplots(figsize=(10, 8))
gdf_ne_4326.plot(ax=ax, cmap="Set3", edgecolor="black", linewidth=1.2)
# Overlay Meghalaya in a distinct highlight color if available
gdf_meghalaya_4326.plot(ax=ax, color="red", alpha=0.5, edgecolor="darkred", label="Meghalaya")

plt.title("North Eastern States (EPSG:4326)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("Q3_NE_States_EPSG4326.png")
plt.show()


# -----------------------------------------------------------------------------
# Question 4: Calculate areas of NE India, sort descending, plot bar chart
# -----------------------------------------------------------------------------
print("--- Question 4: Area Calculation & Bar Chart ---")
# Reproject to an Equal Area projected CRS (EPSG:7755 - India UTM Zone 45N or EPSG:3857) for accurate area calculation in sq km
gdf_ne_projected = gdf_ne_4326.to_crs(epsg=7755)

# Calculate area in sq kilometers
gdf_ne_projected["area_sqkm"] = gdf_ne_projected.geometry.area / 1e6

# Identify the state name column dynamically
state_col = [c for c in gdf_ne_projected.columns if "state" in c.lower() or "name" in c.lower()][0]

# Sort descending
gdf_ne_sorted = gdf_ne_projected.sort_values(by="area_sqkm", ascending=False)

# Plot Bar Chart
plt.figure(figsize=(10, 6))
plt.bar(gdf_ne_sorted[state_col], gdf_ne_sorted["area_sqkm"], color="skyblue", edgecolor="navy")
plt.xlabel("State")
plt.ylabel("Area (sq km)")
plt.title("Area of North Eastern States (Descending Order)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("Q4_NE_States_Area_Bar_Chart.png")
plt.show()


# -----------------------------------------------------------------------------
# Question 5: Download your state shapefile from GADM & plot using matplotlib
# -----------------------------------------------------------------------------
print("--- Question 5: Download & Plot State Shapefile ---")
# Downloading GADM Level 1 (States) GeoJSON/Shapefile for India directly
gadm_india_url = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IND_1.json"
gdf_india_states = gpd.read_file(gadm_india_url)

# Extract your home state (e.g., Kerala or Meghalaya)
my_state_name = "Kerala"  # Change this to your state
gdf_my_state = gdf_india_states[gdf_india_states["NAME_1"] == my_state_name]

# Plot state map
fig, ax = plt.subplots(figsize=(8, 8))
gdf_my_state.plot(ax=ax, color="lightgreen", edgecolor="darkgreen", linewidth=1.5)
plt.title(f"Boundary Map of {my_state_name}")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(True, linestyle="--", alpha=0.5)
plt.savefig("Q5_State_Map.png")
plt.show()


# -----------------------------------------------------------------------------
# Question 6: Download India shapefile, extract favorite region, store in EPSG:4326
# -----------------------------------------------------------------------------
print("--- Question 6: Extract Region & Save in EPSG:4326 ---")
# Extract a specific region (e.g., South India states or a specific state group)
favorite_region_states = ["Kerala", "Tamil Nadu", "Karnataka"]
gdf_fav_region = gdf_india_states[gdf_india_states["NAME_1"].isin(favorite_region_states)]

# Ensure CRS is EPSG:4326
gdf_fav_region_4326 = gdf_fav_region.to_crs(epsg=4326)

# Save to file
gdf_fav_region_4326.to_file("Favorite_Region_EPSG4326.shp")
print("Saved Favorite Region Shapefile successfully.")


# -----------------------------------------------------------------------------
# Question 7: Choose 1 state and plot bar plot for district areas
# -----------------------------------------------------------------------------
print("--- Question 7: District Areas Bar Plot ---")
# Download GADM Level 2 (Districts) for India
gadm_districts_url = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_IND_2.json"
gdf_india_districts = gpd.read_file(gadm_districts_url)

# Filter districts for chosen state (e.g., Kerala or Meghalaya)
chosen_state = "Kerala"
gdf_districts = gdf_india_districts[gdf_india_districts["NAME_1"] == chosen_state].copy()

# Project to equal-area CRS for area calculation
gdf_districts_proj = gdf_districts.to_crs(epsg=7755)
gdf_districts["area_sqkm"] = gdf_districts_proj.geometry.area / 1e6

# Sort districts by area
gdf_districts_sorted = gdf_districts.sort_values(by="area_sqkm", ascending=False)

# Plot District Area Bar Plot
plt.figure(figsize=(12, 6))
plt.bar(gdf_districts_sorted["NAME_2"], gdf_districts_sorted["area_sqkm"], color="coral", edgecolor="darkred")
plt.xlabel("District")
plt.ylabel("Area (sq km)")
plt.title(f"District-wise Area of {chosen_state}")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig("Q7_District_Areas_Bar_Chart.png")
plt.show()