<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "../stores/auth"


const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const errorMessage = ref("")


const form = reactive({
  email: "",
  password: ""
})


async function submitLogin() {
  errorMessage.value = ""
  loading.value = true

  try {
    await authStore.login(form)

    router.push("/dashboard")

  } catch (error) {
    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося виконати вхід."

  } finally {
    loading.value = false
  }
}
</script>


<template>
  <section class="auth-page">
    <div class="auth-card auth-card-small">
      <div class="auth-heading">
        <span class="eyebrow">
          MedBook
        </span>

        <h1>
          Вхід
        </h1>

        <p>
          Увійдіть у свій кабінет пацієнта.
        </p>
      </div>

      <div
        v-if="errorMessage"
        class="alert alert-error">
        {{ errorMessage }}
      </div>

      <form
        class="form"
        @submit.prevent="submitLogin">
        <div class="form-group">
          <label for="email">
            E-mail
          </label>

          <input
            id="email"
            v-model="form.email"
            type="email"
            required>
        </div>

        <div class="form-group">
          <label for="password">
            Пароль
          </label>

          <input
            id="password"
            v-model="form.password"
            type="password"
            required>
        </div>

        <button
          class="button button-full"
          type="submit"
          :disabled="loading">
          {{
            loading
              ? "Вхід..."
              : "Увійти"
          }}
        </button>

        <p class="auth-footer">
          Ще немає профілю?

          <RouterLink to="/register">
            Зареєструватися
          </RouterLink>
        </p>
      </form>
    </div>
  </section>
</template>