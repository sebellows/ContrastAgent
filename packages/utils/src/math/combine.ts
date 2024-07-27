import { createMockNumericArray } from '../array/numericArray'
import { NumericArray } from './math.types'

export function combine<
  A extends NumericArray[number],
  B extends number | NumericArray[number],
>(a: A, b: B, operation: (...nums: number[]) => number): number[] {
  const len = a.length
  const result = createMockNumericArray(len)

  for (let i = 0; i < len; i++) {
    const val1 = a[i] ?? 0
    const val2 = typeof b === 'number' ? b : b[i] ?? 0

    result[i] = operation(val1, val2)
  }

  return result
}
