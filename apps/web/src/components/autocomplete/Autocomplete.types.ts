import { AnyRecord } from '@contrastagent/utils/*'
import { FormControlField } from '../forms/Form.types'
import { ComponentPublicInstance } from 'vue'

interface AutocompleteStatusBaseProps {
  debounceInMs: number
  id: string
  minLength: number
  lessThanMinStatus: (minLength: number) => string
  noResultsStatus: () => string
  optionSelectedStatus: (option: string, length: number, index: number) => string
  totalResultsStatus: (length: number, selectedOption: string) => string
}

export interface UiAutocompleteProps<T extends AnyRecord>
  extends FormControlField<'input', string> {
  name?: string
  autoselect?: boolean
  datum: T[]
  dataKeys?: string[]
  formatLabel?: (option: T) => string
  optionKey: string
  role?: string
  showNoOptionsFound?: boolean
  confirmOnBlur?: boolean
  onConfirm?: (value: T) => void
  assitiveHintMessage?: () => string
  search?: (query: string, options: T[]) => T[]
  displayAs?: 'list' | 'grid'

  textInputClasses?: string | string[] | Record<string, boolean>

  // status props
  debounceInMs?: number
  id?: string
  minLength?: number
  lessThanMinStatus?: (minLength: number) => string
  noResultsStatus?: () => string
  optionSelectedStatus?: (option: string, length: number, index: number) => string
  totalResultsStatus?: (length: number, selectedOption: string) => string
}

export type AutocompleteState<T extends AnyRecord> = {
  ariaHint: boolean
  focused: number | null
  hovered: number | null
  hasValidOption: boolean
  menuIsOpen: boolean
  results: T[]
  query: string
  selected: number | null
}

export interface AutocompleteStatusProps extends AutocompleteStatusBaseProps {
  hasValidOption: boolean
  isInFocus: boolean
  length: number
  queryLength: number
  selectedOption?: string
  selectedOptionIndex: number | null
}

export interface UiAutocompleteOptionProps {
  index: number
  setsize: number
  tag?: string | ComponentPublicInstance
  focused: number | null
  hovered: number | null
  selected: number | null
  displayAs?: 'listitem' | 'griditem'
}
