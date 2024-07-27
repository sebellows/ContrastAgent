import { computed, ref, unref, useSlots } from 'vue'
import {
  // FormControlField,
  FormControlFieldElement,
  FormControlProps,
  FormControlState,
  FormElementType,
} from './Form.types'

export interface DOMEvent<T extends EventTarget = EventTarget> extends Event {
  readonly target: T | null
}

export const getTargetValue = <TType extends FormElementType>(evt: Event) => {
  const target = evt.target as FormControlFieldElement<TType>

  return target.value
}

export const useFormField = <TType extends FormElementType, TValue = any>(
  props: FormControlProps<TValue>, // FormControlField<TType, TValue>,
  emit: ReturnType<typeof defineEmits>,
) => {
  const slots = useSlots()

  /**
   * Form field state flags.
   */
  const state = ref<FormControlState>({
    pristine: true, // has not been interacted with
    dirty: false, // has been interacted with
    touched: false, // has been blurred
    untouched: true, // has not been blurred
    valid: null,
    invalid: null,
  })

  const type = computed(() => props.type ?? 'text')

  const isDisabled = computed(() => Boolean(props?.['disabled'] ?? props.readonly))

  const stateClasses = computed(() => {
    return {
      'is-pristine': state.value.pristine === true,
      'is-dirty': state.value.dirty === true,
      'is-touched': state.value.touched === true,
      'is-untouched': state.value.untouched === true,
      'is-valid': state.value.valid === true,
      'is-invalid': state.value.invalid === true,
      'is-disabled': isDisabled.value,
      'is-readonly': props.readonly,
    }
  })

  const borderClasses = computed(() => {
    const currentState = unref(state)

    return {
      'border-green-300 focus:ring-green-500 focus:border-green-500': currentState.valid === true,
      'border-red-300 focus:ring-red-500 focus:border-red-500': currentState.invalid === true,
      'border-gray-300 focus:ring-primary-500 focus:border-primary-500':
        currentState.valid !== true && currentState.invalid !== true,
    }
  })

  const sizeClasses = computed(() => {
    return {
      'pl-0': !!slots.prefix,
      'pr-0': !!slots.suffix,
      'pl-1.5': props.size === 'sm' && !slots.prefix,
      'pl-2': props.size === 'md' && !slots.prefix,
      'pl-3': props.size === 'lg' && !slots.prefix,
      'pr-1.5': props.size === 'sm' && !slots.suffix,
      'pr-2': props.size === 'md' && !slots.suffix,
      'pr-3': props.size === 'lg' && !slots.suffix,
      'py-0.5 text-sm leading-4': props.size === 'sm',
      'py-1 text-md leading-5': props.size === 'md',
      'py-1.5 text-lg leading-6': props.size === 'lg',
    }
  })

  const inputClasses = computed(() => {
    return {
      'placeholder:text-gray-400 dark:placeholder:text-gray-400': true,
    }
  })

  const formFieldClasses = computed(() => {
    return {
      'block w-full': true,
      ...sizeClasses.value,
      ...borderClasses.value,
      [`rounded-${props.radius}`]: true,
      'text-gray-900 dark:text-gray-100': true,
      ...(!['checkbox', 'radio', 'select'].includes(type.value) ? inputClasses.value : {}),
      'ring-1 ring-inset': true,
      'focus:ring-2 focus:ring-inset focus:ring-indigo-600': true,
    }
  })

  const formControlProps = computed(() => {
    const {
      clearable,
      disabled,
      errorMessage,
      hint,
      id,
      label,
      labelAlign,
      labelPlacement,
      name,
      radius,
      readonly,
      required,
      shadow,
      size,
      status,
      type,
      modelValue,
      loading,
      value,
      formatValue,
      ...rest
    } = props

    return {
      wrapperProps: {
        clearable,
        disabled,
        errorMessage,
        hint,
        id,
        label,
        labelAlign,
        labelPlacement,
        name,
        radius,
        readonly,
        required,
        shadow,
        size,
        status,
        type,
        modelValue,
        loading,
        value,
        formatValue,
      },
      fieldProps: rest,
    }
  })

  const inlineInputPadding = computed(() => {
    const spacing = {} as { prefix?: string; suffix?: string }

    if (slots.prefix) {
      const prefixW = slots.prefix[0].el.clientWidth
      spacing.prefix = `padding-left: ${prefixW}px;`
    }
    if (slots.suffix) {
      const suffixW = slots.suffix[0].el.clientWidth
      spacing.suffix = `padding-right: ${suffixW}px;`
    }

    return spacing
  })

  // const onEvents = computed(() => {
  //   return {
  const onInput = (e: Event) => {
    if (state.value.pristine === true) {
      state.value.dirty = true
      state.value.pristine = false
    }

    // const target = e.target as FormControlFieldElement<TType>
    const value = getTargetValue<TType>(e)
    emit('update:modelValue', value)
    emit('input', e)
  }
  const onFocus = (e: FocusEvent) => {
    state.value.touched = false
    state.value.untouched = true
    emit('focus', e)
  }
  const onBlur = (e: FocusEvent) => {
    state.value.touched = true
    state.value.untouched = false

    emit('blur', e)
  }
  const onClear = (e: Event) => {
    emit('clear', e)
  }
  const onPaste = (e: ClipboardEvent) => {
    emit('paste', e)
  }
  const onChange = (e: Event) => {
    const target = e.target as FormControlFieldElement<TType>
    emit('update:modelValue', target.value)
    emit('change', e)
  }
  const onKeydown = (e: KeyboardEvent) => {
    emit('keydown', e)
  }
  const onClick = (e: MouseEvent) => {
    emit('click', e)
  }
  const onKeyup = (e: KeyboardEvent) => {
    emit('keyup', e)
  }
  // }
  // })

  // provide('onEvents', onEvents)

  return {
    emit,
    formControlProps,
    formFieldClasses,
    inputClasses,
    inlineInputPadding,
    isDisabled,
    slots,
    state,
    stateClasses,
    onInput,
    onFocus,
    onBlur,
    onClear,
    onPaste,
    onChange,
    onKeydown,
    onClick,
    onKeyup,
  }
}
