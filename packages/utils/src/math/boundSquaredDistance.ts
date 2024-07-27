import { Bounds, BoundsList } from './math.types'
import { Plane } from './plane'

/**
 * Squared distance between two points.
 *
 * @param x1 - First x coordinate.
 * @param y1 - First y coordinate.
 * @param x2 - Second x coordinate.
 * @param y2 - Second y coordinate.
 * @returns The squared distance between the two points.
 */
export function boundsSquaredDistance(bounds: Bounds | BoundsList): number
export function boundsSquaredDistance(...bounds: BoundsList[number][]): number
export function boundsSquaredDistance(bounds: any): number {
  if (!bounds || bounds.length !== 4 || Plane.isPlane(bounds)) return -1

  const { x1, y1, x2, y2 } = new Plane(bounds)

  return (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
}
