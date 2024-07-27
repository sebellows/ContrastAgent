<template>
  <div class="sr-only">
    <div
      v-if="!silenced && debounced && bump"
      :id="`${id}__status--A`"
      role='status'
      aria-atomic='true'
      aria-live='polite'
    >
      {{ statusMessage }}
    </div>
    <div
       v-if="!silenced && debounced && !bump"
      :id="`${id}__status--B`"
      role='status'
      aria-atomic='true'
      aria-live='polite'
    >
      {{ statusMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { debounce } from '@contrastagent/utils'
import { computed, ref, onMounted, watch } from 'vue'
import { AutocompleteStatusProps } from './Autocomplete.types';

defineOptions({
  name: 'UiAutocompleteStatus',
})

const props = defineProps<AutocompleteStatusProps>()

const debounceStatusUpdate = ref<ReturnType<typeof debounce> | null>(null)

const bump = ref(false)
const debounced = ref(false)
const silenced = ref(false)

const statusMessage = ref<string | null>(null)

const length = computed(() => props.length)
const currentQueryLength = computed(() => props.queryLength)
const queryTooShort = computed(() => props.queryLength < props.minLength)
const noResults = computed(() => length.value === 0)

const contentSelectedOption = computed(() => props.selectedOption && props.selectedOptionIndex != null
  ? props.optionSelectedStatus(props.selectedOption, length.value, props.selectedOptionIndex)
  : ''
)

watch(queryTooShort, newValue => {
  if (newValue) {
    statusMessage.value = props.lessThanMinStatus(props.minLength)
  }
})

watch(noResults, newValue => {
  if (newValue) {
    statusMessage.value = props.noResultsStatus()
  }
})

watch(length, (newValue, oldValue) => {
  if (newValue !== oldValue) {
    statusMessage.value = props.totalResultsStatus(newValue, contentSelectedOption.value)
  }
})

watch(currentQueryLength, newValue => {
  if (newValue < props.minLength) {
    debounced.value = false
  }
})

onMounted(() => {
  debounceStatusUpdate.value = debounce(() => {
    if (!debounced.value) {
      const shouldSilence = !props.isInFocus || props.hasValidOption

      bump.value = !bump.value
      debounced.value = true
      silenced.value = shouldSilence
    }
  }, { timeoutMs: props.debounceInMs })
})
</script>