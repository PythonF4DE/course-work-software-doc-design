import { defineStore } from "pinia"
import api from "../services/api.js"


export const useAuthStore = defineStore(
  "auth",
  {
    state: () => ({
      user: null,
      patient: null,
      doctor: null,

      token: localStorage.getItem(
        "access_token"
      )
    }),

    getters: {
      isAuthenticated: (state) => {
        return Boolean(state.token)
      }
    },

    actions: {
      async register(formData) {
        const response = await api.post(
          "/auth/register",
          formData
        )

        this.setAuth(response.data)

        return response.data
      },

      async login(credentials) {
        const response = await api.post(
          "/auth/login",
          credentials
        )

        this.setAuth(response.data)

        return response.data
      },

      async loadCurrentUser() {
        if (!this.token) {
          return
        }

        try {
          const response = await api.get(
            "/auth/me"
          )

          this.user =
            response.data.user

          this.patient =
            response.data.patient

          this.doctor =
            response.data.doctor

          if (this.user?.role) {
            localStorage.setItem(
              "user_role",
              this.user.role
            )
          }

        } catch {
          this.logout()
        }
      },

      setAuth(data) {
        this.token =
          data.access_token

        this.user =
          data.user

        this.patient =
          data.patient

        this.doctor =
          data.doctor

        localStorage.setItem(
          "access_token",
          data.access_token
        )

        if (data.user?.role) {
          localStorage.setItem(
            "user_role",
            data.user.role
          )
        }
      },

      logout() {
        this.token = null
        this.user = null
        this.patient = null
        this.doctor = null

        localStorage.removeItem(
          "access_token"
        )

        localStorage.removeItem(
          "user_role"
        )
      }
    }
  }
)