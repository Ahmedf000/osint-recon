import PIL.ExifTags
from gmplot import gmplot
import subprocess
import os
from color.color import Colors
import sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim


def extract_exif(image):

    if not os.path.isfile(image):
        print(Colors.yellow(f"Your Image {image} doesn't exist"))
        sys.exit(1)

    image_path = image

    open_img = Image.open(image_path)
    get_exif = image.getexif()
    exif = {
        PIL.ExifTags.TAGS[t]:v
        for t, v in image.getexif().items()
        if t in PIL.ExifTags.TAGS
    }
    north = exif['GPSInfo'][2]
    east = exif['GPSInfo'][4]

    lat = north[0] + north[1] / 60 + north[2] / 3600
    lng = east[0] + east[1] / 60 + east[2] / 3600

    lat, lng = float(lat), float(lng)
    gmplot_ = gmplot.GoogleMapPlotter(lat, lng, 13)
    gmplot_.marker(lat, lng, 'green')
    gmplot_.draw('gps.html')

    geo_find = Nominatim(user_agent="Geolocating")
    location = geo_find.reverse(f"{lat},{lng}")
    
    return location





