import { describe, expect, it, vi } from 'vitest'
import { MAX_MEMOIZE_SIZE, memoize } from './memoize'

describe('memoize', () => {
  describe('memoize', () => {
    it('recalculates the result when first argument changed', () => {
      const spy = vi.fn()

      const addOne = (number: number) => {
        spy()
        return number + 1
      }

      const addOneMemoized = memoize(addOne)

      expect(addOneMemoized(1)).toBe(2)
      expect(addOneMemoized(2)).toBe(3)
      expect(spy).toHaveBeenCalledTimes(2)
    })

    it('gets the result from cache when the first argument stay the same', () => {
      const spy = vi.fn()
      const addOne = (number: number) => {
        spy()
        return number + 1
      }
      const addOneMemoized = memoize(addOne)

      expect(addOneMemoized(1)).toBe(2)
      expect(addOneMemoized(1)).toBe(2)
      expect(spy).toHaveBeenCalledTimes(1)
    })

    it('deletes oldest cache item when the cache limit is reached', () => {
      const spy = vi.fn()
      const addOne = (number: number) => {
        spy()
        return number + 1
      }
      const addOneMemoized = memoize(addOne)

      for (let i = 0; i < MAX_MEMOIZE_SIZE; i++) {
        expect(addOneMemoized(i)).toBe(i + 1)
      }

      // 0 is in the cache
      expect(addOneMemoized(0)).toBe(1)
      expect(addOneMemoized(1)).toBe(2)
      expect(spy).toHaveBeenCalledTimes(MAX_MEMOIZE_SIZE)

      expect(addOneMemoized(MAX_MEMOIZE_SIZE)).toBe(MAX_MEMOIZE_SIZE + 1)
      expect(spy).toHaveBeenCalledTimes(MAX_MEMOIZE_SIZE + 1)

      // 0 is no longer in the cache
      expect(addOneMemoized(0)).toBe(1)
      expect(spy).toHaveBeenCalledTimes(MAX_MEMOIZE_SIZE + 2)
    })
  })

  describe('only argument is object', () => {
    it('recalculates the result when the first argument changed', () => {
      const spy = vi.fn()
      const getValues = (someObject: object) => {
        spy()
        return Object.values(someObject)
      }
      const getValuesMemoized = memoize(getValues)

      expect(getValuesMemoized({ one: 1, two: 2 })).toStrictEqual([1, 2])
      expect(getValuesMemoized({ one: 3, four: 4 })).toStrictEqual([3, 4])
      expect(spy).toHaveBeenCalledTimes(2)
    })

    it('gets the result from cache when the first argument stay the same', () => {
      const spy = vi.fn()
      const getValues = (someObject: object) => {
        spy()
        return Object.values(someObject)
      }
      const getValuesMemoized = memoize(getValues)

      const testObject1 = { one: 1, two: 2 }
      expect(getValuesMemoized(testObject1)).toStrictEqual([1, 2])
      expect(getValuesMemoized(testObject1)).toStrictEqual([1, 2])
      expect(spy).toHaveBeenCalledTimes(1)
    })

    it('does not change the result when the argument was changed in value only', () => {
      const spy = vi.fn()
      const getValues = (someObject: object) => {
        spy()
        return Object.values(someObject)
      }
      const getValuesMemoized = memoize(getValues)

      const testObject1 = { one: 1, two: 2 }
      expect(getValuesMemoized(testObject1)).toStrictEqual([1, 2])

      testObject1.one = 2
      expect(getValuesMemoized(testObject1)).toStrictEqual([1, 2])

      expect(spy).toHaveBeenCalledTimes(1)
    })
  })

  describe('customized resolver', () => {
    it('recalculates the result when the resolver result was changed', () => {
      const spy = vi.fn()
      const getNameSpy = (name: string, _id: string) => {
        spy()
        return name
      }
      const getNameMemoized = memoize(getNameSpy, (_name: string, id: string) => id)

      expect(getNameMemoized('Lisa', '1')).toBe('Lisa')
      expect(getNameMemoized('Lisa', '2')).toBe('Lisa')
      expect(spy).toHaveBeenCalledTimes(2)
    })

    it('gets the result from cache when the resolver result was not changed', () => {
      const spy = vi.fn()
      const getNameSpy = (name: string, _id: string) => {
        spy()
        return name
      }
      const getNameMemoized = memoize(getNameSpy, (_name: string, id: string) => id)

      expect(getNameMemoized('Lisa', '1')).toBe('Lisa')
      expect(getNameMemoized('Lisa', '1')).toBe('Lisa')
      expect(spy).toHaveBeenCalledTimes(1)
    })
  })

  describe('customized resolver with different return type than the method', () => {
    it('recalculates the result when the resolver result was changed', () => {
      const spy = vi.fn()
      const getNameSpy = (name: string, _id: string) => {
        spy()
        return { name }
      }
      const getNameMemoized = memoize(getNameSpy, (_name: string, id: string) => id)

      expect(getNameMemoized('Lisa', '1')).toStrictEqual({ name: 'Lisa' })
      expect(getNameMemoized('Lisa', '2')).toStrictEqual({ name: 'Lisa' })
      expect(spy).toHaveBeenCalledTimes(2)
    })

    it('gets the result from cache when the resolver result was not changed', () => {
      const spy = vi.fn()
      const getNameSpy = (name: string, _id: string) => {
        spy()
        return { name }
      }
      const getNameMemoized = memoize(getNameSpy, (_name: string, id: string) => id)

      expect(getNameMemoized('Lisa', '1')).toStrictEqual({ name: 'Lisa' })
      expect(getNameMemoized('Lisa', '1')).toStrictEqual({ name: 'Lisa' })
      expect(spy).toHaveBeenCalledTimes(1)
    })
  })
})
