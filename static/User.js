class User {
    constructor(userData) {
        this.id = userData._id;
        this.username = userData.username;
        this.role = userData.role;
    }

    update(newData) {
        Object.assign(this, newData);
    }
}
