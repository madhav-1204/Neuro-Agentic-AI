import { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { gsap } from "gsap";
import { analyzeWithGemini, downloadGeminiPDF } from "../api/api";
import GeminiResultCard from "../components/GeminiResultCard";

/**
 * DiagnosticCenter
 *
 * Allows a diagnostic center to upload MRI scans for multiple patients
 * in a single session. Each patient entry has a name and one or more scans.
 * All scans are analyzed via Gemini Vision and individual reports can be downloaded.
 */

const EMPTY_PATIENT = () => ({
  id: Date.now() + Math.random(),
  name: "",
  files: [],
  previews: [],
  results: [],
  status: "pending", // pending | analyzing | done | error
  progress: 0,
});

export default function DiagnosticCenter() {
  const [patients, setPatients] = useState([EMPTY_PATIENT()]);
  const [globalLoading, setGlobalLoading] = useState(false);
  const [allDone, setAllDone] = useState(false);
  const [downloading, setDownloading] = useState({});

  const navigate = useNavigate();
  const pageRef = useRef(null);
  const fileInputRefs = useRef({});

  useEffect(() => {
    gsap.fromTo(
      pageRef.current,
      { opacity: 0, y: 30 },
      { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" }
    );
  }, []);

  // ── Patient management ──────────────────────────────────────

  const addPatient = () => {
    const newPatient = EMPTY_PATIENT();
    setPatients((prev) => [...prev, newPatient]);

    setTimeout(() => {
      const el = document.getElementById(`patient-${newPatient.id}`);
      if (el) {
        gsap.fromTo(el, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5, ease: "power3.out" });
        el.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }, 50);
  };

  const removePatient = (id) => {
    if (patients.length <= 1) return;
    const el = document.getElementById(`patient-${id}`);
    if (el) {
      gsap.to(el, {
        opacity: 0,
        x: -50,
        height: 0,
        duration: 0.4,
        ease: "power3.in",
        onComplete: () => {
          setPatients((prev) => prev.filter((p) => p.id !== id));
        },
      });
    } else {
      setPatients((prev) => prev.filter((p) => p.id !== id));
    }
  };

  const updatePatient = (id, updates) => {
    setPatients((prev) =>
      prev.map((p) => (p.id === id ? { ...p, ...updates } : p))
    );
  };

  const handleNameChange = (id, value) => {
    updatePatient(id, { name: value });
  };

  const handleFileChange = (id, e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const previews = files.map((f) => URL.createObjectURL(f));
    updatePatient(id, { files, previews, results: [], status: "pending" });
  };

  const handleFileClick = (id) => {
    if (!globalLoading && fileInputRefs.current[id]) {
      fileInputRefs.current[id].click();
    }
  };

  // ── Analyze all patients ────────────────────────────────────

  const canSubmit = patients.every((p) => p.name.trim() && p.files.length > 0);

  const handleAnalyzeAll = async () => {
    if (!canSubmit) return;

    setGlobalLoading(true);
    setAllDone(false);

    // Mark all as analyzing
    setPatients((prev) =>
      prev.map((p) => ({ ...p, status: "analyzing", progress: 0, results: [] }))
    );

    for (let pi = 0; pi < patients.length; pi++) {
      const patient = patients[pi];
      const results = [];

      for (let fi = 0; fi < patient.files.length; fi++) {
        try {
          const res = await analyzeWithGemini(patient.files[fi]);
          if (res.error) {
            results.push({ error: res.error, filename: res.filename || patient.files[fi].name });
          } else {
            res.patientName = patient.name.trim();
            results.push(res);
          }
        } catch (err) {
          results.push({ error: `Failed to analyze ${patient.files[fi].name}: ${err.message}` });
        }

        // Update progress
        const progress = Math.round(((fi + 1) / patient.files.length) * 100);
        setPatients((prev) =>
          prev.map((p) =>
            p.id === patient.id ? { ...p, progress, results: [...results] } : p
          )
        );
      }

      // Mark patient as done
      const hasError = results.every((r) => r.error);
      setPatients((prev) =>
        prev.map((p) =>
          p.id === patient.id
            ? { ...p, status: hasError ? "error" : "done", results, progress: 100 }
            : p
        )
      );
    }

    setGlobalLoading(false);
    setAllDone(true);
  };

  // ── PDF download ────────────────────────────────────────────

  const handleDownloadPDF = async (patientId, resultIdx, res) => {
    const key = `${patientId}-${resultIdx}`;
    setDownloading((prev) => ({ ...prev, [key]: true }));
    try {
      const patient = patients.find((p) => p.id === patientId);
      const payload = { ...res, patientName: patient?.name?.trim() || "Unknown" };
      const blob = await downloadGeminiPDF(payload);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `report_${(patient?.name || "patient").replace(/\s+/g, "_")}_scan${resultIdx + 1}_${new Date().toISOString().slice(0, 10)}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error("PDF download failed:", err);
      alert("Failed to download PDF. Please try again.");
    } finally {
      setDownloading((prev) => ({ ...prev, [`${patientId}-${resultIdx}`]: false }));
    }
  };

  // ── Download all reports for a patient ──────────────────────

  const handleDownloadAllForPatient = async (patientId) => {
    const patient = patients.find((p) => p.id === patientId);
    if (!patient) return;

    for (let i = 0; i < patient.results.length; i++) {
      if (!patient.results[i].error) {
        await handleDownloadPDF(patientId, i, patient.results[i]);
      }
    }
  };

  // ── Reset ────────────────────────────────────────────────────

  const handleReset = () => {
    setPatients([EMPTY_PATIENT()]);
    setAllDone(false);
    setGlobalLoading(false);
    setDownloading({});
  };

  // ── Stats ────────────────────────────────────────────────────

  const totalScans = patients.reduce((sum, p) => sum + p.files.length, 0);
  const completedPatients = patients.filter((p) => p.status === "done").length;

  // ── Render ───────────────────────────────────────────────────

  return (
    <div ref={pageRef} className="dc-page">
      <div className="dc-container">
        {/* Header */}
        <div className="dc-header">
          <button onClick={() => navigate("/")} className="back-button">
            ← Back to Home
          </button>
          <div className="dc-header-badge">🏥 DIAGNOSTIC CENTER MODE</div>
          <h1 className="dc-title">Multi-Patient MRI Analysis</h1>
          <p className="dc-subtitle">
            Upload MRI scans for multiple patients and generate AI-powered diagnostic reports in one session
          </p>

          {/* Stats bar */}
          <div className="dc-stats-bar">
            <div className="dc-stat">
              <span className="dc-stat-value">{patients.length}</span>
              <span className="dc-stat-label">Patients</span>
            </div>
            <div className="dc-stat">
              <span className="dc-stat-value">{totalScans}</span>
              <span className="dc-stat-label">Total Scans</span>
            </div>
            {allDone && (
              <div className="dc-stat dc-stat-done">
                <span className="dc-stat-value">{completedPatients}</span>
                <span className="dc-stat-label">Completed</span>
              </div>
            )}
          </div>
        </div>

        {/* Patient list */}
        <div className="dc-patient-list">
          {patients.map((patient, idx) => (
            <div
              key={patient.id}
              id={`patient-${patient.id}`}
              className={`dc-patient-card ${patient.status === "done" ? "dc-card-done" : ""} ${patient.status === "error" ? "dc-card-error" : ""} ${patient.status === "analyzing" ? "dc-card-analyzing" : ""}`}
            >
              {/* Patient header row */}
              <div className="dc-patient-top">
                <div className="dc-patient-number">Patient #{idx + 1}</div>
                <div className="dc-patient-status">
                  {patient.status === "pending" && <span className="dc-badge dc-badge-pending">Pending</span>}
                  {patient.status === "analyzing" && <span className="dc-badge dc-badge-analyzing">Analyzing… {patient.progress}%</span>}
                  {patient.status === "done" && <span className="dc-badge dc-badge-done">✓ Complete</span>}
                  {patient.status === "error" && <span className="dc-badge dc-badge-error">✗ Error</span>}
                </div>
                {patients.length > 1 && !globalLoading && (
                  <button className="dc-remove-btn" onClick={() => removePatient(patient.id)} title="Remove patient">
                    ✕
                  </button>
                )}
              </div>

              {/* Patient name input */}
              <div className="dc-patient-fields">
                <div className="dc-field">
                  <label className="dc-label">
                    Patient Name <span className="required">*</span>
                  </label>
                  <input
                    type="text"
                    value={patient.name}
                    onChange={(e) => handleNameChange(patient.id, e.target.value)}
                    placeholder="Enter patient full name"
                    className="dc-input"
                    disabled={globalLoading}
                  />
                </div>

                {/* File upload area */}
                <div className="dc-field">
                  <label className="dc-label">
                    MRI Scans <span className="required">*</span>
                  </label>
                  <div
                    className="dc-upload-zone"
                    onClick={() => handleFileClick(patient.id)}
                    style={{ cursor: globalLoading ? "not-allowed" : "pointer" }}
                  >
                    {patient.previews.length > 0 ? (
                      <div className="dc-preview-strip">
                        {patient.previews.map((url, i) => (
                          <img key={i} src={url} alt={`Scan ${i + 1}`} className="dc-preview-thumb" />
                        ))}
                        <span className="dc-file-count">{patient.files.length} file{patient.files.length > 1 ? "s" : ""}</span>
                      </div>
                    ) : (
                      <div className="dc-upload-placeholder">
                        <span className="dc-upload-icon">🧲</span>
                        <span>Click to select MRI scans</span>
                        <span className="dc-upload-hint">JPEG, PNG, DICOM — multiple allowed</span>
                      </div>
                    )}
                    <input
                      ref={(el) => (fileInputRefs.current[patient.id] = el)}
                      type="file"
                      multiple
                      accept="image/*"
                      onChange={(e) => handleFileChange(patient.id, e)}
                      style={{ display: "none" }}
                    />
                  </div>
                </div>
              </div>

              {/* Progress bar */}
              {patient.status === "analyzing" && (
                <div className="dc-progress-bar">
                  <div className="dc-progress-fill" style={{ width: `${patient.progress}%` }} />
                </div>
              )}

              {/* Results for this patient */}
              {patient.results.length > 0 && (patient.status === "done" || patient.status === "error") && (
                <div className="dc-results-section">
                  <div className="medical-disclaimer-banner">
                    ⚕️ <strong>Disclaimer:</strong> This AI-generated analysis is for informational purposes only and does not constitute a medical diagnosis. Always consult a qualified healthcare professional.
                  </div>
                  <div className="dc-results-header">
                    <h3>Results for {patient.name}</h3>
                    <button
                      className="dc-download-all-btn"
                      onClick={() => handleDownloadAllForPatient(patient.id)}
                    >
                      📄 Download All Reports
                    </button>
                  </div>
                  {patient.results.map((res, ri) => (
                    <div key={ri} className="dc-result-item">
                      <div className="dc-result-item-header">
                        <span className="dc-scan-label">
                          Scan #{ri + 1}: {res.filename || `Image ${ri + 1}`}
                        </span>
                        {!res.error && (
                          <button
                            className="download-pdf-button download-pdf-sm"
                            onClick={() => handleDownloadPDF(patient.id, ri, res)}
                            disabled={downloading[`${patient.id}-${ri}`]}
                          >
                            {downloading[`${patient.id}-${ri}`] ? (
                              <><span className="spinner" /> Generating…</>
                            ) : (
                              "📄 Download PDF"
                            )}
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
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Action bar */}
        <div className="dc-actions">
          {!globalLoading && !allDone && (
            <>
              <button className="dc-add-patient-btn" onClick={addPatient}>
                ➕ Add Another Patient
              </button>
              <button
                className="dc-analyze-all-btn"
                disabled={!canSubmit}
                onClick={handleAnalyzeAll}
                title={!canSubmit ? "Please fill in all patient names and upload scans" : ""}
              >
                🧠 Analyze All Patients ({patients.length} patient{patients.length > 1 ? "s" : ""}, {totalScans} scan{totalScans !== 1 ? "s" : ""})
              </button>
            </>
          )}

          {globalLoading && (
            <div className="dc-global-loading">
              <div className="analysis-loading-bar">
                <div className="loading-progress" />
                <span>Processing {patients.length} patient{patients.length > 1 ? "s" : ""}… Please wait.</span>
              </div>
            </div>
          )}

          {allDone && (
            <button className="dc-reset-btn" onClick={handleReset}>
              🔄 Start New Batch
            </button>
          )}
        </div>

        {/* Footer badges */}
        <div className="analysis-footer">
          <div className="status-badge">🔒 HIPAA COMPLIANT</div>
          <div className="status-badge">🏥 BATCH PROCESSING</div>
          <div className="status-badge">🧠 GEMINI VISION AI</div>
          <div className="status-badge">⚡ REAL-TIME ANALYSIS</div>
        </div>
      </div>
    </div>
  );
}
