from requests import get
from json import loads
from yaml import load, FullLoader

file = '_config.yml'

with open(file, 'r') as f:
    data = load(f, Loader=FullLoader)
    name = data["name"]
    waka = data["waka name"]

response = get(f"https://wakatime.com/api/v1/users/{waka}/stats/")
stats = loads(response.text)

file = 'source/stats.md'


def graph(percent):
    return f"[{'#' * int(round(percent, -1)/10)}{'-' * int(10-round(percent, -1)/10)}]"


with open(file, 'w') as f:
    f.write(f"```console\n{name}@github.com:~$ github.stats\n")
    f.write(f"\nlanguages{' ' * 45}editors\n---------{' ' * 45}-------\n")
    for i in range(9):
        f.write((stats["data"]["languages"][i]["name"] if i < 7 else '')
                + (' ' * (13 - len(stats["data"]["languages"][i]["name"])) if i < 7 else '')
                + (graph(stats["data"]["languages"]
                   [i]["percent"]) if i < 7 else '')
                + ('  ' + str(stats["data"]["languages"]
                   [i]["percent"]) + "%" if i < 7 else '')
                + (' ' * (7 - len(str(stats["data"]["languages"][i]["percent"]))) if i < 7 else '')
                + (stats["data"]["languages"][i]["text"] if i < 7 else '')
                + (' ' * (19 - len(str(stats["data"]["languages"][i]["text"]))) if i < 7 else '')
                + (stats["data"]["editors"][i]["name"] if i < 2 else '')
                + (' ' * (13 - len(str(stats["data"]["editors"][i]["name"]))) if i < 2 else '')
                + (graph(stats["data"]["editors"]
                   [i]["percent"]) if i < 2 else '')
                + ('  ' + str(stats["data"]["editors"][i]
                   ["percent"]) + "%" if i < 2 else '')
                + (' ' * (7 - len(str(stats["data"]["editors"][i]["percent"]))) if i < 2 else '')
                + (stats["data"]["editors"][i]["text"] if i < 2 else '')
                + ('operating systems' if i == 3 else '')
                + ('-----------------' if i == 4 else '')
                + (stats["data"]["operating_systems"][5-i]
                   ["name"] if i > 4 and i < 7 else '')
                + (' ' * (13 - len(str(stats["data"]["operating_systems"][5-i]["name"]))) if i > 4 and i < 7 else '')
                + (graph(stats["data"]["operating_systems"]
                   [5-i]["percent"]) if i > 4 and i < 7 else '')
                + ('  ' + str(stats["data"]["operating_systems"]
                   [5-i]["percent"]) + "%" if i > 4 and i < 7 else '')
                + (' ' * (7 - len(str(stats["data"]["operating_systems"]
                   [5-i]["percent"]))) if i > 4 and i < 7 else '')
                + (stats["data"]["operating_systems"][5-i]
                   ["text"] if i > 4 and i < 7 else '')
                + ("---------" if i == 7 else '')
                + ("\n" if i < 8 else ''))
    f.write("total        "
            + graph(stats["data"]["categories"][0]["percent"])
            + '  ' + str(stats["data"]["categories"][0]["percent"]) + "%"
            + '  ' + stats["data"]["categories"][0]["text"] + "\n```")

f.close
