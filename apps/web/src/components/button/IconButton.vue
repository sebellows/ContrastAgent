<template>
  <component :is="compTag" :class="{ ...btnColorClasses, ...btnSizeClasses, ...radiusClasses, ...shadowClasses }" v-bind="bindings" @click="event => emit('click', event)">
    <ui-icon :name="props.icon" :class="sizeClass" />
  </component>
</template>

<script setup lang="ts">
import { computed, useAttrs } from 'vue';
import { RouterLink } from 'vue-router';
import { UiIcon } from '../icons'
import { UiIconButtonProps } from './Button.types';
import { useTwStyles } from '../../composables/useTwStyles';
import { useSize } from '../../composables/useSize';

defineOptions({
  name: 'UiIconButton'
})

const props = withDefaults(defineProps<UiIconButtonProps>(), {
  block: false,
  flat: true,
  nowrap: false,
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

const btnColorClasses = computed(() => {
  if (!props.flat) return variantClasses.value

  return {
    'text-primary-500': props.variant === 'primary',
    'text-secondary-500': props.variant === 'secondary',
    'text-accent-500': props.variant === 'accent',
    'text-neutral-500': props.variant === 'neutral',
    'text-negative-500': props.variant === 'negative',
    'text-positive-500': props.variant === 'positive',
    'text-warning-500': props.variant === 'warning',
    'text-slate-800': props.variant === 'light',
    'text-slate-200': props.variant === 'dark',
  }
})

const btnSizeClasses = computed(() => {
  return {
    'text-xs px-2 py-1': !props.icon?.length && size.value === 'xs',
    'text-sm px-2 py-1': !props.icon?.length && size.value === 'sm',
    'text-md px-3 py-2': !props.icon?.length && size.value === 'md',
    'text-lg px-4 py-3': !props.icon?.length && size.value === 'lg',
    'text-xl px-5 py-4': !props.icon?.length && size.value === 'xl',
    'w-full': props.block,
    'whitespace-nowrap': props.nowrap,
    'inline-flex items-center justify-center': !!props.icon?.length,
    'w-5 h-5 p-0': !!props.icon?.length && size.value === 'xs',
    'w-6 h-6 p-0': !!props.icon?.length && size.value === 'sm',
    'w-8 h-8 p-0': !!props.icon?.length && size.value === 'md',
    'w-12 h-12 p-0': !!props.icon?.length && size.value === 'lg',
    'w-16 h-16 p-0': !!props.icon?.length && size.value === 'xl',
  }

})
</script>
