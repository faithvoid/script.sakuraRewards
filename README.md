# sakuraRewards
Achievements system for XBMC4Xbox/XBMC4Gamers, powered by Insignia & xb.live
![](resources/icon.png)

## How to Install:
- Download and unzip the latest release file
- Copy "script.sakuraRewards" to "Q:/home/addons"
- In XBMC4Xbox/XBMC4Gamers, go into Settings -> Addon Manager, and enable sakuraRewards
- Once enabled, select "Configure", then enter your Insignia gamertag
- Restart your Xbox and watch as you unlock achievements automagically! Any time you boot into XBMC after unlocking an achievement, you'll get a notification for it!
- You can view your achievements at any time by going into Programs -> Addons -> sakuraRewards

## Configuration:
In the add-on settings, you can configure different variables, such as how long every notification should remain on screen (in ms, set to 5000 by default) as well as point style (15G, 15P, 15 points, 15), select your preferred option, get to grinding and watch as the points come in!

## FAQ
- "Do I need to log in?"
Nope! No login is required, simply point the script towards your Insignia gamertag and the xb.live API takes care of the rest. Yes, it's genuinely that easy!
- "Any (planned) support for offline achievements"?
Nope. This add-on specifically uses Insignia multiplayer statistic data and user-created achievements that target those statistics, none of this script is capable of reading offline information, and anything similar for singleplayer would be a Herculean task involving reading/writing memory addresses (not easily possible outside of devkit units) or save data. Even RetroAchievements doesn't have Xbox achievements for emulators, which have a much easier time accessing memory addresses for those types of things.
- "I'm not getting any achievement notifications on login?"
Make sure you've input your Insignia gamertag correctly into the add-on settings, as well as making sure your system is properly connected to the internet. If you're online and still having issues, try deleting "Q:/userdata/addon_data/script.sakuraRewards/achievements.txt" and restarting, this will re-generate your "unlocked achievements" file, which is used to prevent showing duplicate notifications on startup. 

## TODO:
- Leaderboard support
- Add the ability to set things such as gamerscore, reputation, achievement totals, etc. as skin stings for skin developers (already implemented, but not in release builds in order to reduce potential bugginess, skin developers can reach out for this version!)

## Credits:
- x11x00x00x - for creating the xb.live API and achievements system that makes this all possible
- Insignia Team - for creating one of the best online service replacements of our genratio
- Jackie - Introducing x11x00x00x & I, teamwork makes the dream work!
