<template>
  <UiFormControl
    ref="formControlRef"
    :label="label"
    :labelAlign="labelAlign"
    :labelPlacement="labelPlacement"
    :radius="radius"
    :shadow="shadow"
    :hint="hint"
    :errorMessage="errorMessage"
    :class="stateClasses"
    @focus="onFocus"
    @blur="onBlur"
    @change="onChange"
    @keydown="onKeydown"
    @click="onClick"
  >
    <div v-if="$slots.prefix" class="pointer-events-none absolute inset-y-0 left-0 pl-3 flex items-center">
      <slot name="prefix"></slot>
    </div>

    <div class="select-container relative flex flex-nowrap">
      <input v-if="useInput" :id="nativeInputId" class="sr-only" readonly :tabindex="0" role="combobox" aria-readonly="false" aria-autocomplete="none" />

      <select
        :id="id"
        :name="name ?? id"
        :class="formFieldClasses"
        :style="inlineInputPadding"
        v-bind="{ ...selectAttrs }"
      >
        <option v-if="currentOptions.length" v-for="option of currentOptions" :key="option.value" :value="option.value" :disabled="isDisabled">
          <slot name="option">{{ option.label }}</slot>
        </option>
      </select>
    </div>

    <div v-if="$slots.suffix" class="pointer-events-none absolute inset-y-0 left-auto right-0 pr-3 flex items-center">
      <slot name="suffix"></slot>
    </div>
  </UiFormControl>
</template>

<script setup lang="ts" generic="T extends Option | string | AnyRecord | null | undefined">
import { AnyRecord, isFunction, isNil, isPlainObject } from '@contrastagent/utils';
import { v4 as uuid } from 'uuid';
import { computed, ref } from 'vue';
import { FormControlEvents, Option, SelectFieldProps } from './Form.types';
import { useFormField } from './useFormField';
import UiFormControl from './FormControl.vue'

const props = withDefaults(defineProps<SelectFieldProps<T>>(), {
  radius: 'md',
  size: 'md',
  id: `select-${uuid()}`,
})

defineOptions({
  inheritAttrs: false,
})

const emit = defineEmits<FormControlEvents<typeof props.modelValue>>()

const formField = useFormField(props, emit)
const {
  formFieldClasses,
  inlineInputPadding,
  isDisabled,
  stateClasses,
  onFocus,
  onBlur,
  onChange,
  onKeydown,
  onClick,
} = formField

const formControlRef = ref<null | typeof UiFormControl>(null)

const nativeInputId = computed(() => `select-input-${uuid()}`)

const currentOptions = computed(() => {
  const options = props.options
  if (!options?.length) return []

  return options
    .filter(option => !isNil(option))
    .map((option) => {
      if (isPlainObject(option) && option.label && option.value) {
        return option
      }
      if (option && props.optionLabel && props.optionValue) {
        const optionItem: Option = {}
        if (isFunction(props.optionLabel)) {
          optionItem.label = props.optionLabel(option)
        } else {
          optionItem.label = option[props.optionLabel]
        }
        if (isFunction(props.optionValue)) {
          optionItem.value = props.optionValue(option)
        } else {
          optionItem.value = option[props.optionValue]
        }

        return optionItem
      }

      if (typeof option === 'string') {
        return { label: option, value: option }
      }

      return { label: '', value: '' }
    })

})

const selectAttrs = computed(() => {
  const {
    options,
    optionLabel,
    optionValue,
    selected,
    radius: _radius,
    size: _size,
    shadow: _shadow,
    status: _status,
    modelValue,
    useInput,
    inputClass,
    inputStyle,
    ...rest
  } = props

  const attrs = Object.fromEntries(Object.entries(rest).filter(([key, value]) => !isNil(value)))

  return attrs
})
</script>

<style scoped>

</style>