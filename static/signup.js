async function signup(username, password) {
    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
            throw new Error('Signup failed');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Signup error:', error);
        throw error;
    }
}
