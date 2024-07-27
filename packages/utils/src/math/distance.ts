import { boundsSquaredDistance } from './boundSquaredDistance'

/**
 * Distance between two points.
 *
 * @param x1 - First x coordinate.
 * @param y1 - First y coordinate.
 * @param x2 - Second x coordinate.
 * @param y2 - Second y coordinate.
 * @returns The distance between the two points.
 */
export function distance(
  x1: number,
  y1: number,
  x2: number,
  y2: number,
): number {
  return Math.sqrt(parseFloat(boundsSquaredDistance(x1, y1, x2, y2).toString()))
}

export function valuesAreWithinDistance(
  valueA: number,
  valueB: number,
  delta: number,
) {
  const highest = Math.max(valueA, valueB)
  const lowest = Math.min(valueA, valueB)

  return highest - delta < lowest
}
