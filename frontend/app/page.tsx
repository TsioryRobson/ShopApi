'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { AuthProvider } from '@/lib/auth'
import Header from '@/components/Header'
import { productsApi, categoriesApi, Product, Category } from '@/lib/api'

function HomePage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const [prods, cats] = await Promise.all([
        productsApi.list(),
        categoriesApi.list()
      ])
      setProducts(prods.slice(0, 4))
      setCategories(cats)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  function getCategoryName(catId: number) {
    return categories.find(c => c.id === catId)?.name || 'Categorie'
  }

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-badge">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
            </svg>
            ShopAPI - E-commerce moderne
          </div>
          
          <h1 className="hero-title">
            Decouvrez nos <span>produits</span> exceptionnels
          </h1>
          
          <p className="hero-description">
            Une experience shopping moderne et intuitive. 
            Explorez notre catalogue et trouvez exactement ce que vous cherchez.
          </p>
          
          <div className="hero-buttons">
            <Link href="/shop" className="btn btn-primary btn-lg">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="9" cy="21" r="1"/>
                <circle cx="20" cy="21" r="1"/>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
              </svg>
              Explorer la boutique
            </Link>
            <Link href="/login" className="btn btn-secondary btn-lg">
              Espace Admin
            </Link>
          </div>
          
          <div className="hero-stats">
            <div className="hero-stat">
              <div className="hero-stat-value">{loading ? '...' : products.length * 25}+</div>
              <div className="hero-stat-label">Produits</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">{loading ? '...' : categories.length}</div>
              <div className="hero-stat-label">Categories</div>
            </div>
            <div className="hero-stat">
              <div className="hero-stat-value">24/7</div>
              <div className="hero-stat-label">Support</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="section-header">
          <h2 className="section-title">Pourquoi nous choisir ?</h2>
          <p className="section-subtitle">Une plateforme conçue pour vous offrir la meilleure experience</p>
        </div>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                <line x1="12" y1="22.08" x2="12" y2="12"/>
              </svg>
            </div>
            <h3 className="feature-title">Catalogue complet</h3>
            <p className="feature-desc">Des centaines de produits organises par categories pour faciliter votre recherche.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
              </svg>
            </div>
            <h3 className="feature-title">Recherche avancee</h3>
            <p className="feature-desc">Filtrez par nom, prix, categorie. Trouvez exactement ce dont vous avez besoin.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <line x1="3" y1="9" x2="21" y2="9"/>
                <line x1="9" y1="21" x2="9" y2="9"/>
              </svg>
            </div>
            <h3 className="feature-title">Interface moderne</h3>
            <p className="feature-desc">Une experience utilisateur fluide et agreable sur tous vos appareils.</p>
          </div>
        </div>
      </section>

      {/* Preview Products */}
      {!loading && products.length > 0 && (
        <section className="container" style={{ padding: '4rem 1rem' }}>
          <div className="section-header">
            <h2 className="section-title">Aperçu des produits</h2>
            <p className="section-subtitle">Quelques-uns de nos articles disponibles</p>
          </div>
          
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
          
          <div className="text-center mt-1" style={{ marginTop: '2rem' }}>
            <Link href="/shop" className="btn btn-primary btn-lg">
              Voir tous les produits
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="5" y1="12" x2="19" y2="12"/>
                <polyline points="12 5 19 12 12 19"/>
              </svg>
            </Link>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className="footer">
        <p className="footer-text">ShopAPI - Projet e-commerce FastAPI + Next.js</p>
      </footer>
    </>
  )
}

export default function Home() {
  return (
    <AuthProvider>
      <HomePage />
    </AuthProvider>
  )
}
