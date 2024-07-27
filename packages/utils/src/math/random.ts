/**
 * Returns a random number within a specific range.
 *
 * @param start - Smallest number value that can be returned.
 * @param end - Biggest number value that can be returned.
 * @returns A random number.
 */
export function randomNumber(start: number, end: number): number {
  return start + (end - start) * Math.random()
}

/**
 * Returns a random int within a specific range.
 *
 * @param start - Smallest int value that can be returned.
 * @param end - Biggest int value that can be returned.
 * @returns A random int.
 */
export function randomInt(start: number, end: number): number {
  return start + Math.floor((1 + end - start) * Math.random())
}

/**
 * Returns a random float within a specific range.
 *
 * @param start - Smallest float value that can be returned.
 * @param end - Biggest float value that can be returned.
 * @returns A random float.
 */
export function randomFloat(start: number, end: number): number {
  return start + (end - start) * Math.random()
}
