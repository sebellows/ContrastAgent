<template>
  <div :class="{ 'ui-card': true, 'relative': true, ...radiusClasses, ...shadowClasses, ...textClasses, ...spacingClasses, ...variantClasses }">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { defaultComponentStyleProps, useTwStyles } from '../../composables/useTwStyles';
import { UiCardProps } from './Card.types';

defineOptions({
  name: 'UiCard',
})

const props = withDefaults(
  defineProps<UiCardProps>(),
  {
    ...defaultComponentStyleProps,
    variant: 'light',
    radius: 'md',
    shadow: true,
    bordered: true,
  },
)

const { textClasses, radiusClasses, shadowClasses, spacingClasses, variantClasses } = useTwStyles(props)
</script>
