import requests

def get_token(client_id: str, client_secret: str) -> str:
    url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def search_sentinel(token: str, bbox: str, start_date: str, end_date: str) -> dict:
    url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "$filter": (
            f"Collection/Name eq 'SENTINEL-2' and "
            f"ContentDate/Start gt {start_date}T00:00:00.000Z and "
            f"ContentDate/Start lt {end_date}T00:00:00.000Z"
        ),
        "$top": 5,
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()