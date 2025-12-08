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

2. Refactor Game vs Scene logic to improve separation of logic.
    - Examples:
        - Player should be in Scene
        - Level progression logic should be in scene (at least until the logic between scenes changes)
        - Enemy killing logic (line 127) should move to scene
        - Death should move too (Line 133?)
        - Sparks
        - Projectiles
        - Particles
        - Handle Input function should go to scenes
    - All renders should still go to main game display, but called from the Scene I think
    - Render should check its own transition and the Scene will alter it with its own update
        - This sets us up for #3 where the transition affect can be triggered by different settings (death, touching transitioner, etc.)

3. Make map transition system
    - Start with travelling to a location after all enemies are dead to move on
        - COMPLETE
    - Turn the transition space into its own tile type and formalize the logic for it
        - Need to distinguish loading a new level from the actual graphic change of the transition.
    - Move travel position to "end of map"
    - Change transition screen to swipe instead of circle

4. Improve maps
    - Use the level editor to build larger map with more complexity
    - Make a "Boss Room" level for future use
    - Consider updating the level editor

5. Make a "Special Attack" for Player
    - Re-use Projectile Class
    - Earn on X kills
    - Add a UI element to show it's progress

6. Make a couple assets to fill out the game
    - Special Attack Projectile
    - "Final" Boss

7. Design the Boss in game

8. Consider miscellaneous improvements
    - New jump audio
    - Proper pause menu with:
        - Reset Fight
        - Quit
    - Start Screen
    - Minimap UI?
    - New Enemy w/ Asset
    - Talent or Powerup system?
    - Damage number pop-ups on damaged entities?
