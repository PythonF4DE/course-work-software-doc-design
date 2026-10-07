<script setup>
import {
  ref,
  computed,
  onMounted
} from "vue"

import {
  useRoute,
  useRouter
} from "vue-router"

import api from "../services/api.js"

import {
  useAuthStore
} from "../stores/auth.js"


const route = useRoute()
const router = useRouter()

const authStore = useAuthStore()

const doctor = ref(null)

const selectedDate = ref("")
const selectedTime = ref("")
const reason = ref("")

const slots = ref([])

const loadingSlots = ref(false)
const submitting = ref(false)

const errorMessage = ref("")
const successMessage = ref("")


const doctorId = computed(
  () => Number(
    route.params.id
  )
)


const minimumDate = computed(() => {
  const date = new Date()

  date.setDate(
    date.getDate() + 1
  )

  return date
    .toISOString()
    .split("T")[0]
})


async function loadDoctor() {
  const response = await api.get(
    `/doctors/${doctorId.value}`
  )

  doctor.value =
    response.data.doctor
}


async function loadSlots() {

  selectedTime.value = ""
  slots.value = []
  errorMessage.value = ""

  if (!selectedDate.value) {
    return
  }

  loadingSlots.value = true

  try {
    const response = await api.get(
      `/doctors/${doctorId.value}/available-slots`,
      {
        params: {
          date:
            selectedDate.value
        }
      }
    )

    slots.value =
      response.data.slots

  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося отримати доступний час."

  } finally {
    loadingSlots.value = false
  }
}


async function bookAppointment() {

  errorMessage.value = ""
  successMessage.value = ""

  if (
    !selectedDate.value ||
    !selectedTime.value
  ) {
    errorMessage.value =
      "Оберіть дату та час."

    return
  }

  if (
    !authStore.isAuthenticated
  ) {
    router.push("/login")
    return
  }

  submitting.value = true

  try {
    await api.post(
      "/appointments",
      {
        doctor_id:
          doctorId.value,

        appointment_date:
          selectedDate.value,

        appointment_time:
          selectedTime.value,

        reason:
          reason.value
      }
    )

    successMessage.value =
      "Запис успішно створено."

    slots.value =
      slots.value.filter(
        slot =>
          slot !==
          selectedTime.value
      )

    selectedTime.value = ""

  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося створити запис."

  } finally {
    submitting.value = false
  }
}


onMounted(
  loadDoctor
)
</script>


<template>
  <section class="section">

    <div class="container">

      <div
        v-if="doctor"
        class="booking-layout">

        <aside
          class="doctor-card booking-doctor">

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

        </aside>


        <div class="booking-card">

          <span class="eyebrow">
            Онлайн-запис
          </span>

          <h1>
            Оберіть дату та час
          </h1>

          <div
            v-if="errorMessage"
            class="alert alert-error">
            {{ errorMessage }}
          </div>

          <div
            v-if="successMessage"
            class="alert alert-success">
            {{ successMessage }}
          </div>

          <div class="form">

            <div class="form-group">

              <label>
                Дата прийому
              </label>

              <input
                v-model="selectedDate"
                type="date"
                :min="minimumDate"
                @change="loadSlots">

            </div>


            <div class="form-group">

              <label>
                Доступний час
              </label>

              <div
                v-if="loadingSlots"
                class="muted">
                Завантаження...
              </div>

              <div
                v-else-if="
                  selectedDate &&
                  slots.length === 0
                "
                class="muted">
                На цю дату
                немає вільного часу.
              </div>

              <div
                v-else
                class="time-grid">

                <button
                  v-for="slot in slots"
                  :key="slot"
                  type="button"
                  class="time-slot"
                  :class="{
                    selected:
                      selectedTime === slot
                  }"
                  @click="
                    selectedTime = slot">
                  {{ slot }}
                </button>

              </div>

            </div>


            <div class="form-group">

              <label>
                Причина звернення
              </label>

              <textarea
                v-model="reason"
                rows="4"
                placeholder="Опишіть причину звернення..."/>

            </div>


            <button
              class="button"
              :disabled="
                submitting ||
                !selectedTime"
              @click="bookAppointment">

              {{
                submitting
                  ? "Створення..."
                  : "Підтвердити запис"
              }}

            </button>

          </div>

        </div>

      </div>

    </div>

  </section>
</template>