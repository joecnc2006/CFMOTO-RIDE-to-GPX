# CFMOTO RIDE to GPX

<p align="center">
  <strong>Export your own CFMOTO RIDE historical tracks to a standard GPX file using BlueStacks, ADB, and Android logcat.</strong>
</p>

<p align="center">
  <a href="https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf"><strong>📘 Download PDF Guide</strong></a>
  &nbsp;•&nbsp;
  <a href="AI_PROMPT.md"><strong>🤖 AI Conversion Prompt</strong></a>
  &nbsp;•&nbsp;
  <a href="scripts/capture_ride.cmd"><strong>🧰 Capture Helper</strong></a>
</p>

---

## What this project does

CFMOTO RIDE can display historical rides, but it does not provide a convenient GPX export for every workflow.

This project documents a repeatable method that worked successfully on Windows:

```text
CFMOTO RIDE
    ↓
BlueStacks 5 / Android 11
    ↓
ADB logcat capture
    ↓
CFMOTO ride trajectory
    ↓
Validation
    ↓
GPX 1.1
    ↓
onX Offroad / GPX-compatible apps
```

The important discovery is that the tested CFMOTO RIDE app build writes the selected ride's trajectory data into Android `logcat` when a historical ride is opened.

That means the ride can be recovered without:

- rooting BlueStacks
- accessing protected app storage
- using mitmproxy
- capturing HAR files
- intercepting encrypted traffic
- tracing the route manually from screenshots

---

## Quick Start

### 1. Install BlueStacks 5

Download:

https://www.bluestacks.com/bluestacks-5.html

Create a **fresh Android 11 instance**.

Recommended settings:

| Setting | Recommended value |
|---|---:|
| Android version | Android 11 |
| CPU | 4 cores |
| Memory | 4 GB |
| Resolution | 1600 × 900 |
| Orientation | Landscape |
| ABI | x86 & ARM |
| Performance | Balanced |
| DPI | 240 |

Official BlueStacks Android 11 guide:

https://support.bluestacks.com/hc/en-us/articles/10499358452237-How-to-play-games-with-Android-11-on-BlueStacks-5

---

### 2. Install CFMOTO RIDE

Inside BlueStacks:

1. Open Google Play.
2. Install CFMOTO RIDE / RIDESYNC.
3. Sign in to your CFMOTO account.
4. Confirm your historical rides appear.
5. Make sure the ride you want can be opened and displayed on the map.

Google Play:

https://play.google.com/store/apps/details?id=com.cfmoto.cfmotointernational

---

### 3. Enable ADB

Enable **Android Debug Bridge (ADB)** in BlueStacks settings.

BlueStacks normally installs ADB here:

```text
C:\Program Files\BlueStacks_nxt\HD-Adb.exe
```

Each BlueStacks instance has its own localhost ADB port.

Example:

```text
127.0.0.1:5556
```

Your port may be different.

In all commands below, replace:

```text
PORT
```

with your actual BlueStacks ADB port.

---

### 4. Connect to BlueStacks

Open **Command Prompt** and run:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" connect 127.0.0.1:PORT
```

Then confirm:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" devices
```

A working connection should look similar to:

```text
127.0.0.1:PORT    device
```

---

### 5. Create a working folder

```bat
mkdir C:\CFMOTO_GPX
```

Using a simple local folder avoids problems with OneDrive, redirected Desktop folders, and paths containing spaces.

---

### 6. Capture one ride

Before opening the ride, clear old logs:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" -s 127.0.0.1:PORT logcat -c
```

Start recording:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" -s 127.0.0.1:PORT logcat > "C:\CFMOTO_GPX\ride_capture.txt"
```

Now:

1. Return to BlueStacks.
2. Open **exactly one** historical ride.
3. Wait for the complete track to appear.
4. Wait several additional seconds.
5. Return to Command Prompt.
6. Press **Ctrl+C**.

Your capture should now be here:

```text
C:\CFMOTO_GPX\ride_capture.txt
```

---

### 7. Verify trajectory data exists

Run:

```bat
findstr /i "ridehistory trajectory httplog RequestSignInterceptor" "C:\CFMOTO_GPX\ride_capture.txt"
```

The useful CFMOTO trajectory records observed during testing followed this structure:

```text
longitude,latitude,speed_kmh,cumulative_distance_km,unix_timestamp
```

---

## Convert the ride to GPX

### Option A — Use ChatGPT or another capable AI assistant

