const API_URL = 'https://exercisedb.p.rapidapi.com/exercises'
const API_KEY = 'cb53086b3fmshd99562a97c3c9dcp11b528jsn41d2f80671a7'

export const exerciseService = {
  async getExercises(limit = 10, offset = 0) {
    const url = new URL(API_URL)
    url.searchParams.append('limit', limit)
    url.searchParams.append('offset', offset)

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'exercisedb.p.rapidapi.com'
      }
    })

    if (!response.ok) {
      const error = await response.text()
      throw new Error(error || 'Failed to fetch exercises')
    }

    return response.json()
  }
} 