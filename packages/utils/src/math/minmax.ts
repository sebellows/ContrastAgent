import { isPlainObject } from '../assert'
import { hasOwn } from '../object/hasOwn'
import { WithMinMax } from './math.types'

/**
 * Check if a value is within a specific range.
 *
 * @param value - The specific value.
 * @param min - Minimum value.
 * @param max - Maximum value.
 * @returns Returns true if value is within a specific range.
 */
export function withinMinMax(value: number, min: number, max: number): boolean {
  return value >= min && value <= max
}

/**
 * Determine if a value has a min and max property.
 */
export function hasMinMax(o: unknown): o is WithMinMax {
  return isPlainObject(o) && hasOwn(o, 'min') && hasOwn(o, 'max')
}

export const resolveMinMax = (value: unknown): WithMinMax => {
  let min = -Infinity
  let max = Infinity
  if (typeof value === 'number') {
    min = -value / 2
    max = value / 2
  } else if (hasMinMax(value)) {
    min = value.min
    max = value.max
  }

  return { min, max }
}
