# Platformer Tutorial 2025

Following along with the platformer tutorial found here - https://www.youtube.com/watch?v=2gABYM5M0ww

## Tutorial Progress:
- Totally Complete!

## Troubleshooting Install on New Devices:
- Audio
    - Needed to install pulseaudio and configure using info in `docs/audio_fix.md`

## Distribution
Run `poetry run pyinstaller game.py --noconsole` to compile the game for sharing. Only works on Linux because that's how pyinstaller works.

## Personal next steps:
1. :white_check_mark: Implement Health / Damage instead of insta-kill hits
    - Add health to Player and Enemies
    - Add damage to dash and projectiles

2. Make map transition system
    - Start with travelling to a location after all enemies are dead to move on
        - COMPLETE
    - Turn the transition space into its own tile type and formalize the logic for it
    - Move travel position to "end of map"
    - Change transition screen to swipe instead of circle

3. Improve maps
    - Use the level editor to build larger map with more complexity
    - Make a "Boss Room" level for future use
    - Consider updating the level editor

4. Make a "Special Attack" for Player
    - Re-use Projectile Class
    - Earn on X kills
    - Add a UI element to show it's progress

5. Make a couple assets to fill out the game
    - Special Attack Projectile
    - "Final" Boss

6. Design the Boss in game

7. Consider miscellaneous improvements
    - New jump audio
    - Proper pause menu with:
        - Reset Fight
        - Quit
    - Start Screen
    - Minimap UI?
    - New Enemy w/ Asset
    - Talent or Powerup system?
    - Damage number pop-ups on damaged entities?
