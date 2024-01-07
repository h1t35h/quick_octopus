import requests


def get_catalog_id(download_page, catalog):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'{download_page}',
        'Connection': 'keep-alive',
        'Cookie': 'citrix_ns_id=AAE7nKKZZTuXbDIAAAAAADuMGtjGAxHPGX4gO0RkPkSDj1cqh8oLwdaSFCJh-PD7Ow==ZqmZZQ==-OhQvD73QqGllmT4cox8oST1ZOY=; fontSize=67.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    response = requests.get(
        url=f'https://data.gov.in/backend/dms/v1/catalog/{catalog}?_format=json',
        headers=headers
    )
    return response.json()['nid'][0]['value']


def get_resources(download_page, catalog_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'{download_page}',
        'Connection': 'keep-alive',
        'Cookie': 'citrix_ns_id=AAE7nKKZZTuXbDIAAAAAADuMGtjGAxHPGX4gO0RkPkSDj1cqh8oLwdaSFCJh-PD7Ow==aKmZZQ==4NnS0oYKuBenIfVjjJmojOHfhZY=; fontSize=67.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
    response = requests.get(
        url=f'https://data.gov.in/backend/dmspublic/v1/resources?filters%5Bcatalog_reference%5D={catalog_id}&offset=0&limit=300&sort%5Bchanged%5D=desc&filters%5Bdomain_visibility%5D=4',
        headers=headers
    )
    return response.json()['data']['rows']


def get_catalog_resources(download_page):
    catalog = download_page[download_page.find('catalog/') + len('catalog/'):]
    catalog_id = get_catalog_id(download_page=download_page, catalog=catalog)
    resources_json = get_resources(download_page=download_page, catalog_id=catalog_id)
    resource_paths = []
    for resource in resources_json:
        resource_paths.append(resource["node_alias"][0])
    return resource_paths


if __name__ == '__main__':
    download_page = 'https://data.gov.in/catalog/fleet-personnel-and-financial-statistics-2016-17'
    resource_paths = get_catalog_resources(download_page)
    for resource in sorted(resource_paths):
        print(resource)

