# Aotearoa AgriHire

Aotearoa AgriHire is a digital platform designed to modernize the way farm equipment
and land are rented across New Zealand. It connects farmers, landowners, rental
companies, and dealers in one easy-to-use system, allowing them to list, manage, and
rent out agricultural equipment and land.

### Production URL - 


## Test Users

```
q1/Test@123
q2/Test@123

```


## 🚀 Features

- **User Authentication:** Secure user registration and login system.  
- **Land Leasing:** List, view, and manage land parcels available for short or long-term lease.  
- **Equipment Hire:** Rent and manage agricultural equipment from verified owners.  
- **Requests & Approvals:** Tenants can send requests, schedule visits, and sign digital agreements.  
- **Weather Forecast Integration:** Uses OpenWeatherMap API for weather-based planning.  
- **Responsive UI:** Built using Bootstrap for seamless desktop and mobile experiences.


### Documents
Please click [here](https://miro.com/app/board/uXjVJYioWy8=/?moveToWidget=3458764635965259741&cot=14) to view the mind mapping diagram

Wireframe design completed - Please [click here](docs/wireframe/AotearoaAgriHire_wireframe.pdf)

User stories list - Please [click here](docs/user_stories/user_stories.pdf)

### Weather API

The OpenWeatherMap 5-Day / 3-Hour Forecast API(5 Day Weather Forecast - OpenWeatherMap, n.d.) provides detailed weather predictions for any geographic location.

```bash
api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}

```

### Geo Coding

In this project, Nominatim API(Overview - Nominatim 5.1.0 Manual, 2025), an open-source geocoding service powered by OpenStreetMap (OSM) is used to convert place names or addresses into geographic coordinates (latitude and longitude).

```bash
https://nominatim.openstreetmap.org/search?addressdetails=1&q=bakery+in+berlin+wedding&format=jsonv2&limit=1
```

Sample Response look like this

```bash
[
  {
    "address": {
      "ISO3166-2-lvl4": "DE-BE",
      "borough": "Mitte",
      "city": "Berlin",
      "country": "Deutschland",
      "country_code": "de",
      "neighbourhood": "Sprengelkiez",
      "postcode": "13347",
      "road": "Lindower Straße",
      "shop": "Ditsch",
      "suburb": "Wedding"
    },
    "addresstype": "shop",
    "boundingbox": [
      "52.5427201",
      "52.5427654",
      "13.3668619",
      "13.3669442"
    ],
    "category": "shop",
    "display_name": "Ditsch, Lindower Straße, Sprengelkiez, Wedding, Mitte, Berlin, 13347, Deutschland",
    "importance": 9.99999999995449e-06,
    "lat": "52.54274275",
    "licence": "Data © OpenStreetMap contributors, ODbL 1.0. http://osm.org/copyright",
    "lon": "13.36690305710228",
    "name": "Ditsch",
    "osm_id": 437595031,
    "osm_type": "way",
    "place_id": 204751033,
    "place_rank": 30,
    "type": "bakery"
  }
]

```




### References

5 day weather forecast - OpenWeatherMap. (n.d.). Openweathermap.org. https://openweathermap.org/forecast5


Overview - Nominatim 5.1.0 Manual. (2025). Nominatim.org. https://nominatim.org/release-docs/latest/api/Overview/
