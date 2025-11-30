# Platformer Tutorial 2025

Following along with the platformer tutorial found here - https://www.youtube.com/watch?v=2gABYM5M0ww

Tutorial Progress:
- Introduction -- COMPLETE
- Installing Pygame -- COMPLETE
- Creating a Window -- COMPLETE
- Images, Input & Collisions -- COMPLETE
- Player, Tiles & Physics -- COMPLETE
- Camera & Sky -- COMPLETE
- Optimization -- COMPLETE
- Animation -- COMPLETE
- Level Editor -- COMPLETE
- Particles -- COMPLETE
- Jump & Slide -- COMPLETE
- Dash Attack -- COMPLETE
- Enemies, Guns, Death, etc. -- COMPLETE
- Screenshake -- COMPLETE
- Level Transitions -- COMPLETE
- Outlines -- COMPLETE
- Audio -- COMPLETE
- Making an executable -- COMPLETE
- Next Steps -- COMPLETE

Troubleshooting:
    - Audio
        - Needed to install pulseaudio and configure using info in audio_fix.md
    - Installer
        - Run `poetry run pyinstaller game.py --noconsole` to compile the game for sharing. Only works on Linux because that's how pyinstaller works.

Personal next steps:
    - Add controlled jumps (set an input timer to detect a hop vs a jump)
    - Document each function with a proper comment