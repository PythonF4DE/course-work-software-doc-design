<script setup>
import {
  onMounted,
  reactive,
  ref
} from "vue"

import api from "../services/api.js"


const doctors = ref([])
const patients = ref([])
const schedule = ref([])
const specializations = ref([])

const appointmentReport = ref({
  today: 0,
  month: 0,
  by_doctor: []
})

const doctorLoadReport = ref([])

const newPatientsReport = ref([])

const errorMessage = ref("")


const doctorForm = reactive({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  specialization_id: "",
  description: ""
})


const scheduleForm = reactive({
  doctor_id: "",
  date: "",
  start_time: "09:00",
  end_time: "17:00"
})


async function loadData() {

  try {

    const [
      doctorsResponse,
      patientsResponse,
      scheduleResponse,
      specializationResponse,
      appointmentReportResponse,
      doctorLoadResponse,
      newPatientsResponse
    ] = await Promise.all([

      api.get(
        "/admin/doctors"
      ),

      api.get(
        "/admin/patients"
      ),

      api.get(
        "/admin/schedule"
      ),

      api.get(
        "/admin/specializations"
      ),

      api.get(
        "/admin/reports/appointments"
      ),

      api.get(
        "/admin/reports/doctor-load"
      ),

      api.get(
        "/admin/reports/new-patients"
      )

    ])


    doctors.value =
      doctorsResponse
        .data
        .doctors

    patients.value =
      patientsResponse
        .data
        .patients

    schedule.value =
      scheduleResponse
        .data
        .schedule

    specializations.value =
      specializationResponse
        .data
        .specializations

    appointmentReport.value =
      appointmentReportResponse.data

    doctorLoadReport.value =
      doctorLoadResponse
        .data
        .doctor_load

    newPatientsReport.value =
      newPatientsResponse
        .data
        .new_patients

  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося завантажити дані."
  }
}


async function createDoctor() {

  try {

    await api.post(
      "/admin/doctors",
      doctorForm
    )


    Object.assign(
      doctorForm,
      {
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        specialization_id: "",
        description: ""
      }
    )


    await loadData()


  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося створити лікаря."
  }
}


async function deleteDoctor(
  doctorId
) {

  if (
    !window.confirm(
      "Видалити цього лікаря?"
    )
  ) {
    return
  }


  try {

    await api.delete(
      `/admin/doctors/${doctorId}`
    )

    await loadData()


  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося видалити лікаря."
  }
}


async function createSchedule() {

  try {

    await api.post(
      "/admin/schedule",
      scheduleForm
    )

    await loadData()


  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося додати розклад."
  }
}


async function deleteSchedule(
  scheduleId
) {

  try {

    await api.delete(
      `/admin/schedule/${scheduleId}`
    )

    await loadData()


  } catch (error) {

    errorMessage.value =
      error.response?.data?.error ||
      "Не вдалося видалити розклад."
  }
}


onMounted(
  loadData
)
</script>


