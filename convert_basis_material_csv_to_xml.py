import xml.etree.ElementTree as ET
import csv

database = ET.Element('Database')
materials = ET.SubElement(database, 'Materials')

headers = [
    "Article",
    "Name",
    "Group_Name",
    "Unit_Measure",
    "Price",
    "Coef",
    "Length",
    "Width",
    "Thickness",
    "Sign",
    "Overhang",
    "Color",
    "Texture",
    "Class",
    "Sync_External",
]

with open('in.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader)  # пропускаем заголовки

    for row in reader:
        row = list(row)
        row.pop(2)  # убираем ID группы

        material = ET.SubElement(materials, 'Material')

        for header, elem in zip(headers, row):
            element = ET.SubElement(material, header)
            element.text = elem

with open('out.xml', 'wb') as xmlfile:
    tree = ET.ElementTree(database)
    tree.write(xmlfile, encoding='utf-8', xml_declaration=True)