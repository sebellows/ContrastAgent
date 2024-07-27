import { safeStringify } from './safeStringify'

/**
 * Safely compare two elements for equality.
 *
 * NOTE: Objects are stringified before comparison to avoid circular references
 * and other issues that can arise when comparing objects directly.
 *
 * @example
 * ```ts
 * const dateA = new Date('2012-12-30')
 * const dateB = new Date('2012-12-30')
 * Object.is(dateA, dateB) // FALSE
 * Object.is(dateA.toString(), dateB.toString()) // TRUE
 * isEqual(dateA, dateB) // TRUE
 *
 * const objA = { a: 1, b: 2 }
 * const objB = { b: 2, a: 1 }
 * isEqual(objA, objB) // TRUE
 */
export const isEqual = (a: unknown, b: unknown): boolean => {
  if (a === null || b === null) return a === null && b === null
  if (a === undefined || b === undefined) return a === undefined && b === undefined

  const typeA = typeof a
  const typeB = typeof b

  if (typeA !== typeB) return false

  if (typeA !== 'object') return Object.is(a, b)

  return safeStringify(a) === safeStringify(b)
}
