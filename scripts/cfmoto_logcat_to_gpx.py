#!/usr/bin/env python3
"""
CFMOTO RIDE logcat -> GPX converter

Usage:
    python cfmoto_logcat_to_gpx.py ride_capture.txt ride_output.gpx

Important:
- Capture only ONE selected ride per logcat session.
- The parser intentionally requires trajectory context.
- Always visually validate the resulting GPX.
"""

import sys
import re
import math
from pathlib import Path
from datetime import datetime, timezone
from xml.sax.saxutils import escape

TUPLE_RE = re.compile(
    r'(-?\d{2,3}\.\d+),'
    r'(-?\d{1,2}\.\d+),'
    r'(\d+(?:\.\d+)?),'
    r'(\d+(?:\.\d+)?),'
    r'(\d{10})'
)

def haversine_km(a, b):
    lon1, lat1 = a[0], a[1]
    lon2, lat2 = b[0], b[1]
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2-lat1)
    dl = math.radians(lon2-lon1)
    h = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*r*math.atan2(math.sqrt(h), math.sqrt(1-h))

def extract_trajectory_context(text):
    """
    Find regions around the word 'trajectory'.
    This avoids blindly parsing every coordinate-like tuple in the log.
    """
    lower = text.lower()
    hits = [m.start() for m in re.finditer("trajectory", lower)]
    if not hits:
        raise RuntimeError("No 'trajectory' field found in the log capture.")

    chunks = []
    for pos in hits:
        start = max(0, pos - 2000)
        end = min(len(text), pos + 2_000_000)
        chunks.append(text[start:end])
    return "\n".join(chunks)

def main():
    if len(sys.argv) != 3:
        print("Usage: python cfmoto_logcat_to_gpx.py ride_capture.txt ride_output.gpx")
        sys.exit(2)

    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])

    text = src.read_text(errors="ignore")
    context = extract_trajectory_context(text)

    raw = []
    for m in TUPLE_RE.finditer(context):
        lon, lat, speed, dist, ts = m.groups()
        p = (float(lon), float(lat), float(speed), float(dist), int(ts))

        # Basic legal coordinate/time checks.
        if not (-180 <= p[0] <= 180 and -90 <= p[1] <= 90):
            continue
        if p[4] < 1_500_000_000:
            continue
        raw.append(p)

    if len(raw) < 2:
        raise RuntimeError("Not enough trajectory points were found.")

    # Deduplicate repeated logger copies, using timestamp + coordinates.
    unique = {}
    for p in raw:
        key = (p[4], round(p[0], 6), round(p[1], 6))
        unique[key] = p

    points = sorted(unique.values(), key=lambda p: p[4])

    # Remove exact duplicate timestamps by choosing one point per timestamp.
    by_time = {}
    for p in points:
        by_time.setdefault(p[4], p)
    points = [by_time[t] for t in sorted(by_time)]

    if len(points) < 2:
        raise RuntimeError("Not enough unique trajectory points remain.")

    # Geographic continuity validation.
    jumps = [haversine_km(points[i-1], points[i]) for i in range(1, len(points))]
    max_jump = max(jumps)
    polyline_km = sum(jumps)

    # Conservative automatic guardrail. A point jump > 25 km between adjacent
    # samples almost always means unrelated/outlier data in this workflow.
    if max_jump > 25:
        raise RuntimeError(
            f"Validation failed: largest adjacent-point jump is {max_jump:.2f} km. "
            "The log may contain unrelated coordinate data or more than one ride."
        )

    # Basic monotonic cumulative distance sanity check where available.
    cumulative = [p[3] for p in points]
    decreases = sum(1 for i in range(1, len(cumulative)) if cumulative[i] + 0.5 < cumulative[i-1])
    if decreases > max(3, len(points)//20):
        raise RuntimeError(
            "Validation failed: cumulative ride distance decreases too often. "
            "The capture may contain more than one trajectory/log response."
        )

    name = "CFMOTO Ride"
    gpx = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gpx version="1.1" creator="CFMOTO RIDE logcat converter"',
        ' xmlns="http://www.topografix.com/GPX/1/1">',
        '  <metadata>',
        f'    <name>{escape(name)}</name>',
        '  </metadata>',
        '  <trk>',
        f'    <name>{escape(name)}</name>',
        '    <trkseg>',
    ]

    for lon, lat, speed_kmh, cumulative_km, ts in points:
        iso = datetime.fromtimestamp(ts, timezone.utc).isoformat().replace("+00:00", "Z")
        gpx += [
            f'      <trkpt lat="{lat:.6f}" lon="{lon:.6f}">',
            f'        <time>{iso}</time>',
            '      </trkpt>',
        ]

    gpx += ['    </trkseg>', '  </trk>', '</gpx>']
    dst.write_text("\n".join(gpx), encoding="utf-8")

    print(f"Created: {dst}")
    print(f"Track points: {len(points)}")
    print(f"Start: {points[0][1]:.6f}, {points[0][0]:.6f}")
    print(f"End:   {points[-1][1]:.6f}, {points[-1][0]:.6f}")
    print(f"Latitude range:  {min(p[1] for p in points):.6f} to {max(p[1] for p in points):.6f}")
    print(f"Longitude range: {min(p[0] for p in points):.6f} to {max(p[0] for p in points):.6f}")
    print(f"Calculated polyline: {polyline_km:.2f} km / {polyline_km*0.621371:.2f} mi")
    print(f"Largest adjacent jump: {max_jump:.3f} km")
    print(f"Final CFMOTO cumulative distance field: {points[-1][3]:.2f} km")
    print()
    print("IMPORTANT: Open the GPX in a map and visually validate it before use.")

if __name__ == "__main__":
    main()
