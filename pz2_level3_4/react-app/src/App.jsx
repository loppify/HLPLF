import React, { useState, useEffect } from 'react';
import './App.css';

const initDB = () => {
  if (!localStorage.getItem('mp_users')) localStorage.setItem('mp_users', JSON.stringify([]));
  if (!localStorage.getItem('mp_reviews')) localStorage.setItem('mp_reviews', JSON.stringify([]));
};

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [sessionLoaded, setSessionLoaded] = useState(false);
  const [theme, setTheme] = useState(() => localStorage.getItem('mp_theme') || 'light');

  useEffect(() => {
    initDB();
    const session = localStorage.getItem('mp_session');
    if (session) setCurrentUser(JSON.parse(session));
    setSessionLoaded(true);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('mp_theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleLogin = (user) => {
    setCurrentUser(user);
    localStorage.setItem('mp_session', JSON.stringify(user));
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('mp_session');
  };

  if (!sessionLoaded) return null;

  return (
    <div className="app-wrapper">
      <header>
        <div className="header-content">
          <h1>MarketPulse</h1>
          <p className="subtitle">Платформа для аналізу та відгуків</p>
        </div>
        <button className="theme-toggle" onClick={toggleTheme} title="Перемкнути тему">
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
      </header>

      {!currentUser ? (
        <Auth onLogin={handleLogin} />
      ) : (
        <Dashboard user={currentUser} onLogout={handleLogout} />
      )}
    </div>
  );
}

function Auth({ onLogin }) {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const users = JSON.parse(localStorage.getItem('mp_users'));

    if (isRegister) {
      if (users.find(u => u.username === form.username)) {
        setError('Користувач з таким логіном вже існує');
        return;
      }
      const newUser = { ...form, id: Date.now(), info: 'Новий користувач' };
      localStorage.setItem('mp_users', JSON.stringify([...users, newUser]));
      onLogin(newUser);
    } else {
      const user = users.find(u => u.username === form.username && u.password === form.password);
      if (user) {
        onLogin(user);
      } else {
        setError('Невірний логін або пароль');
      }
    }
  };

  return (
    <div className="panel auth-container">
      <h2>{isRegister ? 'Реєстрація' : 'Вхід у систему'}</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '1rem' }}>
          <label className="form-label">Логін</label>
          <input 
            className="input-field"
            value={form.username}
            onChange={e => setForm({...form, username: e.target.value})}
            required
          />
        </div>
        <div style={{ marginBottom: '1.5rem' }}>
          <label className="form-label">Пароль</label>
          <input 
            type="password"
            className="input-field"
            value={form.password}
            onChange={e => setForm({...form, password: e.target.value})}
            required
          />
        </div>
        {error && <p style={{ color: 'var(--danger-text)', fontSize: '0.875rem', marginBottom: '1rem' }}>{error}</p>}
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <button type="submit" className="btn btn-primary">
            {isRegister ? 'Зареєструватися' : 'Увійти'}
          </button>
          <button 
            type="button"
            className="btn btn-ghost" 
            onClick={() => { setIsRegister(!isRegister); setError(''); }}
          >
            {isRegister ? 'Вже є акаунт? Увідіть' : 'Немає акаунта? Створіть'}
          </button>
        </div>
      </form>
    </div>
  );
}

