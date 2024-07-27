import { FixedLengthArray, TypedArray } from 'type-fest'
import { toFixedArray } from '../array/toFixedArray'
import { isTypedArray } from '../assert'

function toNumericArray(
  vector: readonly number[] | Readonly<TypedArray>,
): number[] {
  return isTypedArray(vector) ? Array.from(vector as readonly number[]) : vector
}

export function minVector<
  Vector extends readonly number[] | Readonly<TypedArray>,
  Length extends number = Vector['length'],
>(vector1: Vector, vector2: Vector): FixedLengthArray<number, Length> {
  const v1 = toNumericArray(vector1)
  const v2 = toNumericArray(vector2)
  const result = v1.map((v, i) => Math.min(v, v2[i]))

  return toFixedArray(result)
}

export function maxVector<
  Vector extends readonly number[] | Readonly<TypedArray>,
  Length extends number = Vector['length'],
>(vector1: Vector, vector2: Vector): FixedLengthArray<number, Length> {
  const v1 = toNumericArray(vector1)
  const v2 = toNumericArray(vector2)
  const result = v1.map((v, i) => Math.max(v, v2[i]))

  return toFixedArray(result)
}
