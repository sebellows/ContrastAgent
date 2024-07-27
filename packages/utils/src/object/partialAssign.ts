/**
 * Copies only an explicit set of keys over to an object.
 */
export function partialAssign<T>(
  keysToCopy: (keyof T)[],
  target: T,
  source?: Partial<T>,
): T {
  if (source === undefined) {
    return target
  }

  for (const key of keysToCopy) {
    const value: T[keyof T] | undefined = source[key]
    if (value !== undefined) {
      target[key] = value
    }
  }

  return target
}
