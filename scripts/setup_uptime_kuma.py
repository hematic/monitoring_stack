from uptime_kuma_api import UptimeKumaApi, MonitorType
import getpass

KUMA_URL = "http://192.168.1.126:3001"
USERNAME = input("Uptime Kuma username: ")
PASSWORD = getpass.getpass("Uptime Kuma password: ")

api = UptimeKumaApi(KUMA_URL)
api.login(USERNAME, PASSWORD)
print("Logged in\n")

existing = {m["name"]: m["id"] for m in api.get_monitors()}


def group(name):
    if name in existing:
        print(f"Group: {name} (exists)")
        return existing[name]
    result = api.add_monitor(type=MonitorType.GROUP, name=name)
    print(f"Group: {name}")
    gid = result["monitorID"]
    existing[name] = gid
    return gid


def http(name, url, parent=None, accept_302=False):
    if name in existing:
        print(f"  ~ {name} (exists)")
        return
    codes = ["200-299", "302"] if accept_302 else ["200-299"]
    kwargs = dict(
        type=MonitorType.HTTP,
        name=name,
        url=url,
        interval=60,
        retryInterval=60,
        maxretries=3,
        accepted_statuscodes=codes,
    )
    if parent:
        kwargs["parent"] = parent
    api.add_monitor(**kwargs)
    print(f"  + {name}")


def ping(name, hostname, parent=None):
    if name in existing:
        print(f"  ~ {name} (exists)")
        return
    kwargs = dict(
        type=MonitorType.PING,
        name=name,
        hostname=hostname,
        interval=60,
        retryInterval=60,
        maxretries=3,
    )
    if parent:
        kwargs["parent"] = parent
    api.add_monitor(**kwargs)
    print(f"  + {name}")


# Media
g = group("Media")
http("Plex",          "https://192.168.1.90:32400/web",          g)
http("Sonarr",        "https://sonarr.apps.hematic.net",        g, accept_302=True)
http("Radarr",        "https://radarr.apps.hematic.net",        g, accept_302=True)
http("Jackett",       "https://jackett.apps.hematic.net",       g, accept_302=True)
http("qBittorrent",   "https://qbittorrent.apps.hematic.net",   g, accept_302=True)

# Books
g = group("Books")
http("Audiobookshelf", "https://listen.apps.hematic.net", g)
http("Komga",          "https://komga.apps.hematic.net",  g)

# Tools
g = group("Tools")
http("Stirling PDF",        "https://pdf.apps.hematic.net",         g, accept_302=True)
http("MeTube",              "https://metube.apps.hematic.net",      g, accept_302=True)
http("FileBrowser Quantum", "https://share.apps.hematic.net",       g, accept_302=True)
http("ConvertX",            "https://convertx.apps.hematic.net",    g, accept_302=True)
http("NexTerm",             "https://nexterm.apps.hematic.net",      g, accept_302=True)
http("Vaultwarden",         "https://vaultwarden.apps.hematic.net", g)
http("Paperless-NGX",       "https://paperless.apps.hematic.net",   g)
http("Immich",              "https://immich.apps.hematic.net",      g)
http("Foundry",             "https://foundry.apps.hematic.net",     g)

# Infrastructure
g = group("Infrastructure")
http("Homepage",             "https://home.apps.hematic.net",              g, accept_302=True)
http("Komodo",               "https://komodo.apps.hematic.net",            g)
http("Traefik",              "https://traefik-dashboard.apps.hematic.net", g)
http("Authelia",             "https://auth.apps.hematic.net",              g)
http("Grafana",              "https://grafana.apps.hematic.net",           g, accept_302=True)
http("Dozzle",               "https://dozzle.apps.hematic.net",            g, accept_302=True)
http("Scrutiny",             "https://scrutiny.apps.hematic.net",          g, accept_302=True)
http("Uptime Kuma",          "https://kuma.apps.hematic.net",              g)
http("Glances NUC",          "https://glances.apps.hematic.net",           g)
http("Glances Thinkcentre",  "https://glances2.apps.hematic.net",          g, accept_302=True)
http("AdGuard Home",         "http://192.168.1.90:8080",                   g)

# NAS
g = group("NAS")
http("DS920+",  "https://nas.apps.hematic.net",  g)
http("DS1815+", "https://nas2.apps.hematic.net", g)

# Servers
g = group("Servers")
ping("NUC",         "192.168.1.7",   g)
ping("Thinkcentre", "192.168.1.126", g)
ping("DS920+",      "192.168.1.90",  g)
ping("DS1815+",     "192.168.1.16",  g)

api.disconnect()
print("\nDone!")
