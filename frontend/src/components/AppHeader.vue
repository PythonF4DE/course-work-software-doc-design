<script setup>
import { useRouter } from "vue-router"
import { useAuthStore } from "../stores/auth"


const router = useRouter()
const authStore = useAuthStore()


function logout() {
  authStore.logout()
  router.push("/")
}
</script>


<template>
  <header class="header">
    <div class="container header-content">
      <RouterLink
        to="/"
        class="logo">
        MedBook
      </RouterLink>

      <RouterLink to="/doctors">
        Лікарі
      </RouterLink>

      <nav class="navigation">
        <RouterLink to="/">
          Головна
        </RouterLink>

        <template
          v-if="!authStore.isAuthenticated">
          <RouterLink to="/login">
            Ввійти
          </RouterLink>

          <RouterLink
            to="/register"
            class="button button-small">
            Реєстрація
          </RouterLink>
        </template>

        <template v-else>
          <RouterLink
            v-if="
              authStore.user?.role === 'patient'
            "
            to="/dashboard"
          >
            Кабінет
          </RouterLink>


          <RouterLink
            v-if="
              authStore.user?.role === 'doctor'
            "
            to="/doctor"
          >
            Кабінет лікаря
          </RouterLink>


          <RouterLink
            v-if="
              authStore.user?.role === 'admin'
            "
            to="/admin"
          >
            Адмін-панель
          </RouterLink>

          <button
            class="link-button"
            @click="logout">
            Вийти
          </button>
        </template>
      </nav>
    </div>
  </header>
</template>