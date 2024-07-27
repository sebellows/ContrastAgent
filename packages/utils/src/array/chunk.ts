import { AnyArray } from '../types/base'
import { isPlainObject } from '../assert'

export type UnchunkedArray<T> = T[]
export type ChunkedArray<T> = T[][]

/**
 * Creates an array of elements split into groups the length of size.
 * If array can't be split evenly, the final chunk will be the remaining elements.
 *
 * NOTE: This function MAY mutate the original array, as the cloning is shallow.
 */
function chunk<T, S extends number = number>(arr: T[], size: S[]): ChunkedArray<T>
function chunk<T, S extends AnyArray[]>(arr: T[], size: S): ChunkedArray<T>
function chunk<T, S extends number>(arr: T[], size: S): ChunkedArray<T> {
  const chunks: ChunkedArray<T> = []
  const queue = arr.map(item => (isPlainObject(item) ? { ...item } : item))

  if (Array.isArray(size)) {
    let sizeCount = 0
    const sizeArr = size.every(s => Array.isArray(s)) ? size.map(item => item.length) : size

    while (queue.length > 0) {
      const size = sizeArr[sizeCount++]
      const entry = queue.splice(0, size)
      chunks.push(entry)
    }

    return chunks
  }

  while (queue.length > 0) {
    const entry = queue.splice(0, size)
    chunks.push(entry)
  }

  return chunks
}

export { chunk }
