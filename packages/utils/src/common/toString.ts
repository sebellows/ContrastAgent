import { AnyRecord, Primitive } from '../types/base'
import { isDate, isNil, isObject, isPrimitive } from '../assert'
import { hasOwn } from '../object/hasOwn'
import { safeStringify } from './safeStringify'

const hasBuiltInToString = <O extends AnyRecord>(
  obj: O,
): obj is O & O['toString'] => {
  return (
    hasOwn(obj, 'toString') &&
    !Object.is(obj.toString, Object.prototype.toString)
  )
}

export const toString = (value: any): string => {
  const INFINITY = 1 / 0

  if (isNil(value)) return ''

  // Exit early for strings to avoid a performance hit in some environments.
  if (typeof value == 'string') return value

  if (
    Array.isArray(value) &&
    value.every((val) => isPrimitive(val)) === false
  ) {
    // Recursively convert values (susceptible to call stack limits).
    return `${(value as Primitive[]).map((other) =>
      other == null ? other : toString(other as any),
    )}`
  }

  if (!isNaN(Number(value))) {
    const numValue = Number(value)
    const result = `${value}`

    return result == '0' && 1 / numValue == -INFINITY ? '-0' : result
  }

  if (isDate(value) || (!isObject(value) && hasBuiltInToString(value))) {
    return value.toString()
  }

  if (isObject(value)) {
    return safeStringify(value)
  }

  // We've exhausted our options by this point...
  return `${value}`
}
