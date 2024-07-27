/** Create a memoized version of a pure function. */
interface MemoizeMap<T, U> {
  get(key: T): U
  has(key: T): boolean
  set(key: T, value: U): MemoizeMap<T, U>
}

export const MAX_MEMOIZE_SIZE = 50

/**
 * Better memoization function that uses a WeakMap for object keys and a Map for
 * other keys. It also has a max size of 50 to prevent memory leaks.
 *
 * @author Shopify
 * @library Quilt
 * @package function-enhancers
 * @see {@link https://github.com/Shopify/quilt/tree/main/packages/function-enhancers}
 *
 * The memoize decorator creates a function that memoizes the results of the function it is decorating.
 * The cache key for storing the results is based on the first argument provided to the memoized function.
 * If the memoization key cannot be inferred from the first argument alone, a resolver should be passed
 * in to ensure a unique key. (ex: the unique key is in the second argument, or the unique key is a
 * combination of a few arguments)
 *
 * Know that memoization will be skipped on server process and the cached results have a maximum limit
 * of 50 entries on a first in first out basis.
 *
 * Memoizing a simple function
 * ```ts
 * import {memoize} from 'src/helpers/collection/internal/memoize'
 *
 * const addOne = (number: number) => {
 *   return number + 1;
 * }
 *
 * const addOneMemoized = memoize(addOne)
 *
 * addOneMemoized(1); // -> 2, addOne is executed
 * addOneMemoized(1); // -> 2, result is from cache
 * ```
 *
 * The memoize decorator creates a function that memoizes the results of the function it is
 * decorating. The cache key for storing the results is based on the first argument provided to
 * the memoized function. If the memoization key cannot be inferred from the first argument alone,
 * a resolver should be passed in to ensure a unique key. (ex: the unique key is in the second
 * argument, or the unique key is a combination of a few arguments)
 *
 * Know that memoization will be skipped on server process and the cached results have a maximum
 * limit of 50 entries on a first in first out basis.
 *
 * Memoizing a simple function
 *
 * ```ts
 * const addOne = (number: number) => {
 *   return number + 1
 * }
 *
 * const addOneMemoized = memoize(addOne)
 *
 * addOneMemoized(1); // -> 2, addOne is executed
 * addOneMemoized(1); // -> 2, result is from cache
 * ```
 *
 * Memoizing a function with object as argument
 * When memoizing a function with object as first argument, make sure the object is immutable.
 *
 * ```ts
 * const getValues = (someObject: { one: string; two: string }) => {
 *   return
 * }
 *
 * const getValuesMemoized = memoize(getValues)
 *
 * const testObject1 = { one: 1, two: 2 }
 * getValuesMemoized(testObject1); // -> [1, 2], getValues is executed
 * getValuesMemoized(testObject1); // -> [1, 2], result is from cache
 *
 * testObject1.two = 3
 * getValuesMemoized(testObject1); // -> [1, 2], result is from cache, BAD
 * ```
 *
 * Memoizing a function while providing a resolver
 *
 * The resolver takes in the same arguments as the function it is enhancing. Be sure that the
 * resolver returns a unique identifer.
 *
 * ```ts
 * import { memoize } from '@shopify/function-enhancers'
 *
 * const getByCommand = (command: string, value: string) => {
 *   // implementation for getByCommand
 * }
 *
 * const getByCommandMemoized = memoize(
 *   getByCommand,
 *   (command: string, value: string) => `${command}${value}`,
 * )
 *
 * getByCommandMemoized('command name 1', 'command value 1'); // runCommand is executed
 *
 * getByCommandMemoized('command name 1', 'command value 2'); // runCommand is executed
 * ```
 *
 * Next let's fix the example from above so the results will always be correct.
 *
 * ```ts
 * const getByCommand = (command: string, value: string) => {
 *   // implementation for getByCommand
 * }
 *
 * const getByCommandMemoized = memoize(
 *   getByCommand,
 *   (command: string, value: string) => `${command}${value}`,
 * )
 *
 * const testObject1 = {id: 1, value: 2}
 * getByCommandMemoized(testObject1); // -> [1, 2], getValues is executed
 * getByCommandMemoized(testObject1); // -> [1, 2], result is from cache
 *
 * testObject1.value = 3
 * getByCommandMemoized(testObject1); // -> [1, 3], getValues is executed
 * ```
 */
export function memoize<Method extends (this: unknown, ...args: any[]) => any>(
  method: Method,
  resolver?: (...args: Parameters<Method>) => any,
): Method {
  const weakMapCache = new WeakMap()
  const mapCache = new Map()
  const mapKeys: any[] = []

  return function memoized(...args: Parameters<Method>) {
    if (typeof globalThis === 'undefined') {
      return method.apply(this, args)
    }

    const useWeakMap = args.length === 1 && typeof args[0] === 'object' && !resolver

    let key: WeakKey
    if (useWeakMap) {
      key = args[0]
    } else if (resolver && resolver instanceof Function) {
      key = resolver(...args)
    } else {
      key = args[0]
    }

    const cache: MemoizeMap<any, any> = useWeakMap ? weakMapCache : mapCache
    if (cache.has(key)) {
      return cache.get(key)
    }

    const result = method.apply(this, args)

    if (useWeakMap) {
      weakMapCache.set(key, result)
    } else {
      mapCache.set(key, result)
      mapKeys.push(key)

      if (mapCache.size > MAX_MEMOIZE_SIZE) {
        const oldestKey = mapKeys[0]
        mapCache.delete(oldestKey)
        mapKeys.shift()
      }
    }

    return result
  } as Method
}
