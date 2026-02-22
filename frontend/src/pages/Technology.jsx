import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap";

const agents = [
  {
    icon: "👁️",
    name: "Vision Agent",
    tag: "Perception Layer",
    color: "#8b5cf6",
    description:
      "The Vision Agent is a deep-learning-powered convolutional neural network (EfficientNet-B3 / ResNet-18) trained on thousands of labeled brain MRI scans. It ingests raw MRI images, normalises them, and produces a multi-class prediction with per-class probability scores.",
    capabilities: [
      "Multi-class tumor classification (Glioma, Meningioma, Pituitary, No Tumor)",
      "Confidence scoring with full probability distribution",
      "Automatic image pre-processing and tensor normalisation",
      "Support for JPEG, PNG, and DICOM input formats",
    ],
    techStack: ["PyTorch", "EfficientNet-B3", "ResNet-18", "torchvision"],
    flow: "Raw MRI → Pre-processing → CNN Forward Pass → Prediction + Probabilities",
  },
  {
    icon: "🔍",
    name: "Explainability Agent",
    tag: "Interpretability Layer",
    color: "#ec4899",
    description:
      "The Explainability Agent uses Gradient-weighted Class Activation Mapping (Grad-CAM) to generate visual heatmaps that highlight which regions of the MRI scan most influenced the Vision Agent's prediction. This provides transparency and trust in the AI decision.",
    capabilities: [
      "Grad-CAM heatmap generation over the final convolutional layer",
      "Region-of-interest extraction with bounding coordinates",
      "Intensity scoring for each activation region",
      "Visual overlay on the original MRI for side-by-side comparison",
    ],
    techStack: ["pytorch-grad-cam", "OpenCV", "NumPy", "Matplotlib"],
    flow: "Model Gradients → Class Activation Map → Heatmap Overlay → Region Extraction",
  },
  {
    icon: "🧠",
    name: "Reasoning Agent",
    tag: "Intelligence Layer",
    color: "#10b981",
    description:
      "The Reasoning Agent is powered by Google's Gemini large language model. It receives the Vision Agent's prediction, confidence scores, and probability distribution, then generates a detailed medical explanation covering what the detected condition is, why it may have occurred, symptoms, treatment protocols, and prognosis.",
    capabilities: [
      "Contextual medical explanation based on AI prediction",
      "Structured output: What, Why, Symptoms, Treatment, Prognosis",
      "Confidence-aware language (adjusts certainty of statements)",
      "Gemini Vision mode for direct image analysis with richer context",
    ],
    techStack: ["Google Gemini API", "google-genai SDK", "Prompt Engineering"],
    flow: "Prediction + Probabilities → Structured Prompt → Gemini LLM → Medical Explanation",
  },
];

export default function Technology() {
  const navigate = useNavigate();
  const pageRef = useRef(null);
  const cardsRef = useRef([]);

  useEffect(() => {
    const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

    tl.fromTo(
      pageRef.current.querySelector(".tech-header"),
      { opacity: 0, y: 40 },
      { opacity: 1, y: 0, duration: 0.8 }
    );

    tl.fromTo(
      pageRef.current.querySelector(".tech-pipeline"),
      { opacity: 0, scale: 0.95 },
      { opacity: 1, scale: 1, duration: 0.6 },
      "-=0.3"
    );

    cardsRef.current.forEach((card, i) => {
      tl.fromTo(
        card,
        { opacity: 0, y: 50, rotationX: -8 },
        { opacity: 1, y: 0, rotationX: 0, duration: 0.7 },
        `-=${i === 0 ? 0.2 : 0.4}`
      );
    });

    return () => tl.kill();
  }, []);

  return (
    <div ref={pageRef} className="tech-page">
      <div className="tech-container">
        {/* Header */}
        <div className="tech-header">
          <button onClick={() => navigate("/")} className="back-button">
            ← Back to Home
          </button>
          <h1 className="tech-title">
            Multi-Agent <span className="gradient-text">AI Architecture</span>
          </h1>
          <p className="tech-subtitle">
            Three specialised AI agents work in concert — each one a domain
            expert — to deliver accurate, explainable, and actionable brain
            tumor diagnostics.
          </p>
        </div>

        {/* Pipeline visualisation */}
        <div className="tech-pipeline">
          <div className="pipeline-step" style={{ "--ac": agents[0].color }}>
            <span className="pipeline-icon">{agents[0].icon}</span>
            <span className="pipeline-label">Vision</span>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step" style={{ "--ac": agents[1].color }}>
            <span className="pipeline-icon">{agents[1].icon}</span>
            <span className="pipeline-label">Explainability</span>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step" style={{ "--ac": agents[2].color }}>
            <span className="pipeline-icon">{agents[2].icon}</span>
            <span className="pipeline-label">Reasoning</span>
          </div>
          <div className="pipeline-arrow">→</div>
          <div className="pipeline-step pipeline-step-output">
            <span className="pipeline-icon">📄</span>
            <span className="pipeline-label">Report</span>
          </div>
        </div>

        {/* Agent cards */}
        <div className="tech-agents">
          {agents.map((agent, idx) => (
            <div
              key={agent.name}
              ref={(el) => (cardsRef.current[idx] = el)}
              className="tech-agent-card"
              style={{ "--agent-color": agent.color }}
            >
              <div className="tech-agent-header">
                <div className="tech-agent-icon">{agent.icon}</div>
                <div>
                  <h2 className="tech-agent-name">{agent.name}</h2>
                  <span className="tech-agent-tag">{agent.tag}</span>
                </div>
              </div>

              <p className="tech-agent-desc">{agent.description}</p>

              <div className="tech-section">
                <h3>Key Capabilities</h3>
                <ul className="tech-capabilities">
                  {agent.capabilities.map((cap, i) => (
                    <li key={i}>{cap}</li>
                  ))}
                </ul>
              </div>

              <div className="tech-section">
                <h3>Tech Stack</h3>
                <div className="tech-tags">
                  {agent.techStack.map((t, i) => (
                    <span key={i} className="tech-tag">
                      {t}
                    </span>
                  ))}
                </div>
              </div>

              <div className="tech-flow">
                <h3>Data Flow</h3>
                <code>{agent.flow}</code>
              </div>
            </div>
          ))}
        </div>

        {/* Orchestrator note */}
        <div className="tech-orchestrator">
          <div className="tech-orchestrator-icon">⚙️</div>
          <div>
            <h3>Orchestrator</h3>
            <p>
              A central coordinator initialises all three agents, loads the CNN
              model weights, and pipes data through the full pipeline —
              prediction → explainability → reasoning → final report — in a
              single deterministic pass.
            </p>
          </div>
        </div>

        {/* CTA */}
        <div className="tech-cta">
          <button className="cta-btn cta-primary" onClick={() => navigate("/analysis")}>
            Try It Now →
          </button>
        </div>
      </div>
    </div>
  );
}
