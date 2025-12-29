import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getTaxSchemes = async () => {
  try {
    const response = await api.get('/tax-schemes');
    return response.data;
  } catch (error) {
    console.error('Error fetching tax schemes:', error);
    throw error;
  }
};

export const getPendingUpdates = async () => {
  try {
    const response = await api.get('/updates');
    return response.data;
  } catch (error) {
    console.error('Error fetching pending updates:', error);
    throw error;
  }
};

export const getUpdateDetail = async (updateId) => {
  try {
    const response = await api.get(`/updates/${updateId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching update detail:', error);
    throw error;
  }
};

export const acceptUpdate = async (updateId, accept) => {
  try {
    const response = await api.post(`/updates/${updateId}/accept`, {
      accept,
    });
    return response.data;
  } catch (error) {
    console.error('Error processing update:', error);
    throw error;
  }
};

export const getEvidenceFile = (filename) => {
  return `${API_BASE_URL}/evidence/${filename}`;
};

export const triggerCrawl = async (url) => {
  try {
    const response = await api.post('/crawl', null, {
      params: { url },
    });
    return response.data;
  } catch (error) {
    console.error('Error triggering crawl:', error);
    throw error;
  }
};

export const getAuditLogs = async () => {
  try {
    const response = await api.get('/audit-logs');
    return response.data;
  } catch (error) {
    console.error('Error fetching audit logs:', error);
    throw error;
  }
};

export default api;
