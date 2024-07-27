import { TypedArray } from 'type-fest'
import { toFixedArray } from '../array/toFixedArray'
import { maxVector, minVector } from './vector'

export function multiplyScalar<Vector extends readonly number[]>(
  vector: Vector,
  scalar: number,
) {
  return toFixedArray(vector.map((v) => (v *= scalar)))
}

export function divideScalar<Vector extends readonly number[]>(
  vector: Vector,
  scalar: number,
) {
  return multiplyScalar(vector, 1 / scalar)
}

export function clampScalar<
  Vector extends readonly number[] | Readonly<TypedArray>,
>(vector: Vector, minVal: number, maxVal: number) {
  if (Array.isArray(vector)) {
    const minVals = Object.freeze(
      new Array(vector.length).fill(minVal) as number[],
    )
    const maxVals = Object.freeze(
      new Array(vector.length).fill(maxVal) as number[],
    )
    const minMax = minVector(maxVals, vector)

    return maxVector(minVals, minMax)
  } else {
    const arrCtor = vector.constructor
    const minVals = arrCtor(vector.length).fill(minVal)
    const maxVals = arrCtor(vector.length).fill(maxVal)
    const minMax = minVector(maxVals, vector)

    return maxVector(minVals, minMax)
  }
}
