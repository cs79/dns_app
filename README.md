# Overview
Simple orchestrated Flask applications + UDP server for name registration.

## Deployment
First, create a Docker network for the applications to communicate on; we call our network `dcn`:

`docker network create dcn`

Next, deploy the individual Docker application containers:

* **AS (DNS server):** `docker run --network dcn --name dns_server -p 53533:53533/udp -it cs79/as:latest`
* **FS (performs Fibonacci calculations):** `docker run --network dcn --name fs_flask -p 9090:9090 -it cs79/fs:latest`
* **US (processes user requests):** `docker run --network dcn --name us_flask -p 8080:8080 -it cs79/us:latest`

N.B. if using a different Docker network, the names must be changed in the commands accordingly.

## DNS Registration
Next, have the FS register with the AS so that the US will be able to find it:

`curl -X POST -H "Content-Type: application/json" -d '{"hostname":"fibonacci.com", "ip":"172.18.0.2", "as_ip":"172.18.0.4", "as_port":"53533"}' localhost:9090/register`

(N.B. this `curl` command assumes a Linux terminal; if using a different platform you may need to alter the command accordingly.)

## Using the application
Once all Docker applications have been deployed and the FS has been registered with the AS, user requests can be processes via a web browser at `localhost:8080` using the specially formatted URL string:

`localhost:8080/fibonacci?hostname=fibonacci.com/fs_port=9090&number=X&as_ip=Y&as_port=53533`

Where `X` is the `n`th Fibonacci number for the FS to calculate, and `Y` is the IP address of the AS (DNS server).
