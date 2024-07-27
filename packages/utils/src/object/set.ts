import { UnknownRecord } from 'type-fest'
import { SKIP_JS_BUILTINS, toPathArray } from './paths'
import { get } from './get'

export function setNestedValue<
  BaseType extends UnknownRecord,
  Path extends string | readonly string[],
>(obj: BaseType, path: Path, newValue: unknown) {
  const paths = toPathArray(path).slice()
  const lastKey = paths.pop()!

  if (paths.some((p) => SKIP_JS_BUILTINS.has(p))) return

  const lastObject = get(obj, paths) as UnknownRecord
  lastObject[lastKey] = newValue

  return lastObject[lastKey]
}
