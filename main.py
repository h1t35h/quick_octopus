from downloads.catalog_fetcher import get_catalog_resources
from downloads.resource_fetcher import download_resource

if __name__ == '__main__':
    download_urls = [
        # "https://data.gov.in/catalog/basic-road-statistics-india-2017-18",
        # anurag # "https://data.gov.in/catalog/fleet-personnel-and-financial-statistics-2016-17",
        # anurag # "https://data.gov.in/catalog/operating-statistics-trains",
        # "https://data.gov.in/catalog/review-performance-state-road-transport-undertakings-srtus-2017-18-and-2018-19",
        # "https://data.gov.in/catalog/review-performance-state-road-transport-undertakings-srtus-april2016-march-2017",
        # "https://data.gov.in/catalog/road-accidents-india-2019",
        # "https://data.gov.in/catalog/road-transport-year-book-2017-18-2018-19",
        # "https://data.gov.in/catalog/road-transport-year-book-2019-20",
        # "https://data.gov.in/resource/basic-fare-ordinary-passenger-trains-vis-vis-express-trains-over-non-suburban-sections",
        # "https://data.gov.in/resource/growth-indian-fleet-type-vessels-1985-2022",
        "https://data.gov.in/resource/passenger-bus-transport-operational-aggregates-during-1979-80",
    ]

    # ViR1kXa1PBJk3DJHuB1uuQ64tQlDVZ518xQE47RKgfQ
    for url in download_urls:
        if "catalog" in url:
            resources = get_catalog_resources(url)
            catalog = url[url.find('catalog/') + len('catalog/'):]
            for resource in resources:
                download_resource(
                    download_page=f'https://data.gov.in{resource}',
                    dir=f'data/{catalog}')
            print(f"Catalog: {url}")
        elif "resource" in url:
            download_resource(download_page=url, dir=f'data')
            print(f"Resource: {url}")
