import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap";
import { analyzeWithGemini, downloadGeminiPDF } from "../api/api";
import GeminiResultCard from "../components/GeminiResultCard";

export default function AnalysisResult() {
  // Mode: null = choose, "single", "multi"
  const [mode, setMode] = useState(null);
  const [patientName, setPatientName] = useState("");
  const [result, setResult] = useState(null);
  const [multiResults, setMultiResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [fileName, setFileName] = useState("");
  const [previewUrl, setPreviewUrl] = useState(null);
  // Multi-image state
  const [multiFiles, setMultiFiles] = useState([]);
  const [multiPreviews, setMultiPreviews] = useState([]);
  const [duplicateTumorWarning, setDuplicateTumorWarning] = useState(false);

  const navigate = useNavigate();
  const pageRef = useRef(null);
  const fileInputRef = useRef(null);
  const multiFileInputRef = useRef(null);
  const uploadBoxRef = useRef(null);
  const modeRef = useRef(null);

  useEffect(() => {
    gsap.fromTo(
      pageRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }
    );
  }, []);

  useEffect(() => {
    if (mode && modeRef.current) {
      gsap.fromTo(
        modeRef.current,
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }
      );
    }
  }, [mode]);

  // ── Single file handling ───────────────────────────────────────

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFileName(file.name);
      setPreviewUrl(URL.createObjectURL(file));
      if (uploadBoxRef.current) {
        gsap.fromTo(
          uploadBoxRef.current,
          { scale: 0.95 },
          { scale: 1, duration: 0.3, ease: "back.out(1.7)" }
        );
      }
    }
  };

  const handleBoxClick = () => {
    if (!loading) fileInputRef.current.click();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = fileInputRef.current.files[0];
    if (!file || !patientName.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await analyzeWithGemini(file);
      res.patientName = patientName.trim();
      setResult(res);
      if (res.image) setPreviewUrl(res.image);

      if (uploadBoxRef.current) {
        gsap.to(uploadBoxRef.current, {
          backgroundColor: "rgba(16, 185, 129, 0.1)",
          duration: 0.5,
          yoyo: true,
          repeat: 1,
        });
      }
    } catch (err) {
      setResult({ error: "Failed to connect to backend." });
      if (uploadBoxRef.current) {
        gsap.to(uploadBoxRef.current, {
          x: [-10, 10, -10, 10, 0],
          duration: 0.5,
        });
      }
    }

    setLoading(false);
  };

  // ── Multi file handling ────────────────────────────────────────

  const handleMultiFileChange = (e) => {
    const newFiles = Array.from(e.target.files);
    if (newFiles.length > 0) {
      setMultiFiles((prev) => [...prev, ...newFiles]);
      setMultiPreviews((prev) => [...prev, ...newFiles.map((f) => URL.createObjectURL(f))]);
      setDuplicateTumorWarning(false);
      setMultiResults([]);
      // Reset input so the same file can be re-selected
      e.target.value = "";
    }
  };

  const handleRemoveMultiFile = (index) => {
    URL.revokeObjectURL(multiPreviews[index]);
    setMultiFiles((prev) => prev.filter((_, i) => i !== index));
    setMultiPreviews((prev) => prev.filter((_, i) => i !== index));
  };

  const handleMultiBoxClick = () => {
    if (!loading) multiFileInputRef.current.click();
  };

  const handleMultiSubmit = async (e) => {
    e.preventDefault();
    if (multiFiles.length === 0 || !patientName.trim()) return;

    setLoading(true);
    setMultiResults([]);
    setDuplicateTumorWarning(false);

    const results = [];
    for (const file of multiFiles) {
      try {
        const res = await analyzeWithGemini(file);
        res.patientName = patientName.trim();
        results.push(res);
      } catch {
        results.push({ error: `Failed to analyze ${file.name}` });
      }
    }

    // Check for duplicate tumors (2+ detected tumors of different types)
    const detectedTumors = results
      .filter(
        (r) =>
          r.analysis &&
          r.analysis.tumorType &&
          !r.analysis.tumorType.toLowerCase().includes("no tumor") &&
          !r.analysis.tumorType.toLowerCase().includes("normal")
      )
      .map((r) => r.analysis.tumorType);

    const uniqueTumors = [...new Set(detectedTumors)];

    if (uniqueTumors.length >= 2) {
      setDuplicateTumorWarning(true);
      setMultiResults([]);
    } else {
      setMultiResults(results);
    }

    setLoading(false);
  };

  // ── PDF download ───────────────────────────────────────────────

  const handleDownloadPDF = async (res) => {
    if (!res) return;
    setDownloading(true);
    try {
      const payload = { ...res, patientName: patientName.trim() };
      const blob = await downloadGeminiPDF(payload);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `neuro_ai_report_${patientName.trim().replace(/\s+/g, "_")}_${new Date()
        .toISOString()
        .slice(0, 10)}.pdf`;
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
    setMultiResults([]);
    setFileName("");
    setPreviewUrl(null);
    setMultiFiles([]);
    setMultiPreviews([]);
    setDuplicateTumorWarning(false);
    if (fileInputRef.current) fileInputRef.current.value = "";
    if (multiFileInputRef.current) multiFileInputRef.current.value = "";
  };

  const handleBackToMode = () => {
    handleReset();
    setMode(null);
    setPatientName("");
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
          <h1 className="analysis-title">Analyze your MRI Images</h1>
          <p className="analysis-subtitle">
            Upload MRI scans for AI-powered brain tumor detection and analysis
          </p>
        </div>

        {/* Mode selector */}
        {!mode && (
          <div className="mode-selector">
            <div className="mode-card" onClick={() => setMode("single")}>
              <div className="mode-icon">🧠</div>
              <h3>Single Image</h3>
              <p>Upload a single MRI scan for analysis</p>
            </div>
            <div className="mode-card" onClick={() => setMode("multi")}>
              <div className="mode-icon">🔬</div>
              <h3>Multiple Images</h3>
              <p>Upload multiple MRI scans of the same patient</p>
            </div>
          </div>
        )}

        {/* Patient name + upload */}
        {mode && (
          <div ref={modeRef}>
            <button onClick={handleBackToMode} className="back-mode-btn">
              ← Change Upload Mode
            </button>

            {/* Patient name input */}
            <div className="patient-name-section">
              <label htmlFor="patientName" className="patient-label">
                Patient Name <span className="required">*</span>
              </label>
              <input
                id="patientName"
                type="text"
                value={patientName}
                onChange={(e) => setPatientName(e.target.value)}
                placeholder="Enter patient full name"
                className="patient-input"
              />
            </div>

            <div className="analysis-content">
              {/* ──── SINGLE IMAGE MODE ──── */}
              {mode === "single" && (
                <div className="upload-section">
                  <form onSubmit={handleSubmit}>
                    <div
                      ref={uploadBoxRef}
                      className="upload-box"
                      onClick={handleBoxClick}
                      style={{
                        cursor: loading ? "not-allowed" : "pointer",
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
                          <div className="upload-icon">
                            {loading ? "⏳" : "📁"}
                          </div>
                          <p className="upload-text">
                            {loading
                              ? "Analyzing with Gemini Vision..."
                              : fileName
                              ? fileName
                              : "Drop your DICOM/JPEG/PNG MRI scan here"}
                          </p>
                          <p className="upload-subtext">
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
                      <button
                        type="submit"
                        className="analyze-btn"
                        disabled={!patientName.trim()}
                        title={
                          !patientName.trim()
                            ? "Please enter patient name first"
                            : ""
                        }
                      >
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
              )}

              {/* ──── MULTI IMAGE MODE ──── */}
              {mode === "multi" && (
                <div className="upload-section">
                  <form onSubmit={handleMultiSubmit}>
                    <div
                      ref={uploadBoxRef}
                      className="upload-box"
                      onClick={handleMultiBoxClick}
                      style={{
                        cursor: loading ? "not-allowed" : "pointer",
                      }}
                    >
                      {multiPreviews.length > 0 && !loading ? (
                        <div className="multi-preview-grid">
                          {multiPreviews.map((url, i) => (
                            <div key={i} className="multi-preview-wrapper">
                              <img
                                src={url}
                                alt={`MRI ${i + 1}`}
                                className="multi-preview-img"
                              />
                              <button
                                className="multi-preview-remove-btn"
                                onClick={(e) => { e.stopPropagation(); handleRemoveMultiFile(i); }}
                                title="Remove this scan"
                              >✕</button>
                            </div>
                          ))}
                          <div className="multi-preview-add-hint">Click to add more</div>
                        </div>
                      ) : (
                        <>
                          <div className="upload-icon">
                            {loading ? "⏳" : "📂"}
                          </div>
                          <p className="upload-text">
                            {loading
                              ? "Analyzing multiple scans..."
                              : multiFiles.length > 0
                              ? `${multiFiles.length} files selected`
                              : "Select multiple MRI scans of the same patient"}
                          </p>
                          <p className="upload-subtext">
                            {!loading &&
                              multiFiles.length === 0 &&
                              "or click to browse files"}
                          </p>
                        </>
                      )}
                      <input
                        ref={multiFileInputRef}
                        type="file"
                        multiple
                        onChange={handleMultiFileChange}
                        onClick={(e) => e.stopPropagation()}
                        accept="image/*"
                        style={{ display: "none" }}
                      />
                    </div>

                    {multiFiles.length > 0 && !loading && (
                      <button
                        type="submit"
                        className="analyze-btn"
                        disabled={!patientName.trim()}
                        title={
                          !patientName.trim()
                            ? "Please enter patient name first"
                            : ""
                        }
                      >
                        🧠 Analyze {multiFiles.length} Scans
                      </button>
                    )}

                    {loading && (
                      <div className="analysis-loading-bar">
                        <div className="loading-progress" />
                        <span>Analyzing scans... Please wait.</span>
                      </div>
                    )}
                  </form>
                </div>
              )}

              {/* ──── DUPLICATE TUMOR WARNING ──── */}
              {duplicateTumorWarning && (
                <div className="duplicate-warning">
                  <div className="warning-icon">⚠️</div>
                  <h3>Conflicting Tumor Detections</h3>
                  <p>
                    The AI detected <strong>2 or more different tumor types</strong> across
                    the uploaded scans for the same patient. This may indicate
                    inconsistent image quality or mislabeled scans.
                  </p>
                  <p className="warning-action">
                    Please verify the images belong to the same patient and
                    re-upload for accurate results.
                  </p>
                  <button onClick={handleReset} className="reupload-btn">
                    🔄 Re-upload Images
                  </button>
                </div>
              )}

              {/* ──── SINGLE RESULT ──── */}
              {result && !result.error && (
                <div className="results-section">
                  <div className="medical-disclaimer-banner">
                    ⚕️ <strong>Disclaimer:</strong> This AI-generated analysis is for informational purposes only and does not constitute a medical diagnosis. Always consult a qualified healthcare professional.
                  </div>
                  <div className="results-header">
                    <h2>Analysis Results</h2>
                    <div className="results-patient-badge">
                      Patient: <strong>{patientName}</strong>
                    </div>
                    <button
                      onClick={() => handleDownloadPDF(result)}
                      disabled={downloading}
                      className="download-pdf-button"
                    >
                      {downloading ? (
                        <>
                          <span className="spinner"></span> Generating PDF...
                        </>
                      ) : (
                        <>📄 Download Report</>
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

              {/* ──── MULTI RESULTS ──── */}
              {multiResults.length > 0 && (
                <div className="results-section">
                  <div className="medical-disclaimer-banner">
                    ⚕️ <strong>Disclaimer:</strong> This AI-generated analysis is for informational purposes only and does not constitute a medical diagnosis. Always consult a qualified healthcare professional.
                  </div>
                  <div className="results-header">
                    <h2>
                      Analysis Results ({multiResults.length} scan
                      {multiResults.length > 1 ? "s" : ""})
                    </h2>
                    <div className="results-patient-badge">
                      Patient: <strong>{patientName}</strong>
                    </div>
                  </div>

                  {multiResults.map((res, idx) => (
                    <div key={idx} className="multi-result-item">
                      <div className="multi-result-header">
                        <h3>Scan #{idx + 1}: {res.filename || `Image ${idx + 1}`}</h3>
                        {!res.error && (
                          <button
                            onClick={() => handleDownloadPDF(res)}
                            disabled={downloading}
                            className="download-pdf-button download-pdf-sm"
                          >
                            {downloading ? "..." : "📄 Download PDF"}
                          </button>
                        )}
                      </div>
                      {res.error ? (
                        <div className="error-message">⚠️ {res.error}</div>
                      ) : (
                        <GeminiResultCard result={res} />
                      )}
                    </div>
                  ))}

                  <div className="analysis-actions">
                    <button onClick={handleReset} className="analyze-another-btn">
                      Analyze More Scans
                    </button>
                  </div>
                </div>
              )}

              {/* ──── ERROR ──── */}
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
          </div>
        )}

        <div className="analysis-footer">
          <div className="status-badge">🔒 HIPAA COMPLIANT</div>
          <div className="status-badge">🧠 GEMINI VISION AI</div>
          <div className="status-badge">⚡ REAL-TIME ANALYSIS</div>
        </div>
      </div>
    </div>
  );
}
