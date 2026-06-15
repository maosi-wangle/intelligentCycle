import request from '@/utils/axios'

export const getCurrentUser = () => {
  return request.get('/users/me')
}