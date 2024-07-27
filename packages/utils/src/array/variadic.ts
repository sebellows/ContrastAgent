export function variadic<T extends any[]>(...args: T) {
  return Array.isArray(args[0]) ? args[0] : args
}
