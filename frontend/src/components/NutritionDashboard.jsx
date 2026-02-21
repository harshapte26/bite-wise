import React from 'react';
import './NutritionDashboard.css';

const NutritionDashboard = ({ data }) => {
    if (!data || !data.total_nutrients) return null;

    return (
        <div className="nutrition-dashboard">
            <div className="nutrition-stats-box">
                <div className="nutrition-header">
                    <h2>Nutrition Overview</h2>
                    <div className="badge">Analyzed by AI</div>
                </div>

                <div className="nutrient-grid">
                    {Object.entries(data.total_nutrients).map(([name, value]) => (
                        <div key={name} className="nutrient-tile">
                            <span className="tile-label">{name}</span>
                            <span className="tile-value">{value}</span>
                        </div>
                    ))}
                </div>
            </div>

            <div className="nutrition-advice-box">
                <div className="advice-header">
                    <div className="advice-icon">💡</div>
                    <h3>Ingredient Suggestions</h3>
                </div>

                <p className="advice-summary">{data.summary}</p>

                {data.suggestions && data.suggestions.length > 0 && (
                    <div className="suggestions-grid">
                        {data.suggestions.map((item, idx) => (
                            <div key={idx} className="suggestion-card">
                                <div className="suggestion-indicator"></div>
                                <p className="suggestion-text">{item}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default NutritionDashboard;
