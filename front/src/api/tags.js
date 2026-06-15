import request from '@/utils/axios'

export const getTags = () => {
  return request.get('/tags')
}

export const createTag = (data) => {
  return request.post('/tags', data)
}