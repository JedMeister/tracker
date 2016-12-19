#!/usr/bin/python

import json
from octohub.connection import Connection
from octohub.connection import Pager

app_data = []
with open("config.json","rb") as fob:
    config=json.load(fob)
conn = Connection(config["gh_token"])
uri = '/users/turnkeylinux-apps/repos'
pager = Pager(conn, uri, {}, max_pages=0)
for response in pager:
    data = response.json()
    for app in data:
        uri = '/repos/turnkeylinux-apps/' + app['name'] + '/tags'
        print uri
        pager2 = Pager(conn, uri, {}, max_pages=0)
        for response2 in pager2:
            data2 = response2.json()
            release = [0,0]
            for entry in data2:
                version = entry["name"].split("+")
                if len(version) < 2:
                    version.append(0)

                version[0] = float(version[0])
                version[1] = int(version[1])
                if version > release:
                    release = version

            if release[1] == 0:
                latest_release = str(release[0])
            else:
                latest_release = str(release[0]) + '+' + str(release[1])

            app_data.append({
                "app_name": app['name'],
                "release": latest_release,
                "app_page": app["homepage"],
                "gh_page": app["html_url"]
                })

with open("apps.json","wb") as fob:
    json.dump(app_data, fob, indent=4)

