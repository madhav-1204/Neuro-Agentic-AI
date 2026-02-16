export default function PredictionCard({ result }) {
    if (!result) return null;

    if (result.error) {
        return <div style={{ color: "red" }}>{result.error}</div>;
    }

    const { prediction, explanation } = result;

    return (
        <div style={{ marginTop: "20px", border: "1px solid #ccc", padding: "15px" }}>
            <h3>Prediction</h3>
            <p><strong>Class:</strong> {prediction.predicted_class}</p>
            <p><strong>Confidence:</strong> {prediction.confidence.toFixed(2)}%</p>

            <h4>Explanation</h4>
            <p>{explanation}</p>
        </div>
    );
}