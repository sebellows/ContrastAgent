import { UnknownRecord } from 'type-fest'

/**
 * `Object.keys()` defines all keys as strings which can lead to TS issues with
 * typed objects. This helper will coerce the type of the keys to avoid warnings.
 */
export const getKeys = <T extends UnknownRecord>(obj: T) =>
  Object.keys(obj) as (keyof T)[]
