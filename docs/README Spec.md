# README and tooltip spec

These are this template's defaults for the words users read. Change them if you like; if you do, update this file so Claude follows your version.

## README.md

The README at the project root is the only copy. `build.py` puts it inside the legacy zip, so it is what users read after they install.

Seven sections, top to bottom:

1. `# <Name>`, then one sentence saying what the add-on is.
2. `## Why I made this`. The author writes this, in their own words. Claude never writes or rewrites it; if it is empty, leave the placeholder and say so.
3. `## What it does`. A short paragraph in the user's words. What happens when you use it. No implementation talk.
4. `## Install`. The steps for the install type you ship, and the minimum Blender version.
   - Legacy zip: Edit > Preferences > Add-ons > arrow menu > Install from Disk, pick the zip, tick it on.
   - Extension: Edit > Preferences > Get Extensions, search for it and click Install. Or, for a downloaded zip, Get Extensions > arrow menu > Install from Disk.
5. `## How to use`. Where to find it (for example "Press N in the 3D Viewport and open the Addon Name tab"), then every button and setting you can see, in the order you see it, one line each, with the exact labels from the panel. Then the same for the preferences, if they show anything.
6. `## Bugs and feedback`. Where to report a bug. If the links footer has a bug report button, say it goes to the same place.
7. `## Thanks`. Anyone you want to credit. Delete the section if there is no one.

Leave out: "Version:" lines, changelogs, build and zip instructions, developer and test notes, an "Author:" line (Blender's add-on list already shows it), and anything a user cannot see or do.

## Skeleton

`ADDON_README.md` is the skeleton. `build.py` ships it in the zip while it exists. `/setup-addon` fills it in and moves it over `README.md`, which until then describes the template. Do the same by hand if you set the project up without it.

## Voice

- Plain sentences, second person ("you"), short.
- No hype words ("powerful", "seamless", "effortless", "revolutionary").
- Say what happens, not what the add-on "allows you to" do.
- No em dashes. Use a comma, a colon, a full stop or brackets.

## Tooltips and other UI text

- Operator docstrings and `bl_description`, property `description=`, and panel docstrings: one line that says what happens when you click, or what the setting changes. It must match what the code does today.
- `self.report()` messages: say what happened or what to do next ("Pick a target object in this view layer first").
- Labels (`bl_label`, `name=`, `text=`): short, and the same words the README uses.
- `bl_info["description"]` and the manifest `tagline`: one user-facing sentence in the same voice. The tagline has at most 64 characters and no full stop at the end.

## Code comments

Say why, not what. A comment that repeats the code gets deleted.

## After a change

If a control was added, renamed, moved or removed, update "How to use" so it still lists every control in panel order with the exact labels, and check every tooltip it touches.
