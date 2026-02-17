import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap";
import UploadForm from "../components/UploadForm";
import PredictionCard from "../components/PredictionCard";

export default function AnalysisResult() {
  const [result, setResult] = useState(null);
  const [downloading, setDownloading] = useState(false);
  const navigate = useNavigate();
  const pageRef = useRef(null);

  useEffect(() => {
    // Animate page entrance
    gsap.fromTo(
      pageRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }
    );
  }, []);

  const handleDownloadPDF = async () => {
    if (!result) return;

    setDownloading(true);
    try {
      const response = await fetch("http://localhost:8000/analyze/download-pdf", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(result),
      });

      if (!response.ok) {
        throw new Error("Failed to generate PDF");
      }

      // Get the PDF blob
      const blob = await response.blob();
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `analysis_report_${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error downloading PDF:", error);
      alert("Failed to download PDF. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div ref={pageRef} className="analysis-page">
      <div className="analysis-container">
        <div className="analysis-header">
          <button onClick={() => navigate("/")} className="back-button">
            ← Back to Home
          </button>
          <h1 className="analysis-title">Neural Analysis</h1>
          <p className="analysis-subtitle">
            Upload an MRI scan for AI-powered brain tumor detection and analysis
          </p>
        </div>

        <div className="analysis-content">
          <div className="upload-section">
            <UploadForm onResult={setResult} />
          </div>

          {result && (
            <div className="results-section">
              <div className="results-header">
                <h2>Analysis Results</h2>
                <button
                  onClick={handleDownloadPDF}
                  disabled={downloading}
                  className="download-pdf-button"
                >
                  {downloading ? (
                    <>
                      <span className="spinner"></span> Generating PDF...
                    </>
                  ) : (
                    <>
                      📄 Download PDF Report
                    </>
                  )}
                </button>
              </div>
              
              <PredictionCard result={result} />

              <div className="analysis-actions">
                <button onClick={() => setResult(null)} className="analyze-another-btn">
                  Analyze Another Scan
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="analysis-footer">
          <div className="status-badge">🔒 HIPAA COMPLIANT</div>
          <div className="status-badge">🧠 AI-POWERED</div>
          <div className="status-badge">⚡ REAL-TIME ANALYSIS</div>
        </div>
      </div>
    </div>
  );
}
