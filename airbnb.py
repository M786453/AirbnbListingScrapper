import requests
from bs4 import BeautifulSoup
import json

def getAirbnbData(url):
    
    # Scrape data from given url 

    try:

        response = requests.get(url)

        html_content = response.content

        b_soup = BeautifulSoup(html_content, "html.parser")

        raw_data = b_soup.find('script', attrs={'id':'data-state'})

        json_data = json.loads(raw_data.text)

        data_sections = json_data["niobeMinimalClientData"][1][1]["data"]["presentation"]["stayProductDetailPage"]["sections"]["sections"]

        # Initializing Data Dictionary 

        data_dict = {"hostname": "","title": "", "description": "", "address":"", "images": [], "amenities": []}

        # Title

        data_dict["title"] = getTitle(json_data)

        # Getting other data i.e., Description, Address, Images, Amenities

        for parent_section in data_sections:

            if data_dict["hostname"] == "":

                data_dict["hostname"] = getHostname(parent_section)

            if data_dict["description"] == "":

                data_dict["description"] = getDescription(parent_section)
            
            if data_dict["address"] == "":

                data_dict["address"] = getAddress(parent_section)

            if len(data_dict["images"]) == 0:

                data_dict["images"] = getImages(parent_section)

            if len(data_dict["amenities"]) == 0:

                data_dict["amenities"] = getAmenities(parent_section)
        

        return data_dict
    
    except Exception as e:
        
        print(e)
        return "Error occured while scraping."


def getTitle(json_data):

    title = json_data["niobeMinimalClientData"][1][1]["data"]["presentation"]["stayProductDetailPage"]["sections"]["metadata"]["sharingConfig"]["title"]
    
    return title

def getDescription(parent_section):

    description = ""

    if parent_section["section"]["__typename"] == "PdpDescriptionSection":

        description = parent_section["section"]["htmlDescription"]["htmlText"]

                
    return description

def getAddress(parent_section):

    address = ""

    if parent_section["section"]["__typename"] == "LocationSection":

        address = parent_section["section"]["previewLocationDetails"][0]["title"]

    return address

def getImages(parent_section):

    images = []

    if  parent_section["section"]["__typename"] == "PhotoTourModalSection":
                
        images_section = parent_section["section"]["mediaItems"]

        for image in images_section:

            images.append(image["baseUrl"])

    return images

def getAmenities(parent_section):

    amenities_list = []

    if parent_section["section"]["__typename"] == "AmenitiesSection":
        amenities = parent_section["section"]["seeAllAmenitiesGroups"]
        
        for amenity_group in amenities:
                amenity_group_dict = {"title": amenity_group["title"], "amenities": [amenity["title"] for amenity in amenity_group["amenities"]]}
                amenities_list.append(amenity_group_dict)

        

    return amenities_list

def getHostname(parent_section):

    hostname = ""

    if parent_section["section"]["__typename"] == "HostProfileSection":

        raw_hostname = parent_section["section"]["title"]

        hostname = raw_hostname.split("Hosted by ")[1]

    return hostname


# with open("airbnb.json", "w") as out:

#     out.write(json.dumps(getAirbnbData("https://www.airbnb.com/rooms/31273922?adults=2&check_in=2023-04-23&check_out=2023-04-30&federated_search_id=532f443f-bc8b-408d-b3c5-d9518e1bad30&source_impression_id=p3_1681934249_AA0Jbg4CBAHynUDk")))
print(getAirbnbData("https://www.airbnb.com/rooms/31273922?adults=2&check_in=2023-04-23&check_out=2023-04-30&federated_search_id=532f443f-bc8b-408d-b3c5-d9518e1bad30&source_impression_id=p3_1681934249_AA0Jbg4CBAHynUDk"))