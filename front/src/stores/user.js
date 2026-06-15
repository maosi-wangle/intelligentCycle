import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin, register as apiRegister, logout as apiLogout } from '@/api/auth'
import { getCurrentUser } from '@/api/users'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))

  const login = async (username, password) => {
    const res = await apiLogin({ username, password })
    token.value = res.access_token
    user.value = res.user
    localStorage.setItem('token', res.access_token)
    localStorage.setItem('user', JSON.stringify(res.user))
    return res
  }

  const register = async (username, password, email) => {
    const res = await apiRegister({ username, password, email })
    return res
  }

  const logout = () => {
    apiLogout()
    user.value = null
    token.value = null
  }

  const fetchUser = async () => {
    if (token.value) {
      try {
        const res = await getCurrentUser()
        user.value = res
        localStorage.setItem('user', JSON.stringify(res))
      } catch {
        logout()
      }
    }
  }

  const isLoggedIn = () => {
    return !!token.value
  }

  return {
    user,
    token,
    login,
    register,
    logout,
    fetchUser,
    isLoggedIn
  }
})