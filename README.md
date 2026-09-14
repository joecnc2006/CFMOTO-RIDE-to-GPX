# CFMOTO RIDE to GPX

A repeatable Windows workflow for exporting **your own historical CFMOTO RIDE tracks** to a standard `.gpx` file.

This project documents the method that successfully worked with:

- Windows 10 / 11
- BlueStacks 5
- Android 11 instance
- CFMOTO RIDE / RIDESYNC
- BlueStacks ADB
- Android `logcat`
- GPX 1.1
- onX Offroad

> **Important:** Use this only for an account and ride history you are authorized to access.  
> Raw Android logs may contain account tokens, vehicle identifiers, location history, and other private information. Do not post raw logcat files publicly.

---

## What this does

When a historical ride is opened in CFMOTO RIDE, the app requests ride-detail data from CFMOTO's service. In the tested app build, the app logs the request/response information to Android `logcat`, including the selected ride's `trajectory`.

The working process is:

```text
Windows PC
   ↓
BlueStacks 5 / Android 11
   ↓
CFMOTO RIDE
   ↓
Open one historical ride
   ↓
ADB logcat capture
   ↓
Find selected ride trajectory
   ↓
Validate GPS points
   ↓
Create GPX 1.1
   ↓
Import into onX / GPX-capable software
```

No proxy, rooting, HAR capture, packet interception, or screenshot tracing is required for this method.

---

# 1. Install BlueStacks 5

Official download:

https://www.bluestacks.com/bluestacks-5.html

Create a **fresh Android 11 instance** from BlueStacks Multi-instance Manager.

Official Android 11 instructions:

https://support.bluestacks.com/hc/en-us/articles/10499358452237-How-to-play-games-with-Android-11-on-BlueStacks-5

Recommended settings that worked successfully:

| Setting | Value |
|---|---|
| Android version | Android 11 |
| CPU | 4 cores |
| Memory | 4 GB |
| Resolution | 1600 × 900 |
| Orientation | Landscape |
| ABI | x86 & ARM |
| Performance | Balanced |
| DPI | 240 |

---

# 2. Install CFMOTO RIDE

Inside the Android 11 BlueStacks instance:

1. Open Google Play.
2. Sign in.
3. Install CFMOTO RIDE / RIDESYNC.
4. Sign in to your CFMOTO account.
5. Confirm your historical rides are visible.
6. Open a ride once to confirm its map displays correctly.

Google Play:

https://play.google.com/store/apps/details?id=com.cfmoto.cfmotointernational

> App package names and store listings may change between app versions. The important part is that you are using the official CFMOTO ride app that contains your historical ride data.

---

# 3. Enable ADB in BlueStacks

Open BlueStacks settings and enable **Android Debug Bridge (ADB)**.

BlueStacks normally installs its bundled ADB executable here:

```text
C:\Program Files\BlueStacks_nxt\HD-Adb.exe
```

Each BlueStacks instance has its own localhost ADB port.

The tested Android 11 instance used:

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

# 4. Connect to BlueStacks with Command Prompt

Open **Command Prompt** (`cmd.exe`).

Connect:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" connect 127.0.0.1:PORT
```

Check devices:

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" devices
```

A working connection should look similar to:

```text
127.0.0.1:PORT    device
```

---

# 5. Create a simple working folder

Use a short path without OneDrive or redirected Desktop folders:

```bat
mkdir C:\CFMOTO_GPX
```

---

# 6. Capture the ride with logcat

## A. Prepare CFMOTO RIDE

In BlueStacks, navigate to the historical ride list, but **do not open the target ride yet**.

