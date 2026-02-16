import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import UploadForm from './UploadForm';
import PredictionCard from './PredictionCard';

export default function DiagnosticHub({ onResult, result }) {
  const hubRef = useRef(null);
  const [isVisible, setIsVisible] = useState(false);
  const [activeSection, setActiveSection] = useState('upload');

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isVisible) {
          setIsVisible(true);
          animateHub();
        }
      },
      { threshold: 0.2 }
    );

    if (hubRef.current) {
      observer.observe(hubRef.current);
    }

    return () => observer.disconnect();
  }, [isVisible]);

  const animateHub = () => {
    const tl = gsap.timeline();
    
    tl.fromTo('.hub-title',
      { x: -100, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.8 }
    )
    .fromTo('.hub-subtitle',
      { x: -100, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.8 },
      '-=0.6'
    )
    .fromTo('.data-intake-card',
      { scale: 0.8, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.6 }
    )
    .fromTo('.agent-card',
      { y: 50, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.5, stagger: 0.15 },
      '-=0.4'
    );
  };

  const handleCardClick = (section) => {
    setActiveSection(section);
  };

  return (
    <section ref={hubRef} className="diagnostic-hub">
      <div className="hub-header">
        <h2 className="hub-title">Clinical Diagnostic Hub</h2>
        <p className="hub-subtitle">
          Analyze neuro-pathologies using our state-of-the-art cooperative multi-agent
          architecture with integrated Saliency Maps.
        </p>
      </div>

      <div className="hub-grid">
        <div 
          className={`data-intake-card ${activeSection === 'upload' ? 'active' : ''}`}
          onClick={() => handleCardClick('upload')}
          style={{ cursor: 'pointer' }}
        >
          <div className="card-icon">📤</div>
          <h3>Data Intake</h3>
          {activeSection === 'upload' ? (
            <div className="upload-zone">
              <UploadForm onResult={onResult} />
            </div>
          ) : (
            <p style={{ color: 'var(--text-secondary)', marginTop: '1rem' }}>
              Click to upload MRI scans
            </p>
          )}
        </div>

        <div className="agent-cards">
          <div 
            className={`agent-card vision-agent ${activeSection === 'vision' ? 'active' : ''}`}
            onClick={() => handleCardClick('vision')}
            style={{ cursor: 'pointer' }}
          >
            <div className="agent-icon">👁️</div>
            <div>
              <h4>VISION AGENT</h4>
              <p>CNN Analysis &amp; Localization</p>
            </div>
            <div className="card-arrow">→</div>
          </div>

          <div 
            className={`agent-card reasoning-agent ${activeSection === 'reasoning' ? 'active'  : ''}`}
            onClick={() => handleCardClick('reasoning')}
            style={{ cursor: 'pointer' }}
          >
            <div className="agent-icon">🧠</div>
            <div>
              <h4>REASONING AGENT</h4>
              <p>Medical Context &amp; Pathophysiology</p>
            </div>
            <div className="card-arrow">→</div>
          </div>

          <div 
            className={`agent-card report-agent ${activeSection === 'report' ? 'active' : ''}`}
            onClick={() => handleCardClick('report')}
            style={{ cursor: 'pointer' }}
          >
            <div className="agent-icon">📋</div>
            <div>
              <h4>REPORT AGENT</h4>
              <p>Final Clinical Documentation</p>
            </div>
            <div className="card-arrow">→</div>
          </div>
        </div>
      </div>

      {result && (
        <div className="results-container">
          <PredictionCard result={result} />
        </div>
      )}

      <div className="hub-footer">
        <div className="status-badge">🔒 AES-256 COMPLIANT</div>
        <div className="status-badge">🛠️ BUILD V4.1.0-STABLE</div>
        <div className="status-badge">⚡ NEURAL ENGINE ACTIVE</div>
        <div className="status-badge">🌐 CLUSTER: ONLINE</div>
      </div>
    </section>
  );
}
