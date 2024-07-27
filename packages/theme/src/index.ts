import { CustomThemeConfig } from 'tailwindcss/types/config'
import { screens } from './screens'
import { boxShadow } from './shadow'
import { fontFamily, fontSize } from './typography'
import { zIndex } from './zIndex'
import { colors, generateThemeColorsConfig, TailwindColorMap } from './colors'
import {
  getColorClass,
  palette,
  type PaletteColorPath,
  type ThemeSizeAlias,
  type ThemeSizeParamType,
  type TwSizeSuffix,
  getTwSizeClass,
  getTwDimensionalClasses,
  getRawTwSize,
  isTwHeightValue,
  isTwWidthValue,
  getTailwindSizeSuffixAsNumber,
  sizes,
} from './utils'
import { size } from './sizes'

const theme = {
  boxShadow,
  colors,
  screens,
  extend: {
    fontFamily,
    fontSize,
    size,
    zIndex,
  },
} as Partial<CustomThemeConfig>

const generateThemeConfig = (themeColors: TailwindColorMap) => {
  Object.assign(theme.extend, {
    colors: generateThemeColorsConfig(themeColors),
  })

  return theme
}

export {
  boxShadow,
  palette,
  sizes,
  theme,
  generateThemeConfig,
  getColorClass,
  type PaletteColorPath,
  type ThemeSizeAlias,
  type ThemeSizeParamType,
  type TwSizeSuffix,
  getTwSizeClass,
  getTwDimensionalClasses,
  getRawTwSize,
  isTwHeightValue,
  isTwWidthValue,
  getTailwindSizeSuffixAsNumber,
}
