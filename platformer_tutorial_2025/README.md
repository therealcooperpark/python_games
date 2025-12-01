# Platformer Tutorial 2025

Following along with the platformer tutorial found here - https://www.youtube.com/watch?v=2gABYM5M0ww

## Tutorial Progress:
- Totally Complete!

## Troubleshooting Install on New Devices:
- Audio
    - Needed to install pulseaudio and configure using info in `docs/audio_fix.md`
- Installer
    - Run `poetry run pyinstaller game.py --noconsole` to compile the game for sharing. Only works on Linux because that's how pyinstaller works.

## Claude recommended next steps:
- See `docs/ai_recommendations.md`

## Personal next steps:
- Add controlled jumps (set an input timer to detect a hop vs a jump)
- Document each function with a proper comment and type hints
- Add a new ability (power-shot?)
    - Ranged attack, earned after X kills. Add a UI element to show this?