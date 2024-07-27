import { CSSProperties } from '../types/dom'

export const css = (styles: CSSProperties): string => {
  return Object.entries(styles).reduce((acc, [selector, styleBlock]) => {
    acc += `${selector} {\n`
    acc += Object.entries(styleBlock).reduce((acc, [property, value]) => {
      acc += `  ${property}: ${value};\n`
      return acc
    }, '')
    acc += '}\n'
    return acc
  }, '')
}
