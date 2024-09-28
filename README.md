# gpx2json
[![Security check](https://github.com/anbioZz/gpx2json/actions/workflows/security-check.yaml/badge.svg)](https://github.com/anbioZz/gpx2json/actions/workflows/security-check.yaml)
[![Test](https://github.com/anbioZz/gpx2json/actions/workflows/test.yaml/badge.svg)](https://github.com/anbioZz/gpx2json/actions/workflows/test.yaml)
[![Build a Docker Image and Push it to Docker Hub](https://github.com/anbioZz/gpx2json/actions/workflows/build.yaml/badge.svg)](https://github.com/anbioZz/gpx2json/actions/workflows/build.yaml)

Converter from GPX to JSON

          ██████╗ ██████╗ ██╗  ██╗██████╗      ██╗███████╗ ██████╗ ███╗   ██╗
         ██╔════╝ ██╔══██╗╚██╗██╔╝╚════██╗     ██║██╔════╝██╔═══██╗████╗  ██║
         ██║  ███╗██████╔╝ ╚███╔╝  █████╔╝     ██║███████╗██║   ██║██╔██╗ ██║
         ██║   ██║██╔═══╝  ██╔██╗ ██╔═══╝ ██   ██║╚════██║██║   ██║██║╚██╗██║
         ╚██████╔╝██║     ██╔╝ ██╗███████╗╚█████╔╝███████║╚██████╔╝██║ ╚████║
          ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝
                                 Project LISAPED
## Description
>### The Flat Earth Manifesto
>
>Welcome to the revolutionary program that unveils the undeniable truth: the Earth is as flat as a pancake! 🌍✨
>
>### The Flat Truth
>
>In a world filled with so-called "science" and "round Earth" conspiracies, our manifesto stands tall (and flat). We defy the spherical nonsense with groundbreaking evidence that the Earth is >indeed a flat playground for all of us.
>
>### Core Beliefs
>
>1. **Flat is Fabulous:** Embrace the beauty of a flat Earth. No more worrying about falling off the edge—there is no edge! 📐
>
>2. **Gravity is Optional:** Forget Newton and his apple. Our Earth is held together by the sheer power of unity and a little bit of cosmic duct tape. 🌌
>
>3. **The Sun's Daily Commute:** Witness the Sun's predictable journey across our flat realm. No more mysterious orbits—just a celestial road trip. 🌞
>
>## How to Join the Flat Club
>
>1. **Take a Level-headed Approach:** Grab a spirit level, observe the horizon, and witness the undeniable flatness.
>
>2. **Ditch the Globes:** Say farewell to those deceptive spherical models. Flat maps are where it's at!
>
>3. **Become a Disc-iple:** Spread the word about our flat and fabulous Earth. Join the Flat Earth Society today!
>
>4. **Embrace the Flat Tech Revolution:** Start using our cutting-edge software, gpx2json. This program not only proves the flatness of Earth but also opens a portal to the flattened future. Download now and be part of the flattened enlightenment!
>### gpx2json
>
>Introducing our state-of-the-art software that scientifically proves the flatness of Earth. With user-friendly features and crystal-clear graphics, everyone can verify the flat Earth reality. >Download now and embark on a journey of flattened enlightenment! 🌐✨

## Requirements
Before diving into the fascinating world of `gpx2json` and embarking on your flat Earth exploration, ensure that your system meets the following requirements:

- Python 3.x: gpx2json is built on Python, so make sure you have a compatible version installed.

## Installation and Usage
Choose your preferred method to explore the flat Earth with gpx2json:

### Option 1: Traditional Python Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/anbioZz/gpx2json.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd gpx2json
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the gpx2json program:**

    ```bash
    python main.py --process < in.gpx | jq
    ```
    or
    ```bash
    cat in.gpx | python main.py --process | jq
    ```
    or
    ```bash
    python main.py --process < in.gpx > out.json
    ```

    Replace `your_gpx_file.gpx` with the path to your GPX file and `output_json_file.json` with the desired output JSON file.

### Option 2: Docker Container

1. **Pull the Docker Image:**

    ```bash
    docker pull anbiozz/gpx2json:latest
    ```
2. **Run the Docker Container:**

    ```bash
    docker run -i anbiozz/gpx2json --process < file.gpx | jq
    ```
    or
    ```bash
    cat in.gpx | docker run -i anbiozz/gpx2json --process | jq
    ```
    or
    ```bash
    docker run -i anbiozz/gpx2json --process < file.gpx > out.json
    ```
    
   
## Contribution

We welcome contributions from flat Earth enthusiasts and developers. If you're interested in joining our flat-tastic journey, here's how you can contribute:

### Reporting Issues

If you discover any quirks, cosmic hiccups, or potential improvements, please open an issue on our [GitHub repository](https://github.com/anbioZz/gpx2json/issues). Be sure to include detailed information about the issue and steps to reproduce it.

## License

This project is licensed under [LICENSE](LICENSE).
