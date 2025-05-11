// Django Authentication Client

// /**
//  * Authenticates with Django REST framework and stores the token
//  * @param {string} baseUrl - API base URL (e.g., 'https://api.example.com')
//  */
// async function getCSRFToken(baseUrl) {
//   const response = await fetch(`${baseUrl}/csrf-token/`);
//   const data = await response.json();
//   console.log('Response:', data);
//   return data.csrfToken;
// }

/**
 * Authenticates with Django REST framework and stores the token
 * @param {string} baseUrl - API base URL (e.g., 'https://api.example.com')
 * @param {string} username - User's username
 * @param {string} password - User's password
 * @returns {Promise<string>} - Authentication token if successful
 */
export async function authenticateWithDjango(baseUrl, username, password) {
  try {
    // Make API request to Django's token auth endpoint
    const response = await fetch(`${baseUrl}/api-token-auth/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password
      })
    });
    console.log('Response:', response);
    // Check if request was successful
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || 'Authentication failed');
    }

    // Extract token from response
    const data = await response.json();
    const token = data.token;

    // Store token in localStorage
    localStorage.setItem('authToken', token);

    // Also store the expiry time if your Django setup includes it
    if (data.expiry) {
      localStorage.setItem('tokenExpiry', data.expiry);
    }

    console.log('Authentication successful');
    return token;
  } catch (error) {
    console.error('Authentication error:', error);
    throw error;
  }
}

/**
 * Checks if the stored token is still valid
 * @returns {boolean} - True if token exists and is not expired
 */
export function isAuthenticated() {
  const token = localStorage.getItem('authToken');
  const expiry = localStorage.getItem('tokenExpiry');

  if (!token) return false;

  // If expiry date is stored, check if token is still valid
  if (expiry) {
    return new Date(expiry) > new Date();
  }

  // If no expiry is stored, just check for token existence
  return !!token;
}

/**
 * Retrieves the stored authentication token
 * @returns {string|null} - The authentication token or null if not found
 */
export function getAuthToken() {
  return localStorage.getItem('authToken');
}

/**
 * Adds authentication token to request headers
 * @param {Object} headers - Existing headers object
 * @returns {Object} - Headers with authentication token added
 */
export function addAuthHeader(headers = {}) {
  const token = getAuthToken();
  if (token) {
    return {
      ...headers,
      'Authorization': `Token ${token}`  // Django REST framework uses Token auth by default
    };
  }
  return headers;
}

/**
 * Logs out the user by removing the stored token
 */
export function logout() {
  localStorage.removeItem('authToken');
  localStorage.removeItem('tokenExpiry');
  console.log('Logged out successfully');
}

/**
 * Example usage of the authentication functions
 */
// export async function exampleUsage() {
//   // Login
//   try {
//     const baseUrl = 'https://api.example.com';
//     const username = 'user123';
//     const password = 'securepassword';

//     await authenticateWithDjango(baseUrl, username, password);
//     let table = {
//       headers: addAuthHeader({
//         'Content-Type': 'application/json'
//       })
//     }; 
//     // Make authenticated request
//     if (isAuthenticated()) {
//       const response = await fetch(`${baseUrl}/api/protected-resource/`,
//         table  
//       );

//       const data = await response.json();
//       console.log('Protected data:', data);
//     }
//   } catch (error) {
//     console.error('Error in example:', error);
//   }
// }

