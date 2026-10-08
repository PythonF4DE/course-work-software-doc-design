<script setup>
import {
  computed,
  onMounted,
  ref
} from "vue"

import api from "../services/api.js"
import { useAuthStore } from "../stores/auth.js"


const authStore = useAuthStore()

const appointments = ref([])
const schedule = ref([])

const loading = ref(true)
const errorMessage = ref("")


const activeAppointments = computed(() => {
  return appointments.value.filter(
    item =>
      item.status === "scheduled"
  )
})


const historyAppointments = computed(() => {
  return appointments.value.filter(
    item =>
      item.status !== "scheduled"
  )
})


async function loadData() {

  loading.value = true

  try {

    const [
      appointmentsResponse,
      scheduleResponse
    ] = await Promise.all([
      api.get(
        "/doctor/appointments"
      ),

      api.get(
        "/doctor/schedule"
      )
    ])

    appointments.value =
      appointmentsResponse
        .data
        .appointments

    schedule.value =
      scheduleResponse
        .data
        .schedule

  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося завантажити кабінет лікаря."

  } finally {

    loading.value = false
  }
}


async function completeAppointment(
  appointmentId
) {

  try {

    await api.patch(
      `/doctor/appointments/${appointmentId}/complete`
    )

    await loadData()

  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося завершити прийом."
  }
}


function formatDate(dateString) {

  return new Date(
    `${dateString}T00:00:00`
  ).toLocaleDateString(
    "uk-UA",
    {
      day: "2-digit",
      month: "long",
      year: "numeric"
    }
  )
}


onMounted(async () => {

  await authStore.loadCurrentUser()

  await loadData()
})
</script>


<template>
  <section class="section">

    <div class="container">

      <span class="eyebrow">
        Кабінет лікаря
      </span>

      <h1>
        {{
          authStore.doctor?.full_name
        }}
      </h1>


      <div
        v-if="errorMessage"
        class="alert alert-error"
      >
        {{ errorMessage }}
      </div>


      <p
        v-if="loading"
        class="muted"
      >
        Завантаження...
      </p>


      <template v-else>

        <div class="dashboard-grid">

          <article class="dashboard-card">

            <h2>
              Мій профіль
            </h2>

            <dl
              v-if="authStore.doctor"
            >

              <div>
                <dt>
                  Лікар
                </dt>

                <dd>
                  {{
                    authStore
                      .doctor
                      .full_name
                  }}
                </dd>
              </div>

              <div>
                <dt>
                  Спеціалізація
                </dt>

                <dd>
                  {{
                    authStore
                      .doctor
                      .specialization
                      ?.name
                  }}
                </dd>
              </div>

            </dl>

          </article>


          <article class="dashboard-card">

            <h2>
              Розклад
            </h2>

            <div
              v-if="schedule.length === 0"
              class="muted"
            >
              Розклад відсутній.
            </div>

            <div
              v-else
              class="schedule-list"
            >

              <div
                v-for="item in schedule"
                :key="item.id"
                class="schedule-item"
              >
                <strong>
                  {{
                    formatDate(
                      item.date
                    )
                  }}
                </strong>

                <span>
                  {{
                    item.start_time
                  }}
                  –
                  {{
                    item.end_time
                  }}
                </span>
              </div>

            </div>

          </article>

        </div>


        <article
          class="
            dashboard-card
            doctor-appointments
          "
        >

          <h2>
            Майбутні прийоми
          </h2>


          <p
            v-if="
              activeAppointments.length === 0
            "
            class="muted"
          >
            Запланованих прийомів немає.
          </p>


          <div
            v-else
            class="appointment-list"
          >

            <article
              v-for="
                appointment
                in activeAppointments
              "
              :key="appointment.id"
              class="appointment-item"
            >

              <div class="appointment-main">

                <div class="appointment-date">

                  <strong>
                    {{
                      formatDate(
                        appointment
                          .appointment_date
                      )
                    }}
                  </strong>

                  <span>
                    {{
                      appointment
                        .appointment_time
                    }}
                  </span>

                </div>


                <div class="appointment-info">

                  <h3>
                    {{
                      appointment
                        .patient
                        .full_name
                    }}
                  </h3>

                  <p>
                    {{
                      appointment
                        .patient
                        .phone
                    }}
                  </p>

                  <p>
                    {{
                      appointment
                        .patient
                        .email
                    }}
                  </p>

                  <p
                    v-if="
                      appointment.reason
                    "
                  >
                    <strong>
                      Причина:
                    </strong>

                    {{
                      appointment.reason
                    }}
                  </p>

                </div>

              </div>


              <div class="appointment-footer">

                <span
                  class="
                    appointment-status
                    status-scheduled
                  "
                >
                  Заплановано
                </span>


                <button
                  class="
                    button
                    button-small
                  "
                  @click="
                    completeAppointment(
                      appointment.id
                    )
                  "
                >
                  Завершити прийом
                </button>

              </div>

            </article>

          </div>

        </article>


        <article
          v-if="
            historyAppointments.length > 0
          "
          class="
            dashboard-card
            appointments-history
          "
        >

          <h2>
            Історія прийомів
          </h2>


          <div class="appointment-list">

            <article
              v-for="
                appointment
                in historyAppointments
              "
              :key="appointment.id"
              class="appointment-item"
            >

              <strong>
                {{
                  formatDate(
                    appointment
                      .appointment_date
                  )
                }}
                —
                {{
                  appointment
                    .appointment_time
                }}
              </strong>

              <p>
                {{
                  appointment
                    .patient
                    .full_name
                }}
              </p>

              <span
                class="appointment-status"
                :class="
                  `status-${appointment.status}`
                "
              >
                {{
                  appointment.status ===
                  "completed"
                    ? "Завершено"
                    : "Скасовано"
                }}
              </span>

            </article>

          </div>

        </article>

      </template>

    </div>

  </section>
</template>