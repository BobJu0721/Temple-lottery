async function apiCall(endpoint, options = {}) {
  const url = `/api/v1${endpoint}`;
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'API 請求失敗');
    }
    return await response.json();
  } catch (error) {
    console.error(`API Error (${endpoint}):`, error);
    throw error;
  }
}

const API = {
  getGods: () => apiCall('/gods'),
  drawFortune: (godId, wishText) => apiCall('/fortune/draw', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ god_id: godId, wish_text: wishText })
  }),
  getFortuneHistory: () => apiCall('/fortune/history'),
  createDonation: (data) => apiCall('/donation', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  }),
  getDonationHistory: () => apiCall('/donation/history')
};
