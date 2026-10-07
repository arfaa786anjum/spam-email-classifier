const API_BASE_URL = 'http://127.0.0.1:8000';

export const analyzeEmail = async (subject, body) => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ subject, body }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      // FastAPI Validation error (422) often has details in 'detail' array
      let errorMessage = errorData.detail || 'Failed to analyze email';
      if (Array.isArray(errorMessage)) {
         errorMessage = errorMessage[0]?.msg || 'Invalid input';
      }
      throw new Error(errorMessage);
    }

    return await response.json();
  } catch (error) {
    if (error.message === 'Failed to fetch') {
      throw new Error('Could not connect to the server. Please ensure the backend is running.');
    }
    throw error;
  }
};
