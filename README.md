# CFMOTO RIDE to GPX

<p align="center">
  <strong>Export your own CFMOTO RIDE historical tracks to standard GPX files using BlueStacks, ADB, and Android logcat.</strong>
</p>

<p align="center">
  <a href="https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf"><strong>📘 DOWNLOAD COMPLETE PDF GUIDE</strong></a>
  &nbsp; • &nbsp;
  <a href="AI_PROMPT.md"><strong>🤖 AI CONVERSION PROMPT</strong></a>
  &nbsp; • &nbsp;
  <a href="scripts/capture_ride.cmd"><strong>🧰 CAPTURE HELPER</strong></a>
</p>

<p align="center">
  <a href="https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/latest"><strong>Latest Release: v1.0</strong></a>
</p>

---

## What This Project Does

CFMOTO RIDE can display historical motorcycle rides, but it does not provide a convenient GPX export for every workflow.

This project documents a **tested, repeatable method** for recovering your own historical CFMOTO RIDE track and converting it into a standard **GPX 1.1** file.

The finished GPX can be imported into:

- onX Offroad
- Garmin-compatible software
- GPX viewers
- mapping applications
- route-planning software
- other GPX-compatible applications

### How it works

```text
CFMOTO RIDE
     ↓
BlueStacks 5 / Android 11
     ↓
ADB Logcat Capture
     ↓
CFMOTO Ride Trajectory
     ↓
Trajectory Extraction
     ↓
Geographic & Distance Validation
     ↓
GPX 1.1 File
     ↓
onX Offroad / GPX-Compatible Apps
```

The important discovery behind this project is that the tested CFMOTO RIDE / RIDESYNC application writes the selected historical ride's trajectory information into Android **logcat** when the ride is opened.

This allows the ride to be recovered without:

- Rooting BlueStacks
- Accessing protected Android app storage
- Using mitmproxy
- Capturing HAR files
- Intercepting encrypted network traffic
- Manually tracing the route from screenshots

---

# 📘 Complete Step-by-Step Guide

For the easiest start-to-finish instructions, download the complete PDF:

## 👉 [DOWNLOAD THE COMPLETE CFMOTO RIDE TO GPX PDF GUIDE](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf)

This download is provided through the project's official **GitHub v1.0 Release**.

---

# Quick Start

## 1. Install BlueStacks 5

Download BlueStacks 5:

https://www.bluestacks.com/bluestacks-5.html

Create a **fresh Android 11 instance**.

Recommended settings:

| Setting | Recommended Value |
|---|---|
| Android version | Android 11 |
| CPU | 4 cores |
| Memory | 4 GB |
| Resolution | 1600 × 900 |
| Orientation | Landscape |
| ABI | x86 & ARM |
| Performance | Balanced |
| DPI | 240 |

Official BlueStacks Android 11 instructions:

https://support.bluestacks.com/hc/en-us/articles/10499358452237-How-to-play-games-with-Android-11-on-BlueStacks-5

---

## 2. Install CFMOTO RIDE / RIDESYNC

Inside BlueStacks:

1. Open Google Play.
2. Install CFMOTO RIDE / RIDESYNC.
3. Sign in to your CFMOTO account.
4. Confirm that your historical rides appear.
5. Make sure the ride you want to export can be opened and displayed on the map.

Google Play:

https://play.google.com/store/apps/details?id=com.cfmoto.cfmotointernational

> **Note:** CFMOTO may change the application name, package name, or store listing in future versions.

---

## 3. Enable ADB

Enable **Android Debug Bridge (ADB)** in BlueStacks settings.

BlueStacks normally installs its ADB executable here:

```text
C:\Program Files\BlueStacks_nxt\HD-Adb.exe
```

Each BlueStacks instance has its own localhost ADB port.

For example:

```text
127.0.0.1:5556
```

Your port may be different.

In the commands below, replace:

```text
PORT
```

with your actual BlueStacks ADB port.

---

