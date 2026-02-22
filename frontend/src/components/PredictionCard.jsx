import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

export default function PredictionCard({ result }) {
    const cardRef = useRef(null);

    useEffect(() => {
        if (result && cardRef.current) {
            gsap.fromTo(cardRef.current,
                { 
                    opacity: 0, 
                    y: 50,
                    scale: 0.9
                },
                { 
                    opacity: 1, 
                    y: 0,
                    scale: 1,
                    duration: 0.8,
                    ease: 'power3.out'
                }
            );
        }
    }, [result]);

    if (!result) return null;

    if (result.error) {
        return (
            <div ref={cardRef} className="error-message">
                ⚠️ {result.error}
            </div>
        );
    }

    const { prediction, explanation } = result;

    return (
        <div ref={cardRef} className="prediction-card">
            <h3>🎯 Diagnostic Results</h3>
            
            <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1.5rem',
                marginBottom: '2rem'
            }}>
                <div style={{ 
                    background: 'rgba(139, 92, 246, 0.15)', 
                    padding: '1.5rem', 
                    borderRadius: '12px',
                    border: '1px solid rgba(139, 92, 246, 0.4)'
                }}>
                    <p style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>Predicted Class</p>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#A78BFA' }}>
                        {prediction.predicted_class}
                    </p>
                </div>
                
                <div style={{ 
                    background: 'rgba(236, 72, 153, 0.15)', 
                    padding: '1.5rem', 
                    borderRadius: '12px',
                    border: '1px solid rgba(236, 72, 153, 0.4)'
                }}>
                    <p style={{ fontSize: '0.875rem', marginBottom: '0.5rem' }}>Confidence Level</p>
                    <p style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#F472B6' }}>
                        {prediction.confidence.toFixed(2)}%
                    </p>
                </div>
            </div>

            <h4>🔬 AI Explanation</h4>
            <p style={{ 
                lineHeight: '1.8',
                padding: '1.5rem',
                background: 'rgba(10, 5, 20, 0.5)',
                borderRadius: '12px',
                border: '1px solid rgba(139, 92, 246, 0.3)'
            }}>
                {explanation}
            </p>
        </div>
    );
}
