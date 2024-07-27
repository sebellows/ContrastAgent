/**
 * Matches any primitive value
 * @see {@link https://developer.mozilla.org/en-US/docs/Glossary/Primitive}
 *
 * @category Type
 */
export type Primitive = null | undefined | string | number | boolean | symbol | bigint

/** Matches any primitive, `void`, `Date`, or `RegExp` value. */
export type BuiltIn = Primitive | void | Date | RegExp

export type BasicType = Primitive | object | Function
export type BasicTypeName =
  | 'string'
  | 'boolean'
  | 'number'
  | 'object'
  | 'function'
  | 'symbol'
  | 'bigint'

/** Matches non-recursive types (i.e., types that can never circularly reference themselves). */
export type NonRecursiveType =
  | Primitive
  | void
  | Date
  | RegExp
  | Function
  | (new (...args: any[]) => unknown)

export type Mutable<T extends { [x: string]: any }, K extends string> = {
  [P in K]: T[P]
}

/**
 * Returns a version of a type comprised only of its writable properties.
 *
 * @example
 * ```ts
 * class User {
 *   readonly id: number
 *   name: string
 *   constructor(id: string, name: string) {
 *     this.id = id
 *     this.name = name
 *   }
 * }
 * const user = new User(id: 1, name: 'John')
 * user.name = 'Jane' // OK
 * user.id = 2 // TypeError
 * (user as Writable<User>).id = 2 // OK
 *
 * \// Error: There is no `iq` property on `User`
 * (user as Writable<User>).iq = 75;
 * ```
 */
export type Writable<T> = {
  -readonly [K in keyof T]: T[K]
}

/** Why is this not a thing yet?!? */
export type AsyncFunction = <T = any, R = unknown>(...args: T[]) => Promise<R>

declare const emptyObjectSymbol: unique symbol

/**
 * Represents a strictly empty plain object, the `{}` value.
 *
 * Because just using `{}` cit can be anything except `null` and `undefined`.
 * This means that you cannot use `{}` to represent an empty plain object
 *
 * @see {@link https://stackoverflow.com/questions/47339869/typescript-empty-object-and-any-difference/52193484#52193484}.
 */
export type EmptyObject = { [emptyObjectSymbol]?: never }

/**
 * Convience object types for when dealing with dynamic or unknown types
 * (or you just want to get through the day without pulling your hair out).
 */
export type AnyRecord = { [key: PropertyKey]: any }
export type AnyFunction = (...args: any[]) => any
export type AnyArray = any[]

/**
 * @description
 * Represents a type that is an object with string keys and values of same type.
 *
 * @example
 * ```ts
 * const obj: Dict<number> = { a: 1, b: 2 }
 * ```
 */
export type Dict<T = any> = Record<string, T>

/** Useful, non-exported type used in the Vue source code. */
export type Booleanish = boolean | 'true' | 'false'

export type FalsyType = false | null | undefined
export type EmptyType = false | null | undefined | '' | 0 | EmptyObject | []

/**
 * @description
 * Represents a type that is an instance of a class or object constructor.
 *
 * @example
 * ```ts
 * interface IUser { name: string }
 * class User implements IUser { name: string }
 * const user = new User()
 * const registerUser = async (user: Type<IUser>) => {
 *   const registered = await fetch('/api/users', { method: 'POST', body: JSON.stringify(user) })
 *     .catch(error => throw new Error('Failed to register user'))
 *   return registered
 * }
 * const registeredUser = registerUser(user)
 * ```
 */
export interface Type<T> extends Function {
  new (...args: any[]): T
}
export const Type = Function
export const isType = (v: any): v is Type<any> => typeof v === 'function'

export type Constructor<T> = new (...args: any[]) => T

/**
 * @description
 * Represents an abstract class of `C`, which cannot be applied to an actual class
 * because it is not instantiable.
 */
export interface AbstractType<C> extends Function {
  prototype: C
}

export type Intersection<U> = (U extends any ? (k: U) => void : never) extends (k: infer I) => void
  ? I
  : never

export type Variadic<T> = T[] | [Array<T>]

/**
 * Revision of Type-Fest's `FixedLengthArray` utility that doesn't strip mutable methods in order to prevent the unavoidable
 * gymnastics required for convincing your code that, no, it really, truly is an array.
 *
 * Create a type that represents an array of the given type and length. The array's length and the `Array` prototype methods
 * that manipulate its length are excluded in the resulting type.
 *
 * Please participate in [this issue](https://github.com/microsoft/TypeScript/issues/26223) if you want to have a similar
 * type built into TypeScript.
 *
 * Use-cases:
 * - Declaring fixed-length tuples or arrays with a large number of items.
 * - Creating a range union (for example, `0 | 1 | 2 | 3 | 4` from the keys of such a type) without having to resort
 *   to recursive types.
 * - Creating an array of coordinates with a static length, for example, length of 3 for a 3D vector.
 *
 * Note: This type does not prevent out-of-bounds access. Prefer `ReadonlyTuple` unless you need mutability.
 *
 * @example
 * ```
 * import type { AsTuple } from '@contrastagent/utils';
 *
 * type RGBA = AsTuple<number, 4>
 *
 * const seasonColor: RGBA = [84, 174, 255, 0.8]
 *
 * const springColor: RGBA = [57, 211, 83]
 * //=> error TS2322: Type number[] is not assignable to type 'RGBA'
 * ```
 *
 * @see {@link type-fest#FixedLengthArray}
 */
export type AsTuple<T, Length extends number, ArrayPrototype = [T, ...T[]]> = ArrayPrototype & {
  [index: number]: T
  [Symbol.iterator]: () => IterableIterator<T>
  readonly length: Length
}
