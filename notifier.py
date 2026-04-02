import xbmc
import xbmcgui
import xbmcaddon
import urllib2
import json
import os

# Addon and file global variables
ADDON = xbmcaddon.Addon()
ADDON_DATA = xbmc.translatePath(ADDON.getAddonInfo('profile'))
TRACKER_FILE = os.path.join(ADDON_DATA, "achievements.txt")
NOTIFICATION_MS = int(ADDON.getSetting('notification_ms') or 5000)
ADDON_PATH = xbmc.translatePath(ADDON.getAddonInfo('path')).decode('utf-8')
FALLBACK_ICON = xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'icon.png'))

# Functions to save and load new achievements into "achievements.txt" in "Q:/userdata/addon_data/script.sakuraRewards", alongside "settings.xml"
def load_processed_ids():
    if not os.path.exists(TRACKER_FILE):
        if not os.path.exists(ADDON_DATA):
            os.makedirs(ADDON_DATA)
        return set()
    with open(TRACKER_FILE, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def save_processed_id(ach_id):
    with open(TRACKER_FILE, 'a') as f:
        f.write(str(ach_id) + "\n")

# Function to send callback to xb.live on first launch for anonymous installation metrics
def send_callback(username):
    try:
        url = "https://xb.live/api/callback/dashboard"
        data = json.dumps({"message": "xbox"})
        
        req = urllib2.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        
        response = urllib2.urlopen(req)
        response_body = response.read()
        
        if response.getcode() == 200 and "success" in response_body.lower():
            xbmc.log("sakuraRewards - Callback successful")
            ADDON.setSetting('callback_sent', 'true')
        else:
            xbmc.log("sakuraRewards - Callback failed: Unexpected response body")
            
    except Exception as e:
        xbmc.log("sakuraRewards - Error sending callback: " + str(e))

# The real meat & potatoes of everything, fetches achievement data from xb.live's achievement API, formatting it to the user's preferences, as well as pulling information from MobCat's icon database where possible, falling back to the default imageURL from the API if unavailable.
def fetch_achievements():
    try:
        username = ADDON.getSetting('gamertag')
        if not username: return
	# This part handles displayed points suffix, ie; "15G / 15P / 15 points / 15 gamersccore"
        use_g = ADDON.getSetting('use_g_suffix') == "true"
        use_p = ADDON.getSetting('use_p_suffix') == "true"
        use_points = ADDON.getSetting('use_points_suffix') == "true"
        use_gamerscore = ADDON.getSetting('use_gamerscore_suffix') == "true"

        if use_g:
            suffix = "G"
        elif use_p:
            suffix = "p"
        elif use_points:
            suffix = " points"
        elif use_gamerscore:
            suffix = " Gamerscore"
        else:
            suffix = ""

        url = "https://xb.live/api/profile/{0}/achievements".format(username.replace(" ", "%20"))
        response = urllib2.urlopen(url)
        data = json.loads(response.read())

        processed_ids = load_processed_ids()
        queue = []

        for group in data.get('groups', []):
            game_title = group.get('displayName', 'Insignia').encode('utf-8')

            title_id = group.get('titleId')
            game_icon = None
            # Attempt to fetch square icons from MobCat's icon database first, otherwise, fall back to the default imageUrl or add-on image.
            if title_id:
                tid_str = str(title_id).upper()
                prefix = tid_str[:4]
                game_icon = "https://raw.githubusercontent.com/MobCat/MobCats-original-xbox-game-list/refs/heads/main/icon/{0}/{1}.png".format(prefix, tid_str)
            else:
                game_icon = group.get('imageUrl', '')

            if not game_icon or not str(game_icon).startswith('http'):
                game_icon = FALLBACK_ICON
            
            for ach in group.get('achievements', []):
                ach_id = str(ach.get('id'))
                
                if ach.get('earned') and ach_id not in processed_ids:
                    save_processed_id(ach_id)
                    processed_ids.add(ach_id)

                    points = ach.get('points', 0)
                    ach_name = ach.get('name', 'Unlocked!').encode('utf-8')
                    
                    queue.append({'title': game_title, 'msg': "{0}{1} - {2}".format(points, suffix, ach_name), 'icon': game_icon})

        for item in queue:
            xbmcgui.Dialog().notification(item['title'], item['msg'], item['icon'], NOTIFICATION_MS)
            xbmc.sleep(NOTIFICATION_MS)
                    
    except Exception as e:
        xbmc.log("sakuraRewards - Error fetching achievements: " + str(e))

# Main function: If the Insignia gamertag is set, the script will run, and on first run, will send a hit to the API for installation metrics.
if __name__ == '__main__':

    user = ADDON.getSetting('gamertag')

    if ADDON.getSetting('callback_sent') != "true" and user:
        send_callback(user)
        ADDON.setSetting('callback_sent', 'true')

    if user:
        fetch_achievements()