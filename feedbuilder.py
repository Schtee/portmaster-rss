import datetime 
import dateutil.parser
import rfeed
import requests
import dateutil

res = requests.get("https://raw.githubusercontent.com/PortsMaster/PortMaster-Info/main/ports.json")
ports = res.json()['ports']

port_keys = list(ports.keys())
port_keys.sort(reverse=True, key=lambda k : ports[k]['source']['date_added'])
port_keys = port_keys[:20]

rss_items = []

for key in port_keys:
	port = ports[key]

	image_url = None
	if port['attr']['image']['screenshot'] != None:
		if port['source']['repo'] == 'main':
			image_url = f"https://raw.githubusercontent.com/PortsMaster/PortMaster-New/main/ports/{port['name'].replace('.zip', '/')}{port['attr']['image']['screenshot']}"
		elif port['source']['repo'] == 'multiverse':
			image_url = f"https://raw.githubusercontent.com/PortsMaster-MV/PortMaster-MV-New/main/ports/{port['name'].replace('.zip', '/')}{port['attr']['image']['screenshot']}"
	
	item = rfeed.Item(
		title = port['attr']['title'],
		link = f"https://portmaster.games/detail.html?name={port['name'].replace('.zip', '')}",
		description = f"<![CDATA[<img src=\"{image_url}\" /><br />{port['attr']['desc']}]]>",
		author = ','.join(port['attr']['porter']),
		guid = rfeed.Guid(port['name']),
		pubDate = dateutil.parser.parse(port['source']['date_added'])
	)
	rss_items.append(item)

feed = rfeed.Feed(
	title = "PortMaster Ports",
	link = "https://portmaster.games",
	description = "A feed of PortMaster games",
	language = "en-US",
	lastBuildDate = datetime.datetime.now(),
	items = rss_items)

with open("out/feed.xml", "w", encoding="utf-8") as f:
	f.write(feed.rss())