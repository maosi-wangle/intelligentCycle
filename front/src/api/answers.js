import request from '@/utils/axios'

export const getAnswers = (questionId, params) => {
  return request.get(`/questions/${questionId}/answers`, { params })
}

export const createAnswer = (questionId, data) => {
  return request.post(`/questions/${questionId}/answers`, data)
}

export const likeAnswer = (answerId) => {
  return request.post(`/answers/${answerId}/like`)
}

export const unlikeAnswer = (answerId) => {
  return request.delete(`/answers/${answerId}/like`)
}

export const acceptAnswer = (answerId) => {
  return request.post(`/answers/${answerId}/accept`)
}