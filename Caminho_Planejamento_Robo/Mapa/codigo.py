from xml.dom import minidom
print(minidom.parse('bitmap.svg').toprettyxml())