import { ElementType, GetTag, RootElement, Tag } from '../types/dom'
import { isBoolean, isNumber, isString } from '../assert'
import { isDocumentFragment, isShadowRoot } from './dom-assert'

/**
 * Get an attribute value from a custom web component.
 */
// function getAttributeItem<E extends HTMLElement>(
//   context: E,
//   key: string,
//   defaultValue = '',
// ) {
//   return context.attributes.getNamedItem(key)?.textContent ?? defaultValue
// }

type DomElement<T extends Tag | string> = T extends Tag
  ? ElementType<Tag>
  : HTMLElement

function getChildDom(selector: number | string, children: DomService<Tag>[]) {
  if (isNumber(selector)) {
    return children[selector]
  }

  return children.find((child) => (child.$el as HTMLElement).matches(selector))
}

class DomService<T extends Tag = 'div'> {
  #el: ElementType<T>

  static create<T extends Tag | string>(
    tag: T,
    root?: RootElement | ElementType<Tag>,
    options?: ElementCreationOptions,
  ) {
    const el = document.createElement(tag, options)
    return new DomService(el, root)
  }

  static createNS<T extends Tag | string>(
    tag: T,
    root?: RootElement | ElementType<Tag>,
    options?: ElementCreationOptions,
  ) {
    let ns = ''
    if (tag === 'svg') {
      ns = 'http://www.w3.org/2000/svg'
    } else if (tag === 'math') {
      ns = 'http://www.w3.org/1998/Math/MathML'
    }
    const el = document.createElementNS(ns, tag, options) as ElementType<T>
    return new DomService(el, root)
  }

  static html(strings: string[], ...values: string[]) {
    const h = String.raw({ raw: strings }, ...values)
    const frag = document.createRange().createContextualFragment(h)
    return new DomService(frag)
  }

  get $el() {
    return this.#el
  }

  readonly $root: RootElement | ElementType<Tag>

  private listeners = new Map<string, EventListener>()

  constructor(
    el: T | string | ElementType<T> | DocumentFragment,
    root: RootElement | ElementType<Tag> = document,
  ) {
    this.#el = isString(el)
      ? (root.querySelector(el) as ElementType<T>)
      : ((isDocumentFragment(el) ? el : el) as ElementType<T>)
    this.$root = root
  }

  private self = this

  get $attrs() {
    const _self = { $: self }
    return {
      has: (name: string) => {
        return this.#el?.hasAttribute?.(name) ?? false
      },
      get: (name: string) => {
        return this.#el?.getAttribute?.(name)
      },
      set: (name: string, value: number | string | boolean) => {
        value = isBoolean(value) && !!value ? '' : value.toString()
        this.#el?.setAttribute?.(name, value)
        return this.$attrs
      },
      remove: (name: string) => {
        this.#el?.removeAttribute?.(name)
        return this.$attrs
      },
      $: _self.$,
    }
  }

  get $classes() {
    const _self = { $: self }

    return {
      has: (name: string) => {
        return this.#el?.classList?.contains?.(name)
      },
      add: (...tokens: string[]) => {
        this.#el?.classList?.add?.(...tokens)
        return this.$classes
      },
      remove: (...tokens: string[]) => {
        this.#el?.classList?.remove?.(...tokens)
        return this.$attrs
      },
      toggle: (token: string, force?: boolean) => {
        this.#el?.classList?.toggle?.(token, force)
        return this.$classes
      },
      $: _self.$,
    }
  }

  get $styles() {
    const _self = { $: self }

    return {
      has: (name: string) => this.#el.attributeStyleMap.has(name),
      get: (name: string) => this.#el.attributeStyleMap.get(name),
      set: (name: string, value: string) => {
        this.#el?.attributeStyleMap?.set?.(name, value)
        return this.$styles
      },
      remove: (name: string) => {
        this.#el.attributeStyleMap.delete(name)
        return this.$styles
      },
      clear: () => {
        this.#el.attributeStyleMap.clear()
        return this.$styles
      },
      $: _self.$,
    }
  }

