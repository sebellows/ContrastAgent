import { AnyRecord, AsyncFunction, Booleanish } from './types/base'
import { _protoToString, hasOwn } from './object/hasOwn'
import { UnknownArray, ValueOf } from 'type-fest'

/**
 * Get the type of a value in its named-form only
 * (i.e., `Object` instead of `[object Object]`)
 * @example
 * type(5) // "Number"
 * type(true) // "Boolean"
 * etc.
 */
export function type(value: unknown): string {
  if (value === null) return 'null'

  return _protoToString.call(value).slice(8, -1).toLowerCase()
}

export function is<T>(value: unknown, valueType?: T): value is T {
  return type(value) === valueType
}

function isNot<A extends any[], R>(fn: (...xs: A) => R) {
  return (...args: A) => !fn(...args)
}

/** Verify if a value is null or undefined. */
export function isNil(value: unknown): value is null | undefined
export function isNil(value: unknown): value is undefined
export function isNil(value: unknown): boolean {
  return value == null
}

export function isUndefined(value: unknown): value is undefined {
  return value === undefined
}

/**
 * Check if a value is a primitive type.
 *
 * @param {*} value - Any type of value
 * @returns {boolean}
 */
export function isPrimitive<T>(value: T): value is T {
  const valueType = type(value)
  return [
    'bigint',
    'boolean',
    'null',
    'number',
    'string',
    'symbol',
    'undefined',
  ].includes(valueType)
}

export function isObject<T extends object>(value: unknown): value is T {
  return typeof value === 'object'
}

/**
 * Verify that a value is a plain object created either by the Object constructor
 * or using `Object.create(null)`.
 */
export function isPlainObject<T, R = T extends AnyRecord ? T : AnyRecord>(
  value: unknown,
): value is R {
  return type(value) === 'object'
}

export function isDate(value: unknown): value is Date {
  return type(value) === 'date'
}

// eslint-disable-next-line @typescript-eslint/ban-types
export function isFunction(value: unknown): value is Function {
  return type(value) === 'function'
}

export function isAsyncFunction(value: unknown): value is AsyncFunction {
  return isFunction(value) && value.constructor.name === 'AsyncFunction'
}

export function isRegExp(value: unknown): value is RegExp {
  return type(value) === 'regexp'
}

export function isMap<K, V>(value: unknown): value is Map<K, V> {
  return type(value) === 'map'
}

export function isSet<E>(value: unknown): value is Set<E> {
  return type(value) === 'set'
}

export function isSymbol(value: unknown): value is symbol {
  return type(value) === 'symbol'
}

export function isError(value: unknown): value is Error {
  if (typeof value != 'object' || value == null) return false

  const valueType = type(value)
  return (
    valueType === 'error' ||
    valueType === 'domexception' ||
    (hasOwn(value, 'message') && hasOwn(value, 'name') && !isPlainObject(value))
  )
}

export function isProxy(value: unknown): value is InstanceType<typeof Proxy> {
  try {
    const clone = structuredClone(value)

    // If we can clone the value, then it's not a Proxy object.
    return Boolean(clone) === false
  } catch (error) {
    /**
     * A DOMException with the name of "DataCloneError" is thrown when the
     * value is a proxy object, because a Proxy object cannot be cloned.
     * @see https://developer.mozilla.org/en-US/docs/Web/API/DOMException#datacloneerror
     */
    if (error instanceof DOMException && error.name === 'DataCloneError') {
      return true
    }
    return false
  }
}

type TypedArrayMap = {
  int8array: Int8Array
  uint8array: Uint8Array
  uint8clampedarray: Uint8ClampedArray
  int16array: Int16Array
  uint16array: Uint16Array
  int32array: Int32Array
  uint32array: Uint32Array
  float32array: Float32Array
  float64array: Float64Array
  bigint64array: BigInt64Array
  biguint64array: BigUint64Array
}

const TYPED_ARRAY_LIST = [
  'int8array',
  'uint8array',
  'uint8clampedarray',
  'int16array',
  'uint16array',
  'int32array',
  'uint32array',
  'float32array',
  'float64array',
  'bigint64array',
  'biguint64array',
]

export function isTypedArray<
  V extends ValueOf<TypedArrayMap> | UnknownArray,
  T extends keyof TypedArrayMap = keyof TypedArrayMap,
>(value: V, valueType?: T): value is V {
  const _type = valueType ?? type(valueType)
  return TYPED_ARRAY_LIST.includes(_type) && is(value, _type)
}

export function isEmpty(value: unknown) {
  if (isNil(value)) return true

  if (Object.getOwnPropertyNames(value).includes('length')) {
    return (value as { length: number }).length === 0
  } else if (isPlainObject(value)) {
    return Object.keys(value).length === 0
  } else if (isMap(value) || isSet(value)) {
    return value.size === 0
  }

  return false
}

