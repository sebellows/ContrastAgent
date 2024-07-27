import { Type } from './base'

export type RootElement = Document | ShadowRoot

interface HTMLWebViewElement extends HTMLElement {}

export interface HTMLTagElementMap {
  a: HTMLAnchorElement
  abbr: HTMLElement
  address: HTMLElement
  area: HTMLAreaElement
  article: HTMLElement
  aside: HTMLElement
  audio: HTMLAudioElement
  b: HTMLElement
  base: HTMLBaseElement
  bdi: HTMLElement
  bdo: HTMLElement
  big: HTMLElement
  blockquote: HTMLQuoteElement
  body: HTMLBodyElement
  br: HTMLBRElement
  button: HTMLButtonElement
  canvas: HTMLCanvasElement
  caption: HTMLElement
  cite: HTMLElement
  code: HTMLElement
  col: HTMLTableColElement
  colgroup: HTMLTableColElement
  data: HTMLDataElement
  datalist: HTMLDataListElement
  dd: HTMLElement
  del: HTMLModElement
  details: HTMLDetailsElement
  dfn: HTMLElement
  dialog: HTMLDialogElement
  div: HTMLDivElement
  dl: HTMLDListElement
  dt: HTMLElement
  em: HTMLElement
  embed: HTMLEmbedElement
  fieldset: HTMLFieldSetElement
  figcaption: HTMLElement
  figure: HTMLElement
  footer: HTMLElement
  form: HTMLFormElement
  h1: HTMLHeadingElement
  h2: HTMLHeadingElement
  h3: HTMLHeadingElement
  h4: HTMLHeadingElement
  h5: HTMLHeadingElement
  h6: HTMLHeadingElement
  head: HTMLHeadElement
  header: HTMLElement
  hgroup: HTMLElement
  hr: HTMLHRElement
  html: HTMLHtmlElement
  i: HTMLElement
  iframe: HTMLIFrameElement
  img: HTMLImageElement
  input: HTMLInputElement
  ins: HTMLModElement
  kbd: HTMLElement
  keygen: HTMLElement
  label: HTMLLabelElement
  legend: HTMLLegendElement
  li: HTMLLIElement
  link: HTMLLinkElement
  main: HTMLElement
  map: HTMLMapElement
  mark: HTMLElement
  menu: HTMLElement
  menuitem: HTMLElement
  meta: HTMLMetaElement
  meter: HTMLMeterElement
  nav: HTMLElement
  noscript: HTMLElement
  object: HTMLObjectElement
  ol: HTMLOListElement
  optgroup: HTMLOptGroupElement
  option: HTMLOptionElement
  output: HTMLOutputElement
  p: HTMLParagraphElement
  picture: HTMLElement
  pre: HTMLPreElement
  progress: HTMLProgressElement
  q: HTMLQuoteElement
  rp: HTMLElement
  rt: HTMLElement
  ruby: HTMLElement
  s: HTMLElement
  samp: HTMLElement
  slot: HTMLSlotElement
  script: HTMLScriptElement
  section: HTMLElement
  select: HTMLSelectElement
  small: HTMLElement
  source: HTMLSourceElement
  span: HTMLSpanElement
  strong: HTMLElement
  style: HTMLStyleElement
  sub: HTMLElement
  summary: HTMLElement
  sup: HTMLElement
  table: HTMLTableElement
  template: HTMLTemplateElement
  tbody: HTMLTableSectionElement
  td: HTMLTableCellElement
  textarea: HTMLTextAreaElement
  tfoot: HTMLTableSectionElement
  th: HTMLTableCellElement
  thead: HTMLTableSectionElement
  time: HTMLTimeElement
  title: HTMLTitleElement
  tr: HTMLTableRowElement
  track: HTMLTrackElement
  u: HTMLElement
  ul: HTMLUListElement
  video: HTMLVideoElement
  wbr: HTMLElement
  webview: HTMLWebViewElement
}

export interface SVGTagElementMap {
  animate: SVGAnimateElement
  animateMotion: SVGElement
  animateTransform: SVGAnimateTransformElement
  circle: SVGCircleElement
  clipPath: SVGClipPathElement
  defs: SVGDefsElement
  desc: SVGDescElement
  ellipse: SVGEllipseElement
  feBlend: SVGFEBlendElement
  feColorMatrix: SVGFEColorMatrixElement
  feComponentTransfer: SVGFEComponentTransferElement
  feComposite: SVGFECompositeElement
  feConvolveMatrix: SVGFEConvolveMatrixElement
  feDiffuseLighting: SVGFEDiffuseLightingElement
  feDisplacementMap: SVGFEDisplacementMapElement
  feDistantLight: SVGFEDistantLightElement
  feDropShadow: SVGFEDropShadowElement
  feFlood: SVGFEFloodElement
  feFuncA: SVGFEFuncAElement
  feFuncB: SVGFEFuncBElement
  feFuncG: SVGFEFuncGElement
  feFuncR: SVGFEFuncRElement
  feGaussianBlur: SVGFEGaussianBlurElement
  feImage: SVGFEImageElement
  feMerge: SVGFEMergeElement
  feMergeNode: SVGFEMergeNodeElement
  feMorphology: SVGFEMorphologyElement
  feOffset: SVGFEOffsetElement
  fePointLight: SVGFEPointLightElement
  feSpecularLighting: SVGFESpecularLightingElement
  feSpotLight: SVGFESpotLightElement
  feTile: SVGFETileElement
  feTurbulence: SVGFETurbulenceElement
  filter: SVGFilterElement
  foreignObject: SVGForeignObjectElement
  g: SVGGElement
  image: SVGImageElement
  line: SVGLineElement
  linearGradient: SVGLinearGradientElement
  marker: SVGMarkerElement
  mask: SVGMaskElement
  metadata: SVGMetadataElement
  path: SVGPathElement
  pattern: SVGPatternElement
  polygon: SVGPolygonElement
  polyline: SVGPolylineElement
  radialGradient: SVGRadialGradientElement
  rect: SVGRectElement
  stop: SVGStopElement
  svg: SVGSVGElement
  switch: SVGSwitchElement
  symbol: SVGSymbolElement
  text: SVGTextElement
  textPath: SVGTextPathElement
  tspan: SVGTSpanElement
  use: SVGUseElement
  view: SVGViewElement
}

export type CSSStyleBlock = Record<string, string | number>
export type CSSProperties = Record<string, CSSStyleBlock>

export type HTMLTag = keyof HTMLTagElementMap
export type SVGTag = keyof SVGTagElementMap
export type Tag = HTMLTag | SVGTag
export type GetTag<E extends Element> = Lowercase<E['tagName']> extends Tag ? E['tagName'] : never
export type HTMLElementType<T extends HTMLTag> = HTMLTagElementMap[T]
export type SVGElementType<T extends SVGTag> = SVGTagElementMap[T]
export type ElementType<T extends Tag | string | Function | DocumentFragment> = T extends HTMLTag
  ? HTMLElementType<T>
  : T extends SVGTag
    ? SVGElementType<T>
    : T extends DocumentFragment
      ? DocumentFragment
      : T extends string
        ? HTMLElement
        : T extends Function
          ? Type<T>
          : never