<template>
  <section class="section">

    <div class="container">

      <span class="eyebrow">
        Адміністрування
      </span>

      <h1>
        Кабінет адміністратора
      </h1>

      <div
        v-if="errorMessage"
        class="alert alert-error"
      >
        {{ errorMessage }}
      </div>

      <section class="admin-reports">

        <h2>
          Звіти
        </h2>


        <div class="report-cards">

          <article class="report-card">

            <span class="report-label">
              Прийомів сьогодні
            </span>

            <strong class="report-number">
              {{
                appointmentReport.today
              }}
            </strong>

          </article>


          <article class="report-card">

            <span class="report-label">
              Прийомів цього місяця
            </span>

            <strong class="report-number">
              {{
                appointmentReport.month
              }}
            </strong>

          </article>


          <article class="report-card">

            <span class="report-label">
              Всього лікарів
            </span>

            <strong class="report-number">
              {{ doctors.length }}
            </strong>

          </article>


          <article class="report-card">

            <span class="report-label">
              Всього пацієнтів
            </span>

            <strong class="report-number">
              {{ patients.length }}
            </strong>

          </article>

        </div>


        <article
          class="
            dashboard-card
            admin-section
          "
        >

          <h2>
            Кількість прийомів
            за лікарями
          </h2>


          <div class="admin-table-wrapper">

            <table class="admin-table">

              <thead>

                <tr>
                  <th>
                    Лікар
                  </th>

                  <th>
                    Кількість прийомів
                  </th>
                </tr>

              </thead>


              <tbody>

                <tr
                  v-for="
                    item
                    in appointmentReport.by_doctor
                  "
                  :key="item.doctor_id"
                >

                  <td>
                    {{
                      item.doctor_name
                    }}
                  </td>

                  <td>
                    {{
                      item.appointment_count
                    }}
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </article>


        <article
          class="
            dashboard-card
            admin-section
          "
        >

          <h2>
            Завантаженість лікарів
          </h2>


          <div class="admin-table-wrapper">

            <table class="admin-table">

              <thead>

                <tr>
                  <th>
                    Лікар
                  </th>

                  <th>
                    Всього
                  </th>

                  <th>
                    Заплановано
                  </th>

                  <th>
                    Завершено
                  </th>

                  <th>
                    Скасовано
                  </th>
                </tr>

              </thead>


              <tbody>

                <tr
                  v-for="
                    item
                    in doctorLoadReport
                  "
                  :key="item.doctor_id"
                >

                  <td>
                    {{
                      item.doctor_name
                    }}
                  </td>

                  <td>
                    {{
                      item.total
                    }}
                  </td>

                  <td>
                    {{
                      item.scheduled
                    }}
                  </td>

                  <td>
                    {{
                      item.completed
                    }}
                  </td>

                  <td>
                    {{
                      item.cancelled
                    }}
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </article>


        <article
          class="
            dashboard-card
            admin-section
          "
        >

          <h2>
            Динаміка нових пацієнтів
          </h2>


          <div class="admin-table-wrapper">

            <table class="admin-table">

              <thead>

                <tr>
                  <th>
                    Дата
                  </th>

                  <th>
                    Нових пацієнтів
                  </th>
                </tr>

              </thead>


              <tbody>

                <tr
                  v-for="
                    item
                    in newPatientsReport
                  "
                  :key="item.date"
                >

                  <td>
                    {{
                      item.date
                    }}
                  </td>

                  <td>
                    {{
                      item.count
                    }}
                  </td>

                </tr>

              </tbody>

            </table>

          </div>

        </article>

      </section>

      <article class="dashboard-card">

        <h2>
          Додати лікаря
        </h2>


        <form
          class="form"
          @submit.prevent="createDoctor"
        >

          <div class="form-row">

            <div class="form-group">

              <label>
                Ім'я
              </label>

              <input
                v-model="
                  doctorForm.first_name
                "
                required
              >

            </div>


            <div class="form-group">

              <label>
                Прізвище
              </label>

              <input
                v-model="
                  doctorForm.last_name
                "
                required
              >

            </div>

          </div>


          <div class="form-group">

            <label>
              E-mail
            </label>

            <input
              v-model="
                doctorForm.email
              "
              type="email"
              required
            >

          </div>


          <div class="form-group">

            <label>
              Пароль
            </label>

            <input
              v-model="
                doctorForm.password
              "
              type="password"
              minlength="8"
              required
            >

          </div>


          <div class="form-group">

            <label>
              Спеціалізація
            </label>

            <select
              v-model="
                doctorForm
                  .specialization_id
              "
              required
            >

              <option value="">
                Оберіть спеціалізацію
              </option>

              <option
                v-for="
                  item
                  in specializations
                "
                :key="item.id"
                :value="item.id"
              >
                {{ item.name }}
              </option>

            </select>

          </div>


          <div class="form-group">

            <label>
              Опис
            </label>

            <textarea
              v-model="
                doctorForm.description
              "
              rows="4"
            />

          </div>


          <button class="button">
            Додати лікаря
          </button>

        </form>

      </article>


      <article
        class="
          dashboard-card
          admin-section
        "
      >

        <h2>
          Лікарі
        </h2>


        <div class="admin-table-wrapper">

          <table class="admin-table">

            <thead>
              <tr>
                <th>Лікар</th>
                <th>
                  Спеціалізація
                </th>
                <th></th>
              </tr>
            </thead>


            <tbody>

              <tr
                v-for="
                  doctor in doctors
                "
                :key="doctor.id"
              >

                <td>
                  {{
                    doctor.full_name
                  }}
                </td>

                <td>
                  {{
                    doctor
                      .specialization
                      ?.name
                  }}
                </td>

                <td>

                  <button
                    class="
                      button
                      button-danger
                      button-small
                    "
                    @click="
                      deleteDoctor(
                        doctor.id
                      )
                    "
                  >
                    Видалити
                  </button>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </article>


      <article
        class="
          dashboard-card
          admin-section
        "
      >

        <h2>
          Пацієнти
        </h2>


        <div class="admin-table-wrapper">

          <table class="admin-table">

            <thead>

              <tr>
                <th>ПІБ</th>
                <th>E-mail</th>
                <th>Телефон</th>
                <th>
                  Дата народження
                </th>
              </tr>

            </thead>


            <tbody>

              <tr
                v-for="
                  patient in patients
                "
                :key="patient.id"
              >

                <td>
                  {{
                    patient.full_name
                  }}
                </td>

                <td>
                  {{
                    patient.email
                  }}
                </td>

                <td>
                  {{
                    patient.phone
                  }}
                </td>

                <td>
                  {{
                    patient.birth_date
                  }}
                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </article>


      <article
        class="
          dashboard-card
          admin-section
        "
      >

        <h2>
          Додати розклад
        </h2>


        <form
          class="form"
          @submit.prevent="
            createSchedule
          "
        >

          <div class="form-group">

            <label>
              Лікар
            </label>

            <select
              v-model="
                scheduleForm.doctor_id
              "
              required
            >

              <option value="">
                Оберіть лікаря
              </option>

              <option
                v-for="
                  doctor in doctors
                "
                :key="doctor.id"
                :value="doctor.id"
              >
                {{
                  doctor.full_name
                }}
              </option>

            </select>

          </div>


          <div class="form-row">

            <div class="form-group">

              <label>
                Дата
              </label>

              <input
                v-model="
                  scheduleForm.date
                "
                type="date"
                required
              >

            </div>


            <div class="form-group">

              <label>
                Початок
              </label>

              <input
                v-model="
                  scheduleForm.start_time
                "
                type="time"
                required
              >

            </div>


            <div class="form-group">

              <label>
                Кінець
              </label>

              <input
                v-model="
                  scheduleForm.end_time
                "
                type="time"
                required
              >

            </div>

          </div>


          <button class="button">
            Додати розклад
          </button>

        </form>


        <div
          class="
            admin-table-wrapper
            schedule-table
          "
        >

          <table class="admin-table">

            <thead>

              <tr>
                <th>Лікар</th>
                <th>Дата</th>
                <th>Час</th>
                <th></th>
              </tr>

            </thead>


            <tbody>

              <tr
                v-for="
                  item in schedule
                "
                :key="item.id"
              >

                <td>
                  {{
                    item
                      .doctor
                      .full_name
                  }}
                </td>

                <td>
                  {{ item.date }}
                </td>

                <td>
                  {{
                    item.start_time
                  }}
                  –
                  {{
                    item.end_time
                  }}
                </td>

                <td>

                  <button
                    class="
                      button
                      button-danger
                      button-small
                    "
                    @click="
                      deleteSchedule(
                        item.id
                      )
                    "
                  >
                    Видалити
                  </button>

                </td>

              </tr>

            </tbody>

          </table>

        </div>

      </article>

    </div>

  </section>
</template>