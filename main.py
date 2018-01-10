import cv2
import os
import glob
# files for making xml output
import xml.etree.cElementTree as ET 
import xml.dom.minidom
from xml.dom import minidom


def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


# folder_path
img_files = glob.glob('/home/sharma/Desktop/ESSI TASK/NFPA dataset/*.jpg')


for image_name in img_files:

	filename = image_name.split('.')[0]
	text_file_name = filename+'.txt'

	explicit_file_name = image_name.split('/')[-1]

	annotation = ET.Element("annotation")

	ET.SubElement(annotation,"folder").text = "NFPA dataset"

	ET.SubElement(annotation,"filename").text = explicit_file_name

	ET.SubElement(annotation,"path").text = image_name

	source = ET.SubElement(annotation,"source")

	ET.SubElement(source,"database").text = "Unknown"


	lines = open(text_file_name).read().splitlines()

	img = cv2.imread(image_name)

	height, width, channels = img.shape



	size = ET.SubElement(annotation,"size")

	ET.SubElement(size,"width").text = str(width)
	ET.SubElement(size,"height").text = str(height)
	ET.SubElement(size,"depth").text = str(channels)



	for data_points in lines:

		data_points = data_points.split(' ')

		x = float(data_points[1])
		y = float(data_points[2])
		w = float(data_points[3])
		h = float(data_points[4])

		y_max = height*(2*y+h)/2

		y_min = height*(2*y-h)/2

		x_max = width*(2*x+w)/2

		x_min = width*(2*x-w)/2

		x_min = int(x_min)
		x_max = int(x_max)
		y_min = int(y_min)
		y_max = int(y_max)

		cv2.rectangle(img,(x_min,y_min),(x_max,y_max),(0,0,255),3)


		object_1 = ET.SubElement(annotation,"object")

		ET.SubElement(object_1,"name").text = "nfpa"
		ET.SubElement(object_1,"pose").text = "Unspecified"
		ET.SubElement(object_1,"truncated").text = "0"
		ET.SubElement(object_1,"difficult").text = "0"

		bndbox = ET.SubElement(object_1,"bndbox")

		ET.SubElement(bndbox,"xmin").text = str(x_min)
		ET.SubElement(bndbox,"ymin").text = str(y_min)
		ET.SubElement(bndbox,"xmax").text = str(x_max)
		ET.SubElement(bndbox,"ymax").text = str(y_max)



	image_file_save_add = '/home/sharma/Desktop/ESSI TASK/OutputImages/'+explicit_file_name

	cv2.imwrite(image_file_save_add,img)
	# print explicit_file_name


	tree = ET.ElementTree(annotation)

	xml_file_name = explicit_file_name.split('.')[0]

	xml_file_address = '/home/sharma/Desktop/ESSI TASK/OutputLabels/'+xml_file_name+'.xml'

	output_file = open( xml_file_address, 'w' )
	output_file.write( prettify(annotation))
	output_file.close()

	
