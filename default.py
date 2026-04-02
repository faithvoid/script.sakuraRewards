import xbmcgui
import xbmcaddon
import urllib2
import json
import textwrap

ADDON = xbmcaddon.Addon()
gamertag = ADDON.getSetting('gamertag')

# Text wrapper helper for ensuring achievement data fits in XBMC dialog windows. Separated in case future logic (ie; leaderboards) is added.
def wrap_text(text, width=64):
    return "\n".join(textwrap.wrap(text, width))

# Where the magic happens, fetches achievements from the xb.live achievement API and displays it in a nice, readable, 360-esque format.
def ui_achievements():
    if not gamertag:
        xbmcgui.Dialog().ok('sakuraRewards', 'No Insignia gamertag found in settings, please add one and try again!')
        return

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

    try:
        url = "https://xb.live/api/profile/{0}/achievements".format(gamertag.replace(" ", "%20"))
        response = urllib2.urlopen(url)
        data = json.loads(response.read())

        total_gs = str(data.get('score', 0))
        groups = data.get('groups', [])
        
        chrono_groups = []
        seen_titles = set()

        for ach in data.get('achievements', []):
            t_id = ach.get('game_title_id')
            key = t_id if t_id else ach.get('category')

            if key not in seen_titles:
                for g in groups:
                    g_key = g.get('titleId') if g.get('titleId') else g.get('displayName')
                    if g_key == key:
                        chrono_groups.append(g)
                        seen_titles.add(key)
                        break

        for g in groups:
            key = g.get('titleId') if g.get('titleId') else g.get('displayName')
            if key not in seen_titles:
                chrono_groups.append(g)
                seen_titles.add(key)

        state = 1
        while state > 0:
            if state == 1:
                group_opts = ["{0} ({1}/{2})".format(g.get('displayName', u'Unknown').encode('utf-8'), 
                              g.get('unlockedCount', 0), g.get('totalCount', 0)) for g in chrono_groups]

                header = "{0} ({1}{2})".format(gamertag, total_gs, suffix)
                sel_group_idx = xbmcgui.Dialog().select(header, group_opts or ["No data found"])
                
                state = 2 if sel_group_idx != -1 else 0

            elif state == 2:
                selected_group = chrono_groups[sel_group_idx]
                group_achievements = selected_group.get('achievements', [])
                g_header = "{0} ({1}/{2})".format(selected_group.get('displayName', u'Unknown').encode('utf-8'), selected_group.get('unlockedCount', 0), selected_group.get('totalCount', 0))
                
                ach_opts = []
                for a in group_achievements:
                    status = "[X]" if a.get('earned') else "[ ]"
                    ach_opts.append("{0} {1} ({2}{3})".format(status, a.get('name', u'Unknown').encode('utf-8'), a.get('points', 0), suffix))
                
                sel_ach_idx = xbmcgui.Dialog().select(g_header, ach_opts)
                state = 3 if sel_ach_idx != -1 else 1

            elif state == 3:
                ach = chrono_groups[sel_group_idx].get('achievements', [])[sel_ach_idx]
                ach_title = "{0} ({1}{2})".format(ach.get('name', u'Achievement').encode('utf-8'), ach.get('points', 0), suffix)
                
                raw_desc = ach.get('description', u'No description provided.').encode('utf-8')
                ach_desc = wrap_text(raw_desc, width=64)
                
                if ach.get('unlocked_at'):
                    ach_desc += "\nUnlocked: {0}".format(ach.get('unlocked_at'))
                
                xbmcgui.Dialog().ok(ach_title, ach_desc)
                state = 2

    except Exception as e:
        xbmcgui.Dialog().ok("Error", "sakuraRewards error: " + str(e))

if __name__ == '__main__':
    ui_achievements()