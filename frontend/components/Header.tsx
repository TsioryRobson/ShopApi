'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useAuth } from '@/lib/auth'

export default function Header() {
  const { user, logout, loading } = useAuth()
  const pathname = usePathname()

  return (
    <header className="header">
      <div className="header-content">
        <Link href="/" className="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ display: 'inline', marginRight: '0.5rem', verticalAlign: 'middle' }}>
            <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
            <line x1="3" y1="6" x2="21" y2="6"/>
            <path d="M16 10a4 4 0 0 1-8 0"/>
          </svg>
          ShopAPI
        </Link>
        
        <nav className="nav">
          <Link 
            href="/" 
            className={`nav-link ${pathname === '/' ? 'active' : ''}`}
          >
            Accueil
          </Link>
          <Link 
            href="/shop" 
            className={`nav-link ${pathname === '/shop' ? 'active' : ''}`}
          >
            Boutique
          </Link>
          
          {!loading && (
            <>
              {user ? (
                <>
                  <Link 
                    href="/admin" 
                    className={`nav-link ${pathname === '/admin' ? 'active' : ''}`}
                  >
                    Admin
                  </Link>
                  <span className="text-muted" style={{ padding: '0.5rem', fontSize: '0.875rem' }}>
                    {user.username}
                  </span>
                  <button onClick={logout} className="btn btn-outline btn-sm">
                    Deconnexion
                  </button>
                </>
              ) : (
                <Link href="/login" className="btn btn-primary btn-sm">
                  Connexion
                </Link>
              )}
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
