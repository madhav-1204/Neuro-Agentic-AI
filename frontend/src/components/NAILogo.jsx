import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

export default function NAILogo() {
  const logoRef = useRef(null);

  useEffect(() => {
    const letters = logoRef.current.querySelectorAll('.letter');
    
    gsap.fromTo(letters, 
      {
        opacity: 0,
        y: -50,
        rotationX: -90
      },
      {
        opacity: 1,
        y: 0,
        rotationX: 0,
        duration: 1,
        stagger: 0.2,
        ease: 'elastic.out(1, 0.5)',
        delay: 0.5
      }
    );

    // Continuous subtle animation
    gsap.to(letters, {
      y: -5,
      duration: 2,
      stagger: 0.1,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });
  }, []);

  return (
    <div ref={logoRef} className="nai-logo">
      <span className="letter letter-n">N</span>
      <span className="letter letter-a">A</span>
      <span className="letter letter-i">I</span>
    </div>
  );
}
