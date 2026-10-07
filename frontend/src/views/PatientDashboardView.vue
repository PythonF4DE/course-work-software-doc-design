<script setup>
import { computed } from "vue"

import { useAuthStore } from "../stores/auth.js"


const authStore = useAuthStore()


const fullName = computed(() => {
  return authStore.patient?.full_name ||
    "Пацієнт"
})
</script>


<template>
  <section class="section">
    <div class="container">
      <span class="eyebrow">
        Особистий кабінет
      </span>

      <h1>
        Вітаємо, {{ fullName }}
      </h1>

      <div
        v-if="authStore.patient"
        class="dashboard-grid">
        <article class="dashboard-card">
          <h2>
            Мої дані
          </h2>

          <dl>
            <div>
              <dt>ПІБ</dt>
              <dd>
                {{ authStore.patient.full_name }}
              </dd>
            </div>

            <div>
              <dt>E-mail</dt>
              <dd>
                {{ authStore.patient.email }}
              </dd>
            </div>

            <div>
              <dt>Телефон</dt>
              <dd>
                {{ authStore.patient.phone }}
              </dd>
            </div>

            <div>
              <dt>Дата народження</dt>
              <dd>
                {{
                  authStore.patient.birth_date
                }}
              </dd>
            </div>
          </dl>
        </article>

        <article class="dashboard-card">
          <h2>
            Мої записи
          </h2>

          <p class="muted">
            Активних записів поки немає.
          </p>

          <RouterLink
            to="/"
            class="button">
            Знайти лікаря
          </RouterLink>
        </article>
      </div>
    </div>
  </section>
</template>