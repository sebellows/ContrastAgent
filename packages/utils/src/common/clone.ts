import {
  isDate,
  isError,
  isMap,
  isPlainObject,
  isProxy,
  isRegExp,
  isSet,
  isSymbol,
  type,
} from '../assert'
import { safeStringify } from './safeStringify'

/*************************
 * Clone/Clone-Deep
 *************************/

const valueOf = Symbol.prototype.valueOf

export function clone<TObj>(obj: TObj): TObj {
  if (typeof globalThis.structuredClone === 'function' && !isProxy(obj)) {
    return structuredClone(obj)
  }

  return JSON.parse(safeStringify(obj))
}

/**
 * Make a shallow clone of an object, array or primitive.
 *
 * Adapted from <https://github.com/jonschlinkert/shallow-clone>
 *
 * @param {*} value  The value to be cloned.
 *
 * @example
 * ```
 * const arr = [{ a: 0 }, { b: 1 }];
 * const foo = shallowClone(arr);
 * // foo =>  [{ 'a': 0 }, { 'b': 1 }]
 * ```
 */
export function shallowClone<T = any>(value: T): T {
  if (isDate(value)) {
    return new Date(+value) as T
  }
  if (isError(value)) {
    return Object.create(value)
  }
  if (isMap(value)) {
    const map = new Map()
    const entries = Array.from((value as Map<any, any>).entries())

    for (const [key, item] of entries) {
      map.set(key, shallowClone(item))
    }
    return map as T
  }
  if (isPlainObject(value)) {
    return Object.assign({}, value)
  }
  if (isRegExp(value)) {
    return cloneRegExp(value)
  }
  if (isSet(value)) {
    const entries = Array.from((value as Set<any>).entries())
    return new Set(entries) as T
  }
  if (isSymbol(value)) {
    return cloneSymbol(value as symbol) as T
  }
  if (type(value) == 'arraybuffer') {
    return cloneArrayBuffer(value) as T
  }
  if (Array.isArray(value)) {
    return (value as any[]).slice() as T
  }

  return value
}

function cloneRegExp(value: any) {
  const re = new value.constructor(value.source, /\w+$/.exec(value))
  re.lastIndex = value.lastIndex
  return re
}

function cloneArrayBuffer<T>(value: T): ArrayBuffer {
  if (!(value instanceof ArrayBuffer)) {
    throw new TypeError(
      "'cloneArrayBuffer' must be passed an instance of an ArrayBuffer.",
    )
  }

  const res = new ArrayBuffer(value.byteLength)
  new Uint8Array(res).set(new Uint8Array(value))
  return res
}

function cloneSymbol(value: symbol) {
  return valueOf ? Object(valueOf.call(value)) : {}
}

export function cloneDeep(value: unknown, instance?: unknown) {
  if (isPlainObject(value)) {
    return cloneObjectDeep(value, instance)
  }
  if (Array.isArray(value)) {
    return cloneArrayDeep(value, instance)
  }

  return shallowClone(value)
}

function cloneObjectDeep<
  V extends Record<any, any>,
  // eslint-disable-next-line @typescript-eslint/ban-types
  I extends Function | Record<keyof V, any> | unknown = V,
>(value: V, instance: I = {} as Record<keyof V, any>) {
  if (typeof instance === 'function') {
    return instance(value)
  }
  if (instance || isPlainObject(value)) {
    const res = new (value as any).constructor()

    for (const key in value) {
      res[key] = cloneDeep(value[key], instance)
    }

    return res
  }
  return value
}

function cloneArrayDeep<V extends unknown[] = any>(
  value: V,
  instance: unknown = [],
) {
  const res = new Array(value.length)

  for (let i = 0; i < value.length; i++) {
    res[i] = cloneDeep(value[i], instance)
  }

  return res
}
