import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  createCategory,
  createProduct,
  createUser,
  deleteCategory,
  deleteProduct,
  deleteUser,
  filterProducts,
  getApiBaseUrl,
  getHealth,
  listCategories,
  listProducts,
  listUsers,
  updateCategory,
  updateProduct,
  updateUser,
} from './api'
import './App.css'

function App() {
  const [health, setHealth] = useState('Chargement...')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [categories, setCategories] = useState([])
  const [products, setProducts] = useState([])
  const [users, setUsers] = useState([])

  const [categoryForm, setCategoryForm] = useState({ name: '', description: '' })
  const [productForm, setProductForm] = useState({
    name: '',
    price: '',
    category_id: '',
  })
  const [userForm, setUserForm] = useState({
    username: '',
    email: '',
    password: '',
  })

  const [editingCategoryId, setEditingCategoryId] = useState(null)
  const [editingProductId, setEditingProductId] = useState(null)
  const [editingUserId, setEditingUserId] = useState(null)

  const [filterForm, setFilterForm] = useState({
    name: '',
    category_id: '',
    min_price: '',
    max_price: '',
  })
  const [filteredProducts, setFilteredProducts] = useState(null)
  const [isFiltering, setIsFiltering] = useState(false)

  const apiBaseUrl = getApiBaseUrl()

  const categoryNameById = useMemo(() => {
    const map = new Map()
    categories.forEach((category) => {
      map.set(category.id, category.name)
    })
    return map
  }, [categories])

  const refreshData = useCallback(async () => {
    setLoading(true)
    setError('')

    try {
      const [healthResponse, categoriesResponse, productsResponse, usersResponse] =
        await Promise.all([
          getHealth(),
          listCategories(),
          listProducts(),
          listUsers(),
        ])

      setHealth(healthResponse.message || 'API en ligne')
      setCategories(categoriesResponse)
      setProducts(productsResponse)
      setUsers(usersResponse)
    } catch (requestError) {
      setHealth('API indisponible')
      setError(requestError.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refreshData()
  }, [refreshData])

  function resetForms() {
    setCategoryForm({ name: '', description: '' })
    setProductForm({ name: '', price: '', category_id: '' })
    setUserForm({ username: '', email: '', password: '' })
    setEditingCategoryId(null)
    setEditingProductId(null)
    setEditingUserId(null)
    setFilterForm({ name: '', category_id: '', min_price: '', max_price: '' })
    setFilteredProducts(null)
    setIsFiltering(false)
  }

  async function handleFilterSubmit(event) {
    event.preventDefault()
    setError('')
    setIsFiltering(true)

    try {
      const results = await filterProducts({
        name: filterForm.name.trim() || undefined,
        category_id: filterForm.category_id || undefined,
        min_price: filterForm.min_price !== '' ? Number(filterForm.min_price) : undefined,
        max_price: filterForm.max_price !== '' ? Number(filterForm.max_price) : undefined,
      })
      setFilteredProducts(results)
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setIsFiltering(false)
    }
  }

  function resetFilter() {
    setFilterForm({ name: '', category_id: '', min_price: '', max_price: '' })
    setFilteredProducts(null)
  }

  async function handleCategorySubmit(event) {
    event.preventDefault()
    setError('')

    if (categoryForm.name.trim().length < 1) {
      setError('Le nom de la categorie est requis.')
      return
    }

    try {
      if (editingCategoryId) {
        await updateCategory(editingCategoryId, {
          name: categoryForm.name.trim(),
          description: categoryForm.description.trim() || null,
        })
      } else {
        await createCategory({
          name: categoryForm.name.trim(),
          description: categoryForm.description.trim() || null,
        })
      }

      setCategoryForm({ name: '', description: '' })
      setEditingCategoryId(null)
      await refreshData()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  async function handleProductSubmit(event) {
    event.preventDefault()
    setError('')

    const normalizedPrice = Number(productForm.price)
    const normalizedCategoryId = Number(productForm.category_id)

    if (productForm.name.trim().length < 1) {
      setError('Le nom du produit est requis.')
      return
    }

    if (!Number.isFinite(normalizedPrice) || normalizedPrice <= 0) {
      setError('Le prix doit etre un nombre strictement positif.')
      return
    }

    if (!Number.isInteger(normalizedCategoryId) || normalizedCategoryId <= 0) {
      setError('La categorie du produit est requise.')
      return
    }

    try {
      const payload = {
        name: productForm.name.trim(),
        price: normalizedPrice,
        category_id: normalizedCategoryId,
      }

      if (editingProductId) {
        await updateProduct(editingProductId, payload)
      } else {
        await createProduct(payload)
      }

      setProductForm({ name: '', price: '', category_id: '' })
      setEditingProductId(null)
      await refreshData()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  async function handleUserSubmit(event) {
    event.preventDefault()
    setError('')

    if (userForm.username.trim().length < 1) {
      setError('Le username est requis.')
      return
    }

    if (userForm.email.trim().length < 1) {
      setError("L'email est requis.")
      return
    }

    const payload = {
      username: userForm.username.trim(),
      email: userForm.email.trim(),
    }

    if (userForm.password.trim().length > 0) {
      if (userForm.password.trim().length < 6) {
        setError('Le mot de passe doit contenir au moins 6 caracteres.')
        return
      }
      payload.password = userForm.password.trim()
    }

    if (!editingUserId && !payload.password) {
      setError('Le mot de passe est obligatoire a la creation.')
      return
    }

    try {
      if (editingUserId) {
        await updateUser(editingUserId, payload)
      } else {
        await createUser(payload)
      }

      setUserForm({ username: '', email: '', password: '' })
      setEditingUserId(null)
      await refreshData()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  function startEditCategory(category) {
    setEditingCategoryId(category.id)
    setCategoryForm({
      name: category.name,
      description: category.description || '',
    })
  }

  function startEditProduct(product) {
    setEditingProductId(product.id)
    setProductForm({
      name: product.name,
      price: String(product.price),
      category_id: String(product.category_id || ''),
    })
  }

  function startEditUser(user) {
    setEditingUserId(user.id)
    setUserForm({
      username: user.username,
      email: user.email,
      password: '',
    })
  }

  async function handleDeleteCategory(categoryId) {
    if (!window.confirm('Supprimer cette categorie ?')) {
      return
    }

    try {
      await deleteCategory(categoryId)
      await refreshData()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  async function handleDeleteProduct(productId) {
    if (!window.confirm('Supprimer ce produit ?')) {
      return
    }

    try {
      await deleteProduct(productId)
      await refreshData()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  async function handleDeleteUser(userId) {
    if (!window.confirm('Supprimer cet utilisateur ?')) {
      return
    }

    try {
      await deleteUser(userId)
      await refreshData()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  return (
    <main className="page-shell">
      <header className="hero">
        <p className="eyebrow">Front-office Shop API</p>
        <h1>Gestion complete du backend ShopApi</h1>
        <p>
          API cible: <code>{apiBaseUrl}</code>
        </p>
        <div className="hero-status">
          <span className="status-dot" />
          <strong>Etat:</strong> {loading ? 'Synchronisation...' : health}
        </div>
        <div className="hero-actions">
          <button type="button" onClick={refreshData}>
            Rafraichir
          </button>
          <button type="button" className="ghost" onClick={resetForms}>
            Reinitialiser formulaires
          </button>
        </div>
        {error ? <p className="error-banner">Erreur: {error}</p> : null}
      </header>

      <section className="grid-layout">
        <article className="card">
          <h2>{editingCategoryId ? 'Modifier categorie' : 'Nouvelle categorie'}</h2>
          <form className="stack" onSubmit={handleCategorySubmit}>
            <label>
              Nom
              <input
                type="text"
                value={categoryForm.name}
                onChange={(event) =>
                  setCategoryForm((previous) => ({
                    ...previous,
                    name: event.target.value,
                  }))
                }
                minLength={1}
                maxLength={100}
                required
              />
            </label>
            <label>
              Description
              <textarea
                value={categoryForm.description}
                onChange={(event) =>
                  setCategoryForm((previous) => ({
                    ...previous,
                    description: event.target.value,
                  }))
                }
                maxLength={500}
                rows={3}
              />
            </label>
            <button type="submit">
              {editingCategoryId ? 'Sauvegarder categorie' : 'Creer categorie'}
            </button>
          </form>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nom</th>
                  <th>Description</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {categories.map((category) => (
                  <tr key={category.id}>
                    <td>{category.id}</td>
                    <td>{category.name}</td>
                    <td>{category.description || '-'}</td>
                    <td className="table-actions">
                      <button type="button" onClick={() => startEditCategory(category)}>
                        Editer
                      </button>
                      <button
                        type="button"
                        className="danger"
                        onClick={() => handleDeleteCategory(category.id)}
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="card">
          <h2>{editingProductId ? 'Modifier produit' : 'Nouveau produit'}</h2>

          <form className="stack" onSubmit={handleProductSubmit}>
            <label>
              Nom
              <input
                type="text"
                value={productForm.name}
                onChange={(event) =>
                  setProductForm((previous) => ({
                    ...previous,
                    name: event.target.value,
                  }))
                }
                minLength={1}
                maxLength={255}
                required
              />
            </label>

            <label>
              Prix
              <input
                type="number"
                value={productForm.price}
                onChange={(event) =>
                  setProductForm((previous) => ({
                    ...previous,
                    price: event.target.value,
                  }))
                }
                min="0.01"
                step="0.01"
                required
              />
            </label>

            <label>
              Categorie
              <select
                value={productForm.category_id}
                onChange={(event) =>
                  setProductForm((previous) => ({
                    ...previous,
                    category_id: event.target.value,
                  }))
                }
                required
              >
                <option value="">Choisir une categorie</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </label>

            <button type="submit">
              {editingProductId ? 'Sauvegarder produit' : 'Creer produit'}
            </button>
          </form>

          <details className="filter-panel">
            <summary>Filtrer les produits {filteredProducts !== null ? <span className="filter-badge">{filteredProducts.length} resultat{filteredProducts.length !== 1 ? 's' : ''}</span> : null}</summary>
            <form className="stack filter-grid" onSubmit={handleFilterSubmit}>
              <label>
                Nom
                <input
                  type="text"
                  value={filterForm.name}
                  onChange={(e) => setFilterForm((p) => ({ ...p, name: e.target.value }))}
                  placeholder="ex: iPhone"
                />
              </label>
              <label>
                Categorie
                <select
                  value={filterForm.category_id}
                  onChange={(e) => setFilterForm((p) => ({ ...p, category_id: e.target.value }))}
                >
                  <option value="">Toutes</option>
                  {categories.map((cat) => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
              </label>
              <label>
                Prix min
                <input
                  type="number"
                  value={filterForm.min_price}
                  onChange={(e) => setFilterForm((p) => ({ ...p, min_price: e.target.value }))}
                  min="0"
                  step="0.01"
                  placeholder="0.00"
                />
              </label>
              <label>
                Prix max
                <input
                  type="number"
                  value={filterForm.max_price}
                  onChange={(e) => setFilterForm((p) => ({ ...p, max_price: e.target.value }))}
                  min="0"
                  step="0.01"
                  placeholder="999.99"
                />
              </label>
              <div className="filter-actions">
                <button type="submit" disabled={isFiltering}>
                  {isFiltering ? 'Recherche...' : 'Filtrer'}
                </button>
                <button type="button" className="ghost" onClick={resetFilter}>
                  Reinitialiser
                </button>
              </div>
            </form>
          </details>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nom</th>
                  <th>Prix</th>
                  <th>Categorie</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {(filteredProducts ?? products).map((product) => (
                  <tr key={product.id}>
                    <td>{product.id}</td>
                    <td>{product.name}</td>
                    <td>{Number(product.price).toFixed(2)} EUR</td>
                    <td>{categoryNameById.get(product.category_id) || 'N/A'}</td>
                    <td className="table-actions">
                      <button type="button" onClick={() => startEditProduct(product)}>
                        Editer
                      </button>
                      <button
                        type="button"
                        className="danger"
                        onClick={() => handleDeleteProduct(product.id)}
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>

        <article className="card full-width">
          <h2>{editingUserId ? 'Modifier utilisateur' : 'Nouvel utilisateur'}</h2>
          <form className="stack three-columns" onSubmit={handleUserSubmit}>
            <label>
              Username
              <input
                type="text"
                value={userForm.username}
                onChange={(event) =>
                  setUserForm((previous) => ({
                    ...previous,
                    username: event.target.value,
                  }))
                }
                minLength={1}
                maxLength={50}
                required
              />
            </label>
            <label>
              Email
              <input
                type="email"
                value={userForm.email}
                onChange={(event) =>
                  setUserForm((previous) => ({
                    ...previous,
                    email: event.target.value,
                  }))
                }
                maxLength={100}
                required
              />
            </label>
            <label>
              {editingUserId ? 'Nouveau mot de passe (optionnel)' : 'Mot de passe'}
              <input
                type="password"
                value={userForm.password}
                onChange={(event) =>
                  setUserForm((previous) => ({
                    ...previous,
                    password: event.target.value,
                  }))
                }
                minLength={editingUserId ? 0 : 6}
                required={!editingUserId}
              />
            </label>
            <button type="submit">
              {editingUserId ? 'Sauvegarder utilisateur' : 'Creer utilisateur'}
            </button>
          </form>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.username}</td>
                    <td>{user.email}</td>
                    <td className="table-actions">
                      <button type="button" onClick={() => startEditUser(user)}>
                        Editer
                      </button>
                      <button
                        type="button"
                        className="danger"
                        onClick={() => handleDeleteUser(user.id)}
                      >
                        Supprimer
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </article>
      </section>
    </main>
  )
}

export default App
