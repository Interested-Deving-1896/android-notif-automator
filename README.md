# 🤖 Android Notification Automator

Advanced automation engine for Android notifications — intercept, filter, respond, and trigger actions.

## Features

- **Rule-based automation** — JSON rules with pattern matching
- **Auto-reply** — respond to SMS/messages automatically
- **Call blocking** — block calls/SMSfrom patterns
- **Action triggers** — launch apps, send intents, run shell commands on notification
- **No root required** — works via ADB + logcat monitoring

## Quick start

```bash
python3 automator.py --rules rules.json
```

## Rule format

```json
[
  {
    "trigger": {
      "app": "com.google.android.apps.messaging",
      "contains": ["urgent", "SOS"]
    },
    "actions": [
      {"type": "reply", "text": "Got it, on my way!"},
      {"type": "launch-app", "package": "com.google.android.apps.maps"},
      {"type": "shell", "cmd": "settings put global development_settings_enabled 1"}
    ]
  }
]
```
