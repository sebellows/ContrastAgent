/**
 * Get the angle (in radians) from the X axis to a point.
 * NOTE: reversed order from `Math.atan2` to account for spread vector coordinates that
 * would be in order x then y.
 *
 * @param x — A numeric expression representing the cartesian x-coordinate.
 * @param y — A numeric expression representing the cartesian y-coordinate.
 * @returns The angle (in radians) from the X axis to a point.
 */
export function angle(x: number, y: number): number {
  return Math.atan2(y, x)
}

/**
 * Converts angle from radian to degree.
 *
 * @param angleInRad - The angle in radian.
 * @returns The angle in degree.
 */
export function radToDeg(angleInRad: number): number {
  return (angleInRad * 180) / Math.PI
}

import { valuesAreWithinDistance } from './distance'

/**
 * @function degreeToRadius
 * @description
 * Converts angle from degree to radian.
 *
 * @sign public Number degToRad(angleInDeg)
 * @param angleInDeg - The angle in degrees.
 * @returns The angle in radians.
 */
export function degreeToRadius(angleInDeg: number): number {
  return (angleInDeg * Math.PI) / 180
}

export function rotationsAreWithinAngle(
  rotationA: number,
  rotationB: number,
  angle: number,
) {
  const normalisedA = rotationA % (Math.PI * 2)
  const normalisedB = rotationB % (Math.PI * 2)

  return valuesAreWithinDistance(normalisedA, normalisedB, angle)
}
