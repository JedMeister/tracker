#!/usr/bin/python

import json
import requests
import os
import datetime
from lxml import html
from octohub.connection import Connection
from octohub.connection import Pager

def getTimestamp():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return timestamp

def checkAndBackupFile(file):
    if os.path.isfile(file):
        backup_name = file+".bak."+getTimestamp()
        print(file+" already exists. File renamed to "+backup_name)
        os.rename(file, backup_name)

def checkWebStatus(uri):
    try:
        r = requests.head(uri, allow_redirects=True)
        return_code = {
            200: "stable",
            403: "deprecated",
            404: "not_found"
        }
        code = return_code.get(r.status_code, "error: unknown code "+str(r.status_code))
        return code
    except requests.ConnectionError:
         print("failed to connect to "+uri)

def getURIText(uri, type):
    try:
        r = requests.get(uri)
        if type == "text":
            file = r.text
        elif type == "web":
            file = html.fromstring(r.content)
        else:
            raise ValueError("type not known", type)
        return file
    except requests.ConnectionError:
        print("failed to connect to "+uri)

def checkChangelog(app):
    uri = "https://raw.githubusercontent.com/turnkeylinux-apps/"+app+"/master/changelog"
    changelog = getURIText(uri, "text")
    head = changelog.split('\n', 1)[0]
    changelog_version = head.split(app+'-')[1].split()[0]
    changelog_revision = head.split(app+'-')[1].split()[1]
    return changelog_version, changelog_revision

def checkAppPage(app):
    uri = "https://www.turnkeylinux.org/"+app
    page = getURIText(uri, "web")
    web_version = page.xpath('//*/div[2]/div[3]/div[2]/span/text()')
    return web_version[0]

def checkMirror(app, version, arch, build):
    uri = "http://mirror.turnkeylinux.org/turnkeylinux/images/"+build
    if build == "proxmox":
        #assumes only amd64 proxmox builds
        uri += "/debian-8-turnkey-"+app+"_"+version+"-1_amd64.tar.gz"
    elif build in ("iso", "ova"):
        uri += "/turnkey-"+app+"-"+version+"-jessie-"+arch+"."+build
    else:
        raise ValueError("build not known", build)

    code = checkWebStatus(uri)

    if code == "stable":
        return "yes"
    else:
        return "not found"

def checkPVEIndex(app, pve_app_index):
    pve_index_version = pve_download = None
    for item in pve_app_index.split("\n\n"):
        if app in item:
            for line in item.split("\n"):
                if "Version" in line:
                    pve_index_version = line.split(": ")[1].split("-")[0]
                if "Location" in line:
                    pve_download = line.split(": ")[1]
    return pve_index_version, pve_download

app_data = []
appliance_list = ""
pve_app_index = getURIText('http://mirror.turnkeylinux.org/turnkeylinux/metadata/pve/aplinfo.dat', 'text')

checkAndBackupFile('appliance.list')
checkAndBackupFile('apps.json')

with open("config.json","rb") as fob:
    config=json.load(fob)

conn = Connection(config["gh_token"])
uri = '/users/turnkeylinux-apps/repos'
pager = Pager(conn, uri, {}, max_pages=0)
for response in pager:
    notes = ""
    data = response.json()
    for app in data:
        notes = ""
        print("Processing appliance: "+app['name'])
        uri = '/repos/turnkeylinux-apps/' + app['name'] + '/tags'
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
                latest_tag = str(release[0])
            else:
                latest_tag = str(release[0]) + '+' + str(release[1])

        if not app['homepage']:
            status = "error"
            notes += "|no homepage listed on GH repo|"
            app['homepage'] = "https://www/turnkeylinux.org/"+app['name']

        status = checkWebStatus(app['homepage'])

        downloads = {}

        if status == "stable" and app['name'] != "bitkey":

            appliance_list += app['name'] + "\n"

            changelog_ver, changelog_rev = checkChangelog(app['name'])

            if changelog_ver != latest_tag:
                status = "error"
                notes += "|changelog version and tag version don't match|"

            for build in ("iso", "proxmox", "ova"):
                if build == "iso":
                    for arch in ("amd64", "i386"):
                        downloads[build+"-"+arch] = checkMirror(app['name'], latest_tag, arch, build)
                else:
                    downloads[build] = checkMirror(app['name'], latest_tag, "amd64", build)
                if downloads["iso-amd64"] == "not found":
                    status = "error"
                    notes += "|iso-amd64 not found on mirror|"

            pve_index_version, pve_download = checkPVEIndex(app['name'], pve_app_index)

            if pve_index_version:
                if pve_index_version != latest_tag:
                    status = "error"
                    notes += "|pve index version does not match latest tag|"
                if pve_index_version != changelog_ver:
                    status = "error"
                    notes += "|pve index version does not match latest changelog entry|"
                if checkWebStatus(pve_download) != "stable":
                    status = "error"
                    notes += "|appliance from pve index not found on mirror|"
            else:
                pve_index_version = "not listed"
                notes += "|appliance not listed in pve index|"

            app_page_version = checkAppPage(app['name'])

        else:
            notes = "|skipped sections as noted|"
            for key in ['iso-amd64', 'iso-i386', 'proxmox', 'ova']:
                downloads[key] = "skipped"
            pve_index_version = "skipped"
            app_page_version = "skipped"

        app_data.append({
            "app name": app['name'],
            "app github tag": latest_tag,
            "app page version": app_page_version,
            "app status": status,
            "app webpage": app["homepage"],
            "changelog version": changelog_ver,
            "changelog revison": changelog_rev,
            "file: iso-amd64": downloads["iso-amd64"],
            "file: iso-i386": downloads["iso-i386"],
            "file: proxmox": downloads["proxmox"],
            "proxmox index version": pve_index_version,
            "file: ova-amd64": downloads["ova"],
            "github page": app["html_url"],
            "notes": notes,
            "timestamp": getTimestamp()
            })

with open("apps.json","wb") as fob:
    json.dump(app_data, fob, indent=4, sort_keys=True)

with open("appliance.list", "wb") as fob:
    fob.write(appliance_list)

