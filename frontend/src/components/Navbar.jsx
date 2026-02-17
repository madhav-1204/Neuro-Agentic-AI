import { useEffect, useRef, useState } from 'react';
import { gsap } from 'gsap';
import NAILogo from './NAILogo';
import GoogleLoginButton from './GoogleLoginButton';
import { useAuth } from '../contexts/AuthContext';

export default function Navbar() {
  const navRef = useRef(null);
  const { user, logout, isAuthenticated } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  useEffect(() => {
    gsap.fromTo(navRef.current,
      {
        y: -100,
        opacity: 0
      },
      {
        y: 0,
        opacity: 1,
        duration: 1,
        ease: 'power3.out'
      }
    );
  }, []);

  return (
    <nav ref={navRef} className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <NAILogo />
          <span className="brand-text">Neuro Agentic AI</span>
        </div>
        <ul className="navbar-menu">
          <li><a href="#home">Home</a></li>
          <li><a href="#technology">Technology</a></li>
          <li><a href="#compliance">Compliance</a></li>
          <li><a href="#case-studies">Case Studies</a></li>
          <li><button className="btn-dashboard">Launch Dashboard</button></li>
          
          {isAuthenticated ? (
            <li className="user-menu">
              <div 
                className="user-profile" 
                onClick={() => setShowDropdown(!showDropdown)}
              >
                <img src={user.picture} alt={user.name} className="user-avatar" />
                <span className="user-name">{user.name}</span>
              </div>
              {showDropdown && (
                <div className="dropdown-menu">
                  <div className="dropdown-item user-info">
                    <p>{user.email}</p>
                  </div>
                  <button 
                    className="dropdown-item logout-btn" 
                    onClick={logout}
                  >
                    Logout
                  </button>
                </div>
              )}
            </li>
          ) : (
            <li className="login-button">
              <GoogleLoginButton />
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
}
