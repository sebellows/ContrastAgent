/**
 * Returns `1` or `-1` randomly.
 *
 * @param percent - The probability of returning `-1`
 * @returns 1 or -1.
 */
export function negate(percent: number): number {
  return Math.random() < percent ? -1 : 1
}
