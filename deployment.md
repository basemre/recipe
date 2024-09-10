# Recipe Recommender Deployment Plan

## 1. Prerequisites
- A VPS (e.g., from Hetzner)
- SSH access to the VPS
- Domain name (optional, but recommended)

## 2. Server Setup
1. Connect to your VPS via SSH:
   ```
   ssh user@your_server_ip
   ```
2. Update the system and install required packages:
   ```
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-pip python3-venv nginx -y
   ```

## 3. Application Deployment
1. Clone the repository:
   ```
   git clone https://github.com/your-username/recipe-recommender.git
   cd recipe-recommender
   ```
2. Set up a virtual environment and install dependencies:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create a `.env` file for environment variables:
   ```
   touch .env
   echo "DATABASE_URL=postgresql://username:password@host:port/database" >> .env
   echo "OPENAI_API_KEY=your_openai_api_key" >> .env
   ```
4. Create a `wsgi.py` file in the project root:
   ```python
   from main import app

   if __name__ == "__main__":
       app.run()
   ```

## 4. Gunicorn Setup
1. Create a systemd service file:
   ```
   sudo nano /etc/systemd/system/recipe-recommender.service
   ```
2. Add the following content (adjust paths as necessary):
   ```
   [Unit]
   Description=Recipe Recommender Flask App
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/recipe-recommender
   Environment="PATH=/path/to/recipe-recommender/venv/bin"
   EnvironmentFile=/path/to/recipe-recommender/.env
   ExecStart=/path/to/recipe-recommender/venv/bin/gunicorn --workers 3 --bind unix:recipe-recommender.sock -m 007 wsgi:app

   [Install]
   WantedBy=multi-user.target
   ```
3. Start and enable the service:
   ```
   sudo systemctl start recipe-recommender
   sudo systemctl enable recipe-recommender
   ```

## 5. Nginx Configuration
1. Create a new Nginx configuration file:
   ```
   sudo nano /etc/nginx/sites-available/recipe-recommender
   ```
2. Add the following content:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           include proxy_params;
           proxy_pass http://unix:/path/to/recipe-recommender/recipe-recommender.sock;
       }
   }
   ```
3. Enable the Nginx configuration and restart Nginx:
   ```
   sudo ln -s /etc/nginx/sites-available/recipe-recommender /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## 6. SSL Configuration (Optional)
1. Install Certbot:
   ```
   sudo apt install certbot python3-certbot-nginx
   ```
2. Obtain and install SSL certificate:
   ```
   sudo certbot --nginx -d your_domain.com
   ```

## 7. Database Setup
1. Install PostgreSQL:
   ```
   sudo apt install postgresql postgresql-contrib
   ```
2. Create a database and user:
   ```
   sudo -u postgres psql
   CREATE DATABASE recipe_recommender;
   CREATE USER recipe_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE recipe_recommender TO recipe_user;
   \q
   ```
3. Update the DATABASE_URL in the .env file with the new database credentials.

## 8. Application Initialization
1. Initialize the database:
   ```python
   from database import Base, engine
   Base.metadata.create_all(engine)
   ```

## 9. Firewall Configuration
1. Configure UFW to allow Nginx and SSH:
   ```
   sudo ufw allow 'Nginx Full'
   sudo ufw allow OpenSSH
   sudo ufw enable
   ```

## 10. Monitoring and Logging
1. Set up application logging:
   ```
   sudo mkdir /var/log/recipe-recommender
   sudo chown your_username:your_username /var/log/recipe-recommender
   ```
2. Update the Gunicorn command in the systemd service file to include logging:
   ```
   ExecStart=/path/to/recipe-recommender/venv/bin/gunicorn --workers 3 --bind unix:recipe-recommender.sock -m 007 --access-logfile /var/log/recipe-recommender/access.log --error-logfile /var/log/recipe-recommender/error.log wsgi:app
   ```
3. Restart the service:
   ```
   sudo systemctl restart recipe-recommender
   ```

## 11. Backup Strategy
1. Set up a cron job for daily database backups:
   ```
   sudo crontab -e
   ```
   Add the following line:
   ```
   0 2 * * * pg_dump -U recipe_user recipe_recommender > /path/to/backups/recipe_recommender_$(date +\%Y\%m\%d).sql
   ```

## 12. Updating the Application
1. Pull the latest changes:
   ```
   cd /path/to/recipe-recommender
   git pull origin main
   ```
2. Activate the virtual environment and update dependencies:
   ```
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Restart the application:
   ```
   sudo systemctl restart recipe-recommender
   ```

## 13. Troubleshooting
- Check application logs:
  ```
  sudo journalctl -u recipe-recommender
  ```
- Check Nginx logs:
  ```
  sudo tail -f /var/log/nginx/error.log
  ```
- Verify Gunicorn socket:
  ```
  file /path/to/recipe-recommender/recipe-recommender.sock
  ```

Remember to replace placeholders like your_username, your_domain.com, and /path/to/recipe-recommender with your actual values throughout this deployment plan.

For reference to the project structure and files, you can refer to these code blocks:
```
.
├── .streamlit/
│ └── config.toml
├── data/
│ └── recipes.csv
├── static/
│ ├── index.html
│ ├── script.js
│ ├── style.css
│ └── translations.js
├── database.py
├── main.py
├── model.py
├── recipe_manager.py
├── requirements.txt
└── README.md
```

These show the project structure and the required Python packages, which are important for setting up the deployment environment correctly.

Flask==2.1.0
SQLAlchemy==1.4.31
psycopg2-binary==2.9.3
python-dotenv==0.19.2
openai==0.27.0
pandas==1.3.5
requests==2.27.1
gunicorn==20.1.0