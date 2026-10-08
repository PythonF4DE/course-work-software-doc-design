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
import DoctorDashboardView from "../views/DoctorDashboardView.vue"
import AdminDashboardView from "../views/AdminDashboardView.vue"

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
  },

  {
    path: "/doctor",
    name: "doctor-dashboard",
    component: DoctorDashboardView,
  
    meta: {
      requiresAuth: true,
      role: "doctor"
    }
  },
  
  {
    path: "/admin",
    name: "admin-dashboard",
    component: AdminDashboardView,
  
    meta: {
      requiresAuth: true,
      role: "admin"
    }
  },

]


const router = createRouter({
  history: createWebHistory(),
  routes
})


router.beforeEach((to) => {

  const token =
    localStorage.getItem(
      "access_token"
    )

  const role =
    localStorage.getItem(
      "user_role"
    )


  if (
    to.meta.requiresAuth &&
    !token
  ) {
    return {
      name: "login"
    }
  }


  if (
    to.meta.role &&
    role !== to.meta.role
  ) {
    return {
      name: "home"
    }
  }
})


export default router