## B. Clear old Android logs

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" -s 127.0.0.1:PORT logcat -c
```

## C. Start recording

```bat
"C:\Program Files\BlueStacks_nxt\HD-Adb.exe" -s 127.0.0.1:PORT logcat > "C:\CFMOTO_GPX\ride_capture.txt"
```

The Command Prompt will appear to stop responding.

That is normal — `logcat` is actively recording.

## D. Open exactly one ride

While recording:

1. Return to BlueStacks.
2. Open CFMOTO RIDE.
3. Open the exact historical ride you want.
4. Wait for the entire track to appear.
5. Wait several additional seconds.

## E. Stop recording

Return to Command Prompt and press:

```text
Ctrl+C
```

You should now have:

```text
C:\CFMOTO_GPX\ride_capture.txt
```

---

# 7. Verify that trajectory data was captured

Run:

```bat
findstr /i "ridehistory trajectory httplog RequestSignInterceptor" "C:\CFMOTO_GPX\ride_capture.txt"
```

A useful capture should contain evidence of the selected ride-detail response and/or the word:

```text
trajectory
```

The trajectory records observed in testing followed this pattern:

```text
longitude,latitude,speed_kmh,cumulative_distance_km,unix_timestamp
```

Example structure only:

```text
-98.123456,29.123456,52.00,12.34,1789319634
```

---

# 8. Convert with ChatGPT or another capable AI assistant

Upload `ride_capture.txt` and paste the prompt in:

[`AI_PROMPT.md`](AI_PROMPT.md)

The critical rule is:

> **Extract only the selected ride's `trajectory`. Do not scan the entire log/API response for arbitrary coordinate-looking numbers.**

Ignoring that rule can produce a bogus GPX that jumps hundreds or thousands of miles.

---

# 9. Optional local Python converter

A starter converter is included:

```text
scripts/cfmoto_logcat_to_gpx.py
```

Run it with Python 3:

```bat
python scripts\cfmoto_logcat_to_gpx.py "C:\CFMOTO_GPX\ride_capture.txt" "C:\CFMOTO_GPX\ride_output.gpx"
```

The script:

- looks for trajectory data
- parses longitude / latitude / speed / cumulative distance / Unix timestamps
- removes duplicate points
- sorts chronologically
- rejects obvious invalid coordinates
- checks point-to-point jumps
- calculates approximate polyline distance
- writes a GPX 1.1 track

Always visually inspect the result before relying on it.

---

# 10. Import into onX Offroad

Official onX instructions:

https://onxor.zendesk.com/hc/en-us/articles/360057279192-Importing-and-Exporting-Markups

In onX:

1. Open **My Content**
2. Select **Import**
3. Choose the `.gpx` file
4. Open the imported Track
5. Select **Show on Map**
6. Visually confirm the entire track is in the expected area

A GPX track imports into onX as a **Track**.

---

# Required validation

Before accepting a converted GPX, confirm:

- start point is correct
- end point is correct
- all points remain in the expected geographic region
- timestamps increase in chronological order
- no segment contains an impossible geographic jump
- calculated GPX distance is reasonably close to the distance shown in CFMOTO
- the map does not jump to another state, country, continent, or ocean

---

# Full PDF guide

A printable version is included here:

[`docs/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf`](docs/CFMOTO_RIDE_to_GPX_Complete_Guide.pdf)

---

# Privacy / security

`ride_capture.txt` can contain sensitive information, including:

- authentication tokens
- account identifiers
- vehicle identifiers
- precise location history
- timestamps
- app/device information

**Do not commit raw logcat captures to GitHub.**

This repository's `.gitignore` excludes common capture filenames, but you should still inspect files before publishing.

---

# What did NOT need to be used

The successful workflow did **not** require:

- rooting BlueStacks
- accessing the app's protected private storage
- mitmproxy
- HAR capture
- packet interception
- manually recreating a route from screenshots

The successful source was the CFMOTO app's own output in Android `logcat`.

---

# Disclaimer

This is an independent community workflow and is not affiliated with or endorsed by CFMOTO, BlueStacks, onX, or OpenAI. App behavior and API logging may change in future versions.

Use only with accounts and ride data you are authorized to access.
