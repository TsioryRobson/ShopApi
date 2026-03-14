import { useState } from 'react'
import { LogOut, MoonStar, SunMedium, UserRound } from 'lucide-react'
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
          <h1>ShopAPI</h1>
          <p>E-commerce cockpit</p>
        </div>

        <div className="navbar-right">
          <button 
            className="btn-theme"
            onClick={onToggleDarkMode}
            title={isDark ? 'Mode clair' : 'Mode sombre'}
          >
            {isDark ? <SunMedium size={16} /> : <MoonStar size={16} />}
          </button>

          {user && (
            <div className="user-info">
              <span className="user-name"><UserRound size={14} /> {user.username}</span>
              <button 
                className="btn btn-logout"
                onClick={handleLogout}
                disabled={loading}
              >
                <LogOut size={14} />
                {loading ? 'Deconnexion...' : 'Deconnexion'}
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}
