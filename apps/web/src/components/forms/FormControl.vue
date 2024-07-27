<template>
  <div :class="formControlClasses">
    <slot name="label">
      <label :for="id" :class="labelClasses">{{ label }}</label>
    </slot>

    <div :class="formControlWrapperClasses">
      <slot><!-- default slot for form input --></slot>
    </div>

    <slot name="bottom-text">
      <p v-if="hint || errorMessage" :class="bottomTextClasses">
        {{ errorMessage || hint }}
      </p>
    </slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { FormControlProps } from './Form.types';

defineOptions({
  name: 'UiFormControl',
})

const props = withDefaults(defineProps<FormControlProps>(), {
  labelAlign: 'left',
  labelPosition: 'top',
  radius: 'md',
  shadow: true,
})

const formControlClasses = computed(() => ({
  'form-control': true,
  block: true,
}))

const formControlWrapperClasses = computed(() => ({
  'form-control-wrapper': true,
  relative: true,
  'text-gray-900 dark:text-gray-100': true,
  'shadow-sm': !!props.shadow,
  [`rounded-${props.radius}`]: !!props.radius,
}))

const labelClasses = computed(() => ({
  'block': props.labelPosition === 'top',
  'text-sm font-medium leading-6 text-gray-900 dark:text-gray-100': true,
  'mb-2': props.labelPosition === 'top',
  [`text-${props.labelAlign}`]: true,
}))

const bottomTextClasses = computed(() => ({
  'text-xs leading-5 text-gray-600 dark:text-gray-300': !!props.hint && !props.errorMessage,
  'text-xs leading-5 text-red-400': !!props.errorMessage,
}))

</script>

<style scoped>

</style>