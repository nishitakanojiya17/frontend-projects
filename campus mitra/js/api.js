/**
 * Campus Mitra — API Helper
 * Centralised fetch wrapper that attaches the JWT Bearer token to every request
 * and handles 401 (token expired) by redirecting to login.
 *
 * Usage:
 *   const data = await apiFetch('attendance/my/');
 *   const result = await apiFetch('attendance/mark/', { method: 'POST', body: JSON.stringify({...}) });
 */

const BACKEND_URL = (window.BACKEND_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

/**
 * Make an authenticated API call.
 * @param {string} endpoint  - e.g. 'attendance/my/' (no leading slash)
 * @param {object} options   - standard fetch options (method, body, headers, …)
 * @returns {Promise<any>}   - parsed JSON response
 */
async function apiFetch(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');

  const res = await fetch(`${BACKEND_URL}/api/${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  // Token expired — try to refresh once
  if (res.status === 401) {
    const refreshed = await tryRefresh();
    if (refreshed) {
      // Retry original request with new token
      return apiFetch(endpoint, options);
    }
    // Refresh failed — kick to login
    localStorage.clear();
    window.location.href = 'login.html';
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

/**
 * Attempt to refresh the access token using the stored refresh token.
 * @returns {boolean} true if refresh succeeded
 */
async function tryRefresh() {
  const refresh = localStorage.getItem('refresh_token');
  if (!refresh) return false;

  try {
    const res = await fetch(`${BACKEND_URL}/api/auth/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    localStorage.setItem('access_token', data.access);
    return true;
  } catch {
    return false;
  }
}

/**
 * Check if the user is logged in. Redirect to login if not.
 * Call this at the top of every dashboard page.
 * @param {string} [requiredRole] - optional role check ('student', 'faculty', etc.)
 */
function requireAuth(requiredRole = null) {
  const token = localStorage.getItem('access_token');
  const role  = localStorage.getItem('role');

  if (!token) {
    window.location.href = 'login.html';
    return false;
  }

  if (requiredRole && role !== requiredRole) {
    alert(`Access denied. This page is for ${requiredRole}s only.`);
    window.location.href = 'login.html';
    return false;
  }

  return true;
}

/**
 * Log out — clear storage and redirect to login.
 */
function logout() {
  localStorage.clear();
  window.location.href = 'login.html';
}
