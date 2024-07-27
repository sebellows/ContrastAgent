import { UnknownRecord } from 'type-fest'
import { clone } from '../common/clone'
import { getKeys } from './getKeys'
import { Variadic } from '../types/base'
import { variadic } from '../array/variadic'

export function pick<
  BaseType extends UnknownRecord,
  Key extends keyof BaseType,
>(obj: BaseType, ...keys: Variadic<Key>): Pick<BaseType, Key> {
  const _keys = variadic(keys)
  const cloned = clone(obj)

  const omittedKeys = getKeys(cloned).filter((key) => !_keys.includes(key))

  for (const key of omittedKeys) {
    delete cloned[key]
  }

  return cloned
}
