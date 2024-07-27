import { isPlainObject } from '../assert'
import { CSSProperties } from '../types/dom'
import { css } from './css'

export const styleTag = (styles: string | CSSProperties) => {
  let styleTag = ''
  if (typeof styles === 'string') {
    if (styles.endsWith('.css')) {
      styleTag = `<link rel="stylesheet" href="${styles}"></link>`
    } else {
      styleTag = `<style>${styles}</style>`
    }
  } else if (isPlainObject(styles)) {
    styleTag = `<style>${css(styles)}</style>`
  }

  return styleTag
}

const globalSheets = new Set<CSSStyleSheet>()

export function getGlobalStyleSheets() {
  const documentStyleSheets = Array.from(document.styleSheets)

  for (const stylesheet of documentStyleSheets) {
    const sheet = new CSSStyleSheet()
    const cssRules = Array.from(stylesheet.cssRules)
      .map((rule) => rule.cssText)
      .join(' ')
    sheet.replaceSync(cssRules)
    globalSheets.add(sheet)
  }

  return Array.from(globalSheets)
}

export function addGlobalStylesToShadowRoot(shadowRoot: ShadowRoot) {
  shadowRoot.adoptedStyleSheets.push(...getGlobalStyleSheets())
}
