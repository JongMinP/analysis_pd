import os
from dateutil import rrule
from datetime import date
import json
from .api import api

RESULLT_DIRECTORY = '__results__/crawling'


def preprocess_tourspot_visitor(item):
    # print(item, type(item))
    #  현지인
    if 'csNatCnt' not in item:
        item['cont_locals'] = 0
    else:
        item['cont_locals'] = item['csNatCnt']
        del item['csNatCnt']

    #  외국인
    if 'csForCnt' not in item:
        item['count_forigner'] = 0
    else:
        item['count_forigner'] = item['csForCnt']
        del item['csForCnt']

    # 관광지
    if 'resNm' not in item:
        item['tourist_spot'] = ''
    else:
        item['tourist_spot'] = item['resNm']
        del item['resNm']

    # 날짜
    if 'ym' not in item:
        item['date'] = ''
    else:
        item['date'] = item['ym']
        del item['ym']

    # 시도
    if 'sido' not in item:
        item['restrict1'] = ''
    else:
        item['restrict1'] = item['sido']

        del item['sido']
    # 군
    if 'gungu' not in item:
        item['restrict2'] = ''
    else:
        item['restrict2'] = item['gungu']
        del item['gungu']

    del item['addrCd']
    del item['rnum']


def preprocess_foreign_visitor(data):

    # 국가 코드
    if 'natCd' not in data:
        data['country_code'] = 0
    else:
        data['country_code'] = data['natCd']
        del data['natCd']

    # 국가 이름
    if 'natKorNm' not in data:
        data['country_name'] = data['natKorNm']
        del data['natKorNm']

    # 날짜
    if 'ym' not in data:
        data['date'] = data['ym']
        del data['ym']

    # 방문객
    if 'num' not in data:
        data['visit_count'] = data['num']
        del data['num']

    del data['ed']
    del data['edCd']
    del data['rnum']


def crawling_foreign_visitor(
        country,
        start_year,
        end_year):
    results = []

    filename = '%s/%s(%s)_foreignvisitor_%s_%s.json' % (RESULLT_DIRECTORY, country[0], country[1], start_year, end_year)
    print(country[1])

    diff_year = end_year - start_year
    diff_months = len(list(rrule.rrule(
        rrule.MONTHLY,
        dtstart=date(start_year, 1, 1),
        until=date(end_year, 12, 31))))

    for year in range(0, diff_year + 1):
        start = start_year + year
        for month in range(1, diff_months+1):
            if month == 13:
                break
            # data = api.pd_fetch_foreign_visitor(country_code=country[1], year=start, month=montn)
            for data in api.pd_fetch_foreign_visitor(country_code=country[1], year=start, month=month):
                preprocess_foreign_visitor(data)
                results.append(data)

        diff_months = diff_months - (year * 12)

    with open(filename, 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return filename


def crawling_tourspot_visitor(district, start_year, end_year):
    results = []
    filename = '%s/%s_tourinstspot_%s_%s.json' % (RESULLT_DIRECTORY, district, start_year, end_year)

    diff_year = end_year - start_year
    diff_months = len(list(rrule.rrule(
        rrule.MONTHLY,
        dtstart=date(start_year, 1, 1),
        until=date(end_year, 12, 31))))

    for year in range(0, diff_year + 1):
        start = start_year + year
        for month in range(1, diff_months+1):
            if month == 13:
                break
            for items in api.pd_fetch_tourspot_visitor(district1=district, year=start, month=month):
                for item in items:
                    preprocess_tourspot_visitor(item)
                    results.append(item)

            diff_months = diff_months - (year * 12)

    with open(filename, 'w', encoding='utf-8') as outfile:
        json_string = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(json_string)

    return filename


if os.path.exists(RESULLT_DIRECTORY) is False:
    os.makedirs(RESULLT_DIRECTORY)
