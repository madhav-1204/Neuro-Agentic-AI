import { useState, useEffect, useRef } from "react";
import { gsap } from "gsap";
import GradCAMCanvas from "./GradCAMCanvas";

/**
 * ClaudeResultCard
 *
 * Renders the full structured output from the /analyze/claude endpoint:
 *   - Tumor type badge, confidence, region, grade
 *   - GradCAM canvas overlay
 *   - Expandable medical sections (what, why, symptoms, treatment, prognosis)
 *
 * Props:
 *   result   – { filename, image, analysis: { tumorType, confidence, ... } }
 */

const SECTIONS = [
  { key: "whatIsIt",      icon: "🔬", title: "What Is This Tumor?" },
  { key: "whyItOccurred", icon: "🧬", title: "Why It May Have Occurred" },
  { key: "symptoms",      icon: "⚠️", title: "Typical Symptoms" },
  { key: "treatment",     icon: "💊", title: "Treatment Protocols" },
  { key: "prognosis",     icon: "📊", title: "Prognosis" },
];

export default function GeminiResultCard({ result }) {
  const [expandedSection, setExpandedSection] = useState(null);
  const cardRef = useRef(null);
  const metricsRef = useRef(null);

  useEffect(() => {
    if (!result || !cardRef.current) return;

    gsap.fromTo(
      cardRef.current,
      { opacity: 0, y: 40, scale: 0.96 },
      { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "power3.out" }
    );

    // Stagger metric cards
    if (metricsRef.current) {
      gsap.fromTo(
        metricsRef.current.children,
        { opacity: 0, y: 20 },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          stagger: 0.12,
          ease: "power2.out",
          delay: 0.3,
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

  const { analysis, image } = result;
  if (!analysis) return null;

  const toggleSection = (key) => {
    setExpandedSection((prev) => (prev === key ? null : key));
  };

  const isTumorDetected =
    analysis.tumorType &&
    !analysis.tumorType.toLowerCase().includes("no tumor") &&
    !analysis.tumorType.toLowerCase().includes("normal");

  return (
    <div ref={cardRef} className="claude-result-card">
      {/* ── Tumor type badge ─────────────────────────────────── */}
      <div className={`tumor-badge ${isTumorDetected ? "detected" : "clear"}`}>
        <span className="tumor-badge-dot" />
        {isTumorDetected ? "Tumor Detected" : "No Tumor Detected"}
      </div>

      <h3 className="tumor-type-title">{analysis.tumorType || "Unknown"}</h3>

      {/* ── Metric cards ─────────────────────────────────────── */}
      <div ref={metricsRef} className="metrics-grid">
        <div className="metric-card metric-confidence">
          <span className="metric-label">Confidence</span>
          <span className="metric-value">{analysis.confidence || "N/A"}</span>
        </div>
        <div className="metric-card metric-region">
          <span className="metric-label">Region</span>
          <span className="metric-value">{analysis.region || "N/A"}</span>
        </div>
        <div className="metric-card metric-grade">
          <span className="metric-label">WHO Grade</span>
          <span className="metric-value">{analysis.grade || "N/A"}</span>
        </div>
      </div>

      {/* ── GradCAM visualisation ────────────────────────────── */}
      {image && analysis.gradcamRegions && analysis.gradcamRegions.length > 0 && (
        <GradCAMCanvas imageSrc={image} regions={analysis.gradcamRegions} />
      )}

      {/* ── Expandable medical sections ──────────────────────── */}
      <div className="medical-sections">
        {SECTIONS.map(({ key, icon, title }) => {
          const content = analysis[key];
          if (!content) return null;

          const isOpen = expandedSection === key;

          return (
            <div
              key={key}
              className={`medical-section ${isOpen ? "open" : ""}`}
            >
              <button
                className="section-header"
                onClick={() => toggleSection(key)}
                aria-expanded={isOpen}
              >
                <span className="section-icon">{icon}</span>
                <span className="section-title">{title}</span>
                <span className={`section-chevron ${isOpen ? "rotated" : ""}`}>
                  ▸
                </span>
              </button>

              {isOpen && (
                <div className="section-body">
                  <p>{content}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
