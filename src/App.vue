<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
  name: "App",
  created() {
    document.title = this.$t("kitchenOrderingSystem")
    document
      .querySelector('meta[name="description"]')
      ?.setAttribute(
        "content",
        `${this.$t("kitchenOrderingSystem")} , ${this.$t("kitchen")}`
      )
  },
})
</script>
