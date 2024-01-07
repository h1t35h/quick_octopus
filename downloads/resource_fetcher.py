from PIL import Image
import requests
import os

from downloads.gareeb_ocr import get_value


def get_resource_detail(download_page, resource):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'{download_page}',
        'Connection': 'keep-alive',
        'Cookie': 'citrix_ns_id=AAE77IaZZTuNXjIAAAAAADuMGtjGAxHPGX4gO0RkPkSDj1cqh8oLwdaSFCJh-PD7Ow==roqZZQ==h-I7BXGpmSy7FnqpXBf9ElZS21A=; fontSize=67.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    response = requests.get(url=f'https://data.gov.in/backend/dms/v1/resource/{resource}?_format=json',
                            headers=headers)

    return response.json()['nid'][0]['value']


def ref_image_down(download_page):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'{download_page}',
        'Connection': 'keep-alive',
        'Cookie': 'citrix_ns_id=AAA7s3iZZTuyIxcAAAAAADuMGtjGAxHPGX4gOzVglnj-t-2_KYp3QS5pOwB3wsrGOw==Wn-ZZQ==rOpg9iGVQMtNq6S5EN_dAOJHLzw=; fontSize=67.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    response = requests.get(
        url='https://data.gov.in/backend/dms/v1/ogdp/captcha/refresh/image/download_purpose?_format=json',
        headers=headers)
    return response


def get_captcha_value(download_page, captcha_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'image/avif,image/webp,*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'{download_page}',
        'Connection': 'keep-alive',
        'Cookie': 'citrix_ns_id=AAA7s3iZZTuyIxcAAAAAADuMGtjGAxHPGX4gOzVglnj-t-2_KYp3QS5pOwB3wsrGOw==dH-ZZQ==Jl955AE5uKi1eL3P12EvotX2aGw=; fontSize=67.5',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    captcha_image = Image.open(requests.get(f'https://data.gov.in/backend/dms/v1{captcha_url}', stream=True).raw)
    ocr_value = get_value(captcha_image)
    print(f"GOCR: {ocr_value}")
    return ocr_value
    # response = requests.get(f'https://data.gov.in/backend/dms/v1{captcha_url}')


def download_csv_file(download_page, captcha_details, resource_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': f'{download_page}',
        'Content-Type': 'application/json',
        'Origin': 'https://data.gov.in',
        'Connection': 'keep-alive',
        'Cookie': 'citrix_ns_id=AAA7s3iZZTuyIxcAAAAAADuMGtjGAxHPGX4gOzVglnj-t-2_KYp3QS5pOwB3wsrGOw==dH-ZZQ==Jl955AE5uKi1eL3P12EvotX2aGw=; fontSize=67.5',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    payload = {
        "catalog_id": [
            {
                "target_id": ""
            }
        ],
        "email": [
            {
                "value": "test@gmail.com"
            }
        ],
        "export_status": [
            {
                "value": "download"
            }
        ],
        "field_domain": [
            "4"
        ],
        "field_domain_visibility": [
            "4",
            "4"
        ],
        "file_type": [
            {
                "value": "csv"
            }
        ],
        "ip": [
            {
                "value": ""
            }
        ],
        "name": [
            {
                "value": "Test"
            }
        ],
        "ogdp_captcha_response": [
            {
                "value": f"{captcha_details['response']}"
            }
        ],
        "ogdp_captcha_sid": [
            {
                "value": f"{captcha_details['sid']}"
            }
        ],
        "ogdp_captcha_token": [
            {
                "value": f"{captcha_details['token']}"
            }
        ],
        "parameters": {},
        "purpose": [
            {
                "value": "4"
            }
        ],
        "resource_id": [
            {
                "target_id": f"{resource_id}"
            }
        ],
        "uid": [
            {
                "value": 0
            }
        ],
        "usage": [
            {
                "value": "2"
            }
        ]
    }
    response = requests.post(url='https://data.gov.in/backend/dms/v1/ogdp/download_purpose?_format=json',
                             headers=headers,
                             json=payload)
    print(response)
    return response.json()


def download_file(url, filename, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, filename)
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
    else:
        print(f"Failed to download file. HTTP response code: {response.status_code}")


def download_resource(download_page, dir):
    resource = download_page[download_page.find("resource/") + len("resource/"):]
    resource_id = get_resource_detail(download_page, resource)
    print(f"resource_id: {resource_id}")
    image_down_response = ref_image_down(download_page).json()
    captcha_dowload_url = image_down_response['url']
    captcha_response = get_captcha_value(download_page, captcha_dowload_url)
    captcha_details = {
        'sid': image_down_response['sid'],
        'token': image_down_response['token'],
        'response': captcha_response
    }
    download_details = download_csv_file(download_page, captcha_details=captcha_details, resource_id=resource_id)
    print(download_details)
    download_file(download_details['download_url'], f"{resource}.csv", f'{dir}/')
    print(f"download_details: {download_details}")


if __name__ == '__main__':
    download_page = 'https://data.gov.in/resource/growth-indian-fleet-type-vessels-1985-2022'
    download_resource(download_page, 'data')
