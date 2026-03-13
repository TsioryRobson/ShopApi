'use client'

import { useState, useEffect } from 'react'
import { AuthProvider } from '@/lib/auth'
import Header from '@/components/Header'
import { productsApi, categoriesApi, Product, Category } from '@/lib/api'

function ShopPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  // Filtres
  const [searchName, setSearchName] = useState('')
  const [minPrice, setMinPrice] = useState('')
  const [maxPrice, setMaxPrice] = useState('')
  const [categoryId, setCategoryId] = useState('')

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const [prods, cats] = await Promise.all([
        productsApi.list(),
        categoriesApi.list()
      ])
      setProducts(prods)
      setCategories(cats)
    } catch (err) {
      setError('Impossible de charger les produits')
    } finally {
      setLoading(false)
    }
  }

  async function handleSearch() {
    setLoading(true)
    setError('')
    try {
      const results = await productsApi.filter({
        name: searchName || undefined,
        min_price: minPrice ? Number(minPrice) : undefined,
        max_price: maxPrice ? Number(maxPrice) : undefined,
        category_id: categoryId ? Number(categoryId) : undefined,
      })
      setProducts(results)
    } catch (err) {
      setError('Erreur lors de la recherche')
    } finally {
      setLoading(false)
    }
  }

  function resetFilters() {
    setSearchName('')
    setMinPrice('')
    setMaxPrice('')
    setCategoryId('')
    loadData()
  }

  function getCategoryName(catId: number) {
    return categories.find(c => c.id === catId)?.name || 'Inconnue'
  }

  return (
    <>
      <Header />
      <main className="shop-page container">
        <div className="page-header">
          <div>
            <h1 className="page-title">Boutique</h1>
            <p className="text-muted">Explorez notre catalogue de produits</p>
          </div>
        </div>

        {/* Section recherche */}
        <div className="search-section">
          <div className="search-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="11" cy="11" r="8"/>
              <path d="m21 21-4.35-4.35"/>
            </svg>
            Rechercher des produits
          </div>
          <div className="search-filters">
            <div className="form-group">
              <label className="form-label">Nom du produit</label>
              <input
                type="text"
                className="form-input"
                placeholder="Ex: iPhone, Chaise..."
                value={searchName}
                onChange={(e) => setSearchName(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Prix minimum</label>
              <input
                type="number"
                className="form-input"
                placeholder="0"
                value={minPrice}
                onChange={(e) => setMinPrice(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Prix maximum</label>
              <input
                type="number"
                className="form-input"
                placeholder="1000"
                value={maxPrice}
                onChange={(e) => setMaxPrice(e.target.value)}
              />
            </div>
            <div className="form-group">
              <label className="form-label">Categorie</label>
              <select
                className="form-input"
                value={categoryId}
                onChange={(e) => setCategoryId(e.target.value)}
              >
                <option value="">Toutes les categories</option>
                {categories.map(cat => (
                  <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
              </select>
            </div>
            <div className="form-group" style={{ display: 'flex', gap: '0.5rem', alignItems: 'flex-end' }}>
              <button onClick={handleSearch} className="btn btn-primary">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="m21 21-4.35-4.35"/>
                </svg>
                Rechercher
              </button>
              <button onClick={resetFilters} className="btn btn-outline">
                Reset
              </button>
            </div>
          </div>
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        <div className="results-count">
          {loading ? 'Chargement...' : `${products.length} produit(s) trouve(s)`}
        </div>

        {loading ? (
          <div className="empty-state">
            <div className="empty-state-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10"/>
                <polyline points="12 6 12 12 16 14"/>
              </svg>
            </div>
            <p>Chargement des produits...</p>
          </div>
        ) : products.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">
              <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
                <line x1="8" y1="11" x2="14" y2="11"/>
              </svg>
            </div>
            <p>Aucun produit trouve</p>
            <button onClick={resetFilters} className="btn btn-outline" style={{ marginTop: '1rem' }}>
              Reinitialiser les filtres
            </button>
          </div>
        ) : (
          <div className="products-grid">
            {products.map(product => (
              <div key={product.id} className="product-card">
                <div className="product-image">
                  <div className="product-image-placeholder">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                      <circle cx="8.5" cy="8.5" r="1.5"/>
                      <polyline points="21 15 16 10 5 21"/>
                    </svg>
                    <span>Image produit</span>
                  </div>
                </div>
                <div className="product-content">
                  <div className="product-name">{product.name}</div>
                  <div className="product-category">
                    <span className="badge">{getCategoryName(product.category_id)}</span>
                  </div>
                  <div className="product-price">
                    {product.price.toFixed(2)} <span className="product-price-small">EUR</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="footer">
        <p className="footer-text">ShopAPI - Projet e-commerce FastAPI + Next.js</p>
      </footer>
    </>
  )
}

export default function Shop() {
  return (
    <AuthProvider>
      <ShopPage />
    </AuthProvider>
  )
}