function Dashboard({ user, onLogout }) {
  const [reviews, setReviews] = useState([]);
  const [profile, setProfile] = useState(user);

  useEffect(() => {
    const allReviews = JSON.parse(localStorage.getItem('mp_reviews')) || [];
    setReviews(allReviews);
  }, []);

  const addReview = (newReview) => {
    const updated = [newReview, ...reviews];
    setReviews(updated);
    localStorage.setItem('mp_reviews', JSON.stringify(updated));
  };

  const deleteReview = (id) => {
    const updated = reviews.filter(r => r.id !== id);
    setReviews(updated);
    localStorage.setItem('mp_reviews', JSON.stringify(updated));
  };

  const updateProfile = (updatedUser) => {
    setProfile(updatedUser);
    const users = JSON.parse(localStorage.getItem('mp_users'));
    const updatedUsers = users.map(u => u.id === updatedUser.id ? updatedUser : u);
    localStorage.setItem('mp_users', JSON.stringify(updatedUsers));
    localStorage.setItem('mp_session', JSON.stringify(updatedUser));
  };

  return (
    <div>
      <div className="top-bar">
        <div className="user-info">
          <div className="avatar">{profile.username[0].toUpperCase()}</div>
          <span>{profile.username}</span>
        </div>
        <button className="btn btn-ghost" onClick={onLogout}>Вийти</button>
      </div>

      <div className="dashboard-layout">
        <aside className="dashboard-sidebar">
          <div className="panel">
            <h3>Профіль</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>{profile.info}</p>
            <button className="btn btn-ghost" style={{ width: '100%' }} onClick={() => {
              const info = prompt('Новий статус:', profile.info);
              if (info) updateProfile({...profile, info});
            }}>Редагувати статус</button>
          </div>
          
          <div className="panel">
            <h3 style={{ marginBottom: '1rem' }}>Новий відгук</h3>
            <ReviewForm onAdd={addReview} author={profile.username} />
          </div>
        </aside>

        <main className="dashboard-main">
          <h3 style={{ marginBottom: '1rem' }}>Стрічка відгуків</h3>
          
          {reviews.length === 0 ? (
            <div className="panel" style={{ textAlign: 'center', padding: '3rem 1rem' }}>
              <p style={{ color: 'var(--text-muted)' }}>Відгуків поки немає. Станьте першим!</p>
            </div>
          ) : (
            reviews.map(rev => (
              <ReviewCard 
                key={rev.id} 
                review={rev} 
                canDelete={rev.author === profile.username}
                onDelete={deleteReview}
              />
            ))
          )}
        </main>
      </div>
    </div>
  );
}

function ReviewForm({ onAdd, author }) {
  const [data, setData] = useState({ product: '', text: '', rating: 5, badQuality: false });

  const submit = (e) => {
    e.preventDefault();
    if (!data.product.trim() || !data.text.trim()) return;
    
    onAdd({ ...data, id: Date.now(), author });
    setData({ product: '', text: '', rating: 5, badQuality: false });
  };

  return (
    <form onSubmit={submit}>
      <div style={{ marginBottom: '1rem' }}>
        <label className="form-label">Назва товару</label>
        <input 
          className="input-field" 
          value={data.product} 
          onChange={e => setData({...data, product: e.target.value})}
          required 
        />
      </div>
      
      <div style={{ marginBottom: '1rem' }}>
        <label className="form-label">Відгук</label>
        <textarea 
          className="input-field" 
          value={data.text} 
          onChange={e => setData({...data, text: e.target.value})}
          required 
        />
      </div>
      
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', alignItems: 'flex-end' }}>
         <div style={{ flex: 1 }}>
            <label className="form-label">Оцінка</label>
            <select 
              className="input-field" 
              value={data.rating}
              onChange={e => setData({...data, rating: Number(e.target.value)})}
            >
              {[5,4,3,2,1].map(n => <option key={n} value={n}>{n} ★</option>)}
            </select>
         </div>
         <div style={{ flex: 1, paddingBottom: '0.625rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
               <input 
                 type="checkbox" 
                 checked={data.badQuality} 
                 onChange={e => setData({...data, badQuality: e.target.checked})} 
               />
               <span style={{ fontSize: '0.875rem', fontWeight: 500 }}>Брак</span>
            </label>
         </div>
      </div>
      
      <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>Опублікувати</button>
    </form>
  );
}

function ReviewCard({ review, canDelete, onDelete }) {
  return (
    <div className="review-card">
      <div className="review-header">
        <div className="rating-stars">{'★'.repeat(review.rating)}{'☆'.repeat(5-review.rating)}</div>
        {review.badQuality && <span className="tag tag-bad">Брак</span>}
      </div>
      
      <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>{review.product}</h3>
      <p className="review-text">{review.text}</p>
      
      <div className="review-footer">
        <span>Від: <strong>{review.author}</strong></span>
        {canDelete && (
          <button className="btn btn-danger" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }} onClick={() => onDelete(review.id)}>
            Видалити
          </button>
        )}
      </div>
    </div>
  );
}
