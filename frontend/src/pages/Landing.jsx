import { useNavigate } from "react-router-dom";

export default function Landing() {
    const navigate = useNavigate();

    return (
        <div className="landing-container">
            <div className="hero">
                <h1>Neuro Diagnosis AI</h1>
                <p>
                    AI-powered brain MRI analysis system for automated tumor detection,
                    confidence scoring, and explainable insights.
                </p>

                <button
                    className="button"
                    onClick={() => navigate("/analyze")}
                >
                    Start Analysis
                </button>
            </div>

            <div className="features">
                <div className="feature-card">
                    <h3>Accurate Classification</h3>
                    <p>ResNet & EfficientNet-based tumor classification.</p>
                </div>

                <div className="feature-card">
                    <h3>Explainable AI</h3>
                    <p>Grad-CAM visualizations for transparent decisions.</p>
                </div>

                <div className="feature-card">
                    <h3>Confidence Scoring</h3>
                    <p>Detailed probability distribution across tumor types.</p>
                </div>
            </div>
        </div>
    );
}