# AI Conversion Prompt

Copy and paste the text below into ChatGPT or another capable AI assistant after uploading your `ride_capture.txt` file.

---

This file is an Android ADB logcat capture made while I opened ONE historical ride in the CFMOTO RIDE app running in BlueStacks Android 11.

Find the CFMOTO ride-history detail API response for the ride I opened. Locate the JSON trajectory for that selected ride. Extract ONLY the trajectory records belonging to that ride.

The trajectory records are expected to contain longitude, latitude, speed, cumulative distance, and Unix timestamp values.

DO NOT scan the entire response or entire log for arbitrary coordinate-looking numbers.

Create a standard GPX 1.1 TRACK (.gpx) using the trajectory longitude/latitude points in chronological order. Deduplicate duplicate log copies/points where appropriate.

Android logcat may wrap a trajectory record across lines. Recover a wrapped record only when the surrounding trajectory syntax makes it clear that it belongs to the selected ride.

Before creating the GPX, validate all of the following:

1. All coordinates form one geographically continuous ride.
2. There are no impossible outlier coordinates.
3. There are no giant point-to-point jumps.
4. Timestamps are in chronological order.
5. The calculated polyline distance is reasonably close to the CFMOTO recorded ride distance, if that distance is available.
6. The first and last points are plausible for the displayed start/end locations, if those are available in the response.

Report:

- number of track points
- start coordinate
- end coordinate
- latitude bounds
- longitude bounds
- CFMOTO recorded distance, if available
- calculated GPX/polyline distance
- largest point-to-point jump

If validation passes, create and give me a downloadable `.gpx` file.

If validation fails, DO NOT create a misleading GPX. Explain exactly what failed.

The authoritative source is the selected CFMOTO ride's trajectory contained in the ride-history response. Do not reconstruct the route from screenshots.
