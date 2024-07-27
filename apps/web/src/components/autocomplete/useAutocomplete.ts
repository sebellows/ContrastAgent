import { AnyRecord, isFunction } from '@contrastagent/utils'
import { computed, reactive, Ref, toRefs, watch } from 'vue'
import { FormControlEvents } from '../forms/Form.types'
import { isIOS } from '../../utils/device'
import { getTargetValue } from '../../utils/dom'
import { isPrintableKeyCode } from '../../utils/interaction'
import TextField from '../forms/TextField.vue'
import { useId } from '../../composables/useId'
import { UiAutocompleteProps, AutocompleteState } from './Autocomplete.types'

export const useAutocomplete = <T extends AnyRecord>(
  props: UiAutocompleteProps<T>,
  emit: FormControlEvents,
  textFieldRef: Ref<typeof TextField | null>,
) => {
  const state = reactive<AutocompleteState<T>>({
    ariaHint: false,
    focused: null,
    hovered: null,
    hasValidOption: false,
    menuIsOpen: false,
    results: [],
    query: '',
    selected: null,
  })

  const data = computed(() => props.datum ?? [])

  const inputRef = computed(() => textFieldRef.value?.$el?.querySelector?.('input'))

  const id = useId(props.id)

  const _minLength = computed(() => props.minLength ?? 2)
  const directInputValue = computed(() => inputRef.value?.value)

  watch(directInputValue, newValue => {
    const hasChanged = state.query !== newValue

    if (hasChanged) {
      onInput({ target: inputRef.value } as unknown as KeyboardEvent)
    }
  })

  const updateState = (newState: Partial<AutocompleteState<T>>) => {
    for (const key in newState) {
      state[key] = newState[key]
    }
  }

  const format = (value: string, diacritics?: boolean) => {
    value = String(value).toLowerCase()

    return diacritics
      ? value
          .normalize('NFD')
          .replace(/[\u0300-\u036f]/g, '')
          .normalize('NFC')
      : value
  }

  /**
   * Formats an option into a query string
   */
  const formatOption = (result: T) => {
    if (!result) return ''

    const optionKey = props.optionKey

    if (isFunction(props?.formatLabel)) {
      return props.formatLabel(result)
    }

    console.log('formatOption: ', result, optionKey)
    const option = `${result[optionKey]}`

    return option
  }

  const onUpdateModelValue = (value: string) => {
    const hasChanged = state.query !== value
    if (hasChanged) {
      updateState({ query: value, ariaHint: value.length === 0 })
    }

    emit('update:modelValue', { query: value, results: state.results })
  }

  const options = computed(() => {
    if (!state.results.length) {
      return [] as string[]
    }

    return state.results.map(item => formatOption(item as T))
  })

  const optionIsFocused = computed(() => state.focused !== -1 && state.focused !== null)
  const assistiveHintID = computed(() => `${id.value}__assistiveHint`)
  const ariaProps = computed(() => ({
    'aria-describedby': state.ariaHint ? assistiveHintID : null,
    'aria-expanded': Boolean(state.menuIsOpen).toString(),
    'aria-activedescendant': optionIsFocused.value ? `${id.value}__option--${state.focused}` : null,
    'aria-owns': `${id.value}__listbox`,
    'aria-autocomplete': canAutoSelect.value ? 'both' : 'list',
  }))

  const menuAttributes = {
    id: `${id.value}__listbox`,
    role: 'listbox',
    onMouseLeave: () => {
      updateState({ hovered: null })
    },
  }

  const canAutoSelect = computed(() => {
    // iOS native select does not support autoselect with highlight markup
    return !isIOS() && !!props.autoselect
  })

  const hintValue = computed(() => {
    const { hasValidOption, results, query, selected = 0 } = state
    if (!results.length || !results[selected!]?.[props.optionKey]) return ''

    const currentSelectedOptionText = formatOption(results[selected ?? 0] as T)
    return hasValidOption && canAutoSelect.value
      ? query + currentSelectedOptionText.substring(query.length)
      : ''
  })

  const onInput = (event: KeyboardEvent) => {
    const queryValue = getTargetValue(event)

    const categoryKeys = props.dataKeys?.length
      ? props.dataKeys.filter(key => key !== props.optionKey)
      : []

    if (queryValue.length >= _minLength.value) {
      const currentResults = (state.results?.length ? state.results : data.value) as T[]
      let results = [] as T[]

      if (props.search && !props.dataKeys?.length) {
        results = props.search(queryValue, currentResults as T[])
      } else if (categoryKeys?.length) {
        results = currentResults.filter(item =>
          categoryKeys.some(
            key =>
              typeof item[key] === 'string' && format(item[key]).startsWith(format(queryValue)),
          ),
        ) as T[]
      } else {
        results = currentResults.filter(entry =>
          entry[props.optionKey].toLowerCase().startsWith(queryValue.toLowerCase()),
        )
      }

      const shouldShowMenu = !state.menuIsOpen && results.length > 0
      const shouldCloseMenu = state.menuIsOpen && results.length === 0
      const menuIsOpen = shouldShowMenu
        ? { menuIsOpen: true }
        : shouldCloseMenu
          ? { menuIsOpen: false }
          : {}

      updateState({
        ...menuIsOpen,
        results,
        hasValidOption: false,
        selected: canAutoSelect.value ? 0 : -1,
      })
    } else {
      updateState({ menuIsOpen: false, results: [] })
    }

    emit('input', queryValue)
  }

  const onComponentBlur = (newState: Partial<AutocompleteState<T>>) => {
    const { results, query, selected } = state
    let newQuery = ''
    if (props.confirmOnBlur && isFunction(props.onConfirm) && selected !== null) {
      newQuery = newState.query || query
      const activeOption = results[selected] as T
      props.onConfirm(activeOption)
    } else {
      newQuery = query
    }

    updateState({
      focused: null,
      menuIsOpen: newState.menuIsOpen || false,
      query: newQuery,
      selected: null,
      hasValidOption: queryMatchesOption(newQuery, results as T[]),
    })
  }

  const queryMatchesOption = (q: string, opts: T[]) => {
    return opts.map(entry => formatOption(entry).toLowerCase()).indexOf(q.toLowerCase()) !== -1
  }

  const onBlur = (event: FocusEvent) => {
    const { focused, menuIsOpen, results, query, selected } = state
    const focusingAnOption = focused !== -1
    if (!focusingAnOption && selected !== null) {
      const keepMenuOpen = menuIsOpen && isIOS()
      const newQuery = isIOS() ? query : formatOption(results[selected] as T)
      onComponentBlur({
        menuIsOpen: keepMenuOpen,
        query: newQuery,
      })
    }

    emit('blur', event)
  }

  const onInputClick = (event: any) => {
    onInput(event)

    emit('click', event)
  }

  const onClear = (event: Event) => {
    updateState({
      focused: null,
      hovered: null,
      menuIsOpen: false,
      query: '',
      results: [],
      selected: null,
      hasValidOption: false,
    })

    emit('clear', event)
  }

  const onFocus = (event: FocusEvent) => {
    const { query, hasValidOption, menuIsOpen, results } = state
    const shouldReopenMenu =
      !hasValidOption && query.length >= _minLength.value && results.length > 0

    if (shouldReopenMenu) {
      updateState({
        focused: -1,
        menuIsOpen: shouldReopenMenu ?? menuIsOpen,
        selected: -1,
      })
    } else {
      updateState({ focused: -1 })
    }

    emit('focus', event)
  }

  const onOptionFocus = (index: number) => {
    updateState({
      focused: index,
      hovered: null,
      selected: index,
    })
  }

  const onOptionBlur = (event: FocusEvent, index: number) => {
    const { focused, menuIsOpen, results, selected } = state
    const focusingOutsideComponent = event.relatedTarget === null
    const focusingInput = event.relatedTarget === inputRef.value
    const focusingAnotherOption = focused !== index && focused !== -1
    const blurComponent =
      (!focusingAnotherOption && focusingOutsideComponent) ||
      !(focusingAnotherOption || focusingInput)

    if (blurComponent) {
      const keepMenuOpen = menuIsOpen && isIOS()
      onComponentBlur({
        menuIsOpen: keepMenuOpen,
        query: formatOption(results[selected ?? index] as T),
      })
    }
  }

  const onOptionMouseEnter = (event: Event, index: number) => {
    // iOS Safari prevents click event if mouseenter adds hover background colour
    // See: https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/HandlingEvents/HandlingEvents.html#//apple_ref/doc/uid/TP40006511-SW4
    if (!isIOS()) {
      updateState({
        hovered: index,
      })
    }
  }

  const onOptionClick = (event: MouseEvent | KeyboardEvent, index: number | null) => {
    if (index == null) return

    const { results } = state

    const selectedOption = results[index] as T
    const newQuery = formatOption(selectedOption)

    props?.onConfirm?.(selectedOption)

    updateState({
      focused: -1,
      hovered: null,
      menuIsOpen: false,
      query: newQuery,
      selected: -1,
      hasValidOption: true,
    })
    // forceUpdate()
    emit('click', event)
  }

  const onOptionMouseDown = (event: MouseEvent) => {
    // Safari triggers focusOut before click, but if you
    // preventDefault on mouseDown, you can stop that from happening.
    // If this is removed, clicking on an option in Safari will trigger
    // `onOptionBlur`, which closes the menu, and the click will
    // trigger on the element underneath instead.
    // See: http://stackoverflow.com/questions/7621711/how-to-prevent-blur-running-when-clicking-a-link-in-jquery
    event.preventDefault()
  }

  const _onArrowUp = (event: KeyboardEvent) => {
    const { menuIsOpen, selected } = state
    const isNotAtTop = selected !== -1
    const allowMoveUp = isNotAtTop && menuIsOpen
    if (allowMoveUp && selected != null) {
      onOptionFocus(selected - 1)
    }

    emit('keydown.arrow-up', event)
  }

  const _onArrowDown = (event: KeyboardEvent) => {
    if (!state.menuIsOpen) {
      updateState({
        menuIsOpen: true,
        selected: 0,
        focused: 0,
        hovered: null,
      })

      return
    }

    const { menuIsOpen, results, selected } = state

    if (selected === null || (selected === -1 && results.length > 0)) {
      updateState({
        focused: 0,
        selected: 0,
        hovered: null,
      })
    }

    const isNotAtBottom = selected !== options.value.length - 1
    const allowMoveDown = isNotAtBottom && menuIsOpen
    // console.log('onArrowDown: ', allowMoveDown, selected, menuIsOpen)

    if (allowMoveDown && selected != null) {
      onOptionFocus(selected + 1)
    }

    emit('keydown.arrow-down', event)
  }

  const onSpace = (event: KeyboardEvent) => {
    if (state.menuIsOpen === false && state.query === '') {
      updateState({
        menuIsOpen: true,
      })
    }

    const focusIsOnOption = state.focused !== -1

    if (focusIsOnOption) {
      event.preventDefault()
      onOptionClick(event, state.focused)
    }

    emit('keydown.space', event)
  }

  const _onEnter = (event: KeyboardEvent) => {
    if (!state.menuIsOpen || state.selected == null) return

    const hasSelectedOption = state.selected >= 0

    if (hasSelectedOption) {
      onOptionClick(event, state.selected)
    }

    emit('keydown.enter', event)
  }

  const _onPrintableKey = (event: KeyboardEvent) => {
    const inputElement = inputRef.value
    const eventIsOnInput = event.target === inputElement

    if (!eventIsOnInput) {
      inputRef.value?.focus?.()
    }

    emit('keydown', event)
  }

  const onKeydown = (event: KeyboardEvent) => {
    switch (event.code) {
      case 'Enter':
        _onEnter(event)

        break
      case 'Escape':
        onComponentBlur({ query: state.query })

        break
      case 'Space':
        onSpace(event)

        break
      case 'ArrowUp':
        _onArrowUp(event)

        break
      case 'ArrowDown':
        _onArrowDown(event)

        break
      default:
        if (isPrintableKeyCode(event.code)) {
          _onPrintableKey(event)
        }
    }
  }

  const resetOptions = () => {
    updateState({
      focused: null,
      hovered: null,
      menuIsOpen: false,
      results: [],
      selected: null,
    })
  }

  return {
    ariaProps,
    id,
    data,
    hintValue,
    ...toRefs(state),
    menuAttributes,
    _minLength,
    options,
    formatOption,
    onInput,
    onBlur,
    onClear,
    onFocus,
    onOptionBlur,
    onOptionClick,
    onOptionFocus,
    onOptionMouseDown,
    onOptionMouseEnter,
    onInputClick,
    onKeydown,
    onUpdateModelValue,
    resetOptions,
  }
}
