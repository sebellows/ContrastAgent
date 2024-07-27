<template>
  <component :is="tag" v-bind="bindings">
    <slot>
      <template v-if="label">
        {{ label }}
      </template>
    </slot>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import { UiLinkProps } from './Link.types';

defineOptions({
  name: 'UiLink',
})

const props = defineProps<UiLinkProps>()

const tag = computed(() => {
  if (props.as) return props.as
  if (props.to) return RouterLink

  return 'a';
})

const bindings = computed(() => {
  const binds = {} as UiLinkProps

  if (tag.value === 'a') {
    binds.href = props.href ?? 'javascript:void(0)'
    binds.target = props.target ?? props.href?.startsWith('http') ? '_blank' : '_self'
  }

  if (props.label) binds['aria-label'] = props.label
  binds['aria-current'] = !!props.active

  return binds
})
</script>

<style scoped>

</style>