## 4. Connect to BlueStacks

Open **Windows Command Prompt**.

Run:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" connect 127.0.0.1:PORT
```

Then verify the connection:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" devices
```

A successful connection should look similar to:

```text
127.0.0.1:PORT    device
```

---

## 5. Create a Working Folder

Run:

```bat
mkdir C:\CFMOTO_GPX
```

Using a simple local folder helps avoid problems with OneDrive, redirected Desktop folders, and paths containing spaces.

---

# 6. Capture One Historical Ride

In CFMOTO RIDE, navigate to the list of historical rides.

**Do not open the target ride yet.**

First clear the old Android logs:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" -s 127.0.0.1:PORT logcat -c
```

Now start recording logcat:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" -s 127.0.0.1:PORT logcat > "C:\CFMOTO_GPX\ride_capture.txt"
```

While logcat is recording:

1. Return to BlueStacks.
2. Open **exactly one** historical ride.
3. Wait for the complete route to load.
4. Wait several additional seconds.
5. Return to Command Prompt.
6. Press **Ctrl+C**.

Your captured log should now be located at:

```text
C:\CFMOTO_GPX\ride_capture.txt
```

---

# 7. Verify That Ride Data Was Captured

Run:

```bat
findstr /i "ridehistory trajectory httplog RequestSignInterceptor" "C:\CFMOTO_GPX\ride_capture.txt"
```

The useful CFMOTO trajectory records observed during testing followed this general structure:

```text
longitude,latitude,speed_kmh,cumulative_distance_km,unix_timestamp
```

---

# 8. Convert the Ride to GPX

There are two options.

## Option A — Use ChatGPT or Another Capable AI Assistant

Upload:

```text
ride_capture.txt
```

Then use the conversion instructions included in:

## 👉 [AI_PROMPT.md](AI_PROMPT.md)

The most important rule is:

> **Extract ONLY the selected ride's `trajectory`. Do NOT scan the entire log or API response for arbitrary coordinate-looking numbers.**

This is extremely important.

Numbers elsewhere in the Android logs can accidentally look like longitude and latitude coordinates.

If those unrelated values are interpreted as GPS points, the resulting GPX can contain enormous geographic jumps.

---

## Option B — Use the Included Python Converter

This repository also includes:

```text
scripts/cfmoto_logcat_to_gpx.py
```

Example:

```bat
python scripts\cfmoto_logcat_to_gpx.py "C:\CFMOTO_GPX\ride_capture.txt" "C:\CFMOTO_GPX\ride_output.gpx"
```

The script performs basic parsing and validation.

However:

> **Always visually inspect the resulting GPX before relying on it.**

---

# GPX Validation

Before considering a converted ride valid, confirm:

- [ ] The starting point is correct.
- [ ] The ending point is correct.
- [ ] Coordinates remain in the expected geographic area.
- [ ] Timestamps are chronological.
- [ ] There are no impossible point-to-point jumps.
- [ ] Calculated track distance is reasonably close to the distance shown by CFMOTO RIDE.
- [ ] The route does not suddenly jump to another state or country.
- [ ] The route does not cross an ocean unexpectedly.
- [ ] The complete track looks correct when displayed on a map.

---

# Why Validation Is So Important

During development of this workflow, an early GPX conversion incorrectly included unrelated coordinate-like numbers from the larger Android/API log.

The resulting GPX appeared to begin correctly in Texas but then contained an enormous erroneous jump **across the Atlantic toward Africa**.

The problem was not the original CFMOTO ride data.

The problem was parsing numbers outside the actual ride trajectory.

The corrected procedure prevents this by:

1. Identifying the selected ride's ride-history response.
2. Locating its specific `trajectory`.
3. Extracting **only** trajectory records.
4. Recovering wrapped trajectory records only when their structure clearly identifies them.
5. Deduplicating repeated logger copies.
6. Sorting points chronologically.
7. Checking geographic bounds.
8. Checking consecutive-point distances.
9. Comparing calculated GPX distance with CFMOTO's recorded ride distance.
10. Verifying the finished track visually.

