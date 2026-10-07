<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "../stores/auth"


const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const errorMessage = ref("")


const form = reactive({
  first_name: "",
  last_name: "",
  middle_name: "",
  phone: "",
  email: "",
  birth_date: "",
  password: "",
  password_confirmation: ""
})


async function submitRegistration() {
  errorMessage.value = ""

  if (
    form.password !==
    form.password_confirmation
  ) {
    errorMessage.value =
      "Паролі не співпадають."

    return
  }

  loading.value = true

  try {
    await authStore.register({
      first_name: form.first_name,
      last_name: form.last_name,
      middle_name: form.middle_name,
      phone: form.phone,
      email: form.email,
      birth_date: form.birth_date,
      password: form.password
    })

    router.push("/dashboard")

  } catch (error) {
    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося зареєструватися."

  } finally {
    loading.value = false
  }
}
</script>


<template>
  <section class="auth-page">
    <div class="auth-card">
      <div class="auth-heading">
        <span class="eyebrow">
          Новий пацієнт
        </span>

        <h1>
          Реєстрація
        </h1>

        <p>
          Створіть профіль для онлайн-запису
          до лікарів.
        </p>
      </div>

      <div
        v-if="errorMessage"
        class="alert alert-error">
        {{ errorMessage }}
      </div>

      <form
        class="form"
        @submit.prevent="submitRegistration">
        <div class="form-row">
          <div class="form-group">
            <label for="last_name">
              Прізвище
            </label>

            <input
              id="last_name"
              v-model="form.last_name"
              type="text"
              required>
          </div>

          <div class="form-group">
            <label for="first_name">
              Ім'я
            </label>

            <input
              id="first_name"
              v-model="form.first_name"
              type="text"
              required>
          </div>
        </div>

        <div class="form-group">
          <label for="middle_name">
            По батькові
          </label>

          <input
            id="middle_name"
            v-model="form.middle_name"
            type="text">
        </div>

        <div class="form-group">
          <label for="phone">
            Телефон
          </label>

          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            placeholder="+380..."
            required>
        </div>

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
          <label for="birth_date">
            Дата народження
          </label>

          <input
            id="birth_date"
            v-model="form.birth_date"
            type="date"
            required>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="password">
              Пароль
            </label>

            <input
              id="password"
              v-model="form.password"
              type="password"
              minlength="8"
              required>
          </div>

          <div class="form-group">
            <label for="password_confirmation">
              Повторіть пароль
            </label>

            <input
              id="password_confirmation"
              v-model="form.password_confirmation"
              type="password"
              minlength="8"
              required>
          </div>
        </div>

        <button
          class="button button-full"
          type="submit"
          :disabled="loading">
          {{
            loading
              ? "Реєстрація..."
              : "Зареєструватися"
          }}
        </button>

        <p class="auth-footer">
          Вже маєте обліковий запис?

          <RouterLink to="/login">
            Увійти
          </RouterLink>
        </p>
      </form>
    </div>
  </section>
</template>