<script setup>
import { onMounted } from "vue"

import AppHeader from "./components/AppHeader.vue"
import { useAuthStore } from "./stores/auth"


const authStore = useAuthStore()


onMounted(() => {
  authStore.loadCurrentUser()
})
</script>


<template>
  <div class="app">
    <AppHeader />

    <main>
      <RouterView />
    </main>
  </div>
</template>