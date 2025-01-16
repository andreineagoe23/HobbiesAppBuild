const API_BASE_URL = "http://127.0.0.1:8000";

export const fetchAPI = async (endpoint: string, method: string, body?: Record<string, any>) => {
  const authToken = localStorage.getItem('authToken');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (authToken) {
    headers['Authorization'] = `Token ${authToken}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(`Error from ${endpoint}:`, errorText);
    throw new Error(`HTTP error: ${response.status}`);
  }

  return response.json();
};
