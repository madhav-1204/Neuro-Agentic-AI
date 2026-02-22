import { useState, useRef } from "react";
import { analyzeSingle } from "../api/api";
import { gsap } from "gsap";

export default function UploadForm({ onResult }) {
    const [loading, setLoading] = useState(false);
    const [fileName, setFileName] = useState("");
    const fileInputRef = useRef(null);
    const uploadBoxRef = useRef(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setFileName(file.name);
            gsap.fromTo(uploadBoxRef.current, 
                { scale: 0.95 }, 
                { scale: 1, duration: 0.3, ease: "back.out(1.7)" }
            );
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const file = fileInputRef.current.files[0];
        if (!file) return;

        setLoading(true);
        onResult(null);

        try {
            const result = await analyzeSingle(file);
            onResult(result);
            
            // Success animation
            gsap.to(uploadBoxRef.current, {
                backgroundColor: "rgba(16, 185, 129, 0.1)",
                duration: 0.5,
                yoyo: true,
                repeat: 1
            });
        } catch (err) {
            onResult({ error: "Failed to connect to backend." });
            
            // Error animation
            gsap.to(uploadBoxRef.current, {
                x: [-10, 10, -10, 10, 0],
                duration: 0.5
            });
        }

        setLoading(false);
    };

    const handleBoxClick = () => {
        fileInputRef.current.click();
    };

    return (
        <form onSubmit={handleSubmit}>
            <div 
                ref={uploadBoxRef}
                className="upload-box"
                onClick={!loading ? handleBoxClick : undefined}
                style={{
                    cursor: loading ? 'not-allowed' : 'pointer',
                    transition: 'all 0.3s'
                }}
            >
                <div className="upload-icon">
                    {loading ? "⏳" : "📁"}
                </div>
                <p className="upload-text">
                    {loading 
                        ? "Analyzing..." 
                        : fileName 
                        ? fileName 
                        : "Drop your DICOM/JPEG/PNG MRI scan here"
                    }
                </p>
                <p className="upload-subtext" style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                    {!loading && !fileName && "or click to browse files"}
                </p>
                <input 
                    ref={fileInputRef}
                    type="file" 
                    onChange={handleFileChange}
                    accept="image/*" 
                    style={{ display: 'none' }}
                />
            </div>
            
            {fileName && !loading && (
                <button type="submit" className="analyze-btn">
                    🧠 Start Neural Analysis
                </button>
            )}
        </form>
    );
}
