/**
 * Get the scale of magnitude.
 *
 * @returns Square root of the sum of given squares
 */
export function magnitude(...nums: number[]): number {
  return Math.hypot(...nums)
}
