import { globalView } from './global'

function nodeIs(
  node: unknown,
  type:
    | 'Element'
    | 'HTMLElement'
    | 'HTMLImageElement'
    | 'HTMLInputElement'
    | 'HTMLSlotElement'
    | 'HTMLStyleElement'
    | 'HTMLTemplateElement'
    | 'Node'
    | 'ShadowRoot'
    | 'SVGElement'
    | 'Text',
) {
  if (!globalView) return false

  return globalView[type] && node instanceof globalThis[type]
}

export function isNode(node: unknown): node is Node {
  return nodeIs(node, 'Node')
}

export function isElement(node: unknown): node is Element {
  return nodeIs(node, 'Element')
}

export function isHTMLElement(node: unknown): node is HTMLElement {
  return nodeIs(node, 'HTMLElement')
}

export function isSVGElement(node: unknown): node is SVGElement {
  return nodeIs(node, 'SVGElement')
}

export function isTemplateElement(node: unknown): node is HTMLTemplateElement {
  return nodeIs(node, 'HTMLTemplateElement')
}

export function isImageElement(node: unknown): node is HTMLImageElement {
  return nodeIs(node, 'HTMLImageElement')
}

export function isInputElement(node: unknown): node is HTMLInputElement {
  return nodeIs(node, 'HTMLInputElement')
}

export function isShadowRoot(node: unknown): node is ShadowRoot {
  return nodeIs(node, 'ShadowRoot')
}

export function isStyleElement(node: unknown): node is HTMLStyleElement {
  return nodeIs(node, 'HTMLStyleElement')
}

export function isSlotElement(node: unknown): node is HTMLSlotElement {
  return nodeIs(node, 'HTMLSlotElement')
}

export function isRootElement(
  node: unknown,
): node is HTMLBodyElement | HTMLHtmlElement {
  if (!isElement(node)) return false
  return node.tagName === 'BODY' || node.tagName === 'HTML'
}

export function isTextContent(node: unknown): node is Text {
  return nodeIs(node, 'Text')
}

export function isDocumentFragment(node: unknown): node is DocumentFragment {
  return !!(node && (node as Node).nodeType === Node.DOCUMENT_FRAGMENT_NODE)
}
