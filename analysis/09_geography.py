"""B6b: share of the Mesa attendance area beyond 1.5 miles (straight line) from Bear Creek Elementary.
Uses the attendance-area polygons vendored from BVSD's ArcGIS layer (data/raw/enrollmentdata/BVSD_Attendance_Areas.geojson).
Area-based, not address-based; straight-line distance understates road distance. Output: analysis/output/table09_geography.csv"""
import json, math, numpy as np, pandas as pd
from pathlib import Path
g = json.load(open("data/raw/enrollmentdata/BVSD_Attendance_Areas.geojson"))
BC = (39.9804, -105.2631)   # 2500 Table Mesa Dr (coordinates as recorded in the enrollmentdata map, line 772)
MESA = (39.9722, -105.2610)
def km_per_deg(lat): return 111.32 * math.cos(math.radians(lat)), 110.57
def dist_mi(lat, lon, ref):
    kx, ky = km_per_deg(ref[0]); return math.hypot((lon - ref[1]) * kx, (lat - ref[0]) * ky) / 1.609
def polys(feature):
    geom = feature["geometry"]; return geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
def point_in_ring(x, y, ring):
    inside = False; n = len(ring)
    for i in range(n):
        x1, y1 = ring[i][:2]; x2, y2 = ring[(i + 1) % n][:2]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1: inside = not inside
    return inside
rows = []
for f in g["features"]:
    name = f["properties"].get("SchName")
    if name not in ("Mesa", "Bear Creek", "BC-Mesa"): continue
    pts = [p for poly in polys(f) for p in poly[0]]
    lons, lats = [p[0] for p in pts], [p[1] for p in pts]
    xs = np.linspace(min(lons), max(lons), 220); ys = np.linspace(min(lats), max(lats), 220)
    inside, far, far_mesa = 0, 0, 0
    for x in xs:
        for y in ys:
            if any(point_in_ring(x, y, poly[0]) for poly in polys(f)):
                inside += 1; far += dist_mi(y, x, BC) > 1.5; far_mesa += dist_mi(y, x, MESA) > 1.5
    rows.append(dict(area=name, stdtpop_gis=f["properties"].get("StdtPop"), grid_points_inside=inside, share_beyond_1p5mi_of_bear_creek=far / inside, share_beyond_1p5mi_of_mesa=far_mesa / inside,
                     max_dist_to_bear_creek_mi=max(dist_mi(y, x, BC) for x, y in zip(lons, lats))))
t = pd.DataFrame(rows); t["note"] = "area share on a 220x220 grid; straight-line distance; StdtPop is the GIS layer's resident count (vintage unknown)"
t.to_csv("analysis/output/table09_geography.csv", index=False); print(t.round(3).to_string(index=False))
