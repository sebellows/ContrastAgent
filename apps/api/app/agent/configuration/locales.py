class LocaleDetails:
    name: str
    # language_code: str
    supported_language_codes: list[str]
    country_code: str
    currency_code: str
    currency_decimal_spaces: int
    currency_symbol: str
    symbol_position: str
    decimal_separator: str

locales: dict[str, LocaleDetails] = {
    'AT': {
        'name': 'Austria',
        # 'language_code': 'de',
        'country_code': 'AT',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'AU': {
        'name': 'Australia',
        # 'language_code': 'en',
        'country_code': 'AU',
        'currency_code': 'AUD',
        'currency_decimal_spaces': 2,
        'currency_symbol': '$',
        'symbol_position': 'start',
        'decimal_separator': '.',
    },
    'BE': {
        'name': 'Belgium',
        # 'language_code': 'fr',
        'country_code': 'BE',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'CA': {
        'name': 'Canada',
        # 'language_code': 'en',
        'country_code': 'CA',
        'currency_code': 'CAD',
        'currency_decimal_spaces': 2,
        'currency_symbol': '$',
        'symbol_position': 'start',
        'decimal_separator': '.',
    },
    'CH': {
        'name': 'Switzerland',
        # 'language_code': 'fr',
        'country_code': 'CH',
        'currency_code': 'CHF',
        'currency_decimal_spaces': 2,
        'currency_symbol': 'F',
        'symbol_position': 'end',
        'decimal_separator': '.',
    },
    'DA': {
        'name': 'Denmark',
        # 'language_code': 'da',
        'country_code': 'DA',
        'currency_code': 'DKK',
        'currency_decimal_spaces': 2,
        'currency_symbol': 'kr',
        'symbol_position': 'end',
        'decimal_separator': ',',
    },
    'DE': {
        'name': 'Germany',
        # 'language_code': 'de',
        'country_code': 'DE',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'ES': {
        'name': 'Spain',
        # 'language_code': 'es',
        'country_code': 'ES',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'FI': {
        'name': 'Finland',
        # 'language_code': 'fi',
        'country_code': 'FI',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'FR': {
        'name': 'France',
        # 'language_code': 'fr',
        'country_code': 'FR',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'GB': {
        'name': 'Great Britain',
        # 'language_code': 'en',
        'country_code': 'GB',
        'currency_code': 'GBP',
        'currency_decimal_spaces': 2,
        'currency_symbol': '£',
        'symbol_position': 'start',
        'decimal_separator': '.',
    },
    'IE': {
        'name': 'Ireland',
        # 'language_code': 'en',
        'country_code': 'IE',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'IT': {
        'name': 'Italy',
        # 'language_code': 'it',
        'country_code': 'IT',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'JP': {
        'name': 'Japan',
        # 'language_code': 'ja',
        'country_code': 'JP',
        'currency_code': 'JPY',
        'currency_decimal_spaces': 0,
        'currency_symbol': '¥',
        'symbol_position': 'start',
        'decimal_separator': '',
    },
    'NL': {
        'name': 'Netherlands',
        # 'language_code': 'nl',
        'country_code': 'NL',
        'currency_code': 'EUR',
        'currency_decimal_spaces': 2,
        'currency_symbol': '€',
        'symbol_position': 'start',
        'decimal_separator': ',',
    },
    'NO': {
        'name': 'Norway',
        # 'language_code': 'no',
        'country_code': 'NO',
        'currency_code': 'NOK',
        'currency_decimal_spaces': 2,
        'currency_symbol': 'kr',
        'symbol_position': 'end',
        'decimal_separator': ',',
    },
    'NZ': {
        'name': 'New Zealand',
        # 'language_code': 'en',
        'country_code': 'NZ',
        'currency_code': 'NZD',
        'currency_decimal_spaces': 2,
        'currency_symbol': '$',
        'symbol_position': 'start',
        'decimal_separator': '.',
    },
    'PL': {
        'name': 'Poland',
        # 'language_code': 'pl',
        'country_code': 'PL',
        'currency_code': 'PLN', # Złoty
        'currency_decimal_spaces': 2,
        'currency_symbol': 'zł',
        'symbol_position': 'end',
        'decimal_separator': ',',
    },
    'SE': {
        'name': 'Sweden',
        # 'language_code': 'sv',
        'country_code': 'SE',
        'currency_code': 'SEK', # The "krona"
        'currency_decimal_spaces': 2,
        'currency_symbol': 'kr',
        'symbol_position': 'end',
        'decimal_separator': ',',
    },
    'US': {
        'name': 'United States of America',
        # 'language_code': 'en',
        'country_code': 'US',
        'currency_code': 'USD',
        'currency_decimal_spaces': 2,
        'currency_symbol': '$',
        'symbol_position': 'start',
        'decimal_separator': '.',
    },
}

# locales = {
#     'language_codes': [
#       'de',
#       'en',
#       'es',
#       'fr',
#       'it',
#     ],
    
#     'country_codes': [
#       'AT', # Austria
#       'AU', # Australia
#       'BE', # Belgium
#       'CA', # Canada
#       'CH', # Switzerland
#       'DA', # Denmark
#       'DE', # Germany
#       'ES', # Spain
#       'FI', # Finland
#       'FR', # France
#       'GB', # United Kingdom
#       'IE', # Ireland
#       'IT', # Italy
#       'JP', # Japan
#       'NL', # Netherlands
#       'NO', # Norway
#       'NZ', # New Zealand
#       'PL', # Poland
#       'US', # United States
#     ],
    
#     'countries': countries,
# }

# class LocaleConfig:
#     __language_codes: [
#       'de',
#       'en',
#       'es',
#       'fr',
#       'it',
#     ]
    
#     __country_codes: [
#       'AT', # Austria
#       'AU', # Australia
#       'BE', # Belgium
#       'CA', # Canada
#       'CH', # Switzerland
#       'DA', # Denmark
#       'DE', # Germany
#       'ES', # Spain
#       'FI', # Finland
#       'FR', # France
#       'GB', # United Kingdom
#       'IE', # Ireland
#       'IT', # Italy
#       'JP', # Japan
#       'NL', # Netherlands
#       'NO', # Norway
#       'NZ', # New Zealand
#       'PL', # Poland
#       'US', # United States
#     ]
    
#     __locales: {
#         'AT': {
#             'name': 'Austria',
#             'language_code': 'de',
#             'supported_language_codes': [],
#             'country_code': 'AT',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'AU': {
#             'name': 'Australia',
#             'language_code': 'en',
#             'supported_language_codes': [],
#             'country_code': 'AU',
#             'currency_code': 'AUD',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '$',
#             'symbol_position': 'start',
#             'decimal_separator': '.',
#         },
#         'BE': {
#             'name': 'Belgium',
#             'language_code': 'fr',
#             'supported_language_codes': ['en'],
#             'country_code': 'BE',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'CA': {
#             'name': 'Canada',
#             'language_code': 'en',
#             'supported_language_codes': ['fr'],
#             'country_code': 'CA',
#             'currency_code': 'CAD',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '$',
#             'symbol_position': 'start',
#             'decimal_separator': '.',
#         },
#         'CH': {
#             'name': 'Switzerland',
#             'language_code': 'fr',
#             'supported_language_codes': ['de'],
#             'country_code': 'CH',
#             'currency_code': 'CHF',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': 'F',
#             'symbol_position': 'end',
#             'decimal_separator': '.',
#         },
#         'DA': {
#             'name': 'Denmark',
#             'language_code': 'da',
#             'supported_language_codes': ['en'],
#             'country_code': 'DA',
#             'currency_code': 'DKK',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': 'kr',
#             'symbol_position': 'end',
#             'decimal_separator': ',',
#         },
#         'DE': {
#             'name': 'Germany',
#             'language_code': 'de',
#             'supported_language_codes': [],
#             'country_code': 'DE',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'ES': {
#             'name': 'Spain',
#             'language_code': 'es',
#             'supported_language_codes': [],
#             'country_code': 'ES',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         }
#         'FI': {
#             'name': 'Finland',
#             'language_code': 'fi',
#             'supported_language_codes': ['en'],
#             'country_code': 'FI',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'FR': {
#             'name': 'France',
#             'language_code': 'fr',
#             'supported_language_codes': [],
#             'country_code': 'FR',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'GB': {
#             'name': 'Great Britain',
#             'language_code': 'en',
#             'supported_language_codes': [],
#             'country_code': 'GB',
#             'currency_code': 'GBP',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '£',
#             'symbol_position': 'start',
#             'decimal_separator': '.',
#         },
#         'IE': {
#             'name': 'Ireland',
#             'language_code': 'en',
#             'supported_language_codes': [''],
#             'country_code': 'IE',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'IT': {
#             'name': 'Italy',
#             'language_code': 'it',
#             'supported_language_codes': [''],
#             'country_code': 'IT',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'JP': {
#             'name': 'Japan',
#             'language_code': 'ja',
#             'supported_language_codes': ['en'],
#             'country_code': 'JP',
#             'currency_code': 'JPY',
#             'currency_decimal_spaces': 0,
#             'currency_symbol': '¥',
#             'symbol_position': 'start',
#             'decimal_separator': '',
#         },
#         'NL': {
#             'name': 'Netherlands',
#             'language_code': 'nl',
#             'supported_language_codes': ['en'],
#             'country_code': 'NL',
#             'currency_code': 'EUR',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '€',
#             'symbol_position': 'start',
#             'decimal_separator': ',',
#         },
#         'NO': {
#             'name': 'Norway',
#             'language_code': 'no',
#             'supported_language_codes': ['en'],
#             'country_code': 'NO',
#             'currency_code': 'NOK',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': 'kr',
#             'symbol_position': 'end',
#             'decimal_separator': ',',
#         },
#         'NZ': {
#             'name': 'New Zealand',
#             'language_code': 'en',
#             'supported_language_codes': [''],
#             'country_code': 'NZ',
#             'currency_code': 'NZD',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '$',
#             'symbol_position': 'start',
#             'decimal_separator': '.',
#         },
#         'PL': {
#             'name': 'Poland',
#             'language_code': 'pl',
#             'supported_language_codes': ['en'],
#             'country_code': 'PL',
#             'currency_code': 'PLN', # Złoty
#             'currency_decimal_spaces': 2,
#             'currency_symbol': 'zł',
#             'symbol_position': 'end',
#             'decimal_separator': ',',
#         },
#         'SE': {
#             'name': 'Sweden',
#             'language_code': 'sv',
#             'supported_language_codes': ['en'],
#             'country_code': 'SE',
#             'currency_code': 'SEK', # The "krona"
#             'currency_decimal_spaces': 2,
#             'currency_symbol': 'kr',
#             'symbol_position': 'end',
#             'decimal_separator': ',',
#         },
#         'US': {
#             'name': 'United States of America',
#             'language_code': 'en',
#             'supported_language_codes': [''],
#             'country_code': 'US',
#             'currency_code': 'USD',
#             'currency_decimal_spaces': 2,
#             'currency_symbol': '$',
#             'symbol_position': 'start',
#             'decimal_separator': '.',
#         },
#     }

#     @property
#     def country_codes(self) -> list[str]:
#         return self.__country_codes

#     @property
#     def language_codes(self) -> list[str]:
#         return self.__language_codes

#     @property
#     def locales(self) -> dict[str, LocaleItem]:
#         return self.__locales
