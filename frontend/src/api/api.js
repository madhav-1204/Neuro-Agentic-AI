const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function analyzeSingle(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  return await response.json();
}

export async function analyzeWithGemini(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/analyze/gemini`, {
    method: "POST",
    body: formData,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data?.error || data?.detail || `Server error (${response.status})`);
  }

  return data;
}

export async function downloadGeminiPDF(result) {
  const response = await fetch(`${BASE_URL}/analyze/gemini/download-pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(result),
  });

  if (!response.ok) throw new Error("Failed to generate PDF");
  return await response.blob();
}

export async function analyzeBatch(files) {
  const formData = new FormData();
  files.forEach(file => {
    formData.append("files", file);
  });

  const response = await fetch(`${BASE_URL}/analyze/batch`, {
    method: "POST",
    body: formData,
  });

  return await response.json();
}

export async function analyzeBatchGemini(files) {
  const formData = new FormData();
  files.forEach(file => {
    formData.append("files", file);
  });

  const response = await fetch(`${BASE_URL}/analyze/gemini/batch`, {
    method: "POST",
    body: formData,
  });

  return await response.json();
}