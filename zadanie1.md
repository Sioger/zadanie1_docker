# docker-zadanie1-geoip-server-basic
This project showcases the process of building a Docker image with a server-side application that respond with the client's IP and time.

## Table of Contents

- [Requirements](#requirements)
- [Server application](#server-application)
- [Dockerfile](#dockerfile)
- [Image Building](#image-building)
- [Container Running](#container-running)
- [Diagnostics](#diagnostics)
- [Repository And Scouting](#repository-and-scouting)

## Requirements

W przypadku systemów Linux i Windows należy zainstalować i uruchomić Docker lub Docker Desktop. 

W przypadku systemów Windows należy zainstalować WSL.

## Server application

Kod aplikacji serwerowej wraz z komentarzami.

```php
import http.server
import socketserver
import datetime

# Definicja portu, na którym serwer będzie nasłuchiwał zgłoszenia klienta
PORT = 8080

# Definicja nazwy autora serwera
AUTHOR_NAME = "John Doe"

# Klasa obsługująca żądania HTTP
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # Metoda obsługująca żądania typu GET
    def do_GET(self):
        # Pobranie adresu IP klienta
        client_ip = self.client_address[0]
        
        # Utworzenie wiadomości zawierającej adres IP klienta i aktualną datę i godzinę
        message = "Witaj! Twój adres IP to: {}\n".format(client_ip)
        message += "Data i godzina w twojej strefie czasowej: {}\n".format(datetime.datetime.now())
        
        # Wysłanie odpowiedzi do klienta
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(bytes(message, "utf8"))
        return

# Pobranie aktualnej daty i godziny w formacie "YYYY-MM-DD HH:MM:SS"
log_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Wyświetlenie informacji o uruchomieniu serwera
print(f"Serwer uruchomiony przez: {AUTHOR_NAME}")
print(f"Data uruchomienia: {log_date}")
print(f"Serwer nasłuchuje na porcie: {PORT}")

# Uruchomienie serwera na podanym porcie
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    httpd.serve_forever()

```

The server app was tested on a public server, because on localhost it only shows the local address. For testing, a VPN was used on a British server to confirm that the server works also for public responses.

![Client IP Public VPN](screenshots/client-ip-public-vpn.jpg)

Link: [render-slot-1.onrender.com](https://render-slot-1.onrender.com/)

## Dockerfile

A two-stage Dockerfile divided into building and running parts.

```dockerfile
# Stage 1: Application Building

FROM node:20.13.1-alpine as build

WORKDIR /server-app

COPY package*.json ./

COPY server.js ./

# Only geoip-lite is needed for this project
RUN npm install geoip-lite


# Stage 2: Application Run

FROM node:20.13.1-alpine as production

LABEL org.opencontainers.image.authors="Jakub Kopeć"

WORKDIR /server-app

COPY --from=build /server-app .

# Port 3000 is exposed but if PORT is set in the environment variable it will be used instead
EXPOSE 3000

RUN apk add --no-cache curl

HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:3000 || exit 1

CMD ["node", "server.js"]


# Build the image

# docker build -t geoip-server .

# Run the container

# docker run -d -p 3000:3000 --name ip-check-server geoip-server

# Get logs

# docker logs ip-check-server

# Check how many layers are in the image

# docker inspect --format="{{len .RootFS.Layers}}" geoip-server
```

## Image Building

Example for Windows:

Run the command below to build an image. Change the '-t' parameter value to your desired image name.

```cmd
docker build -t geoip-server .
```

Result:

![Build](screenshots/build.jpg)

## Container Running

Run the command below to run an container. Change the '-p' parameter value to your desired ports and '--name' to your desired name the container.

```cmd
docker run -d -p 3000:3000 --name ip-check-server geoip-server
```

Result:

![Run](screenshots/run.jpg)

## Diagnostics

Checking logs of the server container.

```cmd
docker logs ip-check-server
```

Result:

![Logs](screenshots/logs.jpg)

Checking the number of image layers.

```cmd
docker inspect --format="{{len .RootFS.Layers}}" geoip-server
```

Result:

![Layers](screenshots/layers.jpg)

Checking if the container is healthy.

```cmd
docker ps --filter name=ip-check-server
```

Result:

![Healthy](screenshots/healthy.jpg)

Checking if the service is working on a web browser. Put 'http://localhost:3000' into the search bar.

Result:

![Client IP Local](screenshots/client-ip-local.jpg)

## Repository And Scouting

Create a repository on [hub.docker.com](https://hub.docker.com/) on your account.

Enroll your account.

```cmd
docker scout enroll eyelor
```

Result:

![Enroll Org](screenshots/enroll-org.jpg)

Enroll your repository.

```cmd
docker scout repo enable --org eyelor eyelor/zadanie1
```

Result:

![Enroll Repo](screenshots/enroll-repo.jpg)

Push your image to your repository.

```cmd
docker build -q -t docker.io/eyelor/zadanie1:geoip-server-basic --platform linux/amd64 --push .
```

Now perform scout image scanning using cves showing only critical and high severities.

```cmd
docker cves --only-severity critical,high eyelor/zadanie1:geoip-server-basic
```

Result:

![CVES Inspection](screenshots/cves-inspection.jpg)

There are no critical or high severities.

Link to this image: [hub.docker.com/layers/eyelor/zadanie1/geoip-server-basic/images/sha256-7c32d1136cca6b611a53eea12f8fa7c0c45b66b61c8119b7b5160d14c3abfdeb](https://hub.docker.com/layers/eyelor/zadanie1/geoip-server-basic/images/sha256-7c32d1136cca6b611a53eea12f8fa7c0c45b66b61c8119b7b5160d14c3abfdeb)
