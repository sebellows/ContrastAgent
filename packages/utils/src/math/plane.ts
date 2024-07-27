import { isNumber, isPlainObject } from '../assert'
import { Bounds, BoundsList } from './math.types'

export class Plane implements Bounds {
  private _x1 = 0
  get x1(): number {
    return this._x1
  }
  set x1(value: number) {
    if (isNumber(value) && this._x1 !== value) {
      this._x1 = value
    }
  }

  private _y1 = 0
  get y1(): number {
    return this._y1
  }
  set y1(value: number) {
    if (isNumber(value) && this._y1 !== value) {
      this._y1 = value
    }
  }

  private _x2 = 0
  get x2(): number {
    return this._x2
  }
  set x2(value: number) {
    if (isNumber(value) && this._x2 !== value) {
      this._x2 = value
    }
  }

  private _y2 = 0
  get y2(): number {
    return this._y2
  }
  set y2(value: number) {
    if (isNumber(value) && this._y2 !== value) {
      this._y2 = value
    }
  }

  constructor(coords: Bounds | BoundsList) {
    let [x1, y1, x2, y2] = [0, 0, 0, 0]

    if (isPlainObject<Plane>(coords)) {
      x1 = coords.x1
      y1 = coords.y1
      x2 = coords.x2
      y2 = coords.y2
    } else if (Array.isArray(coords)) {
      ;[x1, y1, x2, y2] = coords
    }

    this.x1 = x1
    this.y1 = y1
    this.x2 = x2
    this.y2 = y2
  }

  static isPlane(value: any): value is Plane {
    return value instanceof Plane
  }
}
