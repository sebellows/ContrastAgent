import { computed } from 'vue'
import { getRawTwSize, TwSizeSuffix, ThemeSizeAlias } from '@contrastagent/theme'
import { UnknownRecord } from 'type-fest'

export interface SizeProps {
  size?: ThemeSizeAlias | TwSizeSuffix | number | string
  width?: ThemeSizeAlias | TwSizeSuffix | number | string
  height?: ThemeSizeAlias | TwSizeSuffix | number | string
}

export const useSize = <P extends SizeProps>(props: P, attrs: UnknownRecord = {}) => {
  const defaultSize = attrs?.defaultSize ?? 'md'

  const size = computed(() => props?.size ?? defaultSize)

  const sizeClass = computed(() => {
    return {
      'size-4': props.size === 'xs',
      'size-5': props.size === 'sm',
      'size-6': props.size === 'md',
      'size-7': props.size === 'lg',
      'size-8': props.size === 'xl',
    }
  })

  const widthClass = computed(() => {
    return {
      'w-4': props.width === 'xs',
      'w-5': props.width === 'sm',
      'w-6': props.width === 'md',
      'w-7': props.width === 'lg',
      'w-8': props.width === 'xl',
    }
  })

  const heightClass = computed(() => {
    return {
      'h-4': props.height === 'xs',
      'h-5': props.height === 'sm',
      'h-6': props.height === 'md',
      'h-7': props.height === 'lg',
      'h-8': props.height === 'xl',
    }
  })

  const rawDimensions = computed(() => {
    const dims = { width: 0, height: 0 }

    // Because Tailwind can't dynamically infer class names at runtime,
    // we need to parse the class attribute to determine the size.
    if (attrs?.class) {
      const matchingClasses = (attrs.class as string)
        ?.split(' ')
        .filter(c => ['size-', 'w-', 'h-'].some(p => c.startsWith(p)))

      if (matchingClasses?.length) {
        matchingClasses.forEach(c => {
          // i.e., 'size-xs' -> ['size', 'xs']
          const [prefix] = c.split('-')

          if (prefix === 'size') {
            dims.width = dims.height = getRawTwSize(c)
          } else if (prefix in dims) {
            dims[prefix] = getRawTwSize(c)
          }
        })

        return dims
      }
    } else {
      if (props.size) {
        dims.width = dims.height = getRawTwSize(`size.${props.size ?? defaultSize}`)
      }

      if (props.width) {
        const width = getRawTwSize(`w.${props.width}`)
        dims.width = width
      }

      if (props.height) {
        const height = getRawTwSize(`h.${props.height}`)
        dims.height = height
      }
    }

    return dims
  })

  return {
    size,
    sizeClass,
    rawDimensions,
    widthClass,
    heightClass,
  }
}
