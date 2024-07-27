import { NumericArray } from '../math/math.types'

export function createMockNumericArray(
  n: number,
  valueOrFn: number | ((v: number, i: number, arr?: number[]) => number) = 0,
): number[] {
  const newArr = new Array(n)

  if (typeof valueOrFn === 'number') {
    return newArr.fill(valueOrFn)
  }

  return newArr.map(valueOrFn)
}

export function forEachNumber<A extends NumericArray[number]>(
  numArr: A,
  operation: (num: number, index: number, arr?: A) => number,
): number[] {
  const len = numArr.length
  const result = createMockNumericArray(len)

  for (let i = 0; i < len; i++) {
    result[i] = operation(numArr[i], i, numArr)
  }

  return result
}
