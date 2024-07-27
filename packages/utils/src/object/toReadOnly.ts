import { UnknownArray, UnknownRecord } from 'type-fest'

export const toReadOnly = <T extends UnknownArray | UnknownRecord>(
  obj: T,
): Readonly<T> => Object.freeze(obj)
