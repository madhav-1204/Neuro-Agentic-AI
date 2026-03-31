const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export async function analyzeSingle(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${BASE_URL}/analyze`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data?.error || data?.detail || `Server error (${response.status})`);
    }

    return await response.json();
  } catch (err) {
    throw new Error(err.message || 'Failed to analyze');
  }
}

export async function analyzeWithGemini(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${BASE_URL}/analyze/gemini`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data?.error || data?.detail || `Server error (${response.status})`);
    }

    const data = await response.json();
    return data;
  } catch (err) {
    throw new Error(err.message || 'Network error or server unreachable');
  }
}

export async function downloadGeminiPDF(result) {
  try {
    const response = await fetch(`${BASE_URL}/analyze/gemini/download-pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(result),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data?.error || data?.detail || `Server error (${response.status})`);
    }
    
    return await response.blob();
  } catch (err) {
    throw new Error(err.message || 'Failed to generate PDF');
  }
}

export async function analyzeBatch(files) {
  const formData = new FormData();
  files.forEach(file => {
    formData.append("files", file);
  });

  try {
    const response = await fetch(`${BASE_URL}/analyze/batch`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data?.error || data?.detail || `Server error (${response.status})`);
    }

    return await response.json();
  } catch (err) {
    throw new Error(err.message || 'Batch analysis failed');
  }
}

export async function analyzeBatchGemini(files) {
  const formData = new FormData();
  files.forEach(file => {
    formData.append("files", file);
  });

  try {
    const response = await fetch(`${BASE_URL}/analyze/gemini/batch`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new Error(data?.error || data?.detail || `Server error (${response.status})`);
    }

    return await response.json();
  } catch (err) {
    throw new Error(err.message || 'Batch analysis failed');
  }
}