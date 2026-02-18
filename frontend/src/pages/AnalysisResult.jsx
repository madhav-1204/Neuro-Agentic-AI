import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap";
import { analyzeWithGemini, downloadGeminiPDF } from "../api/api";
import GeminiResultCard from "../components/GeminiResultCard";

export default function AnalysisResult() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [previewUrl, setPreviewUrl] = useState(null);
  const navigate = useNavigate();
  const pageRef = useRef(null);
  const fileInputRef = useRef(null);
  const uploadBoxRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(
      pageRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }
    );
  }, []);

  // ── File handling ──────────────────────────────────────────────

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      setPreviewUrl(URL.createObjectURL(file));
      gsap.fromTo(
        uploadBoxRef.current,
        { scale: 0.95 },
        { scale: 1, duration: 0.3, ease: "back.out(1.7)" }
      );
    }
  };

  const handleBoxClick = () => {
    if (!loading) fileInputRef.current.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = fileInputRef.current.files[0];
    if (!file) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await analyzeWithGemini(file);
      setResult(res);

      // Use the returned base64 image for preview if available
      if (res.image) setPreviewUrl(res.image);

      gsap.to(uploadBoxRef.current, {
        backgroundColor: "rgba(16, 185, 129, 0.1)",
        duration: 0.5,
        yoyo: true,
        repeat: 1,
      });
    } catch (err) {
      setResult({ error: "Failed to connect to backend." });
      gsap.to(uploadBoxRef.current, {
        x: [-10, 10, -10, 10, 0],
        duration: 0.5,
      });
    }

    setLoading(false);
  };

  // ── PDF download ───────────────────────────────────────────────

  const handleDownloadPDF = async () => {
    if (!result) return;
    setDownloading(true);
    try {
      const blob = await downloadGeminiPDF(result);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `neuro_ai_report_${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error("Error downloading PDF:", error);
      alert("Failed to download PDF. Please try again.");
    } finally {
      setDownloading(false);
    }
  };

  // ── Reset ──────────────────────────────────────────────────────

  const handleReset = () => {
    setResult(null);
    setFileName("");
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  // ── Render ─────────────────────────────────────────────────────

  return (
    <div ref={pageRef} className="analysis-page">
      <div className="analysis-container">
        {/* Header */}
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
          {/* Upload section */}
          <div className="upload-section">
            <form onSubmit={handleSubmit}>
              <div
                ref={uploadBoxRef}
                className="upload-box"
                onClick={handleBoxClick}
                style={{
                  cursor: loading ? "not-allowed" : "pointer",
                  transition: "all 0.3s",
                }}
              >
                {previewUrl && !loading ? (
                  <img
                    src={previewUrl}
                    alt="MRI Preview"
                    className="upload-preview-img"
                  />
                ) : (
                  <>
                    <div className="upload-icon">{loading ? "⏳" : "📁"}</div>
                    <p className="upload-text">
                      {loading
                        ? "Analyzing with Gemini Vision..."
                        : fileName
                        ? fileName
                        : "Drop your DICOM/JPEG/PNG MRI scan here"}
                    </p>
                    <p
                      className="upload-subtext"
                      style={{
                        fontSize: "0.875rem",
                        color: "var(--text-secondary)",
                        marginTop: "0.5rem",
                      }}
                    >
                      {!loading && !fileName && "or click to browse files"}
                    </p>
                  </>
                )}
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={handleFileChange}
                  accept="image/*"
                  style={{ display: "none" }}
                />
              </div>

              {fileName && !loading && (
                <button type="submit" className="analyze-btn">
                  🧠 Start Neural Analysis
                </button>
              )}

              {loading && (
                <div className="analysis-loading-bar">
                  <div className="loading-progress" />
                  <span>Gemini Vision is analyzing your scan...</span>
                </div>
              )}
            </form>
          </div>

          {/* Results section */}
          {result && !result.error && (
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
                    <>📄 Download 3-Page Report</>
                  )}
                </button>
              </div>

              <GeminiResultCard result={result} />

              <div className="analysis-actions">
                <button onClick={handleReset} className="analyze-another-btn">
                  Analyze Another Scan
                </button>
              </div>
            </div>
          )}

          {/* Error display */}
          {result && result.error && (
            <div className="results-section">
              <div className="error-message">⚠️ {result.error}</div>
              <div className="analysis-actions">
                <button onClick={handleReset} className="analyze-another-btn">
                  Try Again
                </button>
              </div>
            </div>
          )}
        </div>

        <div className="analysis-footer">
          <div className="status-badge">🔒 HIPAA COMPLIANT</div>
          <div className="status-badge">🧠 GEMINI VISION AI</div>
          <div className="status-badge">⚡ REAL-TIME ANALYSIS</div>
        </div>
      </div>
    </div>
  );
}
