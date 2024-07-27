import { UnknownRecord, ValueOf } from 'type-fest'
import { getEntries } from './getEntries'

export function mapValues<T extends UnknownRecord, R>(
  obj: T,
  mapper: (value: ValueOf<T>, key: keyof T, obj: T) => R,
) {
  return getEntries(obj).reduce(
    (result, [key, value]) => {
      result[key] = mapper(value, key, obj)
      return result
    },
    {} as Record<keyof T, R>,
  )
}
