import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { format } from 'date-fns'

function Dashboard() {
  const [stats, setStats] = useState({
    vignettes: 0,
    photos: 0,
    audio: 0,
    files: 0,
  })
  const [recentVignettes, setRecentVignettes] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [vignettesRes, photosRes, audioRes, filesRes] = await Promise.all([
        axios.get('/api/vignettes'),
        axios.get('/api/photos?limit=1'),
        axios.get('/api/audio'),
        axios.get('/api/files'),
      ])

      setStats({
        vignettes: vignettesRes.data.length,
        photos: photosRes.data.length || 0,
        audio: audioRes.data.length,
        files: filesRes.data.length,
      })

      setRecentVignettes(vignettesRes.data.slice(0, 5))
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div>
      <div style={{ marginBottom: '3rem' }}>
        <h1>Family Memories</h1>
        <p style={{
          fontSize: '1.2rem',
          color: 'var(--text-secondary)',
          marginTop: '-1rem',
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
        }}>
          Preserving stories for generations to come
        </p>
      </div>

      <div className="grid grid-4">
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>Vignettes</h3>
          <p style={{
            fontSize: '3rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            marginBottom: '1rem'
          }}>
            {stats.vignettes}
          </p>
          <Link to="/vignettes" style={{
            fontSize: '1rem',
            fontWeight: '500',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
          }}>View all stories →</Link>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>Photos</h3>
          <p style={{
            fontSize: '3rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            marginBottom: '1rem'
          }}>
            {stats.photos}
          </p>
          <Link to="/photos" style={{
            fontSize: '1rem',
            fontWeight: '500',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
          }}>View gallery →</Link>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>Audio</h3>
          <p style={{
            fontSize: '3rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            marginBottom: '1rem'
          }}>
            {stats.audio}
          </p>
          <Link to="/audio" style={{
            fontSize: '1rem',
            fontWeight: '500',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
          }}>Listen →</Link>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <h3 style={{ color: 'var(--primary)', marginBottom: '1rem' }}>Files</h3>
          <p style={{
            fontSize: '3rem',
            fontWeight: '700',
            background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            marginBottom: '1rem'
          }}>
            {stats.files}
          </p>
          <Link to="/files" style={{
            fontSize: '1rem',
            fontWeight: '500',
            fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
          }}>Browse →</Link>
        </div>
      </div>

      <div style={{ marginTop: '3rem' }}>
        <h2 style={{ marginBottom: '1.5rem' }}>Recent Vignettes</h2>
        {recentVignettes.length === 0 ? (
          <div className="container" style={{ textAlign: 'center', padding: '3rem' }}>
            <p style={{
              fontSize: '1.1rem',
              color: 'var(--text-secondary)',
              fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
            }}>
              No vignettes yet. <Link to="/vignettes" style={{ fontWeight: '600' }}>Create your first story</Link> and start preserving your family memories.
            </p>
          </div>
        ) : (
          <div className="grid grid-2">
            {recentVignettes.map((vignette) => (
              <div key={vignette.id} className="card">
                <h3 style={{ marginBottom: '0.75rem' }}>{vignette.title}</h3>
                <p style={{
                  color: 'var(--text-muted)',
                  marginBottom: '1rem',
                  fontSize: '0.9rem',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
                }}>
                  {format(new Date(vignette.created_at), 'MMMM d, yyyy')}
                </p>
                <p style={{
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical',
                  color: 'var(--text-secondary)',
                  lineHeight: '1.7',
                  marginBottom: '1.25rem'
                }}>
                  {vignette.content || 'No content'}
                </p>
                <Link to={`/vignettes`} style={{
                  fontWeight: '500',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif'
                }}>Read more →</Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard

