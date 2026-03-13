// Configuration de l'API
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Types
export interface Product {
  id: number
  name: string
  category_id: number
  price: number
}

export interface Category {
  id: number
  name: string
  description: string | null
}

export interface User {
  id: number
  username: string
  email: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

// Helper pour les requêtes
async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Erreur serveur' }))
    throw new Error(error.detail || `Erreur ${res.status}`)
  }

  return res.json()
}

// Auth API
export const authApi = {
  login: (email: string, password: string) =>
    request<AuthResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  register: (username: string, email: string, password: string) =>
    request<AuthResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    }),

  me: () => request<User>('/auth/me'),
}

// Products API
export const productsApi = {
  list: () => request<Product[]>('/products/'),

  filter: (params: {
    category_id?: number
    min_price?: number
    max_price?: number
    name?: string
  }) => {
    const searchParams = new URLSearchParams()
    if (params.category_id) searchParams.set('category_id', String(params.category_id))
    if (params.min_price) searchParams.set('min_price', String(params.min_price))
    if (params.max_price) searchParams.set('max_price', String(params.max_price))
    if (params.name) searchParams.set('name', params.name)
    return request<Product[]>(`/products/filter?${searchParams}`)
  },

  get: (id: number) => request<Product>(`/products/${id}`),

  create: (data: Omit<Product, 'id'>) =>
    request<Product>('/products/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: Partial<Omit<Product, 'id'>>) =>
    request<Product>(`/products/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    request<{ message: string }>(`/products/${id}`, {
      method: 'DELETE',
    }),
}

// Categories API
export const categoriesApi = {
  list: () => request<Category[]>('/categories/'),

  get: (id: number) => request<Category>(`/categories/${id}`),

  create: (data: Omit<Category, 'id'>) =>
    request<Category>('/categories/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: Partial<Omit<Category, 'id'>>) =>
    request<Category>(`/categories/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    request<{ message: string }>(`/categories/${id}`, {
      method: 'DELETE',
    }),
}

// Users API (admin only - requires auth)
export const usersApi = {
  list: () => request<User[]>('/users/'),

  get: (id: number) => request<User>(`/users/${id}`),

  create: (data: { username: string; email: string; password: string }) =>
    request<User>('/users/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: { username?: string; email?: string; password?: string }) =>
    request<User>(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number) =>
    request<{ message: string }>(`/users/${id}`, {
      method: 'DELETE',
    }),
}
