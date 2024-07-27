import { get, getKeys } from '@contrastagent/utils'
import { aliasedSizes } from '../sizes'

const themeAliasedSizes = Object.freeze(aliasedSizes)

export type ThemeSizeAlias = keyof typeof themeAliasedSizes

export const sizes = {
  w: {
    xs: 'w-xs', // 16
    sm: 'w-sm', // 24
    md: 'w-md', // 32
    lg: 'w-lg', // 40
    xl: 'w-xl', // 48
    '2xl': 'w-2xl', // 64
    px: 'w-px',
    0: 'w-0',
    '0.5': 'w-0.5',
    1: 'w-1',
    '1.5': 'w-1.5',
    2: 'w-2',
    '2.5': 'w-2.5',
    3: 'w-3',
    '3.5': 'w-3.5',
    4: 'w-4',
    5: 'w-5',
    6: 'w-6',
    7: 'w-7',
    8: 'w-8',
    9: 'w-9',
    10: 'w-10',
    11: 'w-11',
    12: 'w-12',
    14: 'w-14',
    16: 'w-16',
    20: 'w-20',
    24: 'w-24',
    28: 'w-28',
    32: 'w-32',
    36: 'w-36',
    40: 'w-40',
    44: 'w-44',
    48: 'w-48',
    52: 'w-52',
    56: 'w-56',
    60: 'w-60',
    64: 'w-64',
    72: 'w-72',
    80: 'w-80',
    96: 'w-96',
  },
  h: {
    xs: 'h-xs', // 16
    sm: 'h-sm', // 24
    md: 'h-md', // 32
    lg: 'h-lg', // 40
    xl: 'h-xl', // 48
    '2xl': 'h-2xl', // 64
    px: 'h-px',
    0: 'h-0',
    '0.5': 'h-0.5',
    1: 'h-1',
    '1.5': 'h-1.5',
    2: 'h-2',
    '2.5': 'h-2.5',
    3: 'h-3',
    '3.5': 'h-3.5',
    4: 'h-4',
    5: 'h-5',
    6: 'h-6',
    7: 'h-7',
    8: 'h-8',
    9: 'h-9',
    10: 'h-10',
    11: 'h-11',
    12: 'h-12',
    14: 'h-14',
    16: 'h-16',
    20: 'h-20',
    24: 'h-24',
    28: 'h-28',
    32: 'h-32',
    36: 'h-36',
    40: 'h-40',
    44: 'h-44',
    48: 'h-48',
    52: 'h-52',
    56: 'h-56',
    60: 'h-60',
    64: 'h-64',
    72: 'h-72',
    80: 'h-80',
    96: 'h-96',
  },
  size: {
    xs: 'size-xs', // 16
    sm: 'size-sm', // 24
    md: 'size-md', // 32
    lg: 'size-lg', // 40
    xl: 'size-xl', // 48
    '2xl': 'size-2xl', // 64
    px: 'size-px',
    0: 'size-0',
    '0.5': 'size-0.5',
    1: 'size-1',
    '1.5': 'size-1.5',
    2: 'size-2',
    '2.5': 'size-2.5',
    3: 'size-3',
    '3.5': 'size-3.5',
    4: 'size-4',
    5: 'size-5',
    6: 'size-6',
    7: 'size-7',
    8: 'size-8',
    9: 'size-9',
    10: 'size-10',
    11: 'size-11',
    12: 'size-12',
    14: 'size-14',
    16: 'size-16',
    20: 'size-20',
    24: 'size-24',
    28: 'size-28',
    32: 'size-32',
    36: 'size-36',
    40: 'size-40',
    44: 'size-44',
    48: 'size-48',
    52: 'size-52',
    56: 'size-56',
    60: 'size-60',
    64: 'size-64',
    72: 'size-72',
    80: 'size-80',
    96: 'size-96',
  },
}

type TwSizeClassMap = typeof sizes
type TwSizeClassMapKey = keyof TwSizeClassMap
export type TwSizeSuffix = keyof TwSizeClassMap[TwSizeClassMapKey]

type ThemeSizeDotPath = `${TwSizeClassMapKey}.${TwSizeSuffix}`
type ThemeSizePath = `${TwSizeClassMapKey}-${TwSizeSuffix}` | ThemeSizeDotPath

export type ThemeSizeParamType = number | string | ThemeSizeAlias | ThemeSizePath

const tailwindWidthValues = getKeys(sizes.w).map(String)
const tailwindHeightValues = getKeys(sizes.h).map(String)

