import { useEffect, useRef, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { gsap } from 'gsap';
import NAILogo from './NAILogo';

export default function Navbar() {
  const navRef = useRef(null);
  const [visible, setVisible] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Start hidden
    gsap.set(navRef.current, { y: -100, opacity: 0 });

    const handleScroll = () => {
      const scrollY = window.scrollY;
      if (scrollY > 80 && !visible) {
        setVisible(true);
        gsap.to(navRef.current, {
          y: 0,
          opacity: 1,
          duration: 0.5,
          ease: 'power3.out',
        });
      } else if (scrollY <= 80 && visible) {
        setVisible(false);
        gsap.to(navRef.current, {
          y: -100,
          opacity: 0,
          duration: 0.4,
          ease: 'power3.in',
        });
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [visible]);

  const navTo = (path) => (e) => {
    e.preventDefault();
    navigate(path);
  };

  const isActive = (path) => location.pathname === path ? 'active' : '';

  return (
    <nav ref={navRef} className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand" onClick={navTo('/')} style={{ cursor: 'pointer' }}>
          <NAILogo />
          <span className="brand-text">Neuro Agentic AI</span>
        </div>
        <ul className="navbar-menu">
          <li><a href="/" onClick={navTo('/')} className={isActive('/')}>Home</a></li>
          <li><a href="/analysis" onClick={navTo('/analysis')} className={isActive('/analysis')}>Analyze</a></li>
          <li><a href="/diagnostic-center" onClick={navTo('/diagnostic-center')} className={isActive('/diagnostic-center')}>Diagnostic Center</a></li>
          <li><a href="/technology" onClick={navTo('/technology')} className={isActive('/technology')}>Technology</a></li>
          <li><button className="btn-dashboard" onClick={() => navigate('/analysis')}>Start Analysis →</button></li>
        </ul>
      </div>
    </nav>
  );
}
