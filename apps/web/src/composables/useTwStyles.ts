import { computed } from 'vue'

export interface ComponentStyleProps {
  bordered?: boolean | null

  // Whether to remove background, border, and shadow
  flat?: boolean | null

  // Whether to remove background and keep border
  outlined?: boolean | null

  // Whether to add focus and hover styles
  interactive?: boolean | null

  fontFamily?: 'sans' | 'serif' | 'mono' | 'display'

  fontSize?:
    | 'xs'
    | 'sm'
    | 'base'
    | 'lg'
    | 'xl'
    | '2xl'
    | '3xl'
    | '4xl'
    | '5xl'
    | '6xl'
    | '7xl'
    | '8xl'
    | '9xl'

  fontWeight?:
    | 'thin'
    | 'extralight'
    | 'light'
    | 'normal'
    | 'medium'
    | 'semibold'
    | 'bold'
    | 'extrabold'
    | 'black'

  horizontal?: boolean | null

  italic?: boolean | null

  // Use a lighter variant color
  faded?: boolean | null

  // Use a darker variant color
  darken?: boolean | null

  lineClamp?: '1' | '2' | '3' | '4' | '5' | '6' | 'none'

  lineHeight?:
    | '1'
    | '2'
    | '3'
    | '4'
    | '5'
    | '6'
    | '7'
    | '8'
    | '9'
    | '10'
    | 'none'
    | 'tight'
    | 'snug'
    | 'normal'
    | 'relaxed'
    | 'loose'

  margin?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  marginLeft?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  marginRight?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  marginTop?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  marginBottom?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  marginX?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  marginY?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'

  pad?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  padLeft?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  padRight?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  padTop?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  padBottom?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  padX?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  padY?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl'

  radius?: boolean | null | 'none' | 'DEFAULT' | 'xs' | 'sm' | 'md' | 'lg' | 'full' | 'none'

  shadow?:
    | boolean
    | null
    | 'none'
    | 'DEFAULT'
    | 'xs'
    | 'sm'
    | 'md'
    | 'lg'
    | 'xl'
    | '2xl'
    | 'inner'
    | 'none'

  textAlign?: 'left' | 'center' | 'right'

  textTransform?: 'uppercase' | 'lowercase' | 'capitalize' | 'normal'

  // Background and/or border color variant
  variant?: string

  whitespace?: 'normal' | 'nowrap' | 'pre' | 'pre-line' | 'pre-wrap'
}

export const defaultComponentStyleProps: ComponentStyleProps = {
  bordered: null,
  flat: null,
  outlined: null,
  interactive: null,
  horizontal: null,
  italic: null,
  faded: null,
  darken: null,
  margin: null,
  marginLeft: null,
  marginRight: null,
  marginTop: null,
  marginBottom: null,
  marginX: null,
  marginY: null,
  pad: null,
  padLeft: null,
  padRight: null,
  padTop: null,
  padBottom: null,
  padX: null,
  padY: null,
  radius: null,
  shadow: null,
}

const isTrue = (value: unknown) => `${value}` === 'true'
const isFalse = (value: unknown) => `${value}` === 'false'

