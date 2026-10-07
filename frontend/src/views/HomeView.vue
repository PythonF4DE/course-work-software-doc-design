<script setup>
import {
  ref,
  onMounted
} from "vue"

import api from "../services/api.js"
import { useAuthStore } from "../stores/auth.js"


const doctors = ref([])
const loading = ref(true)

const authStore = useAuthStore()


async function loadDoctors() {
  try {
    const response = await api.get(
      "/doctors"
    )

    doctors.value =
      response.data.doctors

  } catch (error) {
    console.error(
      "Failed to load doctors:",
      error
    )

  } finally {
    loading.value = false
  }
}


onMounted(loadDoctors)
</script>


<template>
  <section class="hero">
    <div class="container hero-content">
      <div class="hero-text">
        <span class="eyebrow">
          Онлайн-запис до лікаря
        </span>

        <h1>
          Запишіться до лікаря
          у зручний для вас час
        </h1>

        <p>
          Знайдіть потрібного спеціаліста,
          оберіть дату та час прийому
          та керуйте своїми записами онлайн.
        </p>

        <div class="hero-actions">

          <RouterLink
            v-if="!authStore.isAuthenticated"
            to="/register"
            class="button">
            Зареєструватися
          </RouterLink>

          <RouterLink
            v-else
            to="/dashboard"
            class="button">
            Мої записи
          </RouterLink>

          <RouterLink
            to="/doctors"
            class="button button-secondary">
            Переглянути лікарів
          </RouterLink>

        </div>
      </div>
    </div>
  </section>


  <section
    id="doctors"
    class="section">
    <div class="container">

      <div class="section-header">
        <div>
          <span class="eyebrow">
            Наші спеціалісти
          </span>

          <h2>
            Лікарі
          </h2>
        </div>
      </div>


      <div
        v-if="loading"
        class="empty-state">
        Завантаження...
      </div>


      <div
        v-else-if="doctors.length === 0"
        class="empty-state">
        Лікарів поки не додано.
      </div>


      <div
        v-else
        class="doctor-grid">
        <article
          v-for="doctor in doctors"
          :key="doctor.id"
          class="doctor-card">

          <div class="doctor-avatar">
            {{ doctor.first_name[0] }}
            {{ doctor.last_name[0] }}
          </div>


          <div>
            <h3>
              {{ doctor.full_name }}
            </h3>

            <p class="specialization">
              {{
                doctor.specialization?.name
              }}
            </p>

            <p>
              {{ doctor.description }}
            </p>

            <RouterLink
              :to="`/doctors/${doctor.id}/book`"
              class="button button-small">
              Записатися
            </RouterLink>
          </div>

        </article>
      </div>

    </div>
  </section>


  <section
    v-if="!authStore.isAuthenticated"
    class="section section-muted">
    <div class="container">

      <span class="eyebrow">
        Як це працює
      </span>

      <h2>
        Три прості кроки
      </h2>


      <div class="steps">

        <article class="step">
          <span>1</span>

          <h3>
            Створіть профіль
          </h3>

          <p>
            Зареєструйтеся як пацієнт.
          </p>
        </article>


        <article class="step">
          <span>2</span>

          <h3>
            Оберіть лікаря
          </h3>

          <p>
            Знайдіть потрібну спеціалізацію.
          </p>
        </article>


        <article class="step">
          <span>3</span>

          <h3>
            Запишіться
          </h3>

          <p>
            Оберіть доступну дату та час.
          </p>
        </article>

      </div>

    </div>
  </section>
</template>