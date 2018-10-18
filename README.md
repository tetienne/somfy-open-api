<img align="left" src="https://developer.somfy.com/sites/default/files/img/SoOpen.png">

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
from src.api.somfy_api import SomfyApi

client_id = r'<CLIENT_ID>'
redir_url = '<REDIR_URL>'
secret = r'<secret>'

api = SomfyApi(client_id, redir_url)
authorization_url = api.get_authorization_url()
print('Please go to {} and authorize access.'.format(authorization_url))
authorization_response = input('Enter the full callback URL')
api.request_token(authorization_response, secret)

sites = api.get_sites()
devices = api.get_devices(sites[0].id)

covers = [d for d in devices if 'roller_shutter' in d.categories]

for cover in covers:
    print(cover.name)


```

