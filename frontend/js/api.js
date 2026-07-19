/**
 * Todas las llamadas se hacen contra rutas relativas "/api/...".
 * Esto es intencional: el navegador SIEMPRE habla con el mismo origen
 * (http://localhost, servido por NGINX), y es NGINX quien decide a que
 * nodo de la aplicacion reenviar la peticion. Nunca se hardcodea una URL
 * de backend distinta.
 */
const Api = (() => {
  const BASE_URL = '/api';

  function getToken() {
    return sessionStorage.getItem('ad_token');
  }

  function setToken(token) {
    sessionStorage.setItem('ad_token', token);
  }

  function clearToken() {
    sessionStorage.removeItem('ad_token');
    sessionStorage.removeItem('ad_user');
  }

  async function request(path, { method = 'GET', body, auth = true } = {}) {
    const headers = { 'Content-Type': 'application/json' };

    if (auth) {
      const token = getToken();
      if (token) headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined
    });

    // Header de diagnostico: que nodo de la app respondio (fines academicos).
    const node = response.headers.get('X-App-Node');
    if (node) {
      document.dispatchEvent(new CustomEvent('ad:node', { detail: node }));
    }

    let data = null;
    try {
      data = await response.json();
    } catch (_) {
      data = null;
    }

    if (!response.ok) {
      const message = (data && data.error) || `Error HTTP ${response.status}`;
      throw new Error(message);
    }

    return data;
  }

  return {
    login: (email, password) =>
      request('/auth/login', { method: 'POST', body: { email, password }, auth: false }),

    getTasks: () => request('/tasks'),

    getTask: (id) => request(`/tasks/${id}`),

    submitTask: (id, answer) =>
      request(`/tasks/${id}/submit`, { method: 'POST', body: { answer } }),

    getSubmissionForTask: (taskId) => request(`/submissions/${taskId}`),

    createTask: (task) => request('/tasks', { method: 'POST', body: task }),

    getToken,
    setToken,
    clearToken
  };
})();
