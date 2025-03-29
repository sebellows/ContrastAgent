supported_language_codes = [
  'de',
  'en',
  'es',
  'fr',
  'it',
]

supported_country_codes = [
  'AT', # Austria
  'AU', # Australia
  'BE', # Belgium
  'CA', # Canada
  'CH', # Switzerland
  'DA', # Denmark
  'DE', # Germany
  'ES', # Spain
  'FI', # Finland
  'FR', # France
  'IE', # Ireland
  'JA', # Japan
  'NL', # Netherlands
  'NO', # Norway
  'NZ', # New Zealand
  'PL', # Poland
  'UK', # United Kingdom
  'US', # United States
]

supported_languages = [
  {
    'language_code': 'en',
    'language': 'English',
    'language_endonym': 'English',
  },
  {
    'language_code': 'de',
    'language': 'German',
    'language_endonym': 'Deutsch',
  },
  {
    'language_code': 'es',
    'language': 'Spanish',
    'language_endonym': 'Espanol',
  },
  {
    'language_code': 'fr',
    'language': 'French',
    'language_endonym': 'Français',
  },
  {
    'language_code': 'it',
    'language': 'Italian',
    'language_endonym': 'Italiano',
  },
]

supported_locales = {
  'en': {
    'AU': {
      'exonym': 'Australia',
      'language_endonym': 'Australia',
      'country_code': 'AU',
      'currency_code': 'AUD',
      'currency_decimal_spaces': 2,
      'currency_symbol': '$',
    },
    'BE': {
      'exonym': 'Belgium',
      'language_endonym': 'Belgique',
      'country_code': 'BE',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
    'CA': {
      'exonym': 'Canada',
      'language_endonym': 'Canada',
      'country_code': 'CA',
      'currency_code': 'CAD',
      'currency_decimal_spaces': 2,
      'currency_symbol': '$',
    },
    'DA': {
      'exonym': 'Denmark',
      'language_endonym': 'Danmark',
      'country_code': 'DA',
      'currency_code': 'DKK',
      'currency_decimal_spaces': 2,
      'currency_symbol': 'kr',
    },
    'FI': {
      'exonym': 'Finland',
      'language_endonym': 'Suomi',
      'country_code': 'FI',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
    'IE': {
      'exonym': 'Ireland',
      'language_endonym': 'Ireland',
      'country_code': 'IE',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
    'JA': {
      'exonym': 'Japan',
      'language_endonym': '日本',
      'country_code': 'JA',
      'currency_code': 'JPY',
      'currency_decimal_spaces': 0,
      'currency_symbol': '¥',
    },
    'NL': {
      'exonym': 'Netherlands',
      'language_endonym': 'Nederland',
      'country_code': 'NL',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
    'NO': {
      'exonym': 'Norway',
      'language_endonym': 'Norge',
      'country_code': 'NO',
      'currency_code': 'NOK',
      'currency_decimal_spaces': 2,
      'currency_symbol': 'kr',
    },
    'NZ': {
      'exonym': 'New Zealand',
      'language_endonym': 'New Zealand',
      'country_code': 'NZ',
      'currency_code': 'NZD',
      'currency_decimal_spaces': 2,
      'currency_symbol': '$',
    },
    'PL': {
      'exonym': 'Poland',
      'language_endonym': 'Polska',
      'country_code': 'PL',
      'currency_code': 'PLN', # Złoty
      'currency_decimal_spaces': 2,
      'currency_symbol': 'zł',
    },
    'SE': {
      'exonym': 'Sweden', # NOTE: language code is 'sv'
      'language_endonym': 'Sverige',
      'country_code': 'SE',
      'currency_code': 'SEK', # The "krona"
      'currency_decimal_spaces': 2,
      'currency_symbol': 'kr',
    },
    'UK': {
      'exonym': 'United Kingdom',
      'language_endonym': 'United Kingdom',
      'country_code': 'GB',
      'currency_code': 'GBP',
      'currency_decimal_spaces': 2,
      'currency_symbol': '£',
    },
    'US': {
      'exonym': 'United States of America',
      'language_endonym': 'United States of America',
      'country_code': 'US',
      'currency_code': 'USD',
      'currency_decimal_spaces': 2,
      'currency_symbol': '$',
    },
  }
  'de': {
    'AT': {
      'exonym': 'Austria',
      'language_endonym': 'Österreich',
      'country_code': 'AT',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
    'CH': {
      'exonym': 'Switzerland',
      'language_endonym': 'Schweiz',
      'country_code': 'CH',
      'currency_code': 'CHF',
      'currency_decimal_spaces': 2,
      'currency_symbol': 'F',
    },
    'DE': {
      'exonym': 'Germany',
      'language_endonym': 'Deutschland',
      'country_code': 'DE',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
  },
  'es': {
    'ES': {
      'exonym': 'Spain',
      'language_endonym': 'España',
      'country_code': 'ES',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    }
  },
  'fr': {
    'BE': {
      'exonym': 'Belgium',
      'language_endonym': 'Belgique',
      'country_code': 'BE',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
    'CH': {
      'exonym': 'Switzerland',
      'language_endonym': 'Suisse',
      'country_code': 'CH',
      'currency_code': 'CHF',
      'currency_decimal_spaces': 2,
      'currency_symbol': 'F',
    },
    'FR': {
      'exonym': 'France',
      'language_endonym': 'France',
      'country_code': 'CH',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
  },
  'it': {
    'IT': {
      'exonym': 'Italy',
      'language_endonym': 'Italia',
      'country_code': 'IT',
      'currency_code': 'EUR',
      'currency_decimal_spaces': 2,
      'currency_symbol': '€',
    },
  },
}
