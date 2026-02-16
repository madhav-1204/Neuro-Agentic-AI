import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import NAILogo from './NAILogo';

export default function Navbar() {
  const navRef = useRef(null);

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
        </ul>
      </div>
    </nav>
  );
}
