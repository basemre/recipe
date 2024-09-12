class Auth {
    constructor() {
        this.token = localStorage.getItem('token') || null;
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
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            const data = await response.json();
            this.token = data.token;
            localStorage.setItem('token', this.token);
            this.user = new User(data.user);
            return this.user;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    logout() {
        this.token = null;
        this.user = null;
        localStorage.removeItem('token');
    }

    isAuthenticated() {
        return !!this.token;
    }

    getToken() {
        return this.token;
    }

    async checkAuthStatus() {
        if (!this.token) {
            return false;
        }

        try {
            const response = await fetch('/auth/user', {
                headers: {
                    'Authorization': `Bearer ${this.token}`,
                },
            });

            if (!response.ok) {
                this.logout();
                return false;
            }

            const userData = await response.json();
            this.user = new User(userData);
            return true;
        } catch (error) {
            console.error('Auth check error:', error);
            this.logout();
            return false;
        }
    }
}

const auth = new Auth();