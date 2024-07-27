<template>
  <component
    :is="tag"
    tabindex="-1"
    :aria-posinset="index + 1"
    :aria-setsize="setsize"
    :aria-selected="isFocused"
    @blur.prevent="onBlur"
    @click.prevent="onClick"
    @focus.prevent="onFocus"
    @mouseenter.prevent="onMouseEnter"
    @mousedown.prevent="onMouseDown"
    :class="classes"
  >
    <div v-if="displayAs === 'listitem'" :class="skeinClasses"></div>
    <slot></slot>
  </component>
</template>

<script setup lang="ts">
import { UiAutocompleteOptionProps } from './Autocomplete.types';
import { computed } from 'vue';

const props = withDefaults(
  defineProps<UiAutocompleteOptionProps>(),
  {
    tag: 'li',
    displayAs: 'listitem',
    skeinProps: () => ({} as Partial<DOMRect>)
  }
)

defineOptions({
  name: 'UiAutoCompleteOption',
})

const emit = defineEmits<{
  (e: 'focus', index: number): void
  (e: 'blur', $event: FocusEvent, index: number): void
  (e: 'click', $event: MouseEvent | KeyboardEvent, index: number): void
  (e: 'mouseenter', $event: MouseEvent, index: number): void
  (e: 'mousedown', $event: MouseEvent, index: number): void
}>()

const isFocused = computed(() => props.index === props.focused)
const isHovered = computed(() => props.index === props.hovered)
const isSelected = computed(() => props.index === props.selected)

const classes = computed(() => {
  return {
    'relative block': true,
  }

})
const skeinClasses = computed(() => {
  return {
    'absolute top-0 left-0 w-0 h-0 bg-violet-500 opacity-0 z-10': true,
    'focus:opacity-30': isFocused.value,
    'hover:opacity-20': isHovered.value,
    'opacity-100 text-white': isSelected.value,
  }
})

const onFocus = () => {
  emit('focus', props.index)
}

const onBlur = (event: FocusEvent) => {
  emit('blur', event, props.index)
}

const onMouseEnter = (event: MouseEvent) => {
  emit('mouseenter', event, props.index)
}

const onClick = (
  event: MouseEvent | KeyboardEvent,
) => {
  emit('click', event, props.index)
}

const onMouseDown = (event: MouseEvent) => {
  // Safari triggers focusOut before click, but if you
  // preventDefault on mouseDown, you can stop that from happening.
  // If this is removed, clicking on an option in Safari will trigger
  // `onOptionBlur`, which closes the menu, and the click will
  // trigger on the element underneath instead.
  // See: http://stackoverflow.com/questions/7621711/how-to-prevent-blur-running-when-clicking-a-link-in-jquery
  event.preventDefault()

  emit('mousedown', event, props.index)
}
</script>

<style scoped>

</style>