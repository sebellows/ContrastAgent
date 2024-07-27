<template>
  <div class="ui-autocomplete relative w-full h-full" ref="autocompleteRef" v-if="data.length > 0">
    <UiAutocompleteStatus
      :id="id"
      :debounceInMs="debounceInMs"
      :length="options.length"
      :queryLength="query.length"
      :minLength="minLength"
      :selectedOption="options[selected ?? -1]"
      :selectedOptionIndex="selected"
      :hasValidOption="hasValidOption"
      :isInFocus="focused !== null"
      :lessThanMinStatus="lessThanMinStatus"
      :noResultsStatus="noResultsStatus"
      :optionSelectedStatus="optionSelectedStatus"
      :totalResultsStatus="totalResultsStatus"
    />

    <span v-if="hintValue">
      <TextField
        :class="['ui-autocomplete--hint absolute', ...textInputClasses]"
        readonly
        tabIndex='-1'
        v-model="hintValue"
      />
    </span>

    <TextField
      ref="inputRef"
      type="text"
      :id="id"
      :name="name"
      role="combobox"
      :model-value="query"
      autocomplete="off"
      v-bind="ariaProps"
      :clearable="clearable"
      :clear-btn-props="{ class: 'text-neutral-500 size-sm'}"
      :class="textInputClasses"
      @update:model-value="onUpdateModelValue"
      @click="onInputClick"
      @input="onInput"
      @focus="onFocus"
      @blur="onBlur"
      @keydown.passive="onKeydown"
    />

    <template v-if="displayAs !== 'grid'">
      <transition-group
        ref="listboxRef"
        name="slide-in"
        tag="ol"
        popover="manual"
        v-bind="menuAttributes"
        class="m-auto rounded-md border border-gray-100 shadow-md overflow-auto bg-white dark:bg-gray-700"
        :style="popoverStyles"
      >
        <UiAutocompleteOption
          v-for="(result, i) in results"
          :key="result.id"
          :index="i"
          :setsize="results.length"
          :class="{
            'flex items-center justify-between p-2 hover:bg-gray-100 dark:hover:bg-gray-800': true,
            'bg-gray-100 dark:bg-gray-800': i === hovered,
            'bg-gray-200 dark:bg-gray-700': i === focused,
          }"
          :hovered="hovered"
          :focused="focused"
          :selected="selected"
          :props="result"
          @blur.prevent="onOptionBlur"
          @click.prevent="onOptionClick"
          @focus.prevent="onOptionFocus"
          @mouseenter.prevent="onOptionMouseEnter"
          @mousedown.prevent="onOptionMouseDown"
        >
          <slot name="option" :props="result"></slot>
        </UiAutocompleteOption>

        <li v-if="showNoOptionsFound" className="autocomplete-option autocomplete-option--no-results">{{ noResultsStatusMessage }}</li>
      </transition-group>
    </template>

    <span id="ui-autocomplete--assistive-hint" style="display: none;">{{ assistiveHintText }}</span>
  </div>
</template>

<script setup lang="ts" generic="T extends AnyRecord">
import { computed, defineEmits, onMounted, PropType, Ref, ref, watch } from 'vue'
import { AnyRecord } from '@contrastagent/utils';
import TextField from '../forms/TextField.vue'
import { FormControlEvents } from '../forms/Form.types';
import { UiAutocompleteProps } from './Autocomplete.types';
import { useAutocomplete } from './useAutocomplete';
import UiAutocompleteStatus from './AutocompleteStatus.vue'
import UiAutocompleteOption from './AutoCompleteOption.vue'

const props = withDefaults(defineProps<UiAutocompleteProps<T>>(), {
  'aria-autocomplete': 'both',
  'aria-controls': 'listbox',
  'aria-haspopup': true,
  'aria-expanded': false,
  'aria-owns': 'listbox',
  displayAs: 'list',
  minLength: 2,
  debounceInMs: 1000,
  textInputClasses: () => ({} as Record<string, boolean>),
  lessThanMinStatus: (minLength: number) => `Please enter at least ${minLength} characters`,
  noResultsStatus: () => 'No results found',
  optionSelectedStatus: (option: string, length: number, index: number) => `${option} (${index + 1} of ${length})`,
  totalResultsStatus: (length: number, selectedOption: string) => `${length} results found. ${selectedOption}`,
})

defineOptions({
  name: 'ui-autocomplete',
  inheritAttrs: false,
})

const emit = defineEmits<FormControlEvents<typeof props.modelValue>>()

const inputRef = ref<typeof TextField | null>()
const autocompleteRef = ref<null | HTMLElement>(null)
const listboxRef = ref<null | HTMLElement>(null)

const {
  ariaProps,
  data,
  id,
  focused,
  hasValidOption,
  hintValue,
  hovered,
  menuAttributes,
  menuIsOpen,
  options,
  query,
  results,
  selected,
  onInput,
  onBlur,
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
} = useAutocomplete<T>(props, emit, inputRef as Ref<typeof TextField | null>)

const noResultsStatusMessage = computed(() => props.noResultsStatus())
const assistiveHintText = computed(() => props?.assitiveHintMessage?.() ?? (() => 'When autocomplete results are available use up and down arrows to review and enter to select.  Touch device users, explore by touch or with swipe gestures.'))

const popoverStyles = computed(() => {
  const inputEl = inputRef.value?.input

  if (!inputEl || !menuIsOpen.value) return {}

  const { top, left, height, width } = inputEl.getBoundingClientRect()

  return {
    top: `${top + height + 2}px`,
    left: `${left}px`,
    width: `${width}px`,
  }
})

watch(menuIsOpen, newValue => {
  if (newValue) {
    autocompleteRef.value?.setAttribute('aria-expanded', 'true')
    listboxRef.value?.['$el']?.showPopover()
  } else {
    listboxRef.value?.['$el']?.hidePopover()
    autocompleteRef.value?.setAttribute('aria-expanded', 'false')
  }
})

onMounted(() => {
  globalThis.addEventListener('click', (e: MouseEvent) => {
    if (autocompleteRef.value && !autocompleteRef.value.contains(e.target as Node)) {
      resetOptions()
    }
  })
})

defineExpose({
  results,
})
</script>

<style scoped>
[popover] {
  position: fixed;
  inset: 0;
  width: fit-content;
  height: fit-content;
  overflow: auto;
  max-height: 50vh;
}
:popover-open {
  position: absolute;
  inset: unset;
  margin: 0;
}

.slide-in-move {
  transition: opacity 0.5s linear, transform 0.5s ease-in-out;
}

.slide-in-leave-active {
  transition: opacity 0.4s linear, transform 0.4s cubic-bezier(0.5, 0, 0.7, 0.4); /* cubic-bezier(.7,0,.7,1); */
  transition-delay: calc(0.1s * (var(--total) - var(--i)));
}

.slide-in-enter-active {
  transition: opacity 0.5s linear, transform 0.5s cubic-bezier(0.2, 0.5, 0.1, 1);
  transition-delay: calc(0.1s * var(--i));
}

.slide-in-enter,
.slide-in-leave-to {
  opacity: 0;
}

.slide-in-enter {
  transform: translateX(-1em);
}
.slide-in-leave-to {
  transform: translateX(1em);
}
</style>
