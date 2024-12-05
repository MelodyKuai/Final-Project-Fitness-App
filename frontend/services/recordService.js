const API_BASE_URL = 'http://localhost:5000/api'

// Helper function: Format date time to specified format
const formatDateTime = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  
  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`
}

// Helper function: Convert image URL to base64
const getBase64FromUrl = async (url) => {
  const response = await fetch(url)
  const blob = await response.blob()
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}

export const recordService = {
  async getAllRecords() {
    const response = await fetch(`${API_BASE_URL}/records`, {
      credentials: 'include'
    })

    if (!response.ok) {
      throw new Error('Failed to fetch records')
    }

    const data = await response.json()
    return data.records;
  },

  async createRecord({ name, duration, imgUrl, date }) {
    const created_time = new Date(date)
    created_time.setHours(10, 0, 0, 0)

    // Get base64 data from image URL
    const imgData = await getBase64FromUrl(imgUrl)

    const response = await fetch(`${API_BASE_URL}/records`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        name,
        duration,
        imgData,
        created_time: formatDateTime(created_time)
      })
    })

    if (!response.ok) {
      throw new Error('Failed to create workout')
    }

    return response.json()
  },

  async updateRecord(id, { name, duration, imgUrl }) {
    // Get base64 data from image URL
    const imgData = await getBase64FromUrl(imgUrl)

    const response = await fetch(`${API_BASE_URL}/records/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        name,
        duration,
        imgData
      })
    })

    if (!response.ok) {
      throw new Error('Failed to update workout')
    }

    return response.json()
  },

  async deleteRecord(id) {
    const response = await fetch(`${API_BASE_URL}/records/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })

    if (!response.ok) {
      throw new Error('Failed to delete workout')
    }
  }
} 