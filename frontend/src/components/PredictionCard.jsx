export default function PredictionCard({ result }) {
    if (!result) return null;

    if (result.error) {
        return (
            <div className="card">
                <div className="error">{result.error}</div>
            </div>
        );
    }

    const { prediction, explanation } = result;

    return (
        <div className="card">
            <h2>Diagnosis Result</h2>

            <p>
                <strong>Predicted Class:</strong> {prediction.predicted_class}
            </p>

            <p>
                <strong>Confidence:</strong>{" "}
                {Number(prediction.confidence).toFixed(2)}%
            </p>

            <h3>Probability Distribution</h3>

            {prediction.class_names.map((cls, index) => {
                const value = prediction.probabilities[index] * 100;

                return (
                    <div key={cls}>
                        <div style={{ fontSize: "14px", marginBottom: "4px" }}>
                            {cls} — {value.toFixed(2)}%
                        </div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${value}%` }}
                            />
                        </div>
                    </div>
                );
            })}

            <h3>Explanation</h3>
            <p>{explanation}</p>
        </div>
    );
  }