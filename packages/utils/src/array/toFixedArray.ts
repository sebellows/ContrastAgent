import { FixedLengthArray } from 'type-fest'
import { toReadOnly } from '../object/toReadOnly'
import { clone } from '../common/clone'

const EmptyItemMap = {
  number: 0,
  string: '',
  boolean: false,
  array: [],
  object: {},
  map: new Map(),
  set: new Set(),
  date: '',
  null: null,
  undefined: undefined,
  function: () => {},
}

export function toFixedArray<T, Length extends number>(
  args: T[],
  limit?: Length,
): FixedLengthArray<T, Length> {
  if (limit === undefined) {
    limit = args.length as Length
  }

  if (args.length === 0 && limit === 0) {
    args = Array(limit).fill(null)
  } else if (args.length < limit) {
    args.push(...Array(limit - args.length).fill(EmptyItemMap[typeof args[0]]))
  } else if (args.length > limit) {
    args = clone(args.slice(0, limit))
  }

  return toReadOnly(args) as FixedLengthArray<T, Length>
}
