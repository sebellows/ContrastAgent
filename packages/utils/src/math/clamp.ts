/**
 * Restricts a value to be within a specified range.
 *
 * @param value - A value.
 * @param max - Maximum that value can be.
 * @param min - Minimum that value can be.
 * @returns The value between minimum and maximum.
 */
export function clamp(value: number, min: number, max: number): number {
  if (value > max) return max

  if (value < min) return min

  return value
}
