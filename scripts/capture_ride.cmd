@echo off
setlocal

REM ============================================================
REM CFMOTO RIDE logcat capture helper
REM ============================================================
REM Change PORT to the ADB port assigned to your BlueStacks
REM Android 11 instance before running this file.
REM ============================================================

set PORT=5556
set ADB=C:\Program Files\BlueStacks_nxt\HD-Adb.exe
set OUT=C:\CFMOTO_GPX\ride_capture.txt

if not exist C:\CFMOTO_GPX mkdir C:\CFMOTO_GPX

echo Connecting to BlueStacks on 127.0.0.1:%PORT% ...
"%ADB%" connect 127.0.0.1:%PORT%

echo.
echo Connected devices:
"%ADB%" devices

echo.
echo Clearing old logcat...
"%ADB%" -s 127.0.0.1:%PORT% logcat -c

echo.
echo ============================================================
echo Logcat capture is starting.
echo NOW open exactly ONE historical ride in CFMOTO RIDE.
echo Wait for the complete route to display.
echo Then return here and press Ctrl+C.
echo ============================================================
echo.

"%ADB%" -s 127.0.0.1:%PORT% logcat > "%OUT%"

echo.
echo Capture saved to:
echo %OUT%
pause
