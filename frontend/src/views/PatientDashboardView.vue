<script setup>
import {
  computed,
  onMounted,
  ref
} from "vue"

import {
  useAuthStore
} from "../stores/auth.js"

import api from "../services/api.js"


const authStore = useAuthStore()

const appointments = ref([])
const loadingAppointments = ref(true)
const errorMessage = ref("")

const notificationMethod = ref("email")
const savingNotificationMethod = ref(false)


const fullName = computed(() => {
  return (
    authStore.patient?.full_name ||
    "Пацієнт"
  )
})


const activeAppointments = computed(() => {
  return appointments.value.filter(
    appointment =>
      appointment.status === "scheduled"
  )
})


const finishedAppointments = computed(() => {
  return appointments.value.filter(
    appointment =>
      appointment.status !== "scheduled"
  )
})


async function loadAppointments() {
  loadingAppointments.value = true
  errorMessage.value = ""

  try {
    const response = await api.get(
      "/appointments"
    )

    appointments.value =
      response.data.appointments

  } catch (error) {
    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося завантажити записи."

  } finally {
    loadingAppointments.value = false
  }
}


async function cancelAppointment(
  appointmentId
) {
  const confirmed = window.confirm(
    "Скасувати цей запис?"
  )

  if (!confirmed) {
    return
  }

  try {
    await api.patch(
      `/appointments/${appointmentId}/cancel`
    )

    await loadAppointments()

  } catch (error) {
    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося скасувати запис."
  }
}


async function saveNotificationMethod() {
  savingNotificationMethod.value = true
  errorMessage.value = ""

  try {
    await api.patch(
      "/auth/notification-method",
      {
        notification_method:
          notificationMethod.value
      }
    )

    if (authStore.patient) {
      authStore.patient.notification_method =
        notificationMethod.value
    }

  } catch (error) {
    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося змінити спосіб нагадувань."

  } finally {
    savingNotificationMethod.value = false
  }
}


function formatDate(dateString) {
  const date = new Date(
    `${dateString}T00:00:00`
  )

  return date.toLocaleDateString(
    "uk-UA",
    {
      day: "2-digit",
      month: "long",
      year: "numeric"
    }
  )
}


function getStatusText(status) {
  const statuses = {
    scheduled: "Заплановано",
    completed: "Завершено",
    cancelled: "Скасовано"
  }

  return statuses[status] || status
}


onMounted(async () => {
  await authStore.loadCurrentUser()

  notificationMethod.value =
    authStore.patient?.notification_method ||
    "email"

  await loadAppointments()
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
        v-if="errorMessage"
        class="alert alert-error"
      >
        {{ errorMessage }}
      </div>


      <div class="dashboard-grid">

        <!-- Дані пацієнта -->

        <article class="dashboard-card">
          <h2>
            Мої дані
          </h2>

          <dl v-if="authStore.patient">

            <div>
              <dt>ПІБ</dt>

              <dd>
                {{
                  authStore.patient.full_name
                }}
              </dd>
            </div>

            <div>
              <dt>E-mail</dt>

              <dd>
                {{
                  authStore.patient.email
                }}
              </dd>
            </div>

            <div>
              <dt>Телефон</dt>

              <dd>
                {{
                  authStore.patient.phone
                }}
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
            Нагадування
          </h2>

          <p class="muted">
            Оберіть спосіб отримання нагадувань
            про майбутні прийоми.
          </p>


          <div class="notification-options">

            <label class="notification-option">
              <input
                v-model="notificationMethod"
                type="radio"
                value="email"
              >

              <div>
                <strong>
                  E-mail
                </strong>

                <p>
                  {{
                    authStore.patient?.email
                  }}
                </p>
              </div>
            </label>


            <label class="notification-option">
              <input
                v-model="notificationMethod"
                type="radio"
                value="sms"
              >

              <div>
                <strong>
                  SMS
                </strong>

                <p>
                  {{
                    authStore.patient?.phone
                  }}
                </p>
              </div>
            </label>

          </div>


          <button
            class="button"
            :disabled="savingNotificationMethod"
            @click="saveNotificationMethod"
          >
            {{
              savingNotificationMethod
                ? "Збереження..."
                : "Зберегти"
            }}
          </button>
        </article>


        <article class="dashboard-card">

          <div class="appointments-header">

            <h2>
              Мої записи
            </h2>

            <RouterLink
              to="/doctors"
              class="button button-small"
            >
              Новий запис
            </RouterLink>

          </div>


          <p
            v-if="loadingAppointments"
            class="muted"
          >
            Завантаження записів...
          </p>


          <p
            v-else-if="
              activeAppointments.length === 0
            "
            class="muted"
          >
            Активних записів поки немає.
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
                        appointment.appointment_date
                      )
                    }}
                  </strong>

                  <span>
                    {{
                      appointment.appointment_time
                    }}
                  </span>
                </div>


                <div class="appointment-info">

                  <h3>
                    {{
                      appointment
                        .doctor
                        ?.full_name
                    }}
                  </h3>

                  <p class="specialization">
                    {{
                      appointment
                        .doctor
                        ?.specialization
                        ?.name
                    }}
                  </p>

                  <p
                    v-if="appointment.reason"
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
                  {{
                    getStatusText(
                      appointment.status
                    )
                  }}
                </span>


                <button
                  class="
                    button
                    button-danger
                    button-small
                  "
                  @click="
                    cancelAppointment(
                      appointment.id
                    )
                  "
                >
                  Скасувати
                </button>

              </div>

            </article>

          </div>

        </article>

      </div>


      <article
        v-if="
          !loadingAppointments &&
          finishedAppointments.length > 0
        "
        class="
          dashboard-card
          appointments-history
        "
      >

        <h2>
          Історія записів
        </h2>


        <div class="appointment-list">

          <article
            v-for="
              appointment
              in finishedAppointments
            "
            :key="appointment.id"
            class="
              appointment-item
              appointment-finished
            "
          >

            <div class="appointment-main">

              <div class="appointment-date">

                <strong>
                  {{
                    formatDate(
                      appointment.appointment_date
                    )
                  }}
                </strong>

                <span>
                  {{
                    appointment.appointment_time
                  }}
                </span>

              </div>


              <div class="appointment-info">

                <h3>
                  {{
                    appointment
                      .doctor
                      ?.full_name
                  }}
                </h3>

                <p class="specialization">
                  {{
                    appointment
                      .doctor
                      ?.specialization
                      ?.name
                  }}
                </p>

                <p
                  v-if="appointment.reason"
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


            <span
              class="appointment-status"
              :class="
                `status-${appointment.status}`
              "
            >
              {{
                getStatusText(
                  appointment.status
                )
              }}
            </span>

          </article>

        </div>

      </article>

    </div>
  </section>
</template>