Upload `ride_capture.txt` and use the prepared prompt:

### 👉 [Open the AI Conversion Prompt](AI_PROMPT.md)

The most important rule is:

> **Extract only the selected ride's `trajectory`. Do not scan the entire log for arbitrary coordinate-looking numbers.**

Failing to isolate the trajectory can produce bogus GPS points and tracks that jump hundreds or thousands of miles.

---

### Option B — Use the included Python converter

The repository includes:

```text
scripts/cfmoto_logcat_to_gpx.py
```

Run:

```bat
python scripts\cfmoto_logcat_to_gpx.py "C:\CFMOTO_GPX\ride_capture.txt" "C:\CFMOTO_GPX\ride_output.gpx"
```

The script performs basic parsing and validation, but you should still inspect every generated GPX visually.

---

## Required validation

Before using a GPX, confirm:

- [ ] Start point is correct.
- [ ] End point is correct.
- [ ] All coordinates stay in the expected geographic area.
- [ ] Timestamps are chronological.
- [ ] There are no impossible point-to-point jumps.
- [ ] Calculated track distance is reasonably close to the distance shown in CFMOTO RIDE.
- [ ] The route does not jump to another state, country, continent, or ocean.
- [ ] The entire track looks correct when displayed on a map.

This validation step is important.

A parser that blindly scans a complete log for numbers that resemble coordinates can create a badly corrupted GPX.

---

## Import into onX Offroad

onX GPX import instructions:

https://onxor.zendesk.com/hc/en-us/articles/360057279192-Importing-and-Exporting-Markups

Typical workflow:

1. Open **My Content**.
2. Select **Import**.
3. Select the finished `.gpx`.
4. Open the imported Track.
5. Choose **Show on Map**.
6. Visually confirm the track.

A GPX track imports into onX as a **Track**.

---

# Downloads and Resources

| Resource | Link |
|---|---|
| Complete printable guide | [Download PDF](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf) |
| AI conversion instructions | [AI_PROMPT.md](AI_PROMPT.md) |
| Windows logcat capture helper | [capture_ride.cmd](scripts/capture_ride.cmd) |
| Python GPX converter | [cfmoto_logcat_to_gpx.py](scripts/cfmoto_logcat_to_gpx.py) |
| Security information | [SECURITY.md](SECURITY.md) |

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

# Privacy and Security

The raw `ride_capture.txt` file can contain sensitive information.

Possible sensitive data includes:

- authentication tokens
- user/account identifiers
- vehicle identifiers
- precise GPS history
- timestamps
- device information

### Never upload your raw logcat capture to a public GitHub repository.

This project's `.gitignore` blocks common sensitive capture filenames:

```text
ride_capture.txt
*logcat*.txt
*.mitm
*.har
*.gpx
```

However, always inspect your files before committing them.

More information:

### 👉 [Read SECURITY.md](SECURITY.md)

---

# Why the validation step matters

During development of this workflow, an early GPX conversion incorrectly included unrelated coordinate-like values from the larger response.

The result was a track that incorrectly stretched from Texas across the Atlantic.

The corrected procedure solves that by:

1. identifying the selected ride's ride-history response
2. isolating only its `trajectory`
3. parsing only trajectory tuples
4. deduplicating repeated logger copies
5. sorting by timestamp
6. checking geographic bounds
7. checking consecutive-point distance
8. comparing GPX distance to CFMOTO's recorded ride distance

Only after those checks should the GPX be considered valid.

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

App behavior can change with future CFMOTO releases, so this repository documents the method that worked at the time of testing.

---

# Contributing

If this workflow works for you, or you discover changes required by newer CFMOTO app versions, contributions are welcome.

Useful contributions include:

- updated BlueStacks instructions
- newer CFMOTO app compatibility information
- parser improvements
- better trajectory validation
- support for additional GPX applications
- screenshots that do not contain personal information

Please do **not** submit raw logcat files containing tokens, account information, or private location history.

---

# Disclaimer

This is an independent community project.

It is **not affiliated with, sponsored by, or endorsed by**:

- CFMOTO
- BlueStacks
- onX
- OpenAI

Use this workflow only with accounts, vehicles, and ride history you are authorized to access.

---

## Full Guide

### 📘 [Download the Complete CFMOTO RIDE to GPX PDF Guide](https://github.com/joecnc2006/CFMOTO-RIDE-to-GPX/releases/download/v1.0/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf)

If you only want the complete start-to-finish instructions, the PDF is the easiest version to share.
