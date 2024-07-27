import { getKeys } from './getKeys'
import { isPlainObject } from '../assert'
import type { AnyRecord, Intersection } from '../types/base'

type FalsyType = false | null | undefined

export function deepMerge<
  TSource extends AnyRecord,
  TArgs extends (TSource | FalsyType)[],
>(...sources: TArgs) {
  return merge(...sources.reverse())
}

export function merge<
  TSource extends AnyRecord,
  TArgs extends (TSource | FalsyType)[],
>(...sources: TArgs) {
  const target: AnyRecord = {}

  for (const source of sources) {
    if (!isPlainObject(source)) continue

    const keys = getKeys(source)

    for (const key of keys) {
      if (isPlainObject(target[key]) && isPlainObject(source[key])) {
        target[key] = merge(target[key], source[key])
      } else {
        target[key] ??= source[key]
      }
    }
  }

  return target as Intersection<Exclude<TArgs[number], FalsyType>>
}

export function mapMerge(dataArray: AnyRecord[], ...itemDefaults: AnyRecord[]) {
  if (itemDefaults && Array.isArray(dataArray)) {
    return dataArray.map((item) => merge(item, ...itemDefaults))
  }
  return dataArray
}
