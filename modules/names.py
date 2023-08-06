class Wait:
    short = 2
    long = 5
    extra_long = 10

class NameSpace:
    carrier_dict = {
        'Ryanair': ['FR'],
        'Eurowings': ['EW'],
        'Lufthansa': ['LH']
    }
    base = '/html/body/fsr-app/fsr-flights-search-result/fsr-qsf-layout/section/div/flights-list/'
    xpath_dict = {
        'to_departure_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/div/div/span[1]',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/div/div/span[1]'
        ],
        'to_arrival_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/div/div/span[2]',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/div/div/span[2]'
        ],
        'to_direct_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/header/div/div[2]/span[1]/span',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/header/div/div[2]/span[1]/span'
        ],
        'from_departure_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/div/div/span[1]',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/div/div/span[1]'
        ],
        'from_arrival_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/div/div/span[2]',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/div/div/span[2]'
        ],
        'from_direct_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/header/div/div[2]/span[1]/span',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/header/div/div[2]/span[1]/span'
        ],
        'price': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/flight-offer-price-info/div/div[1]/div[1]/div[1]/div/esky-offer-price-info/div/esky-price/span[1]',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/flight-offer-price-info/div/div[1]/div[1]/div[1]/div/esky-offer-price-info/div/esky-price/span[1]'
        ],

        'to_carrier_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/header/div/airline-logo[2]/div/img-fallback',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[1]/div/header/div/airline-logo[2]/div/img-fallback'
        ],

        'from_carrier_xpath': [
            'div[2]/div[2]/div/div/ul/li[1]/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/header/div/airline-logo[2]/div/img-fallback',
            'div/div[2]/div/div/ul/li/esky-flight-offer-group/div[1]/div[2]/div/leg-group[2]/div/header/div/airline-logo[2]/div/img-fallback'
        ]
    }