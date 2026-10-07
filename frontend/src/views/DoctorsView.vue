<script setup>
import {
  ref,
  onMounted
} from "vue"

import api from "../services/api.js"


const doctors = ref([])
const specializations = ref([])

const selectedSpecialization = ref("")

const loading = ref(false)


async function loadSpecializations() {
  const response = await api.get(
    "/doctors/specializations"
  )

  specializations.value =
    response.data.specializations
}


async function loadDoctors() {
  loading.value = true

  try {
    const params = {}

    if (
      selectedSpecialization.value
    ) {
      params.specialization_id =
        selectedSpecialization.value
    }

    const response = await api.get(
      "/doctors",
      {
        params
      }
    )

    doctors.value =
      response.data.doctors

  } finally {
    loading.value = false
  }
}


async function changeSpecialization() {
  await loadDoctors()
}


onMounted(async () => {
  await loadSpecializations()
  await loadDoctors()
})
</script>


<template>
  <section class="section">
    <div class="container">

      <span class="eyebrow">
        Медичний персонал
      </span>

      <h1>
        Наші лікарі
      </h1>

      <p class="page-description">
        Оберіть спеціалізацію та
        знайдіть потрібного лікаря.
      </p>

      <div class="filter-bar">

        <label>
          Спеціалізація
        </label>

        <select
          v-model="selectedSpecialization"
          @change="changeSpecialization">
          <option value="">
            Усі спеціалізації
          </option>

          <option
            v-for="specialization
              in specializations"
            :key="specialization.id"
            :value="specialization.id">
            {{ specialization.name }}
          </option>

        </select>

      </div>

      <div
        v-if="loading"
        class="empty-state">
        Завантаження...
      </div>

      <div
        v-else-if="doctors.length === 0"
        class="empty-state">
        Лікарів не знайдено.
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

          <h2>
            {{ doctor.full_name }}
          </h2>

          <p class="specialization">
            {{
              doctor.specialization
                ?.name
            }}
          </p>

          <p>
            {{ doctor.description }}
          </p>

          <RouterLink
            :to="`/doctors/${doctor.id}/book`"
            class="button">
            Записатися
          </RouterLink>

        </article>

      </div>

    </div>
  </section>
</template>