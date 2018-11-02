1) install mysql-server supervisor nginx
1.1)   - mysql -e "create user itea identified by 'itea';"
       - mysql -e "create database itea;"
       - mysql -e "grant all privileges on itea.* to itea;"
2) install redis-server
3) install ufw
4) ufw allow 80
5.0) sudo apt install python3-pip
5) pip install -r requirements.txt
6) python app.py ( для запуску вручну)
7) supervisord -c supervisor.conf   (для запуску supervisorom )
7) для prod налаштувати nginx