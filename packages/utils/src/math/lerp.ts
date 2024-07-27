import { clamp } from './clamp'

/**
 * Linear interpolation. Passing amount with a value of 0 will cause
 * value1 to be returned, a value of 1 will cause value2 to be returned.
 *
 * @param from - One value.
 * @param to - Another value.
 * @param amount - Amount of `from` to `to`.
 * @returns Linear interpolated value.
 */
export function lerp(from: number, to: number, amount: number): number {
  amount = clamp(amount, 0, 1)

  return from + (to - from) * amount
}

export function lerpTheta(
  from: number,
  to: number,
  amount: number,
  circleAt: number = Math.PI * 2,
) {
  const distance = to - from
  const unloopedDistance = clamp(
    distance - Math.floor(distance / circleAt) * circleAt,
    0,
    circleAt,
  )
  const isLeft = unloopedDistance > Math.PI
  const offset = isLeft ? unloopedDistance - Math.PI * 2 : unloopedDistance

  return lerp(from, from + offset, amount)
}
