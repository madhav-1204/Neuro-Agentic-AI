import { useState } from "react";
import UploadForm from "../components/UploadForm";
import PredictionCard from "../components/PredictionCard";

export default function Analyzer() {
    const [result, setResult] = useState(null);

    return (
        <div className="app-container">
            <h1>MRI Analysis</h1>
            <UploadForm onResult={setResult} />
            <PredictionCard result={result} />
        </div>
    );
}