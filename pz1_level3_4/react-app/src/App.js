import React, { useState, useEffect } from 'react';
import './App.css';

// Ініціалізація "Бази Даних" у localStorage
const initDB = () => {
  if (!localStorage.getItem('mp_users')) localStorage.setItem('mp_users', JSON.stringify([]));
  if (!localStorage.getItem('mp_reviews')) localStorage.setItem('mp_reviews', JSON.stringify([]));
};

export default function App() {
  const [currentUser, setCurrentUser] = useState(null);
  const [sessionLoaded, setSessionLoaded] = useState(false);

  useEffect(() => {
    initDB();
    const session = localStorage.getItem('mp_session');
    if (session) {
      setCurrentUser(JSON.parse(session));
    }
    setSessionLoaded(true);
  }, []);

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
    <div className="app-wrapper animate-in">
      <header>
        <h1>MarketPulse AI</h1>
        <p className="subtitle">Сучасна платформа для аналізу якості товарів</p>
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
        setError('Користувач вже існує');
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
    <div className="glass-panel auth-container animate-in">
      <h2 style={{ textAlign: 'center', marginBottom: '24px' }}>
        {isRegister ? 'Створити акаунт' : 'Ласкаво просимо'}
      </h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '20px' }}>
          <label className="form-label">Логін</label>
          <input 
            className="input-field"
            value={form.username}
            onChange={e => setForm({...form, username: e.target.value})}
            required
          />
        </div>
        <div style={{ marginBottom: '24px' }}>
          <label className="form-label">Пароль</label>
          <input 
            type="password"
            className="input-field"
            value={form.password}
            onChange={e => setForm({...form, password: e.target.value})}
            required
          />
        </div>
        {error && <p style={{ color: 'var(--danger)', fontSize: '0.875rem', marginBottom: '16px' }}>{error}</p>}
        <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>
          {isRegister ? 'Зареєструватися' : 'Увійти'}
        </button>
      </form>
      <button 
        className="btn btn-ghost" 
        style={{ width: '100%', marginTop: '12px' }}
        onClick={() => { setIsRegister(!isRegister); setError(''); }}
      >
        {isRegister ? 'Вже є акаунт? Увійти' : 'Немає акаунта? Реєстрація'}
      </button>
    </div>
  );
}

function Dashboard({ user, onLogout }) {
  const [reviews, setReviews] = useState([]);
  const [profile, setProfile] = useState(user);

  useEffect(() => {
    const allReviews = JSON.parse(localStorage.getItem('mp_reviews'));
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
    <div className="animate-in">
      <div className="glass-panel top-bar">
        <div className="user-tag">
          <div className="avatar">{profile.username[0].toUpperCase()}</div>
          <span style={{ fontWeight: 600 }}>{profile.username}</span>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn btn-ghost" onClick={onLogout}>Вийти</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>
        <aside>
          <div className="glass-panel">
            <h3 style={{ marginTop: 0 }}>Мій Профіль</h3>
            <p style={{ color: 'var(--secondary)', fontSize: '0.9rem' }}>{profile.info}</p>
            <button className="btn btn-ghost" style={{ padding: 0 }} onClick={() => {
              const info = prompt('Розкажіть про себе:', profile.info);
              if (info) updateProfile({...profile, info});
            }}>Редагувати статус</button>
          </div>
          
          <div className="glass-panel">
            <h3 style={{ marginTop: 0 }}>Додати відгук</h3>
            <ReviewForm onAdd={addReview} author={profile.username} />
          </div>
        </aside>

        <main>
          <div className="review-grid">
            {reviews.map(rev => (
              <ReviewCard 
                key={rev.id} 
                review={rev} 
                canDelete={rev.author === profile.username}
                onDelete={deleteReview}
              />
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}

function ReviewForm({ onAdd, author }) {
  const [data, setData] = useState({ product: '', text: '', rating: 5, badQuality: false });

  const submit = (e) => {
    e.preventDefault();
    onAdd({ ...data, id: Date.now(), author });
    setData({ product: '', text: '', rating: 5, badQuality: false });
  };

  return (
    <form onSubmit={submit}>
      <div style={{ marginBottom: '16px' }}>
        <label className="form-label">Товар</label>
        <input 
          className="input-field" 
          value={data.product} 
          onChange={e => setData({...data, product: e.target.value})}
          required 
        />
      </div>
      <div style={{ marginBottom: '16px' }}>
        <label className="form-label">Текст відгуку</label>
        <textarea 
          className="input-field" 
          rows="3"
          value={data.text} 
          onChange={e => setData({...data, text: e.target.value})}
          required 
        />
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
         <div>
            <label className="form-label">Оцінка</label>
            <select 
              className="input-field" 
              value={data.rating}
              onChange={e => setData({...data, rating: Number(e.target.value)})}
            >
              {[5,4,3,2,1].map(n => <option key={n} value={n}>{n} зірок</option>)}
            </select>
         </div>
         <div style={{ alignSelf: 'center', marginTop: '20px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
               <input type="checkbox" checked={data.badQuality} onChange={e => setData({...data, badQuality: e.target.checked})} />
               <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>Брак</span>
            </label>
         </div>
      </div>
      <button type="submit" className="btn btn-primary" style={{ width: '100%' }}>Надіслати</button>
    </form>
  );
}

function ReviewCard({ review, canDelete, onDelete }) {
  return (
    <div className="glass-panel review-card animate-in">
      <div className="review-header">
        <div className="rating-stars">{'★'.repeat(review.rating)}</div>
        {review.badQuality && <span className="bad-quality-tag">Неякісний</span>}
      </div>
      <h3 style={{ margin: '8px 0' }}>{review.product}</h3>
      <p className="review-content">{review.text}</p>
      <div className="review-meta">
        <span>Автор: <strong>{review.author}</strong></span>
        {canDelete && (
          <button className="btn btn-danger" style={{ padding: '4px 8px', fontSize: '0.7rem' }} onClick={() => onDelete(review.id)}>Видалити</button>
        )}
      </div>
    </div>
  );
}
