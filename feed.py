#! /usr/bin/env python3

import yaml
import xml.etree.ElementTree as ET

with open("feed.yaml", "r") as file:
    yaml_data = yaml.safe_load(file)

rss = ET.Element("rss", {
    "version": "2.0",
    "xmlns:itune": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
})

channel = ET.SubElement(rss, "channel")

link_prefix = yaml_data['link']

ET.SubElement(channel, "title").text = yaml_data['title']
ET.SubElement(channel, "format").text = yaml_data['format']
ET.SubElement(channel, "subtitle").text = yaml_data['subtitle']
ET.SubElement(channel, "itunes:author").text = yaml_data['author']
ET.SubElement(channel, "description").text = yaml_data['description']

ET.SubElement(channel, "itunes:image", {"href": link_prefix + yaml_data['image']})

ET.SubElement(channel, "language").text = yaml_data['language']

ET.SubElement(channel, "link").text = link_prefix

ET.SubElement(channel, "itunes:category", {"text": yaml_data['category']})

for item in yaml_data['item']:
    item_element = ET.SubElement(channel, "item")
    ET.SubElement(item_element, "title").text = item['title']
    ET.SubElement(item_element, "itunes:author").text = yaml_data['author']
    ET.SubElement(item_element, "description").text = item['description']
    ET.SubElement(item_element, "itunes:duration").text = item['duration']
    ET.SubElement(item_element, "pubDate").text = item['published']

    ET.SubElement(item_element, "enclosure", {
        "url": link_prefix + item['file'],
        "type": "audio/mpeg",
        "length": item['length']
    })

output_tree = ET.ElementTree(rss)
output_file = "podcast.xml"
output_tree.write(output_file, encoding='UTF-8', xml_declaration=True)

print("Podcast feed successfully generated.")
