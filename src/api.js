const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

function getAuthHeader() {
  const token = localStorage.getItem('token')
  if (!token) return {}
  return { 'Authorization': `Bearer ${token}` }
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
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

export function getToken() {
  return localStorage.getItem('token')
}

export function setToken(token) {
  if (token) {
    localStorage.setItem('token', token)
  } else {
    localStorage.removeItem('token')
  }
}

export function clearAuth() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
}

// Auth endpoints
export function register(payload) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function login(payload) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function logout() {
  return request('/auth/logout', { method: 'POST' })
}

export function getCurrentUser() {
  const token = getAuthHeader()['Authorization']
  if (!token) return Promise.resolve(null)
  return request('/auth/me', {
    headers: { 'Authorization': token },
  }).catch(() => null)
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

export function filterProducts({ category_id, min_price, max_price, name } = {}) {
  const params = new URLSearchParams()
  if (category_id) params.set('category_id', category_id)
  if (min_price !== '' && min_price != null) params.set('min_price', min_price)
  if (max_price !== '' && max_price != null) params.set('max_price', max_price)
  if (name) params.set('name', name)
  const query = params.toString()
  return request(`/products/filter${query ? '?' + query : ''}`)
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
