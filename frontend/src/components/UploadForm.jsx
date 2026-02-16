import { useState } from "react";
import { analyzeSingle } from "../api/api";

export default function UploadForm({ onResult }) {
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();

        const file = e.target.file.files[0];
        if (!file) return;

        setLoading(true);

        try {
            const result = await analyzeSingle(file);
            onResult(result);
        } catch (err) {
            console.error(err);
            onResult({ error: "Failed to connect to backend." });
        }

        setLoading(false);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="file" name="file" accept="image/*" />
            <button type="submit" disabled={loading}>
                {loading ? "Analyzing..." : "Analyze"}
            </button>
        </form>
    );
}