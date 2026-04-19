#!/usr/bin/env python3
"""
automator.py -- Advanced Android notification automation engine
Usage: python3 automator.py --rules rules.json [--daemon]
"""
import subprocess, json, re, time, argparse, sys
from pathlib import Path

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout.strip()

def parse_rules(filepath):
    with open(filepath) as f:
        return json.load(f)

def matches_trigger(notif_text, trigger):
    app_match = trigger.get("app", "") in notif_text or not trigger.get("app")
    if not app_match:
        return False
    
    contains = trigger.get("contains", [])
    if contains:
        return any(c.lower() in notif_text.lower() for c in contains)
    
    return True

def execute_action(action):
    atype = action.get("type", "")
    if atype == "reply":
        text = action.get("text", "")
        # Attempt to reply via SMS/messaging (simplified)
        escaped = text.replace("'", "\\'")
        adb(f"input text '{escaped}' && input keyevent 66")
        print(f"  → replied: {text[:50]}")
    
    elif atype == "launch-app":
        pkg = action.get("package", "")
        adb(f"am start -n {pkg}/{adb(f'cmd package resolve-activity --brief {pkg} | tail -1')}")
        print(f"  → launched: {pkg}")
    
    elif atype == "shell":
        cmd = action.get("cmd", "")
        adb(cmd)
        print(f"  → shell: {cmd[:50]}")
    
    elif atype == "notification":
        title = action.get("title", "")
        text = action.get("text", "")
        adb(f"cmd notification post -S bigtext -t '{title}' 'Automator' '{text}'")
        print(f"  → notif: {title}")

def monitor(rules, daemon=False):
    print(f"\n🤖 Notification Automator — {len(rules)} rules active")
    if daemon:
        print("  Running in daemon mode (Ctrl+C to stop)\n")
    
    seen = set()
    proc = subprocess.Popen(
        "adb logcat -v brief *:I",
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
    )
    
    try:
        while True:
            line = proc.stdout.readline()
            if not line: break
            
            for i, rule in enumerate(rules):
                trigger = rule.get("trigger", {})
                if matches_trigger(line, trigger):
                    key = f"{i}:{line[:50]}"
                    if key in seen:
                        continue
                    seen.add(key)
                    
                    actions = rule.get("actions", [])
                    print(f"\n[Rule {i+1}] Matched — executing {len(actions)} action(s)")
                    for action in actions:
                        execute_action(action)
            
            if not daemon:
                break
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        proc.terminate()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", required=True, help="Rules JSON file")
    parser.add_argument("--daemon", action="store_true", help="Run continuously")
    args = parser.parse_args()
    
    if not Path(args.rules).exists():
        print(f"Rules file not found: {args.rules}")
        sys.exit(1)
    
    rules = parse_rules(args.rules)
    monitor(rules, args.daemon)

if __name__ == "__main__":
    main()
