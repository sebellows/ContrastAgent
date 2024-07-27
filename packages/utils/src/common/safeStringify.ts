/**
 * Safely use `JSON.stringify()` without triggering an endless loop
 * when an object circularly references itself.
 */
export const safeStringify = (obj: unknown): string => {
  let cache: any[] = []

  const str = JSON.stringify(obj, function (_key, value) {
    if (typeof value === 'object' && value !== null) {
      if (cache.indexOf(value) !== -1) {
        // Circular reference found, discard key
        return
      }
      // Store value in our collection
      cache.push(value)
    }

    return value
  })

  cache = [] // reset the cache

  return str
}