export const getTwSizeClass = (path: string) => {
  return (get(sizes, path) ?? '') as string
}

export const getTwDimensionalClasses = (size: TwSizeSuffix) => {
  const classes = [] as string[]
  const widthClass = getTwSizeClass(`w.${size}`)

  if (widthClass.length) classes.push(widthClass)

  const heightClass = getTwSizeClass(`h.${size}`)

  if (heightClass.length) classes.push(heightClass)

  return classes
}

/**
 * The raw value that a Tailwind size class can be resolved by using
 * the class suffix (numeric value), which represents a multiple of 4
 * (with the assumption that the default font size is 16px).
 *
 * @example
 * ```css
 * .w-12 { width: 3rem; } // 12 * 4 = 48 (i.e., 3 * 16)
 * const rawSize = getRawTwSize('w-12') // 48
 * ```
 */
export const getRawTwSize = (sizeClassOrPath: ThemeSizeParamType) => {
  let twSize = 0

  if (typeof sizeClassOrPath === 'string') {
    if (sizeClassOrPath in aliasedSizes) {
      twSize = Number(aliasedSizes[sizeClassOrPath as ThemeSizeAlias])
    } else if (/\.|-/g.test(sizeClassOrPath)) {
      if (!!sizeClassOrPath.match(/\./g)?.length) {
        // It's possible that the path has two dots, so we need to
        // get the first one to extract the size suffix.
        const firstDot = sizeClassOrPath.indexOf('.')
        const suffixValue = sizeClassOrPath.slice(firstDot + 1)

        if (suffixValue in aliasedSizes) {
          twSize = Number(aliasedSizes[suffixValue as ThemeSizeAlias])
        } else {
          twSize = isNaN(+suffixValue) ? 1 : Number(suffixValue)
        }
      } else if (['size-', 'w-', 'h-'].some(p => sizeClassOrPath.startsWith(p))) {
        const firstSep = sizeClassOrPath.indexOf('-')
        const prefix = sizeClassOrPath.slice(0, firstSep)
        const suffix = sizeClassOrPath.slice(firstSep + 1)

        if (suffix in aliasedSizes) {
          twSize = Number(aliasedSizes[suffix as ThemeSizeAlias])
        } else {
          twSize = Number((get(sizes, `${prefix}.${suffix}`) as string).split('-')[1])
        }
      }
    }
  } else {
    twSize = isNaN(+sizeClassOrPath) ? 1 : Number(sizeClassOrPath)
  }

  return isNaN(twSize) ? -1 : twSize * 4
}

/**
 * Verify if a value is a valid Tailwind width class suffix value.
 *
 * @example
 * ```ts
 * isTwWidthValue(12) // true
 * isTwWidthValue(13) // false
 * isTwWidthValue('8') // true
 * ```
 */
export const isTwWidthValue = (value: number | string) => tailwindWidthValues.includes(`${value}`)

/**
 * Verify if a value is a valid Tailwind height class suffix value.
 *
 * @example
 * ```ts
 * isTwHeightValue(12) // true
 * isTwHeightValue(13) // false
 * isTwHeightValue('8') // true
 * ```
 */
export const isTwHeightValue = (value: number | string) => tailwindHeightValues.includes(`${value}`)

/**
 * Get the raw computed value of a Tailwind size class using the numeric
 * form of the class suffix as the key from a simple mapped object.
 *
 * @example
 * ```ts
 * twSizeSuffixRawValueMap[12] // 48
 * ```
 */
// export const twSizeSuffixRawValueMap = tailwindWidthValues.reduce(
//   (acc, value, i) => {
//     acc[value] = getRawTwSize(value)
//     return acc
//   },
//   {} as Record<string, number>,
// )

/**
 * Convert the suffix of a Tailwind size class and convert to number
 *
 * @example
 * ```ts
 * const size = 'w-12'
 * const rawSize = getTailwindSizeSuffixAsNumber(size) // 12
 * ```
 */
export const getTailwindSizeSuffixAsNumber = (
  size: ThemeSizeParamType | null | undefined,
): number => {
  if (size == null) return 0

  let numSize = 0

  if (typeof size === 'string') {
    if (size in themeAliasedSizes) {
      return themeAliasedSizes[size as ThemeSizeAlias]
    }

    // Can't return a numeric value for the size key "px"
    if (isNaN(+size)) return -1

    numSize = Number(size)
  }

  return tailwindWidthValues.includes(`${numSize}`) ? numSize : 0
}
