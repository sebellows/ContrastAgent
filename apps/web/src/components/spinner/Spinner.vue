<template>
  <svg :class="{ 'ui-spinner': true, 'ui-spinner-anim': true, ...colorClasses, ...sizeClasses }" :viewBox="viewBox">
    <circle class="path" :cx="rawSize" :cy="rawSize" :r="radius" fill="none" :stroke="color" :stroke-width="strokeWidth" stroke-linecap="round" />
  </svg>
</template>

<script setup lang="ts">
import { ThemeSizeAlias } from '@contrastagent/theme';
import { useSpinner } from './useSpinner'
import { UiSpinnerProps } from './Spinner.types'

defineOptions({
  name: 'UiSpinner',
})

const props = withDefaults(
  defineProps<UiSpinnerProps>(),
  {
    size: 'xl' as ThemeSizeAlias,
    color: 'primary',
    thickness: 5,
  },
)

const {
  colorClasses,
  radius,
  rawSize,
  sizeClasses,
  strokeWidth,
  viewBox,
} = useSpinner(props)

</script>

<style>
.ui-spinner {
  vertical-align: middle;
}
.ui-spinner-anim {
  animation: ui-spin 2s linear infinite;
  transform-origin: center center;
}
.ui-spinner-anim .path {
  stroke-dasharray: 1, 200;
  stroke-dashoffset: 0;
  animation: ui-dash 1.5s ease-in-out infinite;
}

@keyframes ui-spin {
  0% {
    transform: rotate3d(0, 0, 1, 0deg);
  }
  50% {
    transform: rotate3d(0, 0, 1, 180deg);
  }
  75% {
    transform: rotate3d(0, 0, 1, 270deg);
  }
  100% {
    transform: rotate3d(0, 0, 1, 359deg);
  }
}

@keyframes ui-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35px;
  }
  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124px;
  }
}
</style>