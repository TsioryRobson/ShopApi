import { useState } from 'react'
import { logout, clearAuth } from '../api'

export default function Navbar({ user, onLogout, isDark, onToggleDarkMode }) {
  const [loading, setLoading] = useState(false)

  async function handleLogout() {
    setLoading(true)
    try {
      await logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      clearAuth()
      onLogout()
      setLoading(false)
    }
  }

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <div className="navbar-brand">
          <h1>🛍️ ShopAPI</h1>
          <p>Gestion de produits</p>
        </div>

        <div className="navbar-right">
          <button 
            className="btn-theme"
            onClick={onToggleDarkMode}
            title={isDark ? 'Mode clair' : 'Mode sombre'}
          >
            {isDark ? '☀️' : '🌙'}
          </button>

          {user && (
            <div className="user-info">
              <span className="user-name">👤 {user.username}</span>
              <button 
                className="btn btn-logout"
                onClick={handleLogout}
                disabled={loading}
              >
                {loading ? 'Déconnexion...' : 'Déconnexion'}
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
