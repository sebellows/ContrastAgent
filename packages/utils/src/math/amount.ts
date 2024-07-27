/**
 * If checkValue is within the range, this will return a number between 0 and 1.
 *
 * @param checkValue - Value that should checked with minimum and maximum.
 * @param minValue - Bottom of the range
 * @param maxValue - Top of the range
 * @returns The position of the checked value in a coordinate system normalized
 * such that `minValue` is 0 and `maxValue` is 1.
 */
export function amount(
  checkValue: number,
  minValue: number,
  maxValue: number,
): number {
  if (minValue < maxValue) {
    return (checkValue - minValue) / (maxValue - minValue)
  }
  return (checkValue - maxValue) / (minValue - maxValue)
}
