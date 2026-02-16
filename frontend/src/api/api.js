const BASE_URL = "http://127.0.0.1:8000";

export async function analyzeSingle(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  return await response.json();
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