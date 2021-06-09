<p align=center>
    <img src="https://developer.somfy.com/sites/default/files/img/SoOpen.png"/>
</p>
<p align=center>
    <a href="https://pypi.org/project/pymfy/"><img src="https://img.shields.io/pypi/v/pymfy.svg"/></a>
    <a href="https://github.com/tetienne/somfy-open-api/actions"><img src="https://github.com/tetienne/somfy-open-api/workflows/CI/badge.svg"/></a>
    <a href="https://codeclimate.com/github/tetienne/somfy-open-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/efefe25b6c0dc796bc1c/maintainability" /></a>
    <a href="https://codeclimate.com/github/tetienne/somfy-open-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/efefe25b6c0dc796bc1c/test_coverage" /></a>
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
</p>

This library is an attempt to implement the entire Somfy API in Python 3.
Documentation for the Somfy API can be found [here](https://developer.somfy.com/somfy-open-api/apis).

## Get developer credentials

1. Vist https://developer.somfy.com
2. Create an account
3. Open the _My Apps_ menu
4. Add a new App (for testing, redirect url can be anything in https)
5. Plug in your details into the test script below.

## Supported devices

Somfy currently exposes the following type of devices:

- [Blinds](https://developer.somfy.com/products/blinds-interior-and-exterior)
- [Rolling shutters](https://developer.somfy.com/products/rolling-shutters)
- [Cameras](https://developer.somfy.com/products/cameras)
- [Connected Thermostat](https://developer.somfy.com/products/connected-thermostat)

If you find on this [page](https://developer.somfy.com/products-services-informations) devices not yet handle by this
repository, don't hesitate to open an issue.

## Installation

```
pip install pymfy
```

## Limitation

Somfy support sent the following message to third party applications using their API.

```
Dear customer,

As you might have noticed, we have updated the quota policy of the Somfy Open API, in an ongoing effort to provide the best services to our users.

We are contacting you today to inform you about the new rules we are now applying to the API:
- First of all, no limitation will be applied on the POST /device/{deviceId}/exec endpoint as we want to provide you a total freedom on controlling your devices.
- On the other hand, polling frequency on the GET /site and child endpoints will now have to be under 1 call per minute.

To preserve an efficient and available service to any of our users, we want to keep the usage of the Open API to a usable but reasonable level to everybody. As we will keep monitoring the generated traffic and the potential impacts, be aware that we do reserve the rights to modify the authorized polling frequency or take any additional measure at any time as stated in our General Terms of Use.

Thank you for your understanding.
```

## Example usage

Print all covers position.

```python
import os
import json
from urllib.parse import urlparse, parse_qs

from pymfy.api.devices.roller_shutter import RollerShutter
from pymfy.api.somfy_api import SomfyApi
from pymfy.api.devices.category import Category

client_id = r"<CLIENT_ID>"  # Consumer Key
redir_url = "<REDIR_URL>"  # Callback URL (for testing, can be anything)
secret = r"<secret>"  # Consumer Secret


def get_token():
    try:
        with open(cache_path, "r") as cache:
            return json.loads(cache.read())
    except IOError:
        pass


def set_token(token) -> None:
    with open(cache_path, "w") as cache:
        cache.write(json.dumps(token))


cache_path = "/optional/cache/path"
api = SomfyApi(client_id, secret, redir_url, token=get_token(), token_updater=set_token)
if not os.path.isfile(cache_path):
    authorization_url, _ = api.get_authorization_url()
    print("Please go to {} and authorize access.".format(authorization_url))
    authorization_response = input("Enter the full callback URL")
    code = parse_qs(urlparse(authorization_response).query)["code"][0]
    set_token(api.request_token(code=code))

site_ids = api.get_sites()
devices = api.get_devices(site_ids[0], category=Category.ROLLER_SHUTTER)

covers = [RollerShutter(d, api) for d in devices]

for cover in covers:
    print(
        "Cover {} has the following position: {}".format(
            cover.device.name, cover.get_position()
        )
    )
```

## Contribute

The current [documentation](https://developer.somfy.com/products-services-informations) does not give enough information to implement all the devices.
If you want to contribute to this repository adding new devices, you can create an issue with the output of this script:

```python
import json
import re
from urllib.parse import urlparse, parse_qs
from pymfy.api.somfy_api import SomfyApi


client_id = r"<CLIENT_ID>"  # Consumer Key
redir_url = "<REDIR_URL>"  # Callback URL (for testing, can be anything)
secret = r"<secret>"  # Consumer Secret

api = SomfyApi(client_id, secret, redir_url)
authorization_url, _ = api.get_authorization_url()
print("Please go to {} and authorize access.".format(authorization_url))
authorization_response = input("Enter the full callback URL")
code = parse_qs(urlparse(authorization_response).query)["code"][0]
api.request_token(code=code)

site_ids = [s.id for s in api.get_sites()]
devices = [api.get("/site/" + s_id + "/device").json() for s_id in site_ids]

# Remove personal information
dumps = json.dumps(devices, sort_keys=True, indent=4, separators=(",", ": "))
dumps = re.sub('".*id.*": ".*",\n', "", dumps)

print(dumps)
```
