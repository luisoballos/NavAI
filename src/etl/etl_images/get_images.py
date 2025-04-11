import requests

def generate_image(coordinates, API_KEY, SVS_API, count):    
    params = {
        "size": "640x640",          # Max base size (640x640)
        "scale": 2,                 # Doubles resolution to 1280x1280
        "location": coordinates,    # "latitude,longitude"
        "key": API_KEY,
        # Optional adjustments
        #"heading": "0",             # 0-360° (compass direction)
        "fov": "120",                # Field of view (1-120)
        "pitch": "0"                 # Up/down angle (-90 to 90)
    }

    # Send GET request
    response = requests.get(SVS_API, params=params)
    
    # Save file
    if response.status_code == 200:
        with open(f"../../img/streetview{count}.jpg", "wb") as f:
            f.write(response.content)
    else:
        print(f"Error: {response.status_code}: {response.text}")
    return (response)
    
def get_images(decoded_route, API_KEY, SVS_API):

    # Generate images for each coordinate in the route
    images = []
    count = 0               #To avoid overload
    for i in range(0, 5):
        point = decoded_route[i]
        lat = point['lat']
        lng = point['lng']
        coordinates = f"{lat},{lng}"
        image_response = generate_image(coordinates, API_KEY, SVS_API, count)
        count += 1
        
        if image_response.status_code == 200:
            images.append(image_response.content)
        else:
            print(f"Error fetching image for {coordinates}: {image_response.status_code}")  

    return images


    #Generate one image for each point in the route
    # image_array = []
    # for i in range(0,5): # Avoiding overload
    #     response = generate_image(f"{decoded_route[i]['lat']},{decoded_route[i]['lng']}")
    #     # for key, value in response.headers.items():
    #     #    print(f"{key}: {value}")
    #     #    print(response.cookies)
    #     #    print(response.headers[])
    #     #    print(response.apparent_encoding)
    #     image_array.append(response.content)
    #     # Save the image to a file
    #     with open("streetview.jpg", "wb") as f:
    #         f.write(image_array[i])
    #     # Display the first image
    #     img = mpimg.imread("streetview.jpg")
    #     plt.figure(figsize=(10, 10))
    #     plt.imshow(img)
    #     plt.axis('off')
    #     plt.show()