export const useTwStyles = <TProps extends ComponentStyleProps>(props: TProps) => {
  const layoutClasses = computed(() => {
    return {
      'flex flex-col': isFalse(props.horizontal),
      'flex flex-row': isTrue(props.horizontal),
    }
  })

  const variantClasses = computed(() => {
    const classes = {} as Record<string, boolean>

    if (!props.variant) return classes

    if (!props.flat && !props.outlined) {
      const useDefault = !props.darken && !props.faded

      Object.assign(classes, {
        'bg-primary-500 text-white hover:bg-primary-400': useDefault && props.variant === 'primary',
        'bg-secondary-500 text-white': useDefault && props.variant === 'secondary',
        'bg-accent-500 text-white': useDefault && props.variant === 'accent',
        'bg-negative-500 text-white': useDefault && props.variant === 'negative',
        'bg-warning-500 text-white': useDefault && props.variant === 'warning',
        'bg-positive-500 text-white': useDefault && props.variant === 'positive',
        'bg-neutral-500 text-white': useDefault && props.variant === 'neutral',
        'bg-white text-slate-900': useDefault && props.variant === 'light',
        'bg-slate-900 text-slate-100': useDefault && props.variant === 'dark',

        // Faded variants
        'bg-primary-200 text-primary-600': props.faded && props.variant === 'primary',
        'bg-secondary-200 text-secondary-600': props.faded && props.variant === 'secondary',
        'bg-accent-200 text-accent-600': props.faded && props.variant === 'accent',
        'bg-negative-200 text-negative-600': props.faded && props.variant === 'negative',
        'bg-warning-200 text-warning-600': props.faded && props.variant === 'warning',
        'bg-positive-200 text-positive-600': props.faded && props.variant === 'positive',
        'bg-neutral-200 text-neutral-600': props.faded && props.variant === 'neutral',
        'bg-slate-100 text-slate-800': props.faded && props.variant === 'light',
        'bg-slate-800 text-slate-200': props.faded && props.variant === 'dark',

        // Darkened variants
        'bg-primary-900 text-white hover:bg-primary-800':
          props.darken && props.variant === 'primary',
        'bg-secondary-900 text-white': props.darken && props.variant === 'secondary',
        'bg-accent-900 text-white': props.darken && props.variant === 'accent',
        'bg-negative-900 text-white': props.darken && props.variant === 'negative',
        'bg-warning-900 text-white': props.darken && props.variant === 'warning',
        'bg-positive-900 text-white': props.darken && props.variant === 'positive',
        'bg-neutral-900 text-white': props.darken && props.variant === 'neutral',
        'bg-slate-200 text-slate-950': props.darken && props.variant === 'light',
        'bg-slate-950 text-slate-100': props.darken && props.variant === 'dark',
      })
    }

    if (props.outlined) {
      Object.assign(classes, {
        'border-primary-500 text-primary-500': props.variant === 'primary',
        'border-secondary-500 text-secondary-500': props.variant === 'secondary',
        'border-accent-500 text-accent-500': props.variant === 'accent',
        'border-negative-500 text-negative-500': props.variant === 'negative',
        'border-warning-500 text-warning-500': props.variant === 'warning',
        'border-positive-500 text-positive-500': props.variant === 'positive',
        'border-neutral-500 text-neutral-500': props.variant === 'neutral',
        'border-light-500 text-light-500': props.variant === 'light',
        'border-dark-500 text-dark-500': props.variant === 'dark',
      })
    }

    if (!props.flat && (props.bordered || props.outlined)) {
      Object.assign(classes, {
        border: props.bordered === true,
        'border-primary-500': props.variant === 'primary',
        'border-secondary-500': props.variant === 'secondary',
        'border-accent-500': props.variant === 'accent',
        'border-negative-500': props.variant === 'negative',
        'border-warning-500': props.variant === 'warning',
        'border-positive-500': props.variant === 'positive',
        'border-neutral-500': props.variant === 'neutral',
        'border-black/20': props.variant === 'light',
        'border-white/20': props.variant === 'dark',
        'border-black/10': !props.variant,
      })
    }

    if (props.interactive) {
      Object.assign(classes, {
        'focus:opacity-90 hover:opacity-90 disabled:opacity-70': true,
        'focus:ring-2 focus:ring-primary-500': props.variant === 'primary',
        'focus:ring-2 focus:ring-secondary-500': props.variant === 'secondary',
        'focus:ring-2 focus:ring-accent-500': props.variant === 'accent',
        'focus:ring-2 focus:ring-negative-500': props.variant === 'negative',
        'focus:ring-2 focus:ring-warning-500': props.variant === 'warning',
        'focus:ring-2 focus:ring-positive-500': props.variant === 'positive',
        'focus:ring-2 focus:ring-neutral-500': props.variant === 'neutral',
        'focus:ring-2 focus:ring-light-500': props.variant === 'light',
        'focus:ring-2 focus:ring-dark-500': props.variant === 'dark',
        'focus:ring-opacity-50': !props.flat,
        'focus:ring-opacity-100': props.flat,
        'focus:outline-none': true,
        'focus:ring-2': true,
        'focus:ring-offset-2': true,
        'focus:ring-offset-primary-500': props.variant === 'primary',
        'focus:ring-offset-secondary-500': props.variant === 'secondary',
        'focus:ring-offset-accent-500': props.variant === 'accent',
        'focus:ring-offset-negative-500': props.variant === 'negative',
        'focus:ring-offset-warning-500': props.variant === 'warning',
        'focus:ring-offset-positive-500': props.variant === 'positive',
        'focus:ring-offset-neutral-500': props.variant === 'neutral',
        'focus:ring-offset-light-500': props.variant === 'light',
        'focus:ring-offset-dark-500': props.variant === 'dark',
      })
    }

    return classes
  })

  const radiusClasses = computed(() => {
    if (props.flat) return {}

    return {
      rounded: isTrue(props.radius),
      'rounded-xs': props.radius === 'xs',
      'rounded-sm': props.radius === 'sm',
      'rounded-md': props.radius === 'md',
      'rounded-lg': props.radius === 'lg',
      'rounded-full': props.radius === 'full',
      'rounded-none': isFalse(props.radius) || props.radius === 'none',
    }
  })

  const shadowClasses = computed(() => {
    if (props.flat) return {}

    return {
      'shadow-xs': props.shadow === 'sm',
      'shadow-sm': props.shadow === 'sm',
      'shadow-md': isTrue(props.shadow) || props.shadow === 'md',
      'shadow-lg': props.shadow === 'lg',
      'shadow-xl': props.shadow === 'sm',
      'shadow-2xl': props.shadow === '2xl',
      'shadow-inner': props.shadow === 'inner',
      'shadow-none': isFalse(props.shadow) || props.shadow === 'none',
    }
  })

  const spacingClasses = computed(() => {
    return {
      // Margin
      'm-0': props.margin === 'none',
      'm-1': props.margin === 'xs', // 4px
      'm-2': props.margin === 'sm', // 8px
      'm-3': props.margin === 'md', // 12px
      'm-4': isTrue(props.margin) || props.margin === 'DEFAULT', // 16px
      'm-5': props.margin === 'lg', // 20px
      'm-6': props.margin === 'xl', // 24px
      'm-8': props.margin === '2xl', // 32px
      'mt-0': props.marginTop === 'none',
      'mt-1': props.marginTop === 'xs', // 4px
      'mt-2': props.marginTop === 'sm', // 8px
      'mt-3': props.marginTop === 'md', // 12px
      'mt-4': isTrue(props.marginTop) || props.marginTop === 'DEFAULT', // 16px
      'mt-5': props.marginTop === 'lg', // 20px
      'mt-6': props.marginTop === 'xl', // 24px
      'mt-8': props.marginTop === '2xl', // 32px
      'mr-0': props.marginRight === 'none',
      'mr-1': props.marginRight === 'xs', // 4px
      'mr-2': props.marginRight === 'sm', // 8px
      'mr-3': props.marginRight === 'md', // 12px
      'mr-4': isTrue(props.marginRight) || props.marginRight === 'DEFAULT', // 16px
      'mr-5': props.marginRight === 'lg', // 20px
      'mr-6': props.marginRight === 'xl', // 24px
      'mr-8': props.marginRight === '2xl', // 32px
      'mb-0': props.marginBottom === 'none',
      'mb-1': props.marginBottom === 'xs', // 4px
      'mb-2': props.marginBottom === 'sm', // 8px
      'mb-3': props.marginBottom === 'md', // 12px
      'mb-4': isTrue(props.marginBottom) || props.marginBottom === 'DEFAULT', // 16px
      'mb-5': props.marginBottom === 'lg', // 20px
      'mb-6': props.marginBottom === 'xl', // 24px
      'mb-8': props.marginBottom === '2xl', // 32px
      'ml-0': props.marginLeft === 'none',
      'ml-1': props.marginLeft === 'xs', // 4px
      'ml-2': props.marginLeft === 'sm', // 8px
      'ml-3': props.marginLeft === 'md', // 12px
      'ml-4': isTrue(props.marginLeft) || props.marginLeft === 'DEFAULT', // 16px
      'ml-5': props.marginLeft === 'lg', // 20px
      'ml-6': props.marginLeft === 'xl', // 24px
      'ml-8': props.marginLeft === '2xl', // 32px
      'mx-0': props.marginX === 'none',
      'mx-1': props.marginX === 'xs', // 4px
      'mx-2': props.marginX === 'sm', // 8px
      'mx-3': props.marginX === 'md', // 12px
      'mx-4': isTrue(props.marginX) || props.marginX === 'DEFAULT', // 16px
      'mx-5': props.marginX === 'lg', // 20px
      'mx-6': props.marginX === 'xl', // 24px
      'mx-8': props.marginX === '2xl', // 32px
      'my-0': props.marginY === 'none',
      'my-1': props.marginY === 'xs', // 4px
      'my-2': props.marginY === 'sm', // 8px
      'my-3': props.marginY === 'md', // 12px
      'my-4': isTrue(props.marginY) || props.marginY === 'DEFAULT', // 16px
      'my-5': props.marginY === 'lg', // 20px
      'my-6': props.marginY === 'xl', // 24px
      'my-8': props.marginY === '2xl',

      // Padding
      'p-0': props.pad === 'none',
      'p-1': props.pad === 'xs', // 4px
      'p-2': props.pad === 'sm', // 8px
      'p-3': props.pad === 'md', // 12px
      'p-4': isTrue(props.pad) || props.pad === 'DEFAULT', // 16px
      'p-5': props.pad === 'lg', // 20px
      'p-6': props.pad === 'xl', // 24px
      'p-8': props.pad === '2xl', // 32px
      'pt-0': props.padTop === 'none',
      'pt-1': props.padTop === 'xs', // 4px
      'pt-2': props.padTop === 'sm', // 8px
      'pt-3': props.padTop === 'md', // 12px
      'pt-4': isTrue(props.padTop) || props.padTop === 'DEFAULT', // 16px
      'pt-5': props.padTop === 'lg', // 20px
      'pt-6': props.padTop === 'xl', // 24px
      'pt-8': props.padTop === '2xl', // 32px
      'pr-0': props.padRight === 'none',
      'pr-1': props.padRight === 'xs', // 4px
      'pr-2': props.padRight === 'sm', // 8px
      'pr-3': props.padRight === 'md', // 12px
      'pr-4': isTrue(props.padRight) || props.padRight === 'DEFAULT', // 16px
      'pr-5': props.padRight === 'lg', // 20px
      'pr-6': props.padRight === 'xl', // 24px
      'pr-8': props.padRight === '2xl', // 32px
      'pb-0': props.padBottom === 'none',
      'pb-1': props.padBottom === 'xs', // 4px
      'pb-2': props.padBottom === 'sm', // 8px
      'pb-3': props.padBottom === 'md', // 12px
      'pb-4': isTrue(props.padBottom) || props.padBottom === 'DEFAULT', // 16px
      'pb-5': props.padBottom === 'lg', // 20px
      'pb-6': props.padBottom === 'xl', // 24px
      'pb-8': props.padBottom === '2xl', // 32px
      'pl-0': props.padLeft === 'none',
      'pl-1': props.padLeft === 'xs', // 4px
      'pl-2': props.padLeft === 'sm', // 8px
      'pl-3': props.padLeft === 'md', // 12px
      'pl-4': isTrue(props.padLeft) || props.padLeft === 'DEFAULT', // 16px
      'pl-5': props.padLeft === 'lg', // 20px
      'pl-6': props.padLeft === 'xl', // 24px
      'pl-8': props.padLeft === '2xl', // 32px
      'px-0': props.padX === 'none',
      'px-1': props.padX === 'xs', // 4px
      'px-2': props.padX === 'sm', // 8px
      'px-3': props.padX === 'md', // 12px
      'px-4': isTrue(props.padX) || props.padX === 'DEFAULT', // 16px
      'px-5': props.padX === 'lg', // 20px
      'px-6': props.padX === 'xl', // 24px
      'px-8': props.padX === '2xl', // 32px
      'py-0': props.padY === 'none',
      'py-1': props.padY === 'xs', // 4px
      'py-2': props.padY === 'sm', // 8px
      'py-3': props.padY === 'md', // 12px
      'py-4': isTrue(props.padY) || props.padY === 'DEFAULT', // 16px
      'py-5': props.padY === 'lg', // 20px
      'py-6': props.padY === 'xl', // 24px
      'py-8': props.padY === '2xl',
    }
  })

  const textClasses = computed(() => {
    return {
      // Font family
      'font-sans': props.fontFamily === 'sans',
      'font-serif': props.fontFamily === 'serif',
      'font-mono': props.fontFamily === 'mono',
      'font-display': props.fontFamily === 'display',

      // Font style
      italic: isTrue(props.italic),
      'not-italic': isFalse(props.italic),

      // Font weight
      'font-thin': props.fontWeight === 'thin',
      'font-extralight': props.fontWeight === 'extralight',
      'font-light': props.fontWeight === 'light',
      'font-normal': props.fontWeight === 'normal',
      'font-medium': props.fontWeight === 'medium',
      'font-semibold': props.fontWeight === 'semibold',
      'font-bold': props.fontWeight === 'bold',
      'font-extrabold': props.fontWeight === 'extrabold',
      'font-black': props.fontWeight === 'black',

      // Line clamp
      truncate: props.lineClamp === 'none',
      'line-clamp-1': props.lineClamp === '1',
      'line-clamp-2': props.lineClamp === '2',
      'line-clamp-3': props.lineClamp === '3',
      'line-clamp-4': props.lineClamp === '4',
      'line-clamp-5': props.lineClamp === '5',
      'line-clamp-6': props.lineClamp === '6',

      // Line height
      'leading-none': props.lineHeight === 'none',
      'leading-tight': props.lineHeight === 'tight',
      'leading-snug': props.lineHeight === 'snug',
      'leading-normal': props.lineHeight === 'normal',
      'leading-relaxed': props.lineHeight === 'relaxed',
      'leading-loose': props.lineHeight === 'loose',
      'leading-1': props.lineHeight === '1',
      'leading-2': props.lineHeight === '2',
      'leading-3': props.lineHeight === '3',
      'leading-4': props.lineHeight === '4',
      'leading-5': props.lineHeight === '5',
      'leading-6': props.lineHeight === '6',
      'leading-7': props.lineHeight === '7',
      'leading-8': props.lineHeight === '8',
      'leading-9': props.lineHeight === '9',
      'leading-10': props.lineHeight === '10',

      // Text alignment
      'text-left': props.textAlign === 'left',
      'text-center': props.textAlign === 'center',
      'text-right': props.textAlign === 'right',

      // Text color
      'text-slate-900 dark:text-slate-100': !props.variant || props.variant === 'light',
      'text-white': props.variant && props.variant !== 'light',
      'text-xs': props.fontSize === 'xs',
      'text-sm': props.fontSize === 'sm',
      'text-base': props.fontSize === 'base',
      'text-lg': props.fontSize === 'lg',
      'text-xl': props.fontSize === 'xl',
      'text-2xl': props.fontSize === '2xl',
      'text-3xl': props.fontSize === '3xl',
      'text-4xl': props.fontSize === '4xl',
      'text-5xl': props.fontSize === '5xl',
      'text-6xl': props.fontSize === '6xl',
      'text-7xl': props.fontSize === '7xl',
      'text-8xl': props.fontSize === '8xl',
      'text-9xl': props.fontSize === '9xl',

      // Text transform
      uppercase: props.textTransform === 'uppercase',
      lowercase: props.textTransform === 'lowercase',
      capitalize: props.textTransform === 'capitalize',
      'normal-case': props.textTransform === 'normal',

      // Whitespace
      'whitespace-normal': props.whitespace === 'normal',
      'whitespace-nowrap': props.whitespace === 'nowrap',
      'whitespace-pre': props.whitespace === 'pre',
      'whitespace-pre-line': props.whitespace === 'pre-line',
      'whitespace-pre-wrap': props.whitespace === 'pre-wrap',
    }
  })

  return {
    layoutClasses,
    radiusClasses,
    shadowClasses,
    spacingClasses,
    textClasses,
    variantClasses,
  }
}
