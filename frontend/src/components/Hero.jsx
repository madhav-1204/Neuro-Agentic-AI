import { useEffect, useRef } from 'react';
import { gsap } from 'gsap';

export default function Hero() {
  const heroRef = useRef(null);
  const titleRef = useRef(null);
  const subtitleRef = useRef(null);
  const ctaRef = useRef(null);

  useEffect(() => {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    // Title rolling in animation - split by words
    const titleWords = titleRef.current.querySelectorAll('.title-word');
    tl.fromTo(titleWords,
      {
        x: -200,
        opacity: 0,
        rotationY: 90
      },
      {
        x: 0,
        opacity: 1,
        rotationY: 0,
        duration: 1,
        stagger: 0.15,
        ease: 'back.out(1.7)'
      },
      '-=0.4'
    );

    // Subtitle fade in
    tl.fromTo(subtitleRef.current,
      { y: 30, opacity: 0 },
      { y: 0, opacity: 1, duration: 0.8 }
    );

    // CTA buttons
    const buttons = ctaRef.current.querySelectorAll('.cta-btn');
    tl.fromTo(buttons,
      { scale: 0, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.5, stagger: 0.2 }
    );
  }, []);

  const scrollToDiagnostic = () => {
    const diagnosticSection = document.querySelector('.diagnostic-hub');
    if (diagnosticSection) {
      diagnosticSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <section ref={heroRef} className="hero">
      <div className="hero-content">
        <h1 ref={titleRef} className="hero-title">
          <span className="title-word">Precision</span>{' '}
          <span className="title-word gradient-text">AI Tumor</span>{' '}
          <span className="title-word gradient-text-alt">Analysis</span>
        </h1>

        <p ref={subtitleRef} className="hero-subtitle">
          Harness the power of multi-agent neural networks and Grad-CAM
          <br />
          explainability to detect pathologies with unprecedented precision.
        </p>

        <div ref={ctaRef} className="hero-cta">
          <button className="cta-btn cta-primary" onClick={scrollToDiagnostic}>
            Start Neural Analysis →
          </button>
          <button className="cta-btn cta-secondary" onClick={scrollToDiagnostic}>
            View Documentation
          </button>
        </div>
      </div>
    </section>
  );
}
