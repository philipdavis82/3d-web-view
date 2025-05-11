import * as djauth from "$lib/hooks/django-auth.js";

// auth.getAuthToken()

/**
/ * Fetches directories from the Django API
/ * @param   {number} id - User's password
/ * @returns {Promise<any>} - Authentication token if successful
/*/
export async function getDirectories(id){
    const url = 'http://127.0.0.1:8000/api/directories/dirid/'+id;
    const token = djauth.getAuthToken();
    const headers = djauth.addAuthHeader({
        'Content-Type': 'application/json',
    });

    try {
        const response = await fetch(url, {
        method: 'GET',
        headers: headers,
        });

        if (!response.ok) {
        throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching directories:', error);
    }
}

/**
/ * Fetches directories from the Django API
/ * @param   {number} id - User's password
/ * @returns {Promise<any>} - Authentication token if successful
/*/
export async function getSTLs(id){
    const url = 'http://127.0.0.1:8000/api/stls/dirid/'+id;
    const token = djauth.getAuthToken();
    const headers = djauth.addAuthHeader({
        'Content-Type': 'application/json',
    });

    try {
        const response = await fetch(url, {
        method: 'GET',
        headers: headers,
        });

        if (!response.ok) {
        throw new Error('Network response was not ok');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching directories:', error);
    }
}