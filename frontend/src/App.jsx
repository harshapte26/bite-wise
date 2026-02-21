import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/recipes')
      .then(res => res.json())
      .then(data => setRecipes(data))
      .catch(err => console.error('Error fetching recipes:', err));
  }, []);

  const handleSelect = (recipeId) => {
    fetch('http://localhost:8000/api/select_recipe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: '1337',
        recipe_id: recipeId
      })
    })
      .then(res => res.json())
      .then(data => {
        console.log('Success:', data);
        alert(`You've selected recipe ID: ${recipeId}`);
      })
      .catch(err => console.error('Error selecting recipe:', err));
  };

  return (
    <div className="layout">
      {/* Top Header */}
      <header className="header">
        <div className="header-left">
          {/* Empty left side for flexbox balance */}
        </div>
        <div className="header-center">
          <h1 className="app-logo">
            <svg viewBox="0 0 24 24" width="36" height="36" fill="currentColor" stroke="none" className="logo-icon">
              <path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66l.95-2.3c.48.17.96.29 1.43.37c1.27.21 2.59.16 3.84-.25c3.55-1.16 6.17-4.22 6.55-8.22c.11-1.17-.03-2.32-.38-3.38C17.9 8.05 17.47 8 17 8zM15 11c-.55 0-1-.45-1-1s.45-1 1-1s1 .45 1 1s-.45 1-1 1zM20 2v3h-3v2h3v3h2V7h3V5h-3V2h-2z" />
            </svg>
            BiteWise
          </h1>
        </div>
        <div className="header-right">
          {/* Discord-like User Profile */}
          <div className="user-profile">
            <div className="avatar-wrapper">
              <img
                src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=150&q=80"
                alt="User Avatar"
                className="avatar"
              />
              <div className="status-indicator online"></div>
            </div>
            <div className="user-info">
              <span className="user-name">md</span>
              <span className="user-id">#1337</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="restaurant-grid">
          {recipes.map((recipe) => (
            <div key={recipe.recipe_id} className="restaurant-card">
              <div className="card-image-wrapper">
                <img src={recipe.url} alt={recipe.recipe_name} className="card-image" />
                <div className="hover-overlay">
                  <button
                    className="select-btn"
                    onClick={() => handleSelect(recipe.recipe_id)}
                  >
                    Select
                  </button>
                </div>
              </div>
              <div className="card-content">
                <h3 className="restaurant-name">{recipe.recipe_name}</h3>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
