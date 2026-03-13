'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { AuthProvider, useAuth } from '@/lib/auth'
import Header from '@/components/Header'
import { productsApi, categoriesApi, usersApi, Product, Category, User } from '@/lib/api'

function AdminDashboard() {
  const router = useRouter()
  const { user, loading: authLoading } = useAuth()
  
  const [activeTab, setActiveTab] = useState<'products' | 'categories' | 'users'>('products')
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  // Modal states
  const [showProductModal, setShowProductModal] = useState(false)
  const [showCategoryModal, setShowCategoryModal] = useState(false)
  const [showUserModal, setShowUserModal] = useState(false)
  const [editingProduct, setEditingProduct] = useState<Product | null>(null)
  const [editingCategory, setEditingCategory] = useState<Category | null>(null)
  const [editingUser, setEditingUser] = useState<User | null>(null)

  // Form states
  const [productForm, setProductForm] = useState({ name: '', category_id: '', price: '' })
  const [categoryForm, setCategoryForm] = useState({ name: '', description: '' })
  const [userForm, setUserForm] = useState({ username: '', email: '', password: '' })

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login')
    }
  }, [user, authLoading, router])

  useEffect(() => {
    if (user) loadData()
  }, [user])

  async function loadData() {
    try {
      const [prods, cats, usrs] = await Promise.all([
        productsApi.list(),
        categoriesApi.list(),
        usersApi.list()
      ])
      setProducts(prods)
      setCategories(cats)
      setUsers(usrs)
    } catch (err) {
      setError('Erreur de chargement')
    } finally {
      setLoading(false)
    }
  }

  // Products CRUD
  function openProductModal(product?: Product) {
    if (product) {
      setEditingProduct(product)
      setProductForm({
        name: product.name,
        category_id: String(product.category_id),
        price: String(product.price)
      })
    } else {
      setEditingProduct(null)
      setProductForm({ name: '', category_id: categories[0]?.id?.toString() || '', price: '' })
    }
    setShowProductModal(true)
  }

  async function handleProductSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    
    const data = {
      name: productForm.name,
      category_id: Number(productForm.category_id),
      price: Number(productForm.price)
    }

    try {
      if (editingProduct) {
        await productsApi.update(editingProduct.id, data)
        setSuccess('Produit modifie')
      } else {
        await productsApi.create(data)
        setSuccess('Produit cree')
      }
      setShowProductModal(false)
      loadData()
    } catch (err: any) {
      setError(err.message)
    }
  }

  async function handleDeleteProduct(id: number) {
    if (!confirm('Supprimer ce produit?')) return
    try {
      await productsApi.delete(id)
      setSuccess('Produit supprime')
      loadData()
    } catch (err: any) {
      setError(err.message)
    }
  }

  // Categories CRUD
  function openCategoryModal(category?: Category) {
    if (category) {
      setEditingCategory(category)
      setCategoryForm({ name: category.name, description: category.description || '' })
    } else {
      setEditingCategory(null)
      setCategoryForm({ name: '', description: '' })
    }
    setShowCategoryModal(true)
  }

  async function handleCategorySubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')

    try {
      if (editingCategory) {
        await categoriesApi.update(editingCategory.id, categoryForm)
        setSuccess('Categorie modifiee')
      } else {
        await categoriesApi.create(categoryForm)
        setSuccess('Categorie creee')
      }
      setShowCategoryModal(false)
      loadData()
    } catch (err: any) {
      setError(err.message)
    }
  }

  async function handleDeleteCategory(id: number) {
    if (!confirm('Supprimer cette categorie?')) return
    try {
      await categoriesApi.delete(id)
      setSuccess('Categorie supprimee')
      loadData()
    } catch (err: any) {
      setError(err.message)
    }
  }

  // Users CRUD
  function openUserModal(userItem?: User) {
    if (userItem) {
      setEditingUser(userItem)
      setUserForm({ username: userItem.username, email: userItem.email, password: '' })
    } else {
      setEditingUser(null)
      setUserForm({ username: '', email: '', password: '' })
    }
    setShowUserModal(true)
  }

  async function handleUserSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')

    try {
      if (editingUser) {
        const updateData: { username?: string; email?: string; password?: string } = {
          username: userForm.username,
          email: userForm.email,
        }
        if (userForm.password) {
          updateData.password = userForm.password
        }
        await usersApi.update(editingUser.id, updateData)
        setSuccess('Utilisateur modifie')
      } else {
        await usersApi.create(userForm)
        setSuccess('Utilisateur cree')
      }
      setShowUserModal(false)
      loadData()
    } catch (err: any) {
      setError(err.message)
    }
  }

  async function handleDeleteUser(id: number) {
    if (!confirm('Supprimer cet utilisateur?')) return
    try {
      await usersApi.delete(id)
      setSuccess('Utilisateur supprime')
      loadData()
    } catch (err: any) {
      setError(err.message)
    }
  }

  function getCategoryName(catId: number) {
    return categories.find(c => c.id === catId)?.name || 'Inconnue'
  }

  if (authLoading || !user) {
    return <div className="empty-state">Chargement...</div>
  }

  return (
    <>
      <Header />
      <main className="container">
        <div className="page-header">
          <h1 className="page-title">Administration</h1>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'products' ? 'active' : ''}`}
            onClick={() => setActiveTab('products')}
          >
            Produits ({products.length})
          </button>
          <button
            className={`tab ${activeTab === 'categories' ? 'active' : ''}`}
            onClick={() => setActiveTab('categories')}
          >
            Categories ({categories.length})
          </button>
          <button
            className={`tab ${activeTab === 'users' ? 'active' : ''}`}
            onClick={() => setActiveTab('users')}
          >
            Utilisateurs ({users.length})
          </button>
        </div>

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div className="card">
            <div className="card-header">
              <span className="card-title">Gestion des produits</span>
              <button className="btn btn-primary" onClick={() => openProductModal()}>
                + Nouveau produit
              </button>
            </div>

            {loading ? (
              <div className="empty-state">Chargement...</div>
            ) : products.length === 0 ? (
              <div className="empty-state">Aucun produit</div>
            ) : (
              <div className="table-wrapper">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nom</th>
                      <th>Categorie</th>
                      <th>Prix</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {products.map(product => (
                      <tr key={product.id}>
                        <td>{product.id}</td>
                        <td>{product.name}</td>
                        <td><span className="badge">{getCategoryName(product.category_id)}</span></td>
                        <td>{product.price.toFixed(2)} EUR</td>
                        <td>
                          <div className="actions">
                            <button className="btn btn-outline btn-sm" onClick={() => openProductModal(product)}>
                              Modifier
                            </button>
                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteProduct(product.id)}>
                              Supprimer
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Categories Tab */}
        {activeTab === 'categories' && (
          <div className="card">
            <div className="card-header">
              <span className="card-title">Gestion des categories</span>
              <button className="btn btn-primary" onClick={() => openCategoryModal()}>
                + Nouvelle categorie
              </button>
            </div>

            {loading ? (
              <div className="empty-state">Chargement...</div>
            ) : categories.length === 0 ? (
              <div className="empty-state">Aucune categorie</div>
            ) : (
              <div className="table-wrapper">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Nom</th>
                      <th>Description</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {categories.map(category => (
                      <tr key={category.id}>
                        <td>{category.id}</td>
                        <td>{category.name}</td>
                        <td>{category.description || '-'}</td>
                        <td>
                          <div className="actions">
                            <button className="btn btn-outline btn-sm" onClick={() => openCategoryModal(category)}>
                              Modifier
                            </button>
                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteCategory(category.id)}>
                              Supprimer
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="card">
            <div className="card-header">
              <span className="card-title">Gestion des utilisateurs</span>
              <button className="btn btn-primary" onClick={() => openUserModal()}>
                + Nouvel utilisateur
              </button>
            </div>

            {loading ? (
              <div className="empty-state">Chargement...</div>
            ) : users.length === 0 ? (
              <div className="empty-state">Aucun utilisateur</div>
            ) : (
              <div className="table-wrapper">
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map(u => (
                      <tr key={u.id}>
                        <td>{u.id}</td>
                        <td>{u.username}</td>
                        <td>{u.email}</td>
                        <td>
                          <div className="actions">
                            <button className="btn btn-outline btn-sm" onClick={() => openUserModal(u)}>
                              Modifier
                            </button>
                            <button className="btn btn-danger btn-sm" onClick={() => handleDeleteUser(u.id)}>
                              Supprimer
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Product Modal */}
        {showProductModal && (
          <div className="modal-overlay" onClick={() => setShowProductModal(false)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <span className="modal-title">{editingProduct ? 'Modifier le produit' : 'Nouveau produit'}</span>
                <button className="btn btn-outline btn-sm" onClick={() => setShowProductModal(false)}>X</button>
              </div>
              <form onSubmit={handleProductSubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <label className="form-label">Nom</label>
                    <input
                      type="text"
                      className="form-input"
                      value={productForm.name}
                      onChange={e => setProductForm({ ...productForm, name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Categorie</label>
                    <select
                      className="form-input"
                      value={productForm.category_id}
                      onChange={e => setProductForm({ ...productForm, category_id: e.target.value })}
                      required
                    >
                      <option value="">Selectionnez</option>
                      {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Prix (EUR)</label>
                    <input
                      type="number"
                      step="0.01"
                      min="0.01"
                      className="form-input"
                      value={productForm.price}
                      onChange={e => setProductForm({ ...productForm, price: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline" onClick={() => setShowProductModal(false)}>
                    Annuler
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingProduct ? 'Enregistrer' : 'Creer'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Category Modal */}
        {showCategoryModal && (
          <div className="modal-overlay" onClick={() => setShowCategoryModal(false)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <span className="modal-title">{editingCategory ? 'Modifier la categorie' : 'Nouvelle categorie'}</span>
                <button className="btn btn-outline btn-sm" onClick={() => setShowCategoryModal(false)}>X</button>
              </div>
              <form onSubmit={handleCategorySubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <label className="form-label">Nom</label>
                    <input
                      type="text"
                      className="form-input"
                      value={categoryForm.name}
                      onChange={e => setCategoryForm({ ...categoryForm, name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Description</label>
                    <input
                      type="text"
                      className="form-input"
                      value={categoryForm.description}
                      onChange={e => setCategoryForm({ ...categoryForm, description: e.target.value })}
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline" onClick={() => setShowCategoryModal(false)}>
                    Annuler
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingCategory ? 'Enregistrer' : 'Creer'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* User Modal */}
        {showUserModal && (
          <div className="modal-overlay" onClick={() => setShowUserModal(false)}>
            <div className="modal" onClick={e => e.stopPropagation()}>
              <div className="modal-header">
                <span className="modal-title">{editingUser ? 'Modifier utilisateur' : 'Nouvel utilisateur'}</span>
                <button className="btn btn-outline btn-sm" onClick={() => setShowUserModal(false)}>X</button>
              </div>
              <form onSubmit={handleUserSubmit}>
                <div className="modal-body">
                  <div className="form-group">
                    <label className="form-label">Username</label>
                    <input
                      type="text"
                      className="form-input"
                      value={userForm.username}
                      onChange={e => setUserForm({ ...userForm, username: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-input"
                      value={userForm.email}
                      onChange={e => setUserForm({ ...userForm, email: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">
                      Mot de passe {editingUser && <span style={{ fontWeight: 'normal', color: '#888' }}>(laisser vide pour ne pas changer)</span>}
                    </label>
                    <input
                      type="password"
                      className="form-input"
                      value={userForm.password}
                      onChange={e => setUserForm({ ...userForm, password: e.target.value })}
                      required={!editingUser}
                      minLength={6}
                    />
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-outline" onClick={() => setShowUserModal(false)}>
                    Annuler
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingUser ? 'Enregistrer' : 'Creer'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </main>
    </>
  )
}

export default function AdminPage() {
  return (
    <AuthProvider>
      <AdminDashboard />
    </AuthProvider>
  )
}
