import { variadic } from '../array/variadic'

/**
 * Returns a random element of a specific array.
 *
 * @param array - A specific array.
 * @returns A random element of a specific array.
 */
export function random(...nums: number[]): number {
  const arr = variadic(nums)

  return arr[Math.floor(arr.length * Math.random())]
}
