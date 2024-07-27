import { Get } from 'type-fest'
import { toPathArray } from './paths'

export function get<BaseType, Path extends string | readonly string[]>(
  obj: BaseType,
  path: Path,
): Get<BaseType, Path> {
  const pathArray = toPathArray(path)

  const value: any = obj

  return pathArray.reduce((nested, pathKey) => {
    const key = pathKey

    return nested[key] as Get<typeof nested, typeof key>
  }, value) as Get<BaseType, Path>
}
