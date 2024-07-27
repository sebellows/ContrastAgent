import { StringKeyOf } from 'type-fest'
import { default as twColors } from 'tailwindcss/colors'

export const colors = {
  ...twColors,
  transparent: twColors.transparent,
  current: twColors.current,
  neutral: twColors.slate,
  negative: twColors.rose,
  positive: twColors.lime,
  warning: twColors.amber,
}

type TailwindColorName = keyof typeof twColors
export type TailwindColorMap = {
  primary: TailwindColorName
  secondary: TailwindColorName
  accent: TailwindColorName
  [key: string]: string | TailwindColorName
}

type ThemeColorConfig = Record<
  keyof TailwindColorMap,
  (typeof twColors)[TailwindColorName]
>

const isTailwindThemeColor = (color: unknown): color is TailwindColorName => {
  return typeof color === 'string' && color in twColors
}

export const generateThemeColorsConfig = (themeColors: TailwindColorMap) => {
  const { primary, secondary, accent, ...others } = themeColors

  const themeColorsConfig = {
    primary: twColors[primary],
    secondary: twColors[secondary],
    accent: twColors[accent],
  } as ThemeColorConfig

  for (const key in others) {
    if (typeof others[key] === 'string') {
      const customKey = key as StringKeyOf<ThemeColorConfig>

      Object.assign(themeColorsConfig, { [customKey]: others[key] })
    } else if (isTailwindThemeColor(key)) {
      const colorName = others[key] as TailwindColorName

      themeColorsConfig[key] = twColors[colorName]
    }
  }

  return themeColorsConfig
}
