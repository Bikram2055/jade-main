server {
    listen ${LISTEN_PORT};
    server_name ${SERVER_NAME};

    location / {
        proxy_pass ${APP_HOST}:{APP_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
