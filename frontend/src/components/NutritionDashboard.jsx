import React from 'react';
import './NutritionDashboard.css';

const NutritionDashboard = ({ data }) => {
    if (!data || !data.total_nutrients) return null;

    return (
        <div className="nutrition-container">
            <div className="nutrition-header">
                <h2>Nutritional Analysis</h2>
                <p className="nutrition-summary">{data.summary}</p>
            </div>

            <div className="nutrient-grid">
                {Object.entries(data.total_nutrients).map(([name, value]) => (
                    <div key={name} className="nutrient-card">
                        <span className="nutrient-label">{name.replace(/Content$/, '').charAt(0).toUpperCase() + name.replace(/Content$/, '').slice(1)}</span>
                        <span className="nutrient-value">{value}</span>
                    </div>
                ))}
            </div>

            {data.suggestions && data.suggestions.length > 0 && (
                <div className="suggestions-section">
                    <h3>Health Recommendations</h3>
                    <ul className="suggestions-list">
                        {data.suggestions.map((item, idx) => (
                            <li key={idx} className="suggestion-item">
                                <span className="suggestion-bullet">✦</span>
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default NutritionDashboard;
