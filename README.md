# WebSocket Heart Rate to OpenSoundControl 💓

## Overview

This Python script receives heart rate data from a WebSocket server and sends the data as OSC messages to control avatar parameters in VRChat. It is intended to be used with the following project:

- [Ant Plus Heart Rate WebSocket](https://github.com/GhostJumper/ant-plus-heart-rate-ws)

## Features 🌟

- Listen to WebSocket
- Build averages over the past 5 values
- Send OSC values to VRC

## Configuration

The following environment variables can be configured to modify the behavior of the script:

- `VRCHAT_OSC_IP`: IP address of the VRChat OSC server (default: `"127.0.0.1"`).
- `VRCHAT_OSC_PORT`: Port of the VRChat OSC server (default: `9000`).
- `WEBSOCKET_IP`: IP address of the WebSocket server (default: `"127.0.0.1"`).
- `WEBSOCKET_PORT`: Port of the WebSocket server (default: `8080`).
- `DEVICE_ID`: Device ID of the heart rate monitor (default: `19635`).
- `PROFILE`: Profile type (default: `'HR'`).
- `OSC_HEART_RATE_PARAMETER`: OSC message parameter to control avatar parameters (default: `'/avatar/parameters/Hologram'`).
- `MIN_HR`: Minimum heart rate (default: `60`).
- `MAX_HR`: Maximum heart rate (default: `120`).
- `MIN_PARAM_VALUE`: Minimum value of the avatar parameter 📉 (default: `0.1`).
- `MAX_PARAM_VALUE`: Maximum value of the avatar parameter 📈 (default: `0.74`).

Note that variables in all caps are likely to need changes depending on your setup. `"127.0.0.1"` will not work inside the container!

The `MIN_PARAM_VALUE` and `MAX_PARAM_VALUE` set limits for the outgoing (sent) values to control the avatar parameters. These limits need to be specified according to your specific requirements 🎛️.

## Dockerfile 🐳

### Building the Docker image

To build the Docker image, navigate to the directory containing the `Dockerfile` and run:

`docker build -t ws-heart-rate-to-osc .`

This will create an image named `ws-heart-rate-to-osc`.

### Running the Docker container 🏃

To run the Docker container, use the following command:


```bash
docker run -it --rm --name ws-heart-rate-to-osc -e VRCHAT_OSC_IP=<VRCHAT_OSC_IP> -e VRCHAT_OSC_PORT=<VRCHAT_OSC_PORT> -e WEBSOCKET_IP=<WEBSOCKET_IP> -e WEBSOCKET_PORT=<WEBSOCKET_PORT> -e DEVICE_ID=<DEVICE_ID> -e OSC_HEART_RATE_PARAMETER="<OSC_HEART_RATE_PARAMETER>" ws-heart-rate-to-osc
```

Replace `<VRCHAT_OSC_IP>`, `<VRCHAT_OSC_PORT>`, `<WEBSOCKET_IP>`, `<WEBSOCKET_PORT>`, `<DEVICE_ID>`, `<OSC_HEART_RATE_PARAMETER>` with the appropriate values for your setup.

### Official Docker image

An official Docker image is available at [unrea1/ws-heart-rate-to-osc](https://hub.docker.com/r/unrea1/ws-heart-rate-to-osc) 🚀. To use the official image, replace `ws-heart-rate-to-osc` with `unrea1/ws-heart-rate-to-osc:1` in the `docker run` command above.