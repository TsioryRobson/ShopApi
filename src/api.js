const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    let errorDetail = `Erreur HTTP ${response.status}`

    try {
      const errorBody = await response.json()
      errorDetail = errorBody.detail || errorBody.message || errorDetail
    } catch {
      // Ignore parsing failures and keep generic error.
    }

    throw new Error(errorDetail)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export function getApiBaseUrl() {
  return API_BASE_URL
}

export function getHealth() {
  return request('/')
}

export function listCategories() {
  return request('/categories/')
}

export function createCategory(payload) {
  return request('/categories/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateCategory(categoryId, payload) {
  return request(`/categories/${categoryId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteCategory(categoryId) {
  return request(`/categories/${categoryId}`, {
    method: 'DELETE',
  })
}

export function listProducts() {
  return request('/products/')
}

export function createProduct(payload) {
  return request('/products/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateProduct(productId, payload) {
  return request(`/products/${productId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteProduct(productId) {
  return request(`/products/${productId}`, {
    method: 'DELETE',
  })
}

export function listUsers() {
  return request('/users/')
}

export function createUser(payload) {
  return request('/users/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function updateUser(userId, payload) {
  return request(`/users/${userId}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export function deleteUser(userId) {
  return request(`/users/${userId}`, {
    method: 'DELETE',
  })
}
