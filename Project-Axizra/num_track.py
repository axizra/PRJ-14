import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import folium
from opencage.geocoder import OpenCageGeocode
key = "98b349e80c254fb1801322452c6eb0af"
number = input("Enter the phone number with country code: \n")
num_track = phonenumbers.parse(number)
location = geocoder.description_for_number(num_track, "en")
carrier_name = carrier.name_for_number(num_track, 'en')
num_timezone = timezone.time_zones_for_number(num_track)
print("Phone number Details:\n")
print("Location:" + " " + location)
print("Carrier Name:" + " " + carrier_name)
print("Timezone:" + "", num_timezone)
geocoder = OpenCageGeocode(key)
query = str(location)
results = geocoder.geocode(query)
lat = results[0]['geometry']['lat']
lng = results[0]['geometry']['lng']
myMap = folium.Map(loction=[lat,lng],zoom_start=9)
folium.Marker([lat,lng],popup=location).add_to(myMap)
myMap.save("Location.html")