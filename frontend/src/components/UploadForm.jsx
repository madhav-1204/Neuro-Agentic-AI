import { useState } from "react";
import { analyzeSingle } from "../api/api";

export default function UploadForm({ onResult }) {
    const [loading, setLoading] = useState(false);
    const [preview, setPreview] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setPreview(URL.createObjectURL(file));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const file = e.target.file.files[0];
        if (!file) return;

        setLoading(true);
        onResult(null);

        try {
            const result = await analyzeSingle(file);
            onResult(result);
        } catch (err) {
            onResult({ error: "Failed to connect to backend." });
        }

        setLoading(false);
    };

    return (
        <div className="card">
            <form onSubmit={handleSubmit}>
                <input
                    type="file"
                    name="file"
                    accept="image/*"
                    className="input-file"
                    onChange={handleFileChange}
                />

                {preview && (
                    <img
                        src={preview}
                        alt="Preview"
                        style={{ width: "100%", marginBottom: "15px", borderRadius: "8px" }}
                    />
                )}

                <button className="button" type="submit" disabled={loading}>
                    {loading ? "Analyzing..." : "Analyze MRI"}
                </button>
            </form>
        </div>
    );
}