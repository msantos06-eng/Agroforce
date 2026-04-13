import numpy as np

def calculate_ndvi(red, nir):
    return (nir - red) / (nir + red + 1e-10)


def ndvi_farm_mean():

    # simulação (depois vem Sentinel real)
    red = np.random.rand(100,100)
    nir = np.random.rand(100,100)

    ndvi = calculate_ndvi(red, nir)

    return float(ndvi.mean())
    import requests
import numpy as np

def get_ndvi(token, bbox):

    url = "https://sh.dataspace.copernicus.eu/api/v1/process"

    body = {
        "input": {
            "bounds": {
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [bbox]
                }
            },
            "data": [{"type": "sentinel-2-l2a"}]
        },
        "evalscript": """
        //VERSION=3
        function setup() {
            return {
                input: ["B04", "B08"],
                output: { bands: 1 }
            };
        }

        function evaluatePixel(sample) {
            return [(sample.B08 - sample.B04) / (sample.B08 + sample.B04)];
        }
        """
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    r = requests.post(url, json=body, headers=headers)

    return r.content