Only after these checks should the GPX be considered valid.

---

# Import Into onX Offroad

Official onX GPX import instructions:

https://onxor.zendesk.com/hc/en-us/articles/360057279192-Importing-and-Exporting-Markups

Typical workflow:

1. Open **My Content**.
2. Select **Import**.
3. Select the finished `.gpx` file.
4. Open the imported Track.
5. Choose **Show on Map**.
6. Visually verify the complete track.

A GPX track normally imports into onX as a **Track**.

---

# Downloads & Resources

| Resource | Download / Open |
|---|---|
| 📘 Complete PDF Guide | [Download v1.0 PDF](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf) |
| 🏷️ Latest GitHub Release | [Open Releases](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/latest) |
| 🤖 AI Conversion Instructions | [AI_PROMPT.md](AI_PROMPT.md) |
| 🧰 Windows Capture Helper | [capture_ride.cmd](scripts/capture_ride.cmd) |
| 🐍 Python GPX Converter | [cfmoto_logcat_to_gpx.py](scripts/cfmoto_logcat_to_gpx.py) |
| 🔒 Security Information | [SECURITY.md](SECURITY.md) |

---

# Repository Layout

```text
CFMOTO-RIDE-to-GPX/
│
├── README.md
├── AI_PROMPT.md
├── SECURITY.md
├── PUBLISH_TO_GITHUB.md
├── LICENSE
├── .gitignore
│
├── docs/
│   └── CFMOTO_RIDE_to_GPX_Complete_Guide.pdf
│
└── scripts/
    ├── capture_ride.cmd
    └── cfmoto_logcat_to_gpx.py
```

---

# 🔒 Privacy & Security

The raw:

```text
ride_capture.txt
```

file can contain sensitive information.

Depending on the CFMOTO application version and logging behavior, this may include:

- Authentication information
- User/account identifiers
- Vehicle identifiers
- Precise GPS history
- Ride timestamps
- Device information

## Never upload your raw `ride_capture.txt` file to a public GitHub repository.

This project's `.gitignore` blocks several common sensitive/generated file types:

```text
ride_capture.txt
*logcat*.txt
*.mitm
*.har
*.gpx
```

However, `.gitignore` is not a substitute for checking your files before publishing them.

For additional information:

## 👉 [Read SECURITY.md](SECURITY.md)

---

# Tested Workflow

This procedure was successfully demonstrated using:

- Windows
- BlueStacks 5
- Android 11
- CFMOTO RIDE / RIDESYNC
- BlueStacks ADB
- Android logcat
- GPX 1.1
- onX Offroad

Application behavior can change with future CFMOTO releases.

This repository documents the method that worked during testing.

---

# Contributing

If this workflow works for you, or you discover changes required by a newer version of CFMOTO RIDE, contributions are welcome.

Useful contributions could include:

- Updated CFMOTO application compatibility information
- Updated BlueStacks instructions
- Parser improvements
- Better trajectory validation
- Support for additional GPX applications
- Troubleshooting information
- Screenshots that contain **no private information**

### Please do NOT submit:

- Raw logcat files containing authentication data
- Account credentials
- Authentication tokens
- Vehicle identifiers tied to an individual
- Private location history

---

# Disclaimer

This is an **independent community project**.

It is not affiliated with, sponsored by, or endorsed by:

- CFMOTO
- BlueStacks
- onX
- OpenAI

Use this workflow only with accounts, vehicles, and ride history that you are authorized to access.

---

# 📘 Ready to Start?

## 👉 [DOWNLOAD THE COMPLETE CFMOTO RIDE TO GPX v1.0 PDF GUIDE](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf)

Or start with the:

### 👉 [AI Conversion Prompt](AI_PROMPT.md)

### 👉 [Latest GitHub Release](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/latest)

---

**CFMOTO RIDE to GPX — v1.0**
