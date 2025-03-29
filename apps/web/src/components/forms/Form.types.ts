import { AnyRecord } from '@contrastagent/utils'
import {
  EmitsOptions,
  InputHTMLAttributes,
  OptionHTMLAttributes,
  SelectHTMLAttributes,
  TextareaHTMLAttributes,
} from 'vue'
import { ElementAttrs } from '../../types/dom'
import { ThemeSizeAlias } from '@contrastagent/theme'

export type FormValidationStatus = 'success' | 'error' | 'warning'

export type ValidateOn = 'change' | 'blur' | 'input' | 'submit'

export type FormControlEvents<Payload = any> = {
  (event: 'update:modelValue', payload: any): void
  (event: 'focus', payload: FocusEvent): void
  (event: 'blur', payload: FocusEvent): void
  (event: 'paste', payload: ClipboardEvent): void
  (event: 'input', payload: Payload | KeyboardEvent): void
  (event: 'change', payload: Event): void
  (event: 'clear', payload: Event): void
  (event: 'keydown', payload: KeyboardEvent): void
  (event: `keydown.${string}`, payload: KeyboardEvent): void
  (event: 'keyup', payload: KeyboardEvent): void
  (event: 'reset', payload: Event): void
  (event: 'click', payload: MouseEvent | KeyboardEvent): void
}
export type FormControlEmits<Payload = any> = EmitsOptions & FormControlEvents<Payload>

type LabelAlign = 'left' | 'center' | 'right'
type LabelPlacement = 'left' | 'top'

export interface FormControlProps<TValue = any> {
  clearable?: boolean
  disabled?: boolean
  errorMessage?: string
  hint?: string
  id?: string
  label?: string
  labelAlign?: LabelAlign
  labelPlacement?: LabelPlacement
  name?: string
  radius?: ThemeSizeAlias
  readonly?: boolean
  required?: boolean
  shadow?: boolean
  size?: ThemeSizeAlias
  status?: FormValidationStatus
  type?: string
  modelValue?: TValue | null
  loading?: boolean
  value?: TValue
  formatValue?: (value: TValue) => string
}

export type FormElementType = 'input' | 'select' | 'textarea'

export type FormControlFieldAttributes<T extends 'input' | 'select' | 'textarea'> =
  T extends 'select'
    ? SelectHTMLAttributes
    : T extends 'textarea'
      ? TextareaHTMLAttributes
      : InputHTMLAttributes

export type FormControlFieldElement<T extends 'input' | 'select' | 'textarea'> = T extends 'input'
  ? HTMLInputElement
  : T extends 'select'
    ? HTMLSelectElement
    : T extends 'textarea'
      ? HTMLTextAreaElement
      : never

export interface FormControlField<Tag extends 'input' | 'select' | 'textarea', TValue = any>
  extends FormControlProps<TValue>,
    /** @vue-ignore */
    ElementAttrs<Tag> {
  placeholder?: string
  clearBtnProps?: AnyRecord
}

export type Option = OptionHTMLAttributes

export interface SelectFieldProps<T extends Option | string | AnyRecord | null | undefined>
  extends FormControlField<'select'> {
  id?: string
  name?: string
  options?: T[]
  optionLabel?: string | ((value: T) => string)
  optionValue?: string | ((value: T) => string)
  selected?: boolean

  dropdownIcon?: string

  useInput?: boolean
  inputClass?: string | string[] | Record<string, boolean>
  inputStyle?: string | string[] | Record<string, boolean>
}

export type FormControlState = {
  pristine: boolean | null
  dirty: boolean | null
  touched: boolean | null
  untouched: boolean | null
  valid: boolean | null
  invalid: boolean | null
}
