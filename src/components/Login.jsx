import { useState } from 'react'
import { ArrowRight, Lock, Mail, ShieldCheck } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { login, setToken, getCurrentUser } from '../api'

export default function Login({ onLoginSuccess, onSwitchToRegister }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await login({ email, password })
      setToken(response.access_token)
      const user = await getCurrentUser()
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
      }
      toast.success('Connexion reussie')
      onLoginSuccess()
    } catch (err) {
      const message = err.message || 'Erreur de connexion'
      setError(message)
      toast.error(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <div className="auth-orb auth-orb-left" />
      <div className="auth-orb auth-orb-right" />
      <div className="auth-card">
        <div className="auth-brand">
          <span><ShieldCheck size={15} /> Premium Access</span>
          <h1>ShopAPI</h1>
          <h2>Connexion</h2>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Adresse email</label>
            <div className="input-wrap">
              <Mail size={14} />
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Entrez votre email"
                required
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Mot de passe</label>
            <div className="input-wrap">
              <Lock size={14} />
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Entrez votre mot de passe"
                required
                disabled={loading}
              />
            </div>
          </div>

          <button 
            type="submit" 
            className="btn btn-primary btn-full"
            disabled={loading}
          >
            <ArrowRight size={15} />
            {loading ? 'Connexion en cours...' : 'Se connecter'}
          </button>
        </form>

        <div className="auth-footer">
          <p>Pas encore de compte? 
            <button 
              type="button"
              className="link-btn"
              onClick={onSwitchToRegister}
            >
              S'inscrire
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}
