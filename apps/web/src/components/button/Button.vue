<template>
  <component :is="compTag" :class="{ 'flex flex-nowrap items-center': true, ...variantClasses, ...btnSizeClasses, ...radiusClasses, ...shadowClasses }" v-bind="bindings" @click="event => emit('click', event)">
    <span v-if="props.icon" class="mr-2">
      <ui-icon :name="props.icon" :class="sizeClass" />
    </span>
    <slot>
      <template v-if="label">{{ label }}</template>
    </slot>
  </component>
</template>

<script setup lang="ts">
import { computed, useAttrs } from 'vue';
import { RouterLink } from 'vue-router';
import { UiIcon } from '../icons'
import { UiButtonProps } from './Button.types';
import { useTwStyles } from '../../composables/useTwStyles';
import { useSize } from '../../composables/useSize';

defineOptions({
  name: 'UiButton'
})

const props = withDefaults(defineProps<UiButtonProps>(), {
  block: false,
  flat: true,
  nowrap: true,
  outline: false,
  radius: 'md',
  shadow: true,
  size: 'md',
  tag: 'button',
  variant: 'neutral',
})

const emit = defineEmits<
  (e: 'click', $event: MouseEvent | KeyboardEvent) => void
>()

const attrs = useAttrs()

const { radiusClasses, shadowClasses, variantClasses } = useTwStyles(props)
const { size, sizeClass } = useSize(props)

const compTag = computed(() => props.href ? 'a' : props.to ? RouterLink : props.tag)

const bindings = computed(() => {
  const bounds = {
    'aria-role': props.href || props.to ? 'link' : attrs?.['aria-role'] ?? 'button',
    'role': compTag.value === 'button' ? 'button' : undefined,
  } as Record<string, unknown>

  if (props.href) {
    bounds['href'] = props.href
  }
  if (props.to) {
    bounds['to'] = props.to
  }

  return bounds
})

const btnVariantClasses = computed(() => {
  const classes = {} as Record<string, boolean>

  if (!props.outline) return variantClasses.value

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
  return classes
})

const btnSizeClasses = computed(() => {
  return {
    'text-xs px-2 py-1': size.value === 'xs',
    'text-sm px-2 py-1': size.value === 'sm',
    'text-md px-3 py-2': size.value === 'md',
    'text-lg px-4 py-3': size.value === 'lg',
    'text-xl px-5 py-4': size.value === 'xl',
    'w-full': props.block,
    'flex-nowrap whitespace-nowrap': props.nowrap,
  }

})
</script>
