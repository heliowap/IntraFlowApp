# Intra Flow — Install (beta)

## 1. Install

1. Download `IntraFlow-*.dmg` from [Releases](https://github.com/heliowap/IntraFlowApp/releases/latest).
2. Open the DMG.
3. Drag **IntraFlow.app** into **Applications** (shortcut on the DMG).

## 2. First open (Gatekeeper)

This beta is **not notarized**. On first open, macOS may say the app can’t be verified. That’s expected.

Do **one** of these once:

**A — Finder**

1. In Applications, **right-click** IntraFlow.app → **Open** → **Open**.

**B — Terminal**

```bash
xattr -dr com.apple.quarantine /Applications/IntraFlow.app
```

Then open the app normally.

## 3. Permissions

**System Settings → Privacy & Security**

| Permission | Why |
| --- | --- |
| **Accessibility** | Global Trigger + insert text at the cursor |
| **Microphone** | Capture your voice |

Enable Intra Flow under Accessibility. Allow the mic when prompted.

## 4. OpenAI API key (BYOK)

On first run, paste your OpenAI API key.

- Needs **Realtime** + **Chat** enabled on the org.
- Stored only in the **Mac Keychain** — not in project files or logs.

## 5. Use

1. Focus a text field.
2. Hold **left-Option** (default Trigger) and speak.
3. Release to inject polished text at the cursor.

Menu-bar wave icon → Preferences, History, Impact, Mode, Trigger.

---

Feedback: [Issues](https://github.com/heliowap/IntraFlowApp/issues)
