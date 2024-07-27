import { FixedLengthArray } from 'type-fest'

/**
 * @typedef {Object} Bounds
 * @property x1 - The x (horizontal) coordinate of the top of a plane
 * @property y1 - The y (vertical) coordinate of the top of a plane
 * @property x2 - The x (horizontal) coordinate of the bottom of a plane
 * @property y2 - The y (vertical) coordinate of the bottom of a plane
 */
export interface Bounds {
  x1: number
  y1: number
  x2: number
  y2: number
}

export type BoundsList = FixedLengthArray<number, 4>

export type WithMinMax<
  T extends number | number[] | Record<string, number> = number,
> = {
  min: T
  max: T
}

export type Range<
  T extends number | number[] | Record<string, number> = number,
> = {
  min: T
  max: T
}

export type NumericArray = [
  Array<number>,
  Int8Array,
  Uint8Array,
  Uint8ClampedArray,
  Int16Array,
  Uint16Array,
  Int32Array,
  Uint32Array,
  Float32Array,
  Float64Array,
]
