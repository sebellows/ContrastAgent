<template>
  <div class="bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-200">
    <div class="sr-only" tabindex="0" aria-hidden="true"></div>
    <UiSideRail />
    <div class="ui-container w-sidenav relative pl-24">
      <UiSideNav ref="sidenav" class="fixed" />

      <div class="ui-container px-4" style="margin-left: 320px">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import UiSideRail from './partials/SideRail.vue';
import UiSideNav from './partials/SideNav.vue';
</script>

<style scoped>

</style>