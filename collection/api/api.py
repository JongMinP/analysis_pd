from .json_request import json_request
from urllib.parse import urlencode
from .json_request import json_request
from itertools import count
import json

SERVICE_KEY = 'xujjOwOH3FWxN%2F8JoBM4Hsv1NDTn7ijeb7uONJmmtwBYBh1ri0jw1imivNCo2MdCas1c5%2FqEyWrUOw4FCWCsEA%3D%3D'
END_POINT = 'http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList'
END_POINT2 = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'


def pd_gen_url(endpoint, service_key=SERVICE_KEY, **params):
    return '%s?serviceKey=%s&%s' % (endpoint, service_key, urlencode(params))


def pd_fetch_foreign_visitor(country_code=0, year=0, month=0, service_key=SERVICE_KEY):

    for page in count(start=1):
        url = pd_gen_url(endpoint=END_POINT2,
                         YM='{0:04d}{1:02d}'.format(year, month),
                         NAT_CD=country_code,
                         service_key=service_key,
                         _type='json',
                         pageNo=page)

        json_result = json_request(url)
        # print(json_result)
        status = json_result['response']['body']['items']
        if status == '':
            break
        # print(json_result)
        items = json_result['response']['body']['items']['item']

        # return items
        yield items


def pd_fetch_tourspot_visitor(
        district1='',
        district2='',
        tourspot='',
        year=0,
        month=0,
        start_year=0,
        end_year=0,
        service_key=SERVICE_KEY):

    for page in count(start=1):
        url = pd_gen_url(endpoint=END_POINT, service_key=service_key,
                         YM='{0:04d}{1:02d}'.format(year, month),
                         SIDO=district1,
                         GUNGU='',
                         RES_NM='',
                         numOfRows=10,
                         _type='json',
                         pageNo=page)

        json_result = json_request(url)
        status = json_result['response']['body']['items']
        if status == '':
            break

        items = json_result['response']['body']['items']['item']

        yield items



