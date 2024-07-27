<template>
  <div :class="{ 'ui-card-section w-full': true, ...layoutClasses, ...textClasses, ...spacingClasses }">
    <slot></slot>
  </div>
</template>

<script setup lang="ts">
import { defaultComponentStyleProps, useTwStyles } from '../../composables/useTwStyles';
import { UiCardSectionProps } from './Card.types';

defineOptions({
  name: 'UiCardSection',
})

const props = withDefaults(
  defineProps<UiCardSectionProps>(),
  {
    ...defaultComponentStyleProps,
    horizontal: false,
    pad: undefined,
    padX: true,
    padY: 'sm',
  },
)

const { layoutClasses, textClasses, spacingClasses } = useTwStyles(props)
</script>
