import request from '@/utils/axios'

export const getRecommendedQuestions = () => {
  return request.get('/recommendations/questions')
}