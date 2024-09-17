class Auth {
    constructor() {
        this.token = null;
        this.user = null;
    }

    async login(username, password) {
        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            this.user = { id: data.user_id, username };
            return this.user;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    async logout() {
        try {
            await fetch('/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });
            this.user = null;
        } catch (error) {
            console.error('Logout error:', error);
        }
    }

    isAuthenticated() {
        return !!this.user;
    }

    async checkAuthStatus() {
        try {
            const response = await fetch('/auth/user', {
                credentials: 'include'
            });

            if (!response.ok) {
                this.user = null;
                return false;
            }

            const userData = await response.json();
            this.user = userData;
            return true;
        } catch (error) {
            console.error('Auth check error:', error);
            this.user = null;
            return false;
        }
    }
}

const auth = new Auth();