# Install
https://airflow.apache.org/docs/stable/start.html
https://habr.com/ru/post/462161/

export AIRFLOW_HOME="/home/dimk/Python/airflow_course/airflow_1/airflow"
source env/bin/activate

# Start
airflow scheduler -D
airflow webserver -p 8080 -date

# Auth
basic auth: https://airflow.apache.org/docs/1.10.1/security.html


# Services 
https://medium.com/@shahbaz.ali03/run-apache-airflow-as-a-service-on-ubuntu-18-04-server-b637c03f4722


sudo service airflow-schedluer start

# SSH
echo *sha pub key* >> ~/.ssh/authorized_keys