import { UnknownRecord } from 'type-fest'
import { ObjectEntries } from 'type-fest/source/entries'

/**
 * A stricter way of setting what the expected entries are, otherwise there's a
 * damn good chance you'll get `never` or `unknown` as the key/value type.
 */
export const getEntries = <T extends UnknownRecord>(obj: T): ObjectEntries<T> =>
  Object.entries(obj) as ObjectEntries<T>
