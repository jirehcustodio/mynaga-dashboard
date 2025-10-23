import axios from 'axios'

const API = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// CASES API
export const caseAPI = {
  getAll: (skip = 0, limit = 100, filters = {}) =>
    API.get('/cases', { params: { skip, limit, ...filters } }),
  
  getById: (id) => API.get(`/cases/${id}`),
  
  create: (data) => API.post('/cases', data),
  
  update: (id, data) => API.put(`/cases/${id}`, data),
  
  delete: (id) => API.delete(`/cases/${id}`),
  
  addUpdate: (id, data) => API.post(`/cases/${id}/updates`, data),
  
  assignOffice: (caseId, officeId) =>
    API.post(`/cases/${caseId}/offices/${officeId}`),
  
  assignCluster: (caseId, clusterId) =>
    API.post(`/cases/${caseId}/clusters/${clusterId}`),
  
  addTag: (caseId, data) => API.post(`/cases/${caseId}/tags`, data),
}

// OFFICES API
export const officeAPI = {
  getAll: () => API.get('/offices'),
  
  create: (data) => API.post('/offices', data),
}

// CLUSTERS API
export const clusterAPI = {
  getAll: () => API.get('/clusters'),
  
  create: (data) => API.post('/clusters', data),
  
  update: (id, data) => API.put(`/clusters/${id}`, data),
}

// TAGS API
export const tagAPI = {
  delete: (id) => API.delete(`/tags/${id}`),
}

// STATISTICS API
export const statsAPI = {
  getAll: () => API.get('/stats'),
}

// FILE IMPORT/EXPORT API
export const fileAPI = {
  importExcel: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return API.post('/import/excel', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  
  exportExcel: () => API.get('/export/excel'),
}

export default API
