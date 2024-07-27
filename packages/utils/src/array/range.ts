import { isFunction, isNumber } from '../assert'

type RangeMapFn<T> = (v: T, k: number) => T

function rangeFromTo<T>(
  from: number,
  to?: number,
  step = 1,
  initialValue: T | number | undefined = undefined,
) {
  let length = from

  if (!to) {
    // If there's no `to` argument, then `from` sets the length of the array
    to = from - 1
    from = 0
  } else if (from === 0) {
    // If `to` is set and `from` is 0, we want to ensure the result's last item is `to`
    length = to + 1
  } else {
    const diff = to - from
    if (diff % step !== 0) {
      // if step doesn't divide evenly into the difference of `to` and `from`, we want to
      // add an extra slot to the length so we get as close to `to` as we can.
      length = diff + 1
    } else {
      // Otherwise add step value to the difference to ensure `to` is last index value
      length = diff + step
    }
  }

  length = Math.ceil(length / step)

  return Array.from({ length }, (_, i) => {
    if (initialValue) return initialValue

    return from + i * step
  })
}

/**
 * Create a new array of a certain length and populate it with values.
 *
 * @param start - A starting index for an array or the total length of the array.
 * @param stop - [Optional] Number for the last index in the array
 * @param step - [Optional] Number by which to increment values. Default is 1.
 * @param initialValue - [Optional] A shared value to apply to each index in the array
 * @returns A new array of the desired length with a given value.
 *
 * @example
 * const arr = range(12) // [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
 *
 * const iterateBy5 = range(1, 50, 5) // [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
 */
function range<T = any>(start: number, stop: number, step: number, initialValue: T): T[]
function range(start: number, stop: number, step: number): number[]
function range(start: number, stop: number): number[]
function range(start: number): number[]
function range<T>(
  start: number,
  stop: number,
  step: number,
  initialValue: T | undefined,
): undefined extends T ? number[] : T[]
function range<T>(start: number, mapFn: RangeMapFn<T>, thisArg: T): T[]
function range<T = any>(
  start: number,
  mapFn: RangeMapFn<T>,
  thisArg?: T | undefined,
): T[] | number[]
function range(start: number, mapFn: RangeMapFn<any>, thisArg?: any): any[]
function range(start: number, ...args: any[]) {
  if (!args.length) {
    return rangeFromTo(start)
  }

  if (!isNumber(args[0]) && !isFunction(args[0])) {
    throw new Error('Second argument in range function should be either a number or a callback.')
  }

  if (isNumber(args[0])) {
    const [stop, ...rest] = args

    return rangeFromTo(start, stop, ...rest)
  }

  const [mapFn, thisArg] = args

  return Array.from({ length: start }, mapFn, thisArg)
}

export { range }
