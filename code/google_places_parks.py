from googleplaces import GooglePlaces, types, lang
import json
import cPickle as pickle

YOUR_API_KEY = ''

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.nearby_search(
        location='San Francisco, California', keyword='park',
        radius=100000, types=[types.TYPE_PARK])

if query_result.has_attributions:
    print query_result.html_attributions


for place in query_result.places:
    # Returned places from a query are place summaries.
    print place.name
    print place.geo_location
    print place.place_id

    # The following method has to make a further API call.
    place.get_details()
    # Referencing any of the attributes below, prior to making a call to
    # get_details() will raise a googleplaces.GooglePlacesAttributeError.
    print '/n',type(place.details)
    with open(place.name +'.pkl', 'wb') as f:
        pickle.dump(place.details, f)

    print place.details # A dict matching the JSON response from Google.
    # print place.local_phone_number
    # print place.international_phone_number
    # print place.website
    # print place.url
    # detail_json_data = query_request.json()

    # Getting place photos

    for photo in place.photos:
        # 'maxheight' or 'maxwidth' is required
        photo.get(maxheight=500, maxwidth=500)
        # MIME-type, e.g. 'image/jpeg'
        photo.mimetype
        # Image URL
        photo.url
        # Original filename (optional)
        photo.filename
        # Raw image data
        photo.data
