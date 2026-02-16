import { useState } from "react";
import UploadForm from "./components/UploadForm";
import PredictionCard from "./components/PredictionCard";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>Neuro Diagnosis AI</h1>
      <UploadForm onResult={setResult} />
      <PredictionCard result={result} />
    </div>
  );
}

export default App;