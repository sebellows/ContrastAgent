import { UnknownRecord } from 'type-fest'
import { clone } from '../common/clone'
import { variadic } from '../array/variadic'
import { Variadic } from '../types/base'

export function omit<
  BaseType extends UnknownRecord,
  Key extends keyof BaseType,
>(obj: BaseType, ...keys: Variadic<Key>): Omit<BaseType, Key> {
  const _keys = variadic(keys)
  const cloned = clone(obj)

  for (const key of _keys) {
    delete cloned[key]
  }

  return cloned
}
