import collection


if __name__ == '__main__':

    # collection
    collection.crawling_tourspot_visitor(district='서울특별시', start_year=2017, end_year=2017)

    for country in [('중국', 112), ('일본', 130), ('미국', 275)]:
        collection.crawling_foreign_visitor(country, 2017, 2017)
