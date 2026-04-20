#!/usr/bin/env python3
"""
auto_notif.py -- Automate Android notifications (send test notifs, track activity)
Usage: python3 auto_notif.py --send "Test notification"
       python3 auto_notif.py --monitor
"""
import subprocess, argparse, time

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

def send_notification(title, text):
    adb(f'cmd notification post -S bigtext -t "{title}" "AutoBot" "{text}"')
    print(f"✓ Sent: {title}")

def monitor_notifications():
    proc = subprocess.Popen("adb logcat NotificationManager:D *:S", 
                           shell=True, stdout=subprocess.PIPE, text=True)
    print("Monitoring notifications (Ctrl+C to stop)...")
    for line in proc.stdout:
        if "NotificationRecord" in line:
            print(f"📬 {line.strip()[:80]}")

parser = argparse.ArgumentParser()
parser.add_argument("--send", help="Send test notification")
parser.add_argument("--monitor", action="store_true")
args = parser.parse_args()

if args.send:
    send_notification("Test", args.send)
elif args.monitor:
    monitor_notifications()
