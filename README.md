<p align=center>
    <img src="https://developer.somfy.com/sites/default/files/img/SoOpen.png"/>
</p>
<p align=center>
    <a href="https://travis-ci.org/tetienne/somfy-open-api"><img src="https://travis-ci.org/tetienne/somfy-open-api.svg?branch=master"/></a>
    <a href="https://codeclimate.com/github/tetienne/somfy-open-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/efefe25b6c0dc796bc1c/maintainability" /></a>
    <a href="https://codeclimate.com/github/tetienne/somfy-open-api/test_coverage"><img src="https://api.codeclimate.com/v1/badges/efefe25b6c0dc796bc1c/test_coverage" /></a>
</p>
 
This library is an attempt to implement the entire Somfy API in Python 3.
Documentation for the Somfy API can be found [here](https://developer.somfy.com/somfy-open-api/apis).

## Get developer credentials

1. Vist https://developer.somfy.com
2. Create an account
3. Open the *My Apps* menu
4. Add a new App
4. Plug in your details into the test script below.

## Example usage

Print all covers name.

```python
from src.api.devices.roller_shutter import RollerShutter
from src.api.somfy_api import SomfyApi

client_id = r'<CLIENT_ID>'
redir_url = '<REDIR_URL>'
secret = r'<secret>'

api = SomfyApi(client_id, redir_url)
authorization_url, state = api.get_authorization_url()
print('Please go to {} and authorize access.'.format(authorization_url))
authorization_response = input('Enter the full callback URL')
api.request_token(authorization_response, secret)
api.automatic_refresh()

sites = api.get_sites()
devices = api.get_devices(sites[0].id)

covers = [RollerShutter(d, api) for d in devices if 'roller_shutter' in d.categories]

for cover in covers:
    print("Cover {} has the following position: {}".format(cover.device.name, cover.position))

```

