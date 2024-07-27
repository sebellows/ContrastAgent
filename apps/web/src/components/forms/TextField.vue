<template>
  <UiFormControl
    ref="formControlRef"
    :id="id"
    :label="label"
    :labelAlign="labelAlign"
    :labelPlacement="labelPlacement"
    :radius="radius"
    :shadow="shadow"
    :hint="hint"
    :errorMessage="errorMessage"
    :class="stateClasses"
  >
    <div v-if="$slots.prefix" class="pointer-events-none absolute inset-y-0 left-0 pl-3 flex items-center">
      <slot name="prefix"></slot>
    </div>

    <input
      ref="inputRef"
      :type="type"
      :id="id"
      :name="name"
      :class="formFieldClasses"
      :style="inlineInputPadding"
      :disabled="isDisabled"
      :value="modelValue"
      v-bind="{ ...inputAttrs }"
      @input="onInput"
      @focus="onFocus"
      @blur="onBlur"
      @click="onClick"
      @paste="onPaste"
      @change="onChange"
      @keydown="onKeydown"
      @keyup="onKeyup"
    />

    <ui-icon
      v-if="clearable"
      name="close"
      class="absolute inset-y-0 mt-0.5 mr-2 flex items-center cursor-pointer"
      :style="clearBtnStyles"
      v-bind="clearBtnProps"
      @click="onClear"
    />

    <slot name="suffix" class="pointer-events-none absolute inset-y-0 left-auto right-0 pr-3 flex items-center"></slot>
  </UiFormControl>
</template>

<script setup lang="ts">
import { computed, ref, useSlots } from 'vue';
import { FormControlEvents, FormControlField } from './Form.types';
import UiFormControl from './FormControl.vue'
import { useFormField } from './useFormField';
import { useId } from '../../composables/useId';
import UiIcon from '../icons/Icon';

const props = withDefaults(defineProps<FormControlField<'input' | 'textarea'>>(), {
  radius: 'md',
  size: 'md',
})

defineOptions({
  inheritAttrs: true,
})

const slots = useSlots()

const emit = defineEmits<FormControlEvents<typeof props.modelValue>>()

const inputRef = ref<null | HTMLInputElement>(null)

const formField = useFormField(props, emit)
const {
  // formControlProps,
  formFieldClasses,
  inlineInputPadding,
  isDisabled,
  stateClasses,
  onInput,
  onFocus,
  onBlur,
  onClear,
  onPaste,
  onChange,
  onKeydown,
  onClick,
  onKeyup,
} = formField

const formControlRef = ref<null | typeof UiFormControl>(null)

const id = useId(props.id)

const inputAttrs = computed(() => {
  const {
    id: _id,
    clearable,
    disabled,
    errorMessage: _errorMessage,
    hint: _hint,
    label: _label,
    labelAlign: _labelAlign,
    labelPlacement: _labelPlacement,
    name: _name,
    radius: _radius,
    size: _size,
    shadow: _shadow,
    status: _status,
    type = 'text',
    modelValue,
    value: _value,
    ...attrs
  } = props

  return attrs
  // const { readonly, required } = formControlProps.value.wrapperProps

  // return { readonly, required, ...formControlProps.value.fieldProps }
})

const clearBtnStyles = computed(() => {
  if (slots.suffix) {
    const suffixWidth = formControlRef.value?.$refs.suffix?.clientWidth
    return { right: `${suffixWidth}px` }
  }
  return { right: '0' }
})

defineExpose({
  input: inputRef,
})
</script>

<style scoped>

</style>