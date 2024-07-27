import { UnknownRecord } from 'type-fest'

/**
 * @internal
 *
 * Reference to the Object prototype's built-in `toString` method.
 * @example
 * ```
 * _protoToString === {}.toString // TRUE
 *
 * const fn = () => 'hello'
 * _protoToString === fn.toString // FALSE
 * _protoToString === fn.__proto__.toString // FALSE
 *
 * console.log(fn.toString())
 * => "() => 'hello'"
 *
 * console.log(fn.__proto__.toString())
 * => 'function () { [native code] }'
 *
 * console.log(fn.constructor.prototype.toString())
 * => 'function () { [native code] }'
 *
 * console.log(fn.constructor.toString())
 * => 'function Function() { [native code] }'
 * ```
 */
export const _protoToString = Object.prototype.toString

/**
 * NOTE: type-fest's SetRequired errors out here, so we're "rolling our own" for now.
 */
type SetRequired<BaseType, Keys extends keyof any> = Keys extends keyof BaseType
  ? BaseType & Omit<BaseType, Keys> & Required<Pick<BaseType, Keys>>
  : BaseType

export function hasOwn<O, K extends keyof O | string>(
  o: O,
  k: K,
): o is SetRequired<O, K>
export function hasOwn<O extends UnknownRecord, K extends PropertyKey>(
  o: O,
  k: K,
): o is O {
  if (Object.hasOwn) {
    return Object.hasOwn(o, k)
  }
  return Object.prototype.hasOwnProperty.call(o, k)
}

/**
 * Verify that an object has all of the specified properties.
 */
export const hasProperties = <O extends UnknownRecord, K extends keyof O>(
  obj: O,
  ...properties: K[]
) => {
  return (
    obj.toString() === '[object Object]' &&
    properties.every((prop) => hasOwn(obj, prop) && obj[prop] !== undefined)
  )
}