export function notEmpty(value: any) {
  return isNot(isEmpty)(value)
}

/** @deprecated - use `notNil` */
export const isDefined = <T>(
  value: T | null | undefined,
): value is Exclude<T, null | undefined> => {
  return value !== undefined && value !== null
}

export const notNil = <T>(
  value: T | null | undefined,
): value is Exclude<T, null | undefined> => {
  return value !== undefined && value !== null
}

export function isBooleanish(value: unknown): value is Booleanish {
  const valueType = type(value)
  return (
    valueType === 'boolean' ||
    (valueType === 'string' && (value === 'true' || value === 'false'))
  )
}

export function isBoolean(value: unknown): value is boolean {
  return type(value) === 'boolean'
}

export function isNumber(value: unknown): value is number {
  return type(value) === 'number' && Number.isInteger(value)
}

export function isString(value: unknown): value is string {
  return type(value) === 'string'
}

export function isEmptyString(value: string) {
  return isNil(value) || value.trim().length < 1
}

export function notEmptyString(value: string) {
  return isNot(isEmptyString)(value)
}

export function isNumeric(value: unknown): value is number {
  // parseFloat(value) handles most of the cases we're interested in (it treats null, empty string,
  // and other non-number values as NaN, where Number just uses 0) but it considers the string
  // '123hello' to be a valid number. Therefore we also check if Number(value) is NaN.
  const numValue = typeof value === 'string' ? parseFloat(value) : Number(value)
  if (isNaN(numValue)) {
    return false
  }

  return true
}

export function isNumericString(value: string) {
  return value !== '' && (value.match(/[^0-9.,-]/g) || []).length === 0
}

export function notNumericString(value: string) {
  return isNot(isNumericString)(value)
}

export function isPositiveIntegerString(value: string) {
  return notEmptyString(value) && (value.match(/[^0-9]/g) || []).length === 0
}

export function isPositiveNumericString(value: string) {
  return notEmptyString(value) && (value.match(/[^0-9.,]/g) || []).length === 0
}

export function isFalsyType(value: unknown): value is false | null | undefined {
  return value === false || value === null || value === undefined
}

export function isEnumLike<T extends object>(obj: T): obj is T {
  if (Object.isFrozen(obj)) {
    return Object.values(obj).every(
      (value) => isString(value) || isNumber(value),
    )
  }

  return Object.entries(obj).every(([key, value]) => {
    if (isNumber(key)) {
      // Enum values in TS can be numbers, but when compiled to JS, those numbers are set as
      // additional keys whose values are their corresponding key from the TS enum.
      return (
        isString(value) &&
        (obj as Record<typeof value, typeof key>)[value] === key
      )
    }
    return isString(value) || isNumber(value)
  })
}

export const isEnumKey = <T extends object>(
  obj: T,
  key: keyof T,
): key is keyof T => isString(key) && Object.keys(obj).includes(key)

export function isEnumValue<T extends AnyRecord>(
  obj: T,
  value: unknown,
): value is T[keyof T] {
  if (isNumber(value)) {
    /**
     * NOTE: Enum values in TS can be numbers, but when compiled to JS, those numbers are set as
     * additional keys whose values are their corresponding key from the TS enum.
     * @example
     * ```ts
     * enum My_Enum { A = 1, B = 2 }
     * ```
     *
     * would be compiled to the following in JS:
     *
     * ```js
     * var My_Enum;
     * (function (My_Enum) {
     *   My_Enum[My_Enum["A"] = 1] = "A";
     *   My_Enum[My_Enum["B"] = 2] = "B";
     * })(My_Enum || (My_Enum = {}));
     * ```
     *
     * So, the object would look like this:
     *
     * ```js
     * console.log(My_Enum)
     *
     * {
     *   "1": "A",
     *   "2": "B",
     *   "A": 1,
     *   "B": 2
     * }
     * ```
     *
     * Therefore...
     *
     * ```js
     * My_Enum.A === 1 // true
     * My_Enum[1] === 'A' // true
     * ```
     *
     * So, we need to check if the value is a number and if the object has a key of that value.
     */
    const enumValue = obj[value]
    return isString(enumValue) && obj[enumValue] === value
  }

  return Object.values(obj).includes(value)
}

/**
 * NOTE: This returns a function that can be used to verify length, not the result of the verification.
 */
export function lengthMoreThan(length: number) {
  return (value: { length: number }) => value.length > length
}

/**
 * NOTE: This returns a function that can be used to verify length, not the result of the verification.
 */
export function lengthLessThan(length: number) {
  return (value: { length: number }) => value.length < length
}
