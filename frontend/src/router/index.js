import {
    createRouter,
    createWebHistory
  } from "vue-router"

  import HomeView from "../views/HomeView.vue"
  import RegisterView from "../views/RegisterView.vue"
  import LoginView from "../views/LoginView.vue"
  import PatientDashboardView from "../views/PatientDashboardView.vue"
  import DoctorsView from "../views/DoctorsView.vue"
  import DoctorBookingView from "../views/DoctorBookingView.vue"

  const routes = [
    {
      path: "/",
      name: "home",
      component: HomeView
    },

    {
      path: "/register",
      name: "register",
      component: RegisterView
    },

    {
      path: "/login",
      name: "login",
      component: LoginView
    },

    {
      path: "/dashboard",
      name: "dashboard",
      component: PatientDashboardView,
      meta: {
        requiresAuth: true
      }
    },

    {
      path: "/doctors",
      name: "doctors",
      component: DoctorsView
    },

    {
      path: "/doctors/:id/book",
      name: "doctor-booking",
      component: DoctorBookingView
    }
  
  ]


  const router = createRouter({
    history: createWebHistory(),
    routes
  })


  router.beforeEach((to) => {
    if (
      to.meta.requiresAuth &&
      !localStorage.getItem("access_token")
    ) {
      return {
        name: "login"
      }
    }
  })


  export default router