  get $children() {
    const __children = Array.from(this.#el.children).map(
      (child) =>
        new DomService(child as ElementType<GetTag<typeof child>>, this.#el),
    )

    return {
      get: (selector: number | string) => {
        return getChildDom(selector, __children)
      },
      all: <S extends Tag | string = Tag>(selector?: S) => {
        if (!selector) return __children

        const items = __children.filter((child) =>
          (child.$el as HTMLElement).matches(selector),
        )
        return items
      },
      count: () => __children.length,
      forEach: (
        callback: <C extends Tag>(
          child: DomService<C>,
          index?: number,
          arr?: DomService<C>[],
        ) => void,
      ) => {
        __children.forEach(callback)
      },
      map: (
        callback: <C extends Tag>(
          child: DomService<C>,
          index?: number,
          arr?: DomService<C>[],
        ) => void,
      ) => {
        return __children.map(callback)
      },
      only: () => {
        if (__children.length !== 1)
          throw new Error('Expected only one child element')
        return __children[0]
      },
      toRaw: () => __children.map((child) => child.$el),
    }
  }

  on(event: string, listener: EventListener) {
    this.#el.addEventListener(event, listener)
    this.listeners.set(event, listener)
    return this
  }

  get<C extends Tag>(child: string) {
    return new DomService<C>(child)
  }

  getAll<C extends Tag>(child: string) {
    const items = (
      Array.from(this.#el.querySelectorAll(child)) as ElementType<C>[]
    ).map((c) => new DomService(c, this.#el))
    return items
  }

  toRaw<C extends Tag>(...items: (ElementType<C> | DomService<C>)[]) {
    return items.map((item) => {
      if (item instanceof DomService) {
        return item.$el
      }
      return item
    })
  }

  attach(to?: RootElement | ElementType<Tag>, position?: InsertPosition) {
    if (!this.#el) return

    if (!to) to = this.$root

    if (position && !isShadowRoot(to)) {
      ;(to as ElementType<Tag>).insertAdjacentElement(position, this.#el)
      return
    }

    to.appendChild(this.#el)
  }

  contains(child: Element) {
    return this.$el.contains(child)
  }

  append<E extends Tag>(
    position: InsertPosition,
    ...children: ElementType<E>[]
  ): void
  append<E extends Tag>(...children: ElementType<E>[]): void
  append(...args: any[]) {
    const position = isString(args[0]) ? (args[0] as InsertPosition) : null
    const children = isString(args[0]) ? args.slice(1) : args

    if (position) {
      children.forEach((child) =>
        this.$el.insertAdjacentElement(position, child),
      )
    } else {
      children.forEach((child) => this.$el.appendChild(child))
    }
  }

  insert(position: InsertPosition, element?: HTMLElement) {
    if (element) {
      element.insertAdjacentElement(position, this.$el)
    } else if (!isShadowRoot(this.$root)) {
      ;(this.$root as ElementType<Tag>).insertAdjacentElement(
        position,
        this.$el,
      )
    } else {
      this.$root.appendChild(this.$el)
    }
  }

  insertChild(position: InsertPosition, child: Element) {
    this.$el.insertAdjacentElement(position, child)
  }

  remove(child: Element) {
    this.$el.removeChild(child)
  }

  text(text: string) {
    if (this.$el) {
      this.$el.textContent = text
    }
  }
}

export type $Element<T extends Tag> = DomService<T>

export interface $DomService {
  <T extends Tag>(
    el: T | string | ElementType<T>,
    root?: RootElement | DomElement<Tag>,
  ): DomService<T>
  create: typeof DomService.create
  createNS: typeof DomService.createNS
}

const _$ = <T extends Tag>(
  el: T | string | ElementType<T>,
  root?: RootElement | DomElement<Tag>,
) => new DomService<T>(el, root)

Object.defineProperty(_$, 'create', {
  value: DomService.create,
  writable: false,
  enumerable: false,
  configurable: false,
})

Object.defineProperty(_$, 'createNS', {
  value: DomService.createNS,
  writable: false,
  enumerable: false,
  configurable: false,
})

export const $: $DomService = _$ as $DomService
