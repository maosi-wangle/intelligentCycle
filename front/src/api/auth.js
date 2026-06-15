import request from '@/utils/axios'

export const register = (data) => {
  return request.post('/auth/register', data)
}

export const login = (data) => {
  return request.post('/auth/login', data)
}

export const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}