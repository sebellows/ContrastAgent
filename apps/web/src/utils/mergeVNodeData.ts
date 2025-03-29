import { camelCase, getKeys, isNil, isPlainObject, variadic } from '@color-agent/utils'

export type VNodeData = Record<string, unknown>

const pattern = {
  styleProp: /:(.*)/,
  styleList: /;(?![^(]*\))/g,
} as const

function parseStyle(style: string) {
  const styleMap: Record<string, any> = {}

  for (const s of style.split(pattern.styleList)) {
    let [key, val] = s.split(pattern.styleProp)
    key = key.trim()

    if (!key) continue

    // May be undefined if the `key: value` pair is incomplete.
    styleMap[camelCase(key)] = val.trim()
  }

  return styleMap
}

function mergeClasses(mergeTarget: VNodeData, classProps: string | string[] | Record<string, boolean> = {}) {
  const classes = {} as Record<string, boolean>
  const targetClasses = mergeTarget['class'] ?? {}

  ;[targetClasses, classProps].forEach(klassProp => {
    if (Array.isArray(klassProp) || typeof klassProp === 'string') {
      const classObj = variadic(klassProp).reduce((obj, klass) => {
        obj[klass] = true
      }, {} as Record<string, boolean>)

      Object.assign(classes, classObj)
    } else {
      Object.assign(classes, klassProp)
    }
  })

  mergeTarget['class'] = classes
}

function isTrue(value: unknown) {
  return `${value}` === 'true'
}

function mergeStyles(mergeTarget: VNodeData, styleProps: string | string[] | Record<string, any>) {
  const styles = variadic(mergeTarget?.style ?? [])
  const thisStyle = variadic(styleProps)

  for (const style of thisStyle) {
    if (Array.isArray(style) || typeof style === 'string') {
      thisStyle.push(...variadic(style))
    } else if (isPlainObject(style)) {
      for (const [key, value] of Object.entries(style)) {
        if (isTrue(value)) {
          thisStyle.push(key)
        }
      }
    }
  }

  mergeTarget['style'] = styles.concat(thisStyle)
}

/**
 * vue-functional-data-merge 3.1.0
 * @author Alex Regan
 * @see {@link https://github.com/alexsasharegan/vue-functional-data-merge}
 *
 * Intelligently merges data for createElement.
 * Merges args left to right, preferring the right argument.
 *
 * @return {VNodeData}
 */
function mergeData(...vNodeData: VNodeData[]): VNodeData
function mergeData(...args: any[]): VNodeData {
  const mergeTarget: VNodeData = {}
  let i: number = args.length

  // Allow for variadic argument length.
  while (i--) {
    // Iterate through the data properties and execute merge strategies
    // Object.keys eliminates need for hasOwnProperty call
    const props = args[i]
    for (const prop of getKeys(props)) {
      const value = props[prop]

      if (value == null) continue

      switch (prop) {
        case "class": {
          // Repackaging in an array allows Vue runtime
          // to merge class/style bindings regardless of type.
          mergeClasses(mergeTarget, value)
          continue
        }

        // merge style by concatenating arrays
        case "style": {
          mergeStyles(mergeTarget, value)
          continue
        }

        case "id":
        case "key":
        case "ref":
        case "keepAlive": {
          if (isNil(mergeTarget[prop])) {
            mergeTarget[prop] = value
          }
          continue
        }
      }

      if (prop.startsWith("on") && prop !== "on") {
        // Object, the properties of which to merge via array merge strategy (array concatenation).
        // Callback merge strategy merges callbacks to the beginning of the array,
        // so that the last defined callback will be invoked first.
        // This is done since to mimic how Object.assign merging
        // uses the last given value to assign.

        // Concat function to array of functions if callback present.
        if (mergeTarget[prop] && !Array.isArray(mergeTarget[prop])) {
          // Insert current iteration data in beginning of merged array.
          mergeTarget[prop] = [mergeTarget[prop], value]
          continue
        }

        const targetValue = mergeTarget[prop]

        // The `else` condition falls through to a simple assignment.
        if (Array.isArray(targetValue)) {
          targetValue.push(...variadic(value))

          continue
        }
      }

      mergeTarget[prop] = value
    }
  }

  return mergeTarget
}

export { mergeData }
