import httpretty

from src.api.somfy_api import BASE_URL, SomfyApi


@httpretty.activate
def test_sites():
    with open('get_sites.json', 'r') as get_sites:
        httpretty.register_uri(httpretty.GET, BASE_URL + '/site', body=get_sites.read())
    sites = SomfyApi('foo', 'faa').get_sites()
    assert len(sites) == 2
    assert sites[0].id == '12345678-abcdefgh'
    assert sites[0].label == 'TaHoma'
    assert sites[1].id == 'abcdefgh-12345678'
    assert sites[1].label == 'Conexoon'
