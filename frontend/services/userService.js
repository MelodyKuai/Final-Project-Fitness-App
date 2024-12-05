const API_BASE_URL = 'http://localhost:5000/api'

export const userService = {
  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(credentials)
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || 'Login failed')
    }

    return response.json()
  },

  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    })

    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || 'Registration failed')
    }

    return response.json()
  },

  async logout() {
    try {
      const response = await fetch(`${API_BASE_URL}/logout`, {
        method: 'POST',
        credentials: 'include'
      })

      if (!response.ok && response.status !== 401) {
        throw new Error('Logout failed')
      }
    } catch (error) {
      console.error('Logout error:', error)
    }
  }
} 