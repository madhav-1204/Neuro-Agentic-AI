import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

export default function SplashScreen({ onFinish }) {
  const splashRef = useRef(null);
  const logoRef = useRef(null);
  const taglineRef = useRef(null);

  useEffect(() => {
    const tl = gsap.timeline({
      onComplete: () => {
        gsap.to(splashRef.current, {
          opacity: 0,
          scale: 1.1,
          duration: 0.6,
          ease: 'power2.in',
          onComplete: onFinish,
        });
      },
    });

    const letters = logoRef.current.querySelectorAll('.splash-letter');

    // Letters drop in
    tl.fromTo(
      letters,
      { opacity: 0, y: -80, rotationX: -90, scale: 0.5 },
      {
        opacity: 1,
        y: 0,
        rotationX: 0,
        scale: 1,
        duration: 0.8,
        stagger: 0.2,
        ease: 'elastic.out(1, 0.5)',
      }
    );

    // Glow pulse
    tl.to(letters, {
      textShadow: '0 0 40px currentColor, 0 0 80px currentColor',
      duration: 0.6,
      stagger: 0.1,
      yoyo: true,
      repeat: 1,
      ease: 'sine.inOut',
    });

    // Tagline fade in
    tl.fromTo(
      taglineRef.current,
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.5 },
      '-=0.8'
    );

    // Hold for a moment before fading out
    tl.to({}, { duration: 0.8 });

    return () => tl.kill();
  }, [onFinish]);

  return (
    <div ref={splashRef} className="splash-screen">
      <div className="splash-content">
        <div ref={logoRef} className="splash-logo">
          <span className="splash-letter splash-n">N</span>
          <span className="splash-letter splash-a">A</span>
          <span className="splash-letter splash-i">I</span>
        </div>
        <p ref={taglineRef} className="splash-tagline">
          Neuro Agentic AI
        </p>
      </div>
      <button className="splash-skip-btn" onClick={onFinish}>
        Skip &rarr;
      </button>
    </div>
  );
}
