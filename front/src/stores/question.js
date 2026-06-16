import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getQuestions, getQuestionDetail, createQuestion, likeQuestion, unlikeQuestion, collectQuestion, uncollectQuestion } from '@/api/questions'
import { getAnswers, createAnswer, likeAnswer, unlikeAnswer, acceptAnswer } from '@/api/answers'

export const useQuestionStore = defineStore('question', () => {
  const questions = ref([])
  const questionDetail = ref(null)
  const answers = ref([])
  const total = ref(0)

  const loadQuestions = async (params = {}) => {
    const res = await getQuestions(params)
    questions.value = res.items
    total.value = res.total
    return res
  }

  const loadQuestionDetail = async (questionId) => {
    const res = await getQuestionDetail(questionId)
    questionDetail.value = res
    return res
  }

  const loadAnswers = async (questionId, params = {}) => {
    const res = await getAnswers(questionId, params)
    answers.value = res
    return { items: res, total: res.length }
  }

  const addQuestion = async (data) => {
    const res = await createQuestion(data)
    return res
  }

  const addAnswer = async (questionId, content) => {
    const res = await createAnswer(questionId, { content })
    return res
  }

  const toggleLikeQuestion = async (questionId, isLiked) => {
    if (isLiked) {
      await unlikeQuestion(questionId)
    } else {
      await likeQuestion(questionId)
    }
  }

  const toggleCollectQuestion = async (questionId, isCollected) => {
    if (isCollected) {
      const res = await uncollectQuestion(questionId)
      return res
    } else {
      const res = await collectQuestion(questionId)
      return res
    }
  }

  const toggleLikeAnswer = async (answerId, isLiked) => {
    if (isLiked) {
      await unlikeAnswer(answerId)
    } else {
      await likeAnswer(answerId)
    }
  }

  const confirmAcceptAnswer = async (answerId) => {
    const res = await acceptAnswer(answerId)
    const answer = answers.value.find(a => a.id === answerId)
    if (answer) {
      answer.is_accepted = true
    }
    return res
  }

  return {
    questions,
    questionDetail,
    answers,
    total,
    loadQuestions,
    loadQuestionDetail,
    loadAnswers,
    addQuestion,
    addAnswer,
    toggleLikeQuestion,
    toggleCollectQuestion,
    toggleLikeAnswer,
    confirmAcceptAnswer
  }
})