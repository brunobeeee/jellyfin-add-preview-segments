# add-preview-segment

A Python script to add *Preview* segments into your Jellyfin database for every episode in a specified library that already has an *Intro* segment.

## Usecase
- You're watching a show that starts every episode with a preview with massive spoilers.
- You don't want to skip this part manually everytime.
- You have the Intro Skipper pluin installed so Jellyfin already knows where the intro is.

## How it works
The script fetches all episode IDs of your specified via the Jellyfin API (This is necessary bc there is no information in the db about wich episode belongs to wich libary). It looks up those `ItemId`s in the `MediaSegments` table of `jellyfin.db`. If an entry exists with `Type = 5` (Intro) and no entry with `Type = 2` (Preview) it adds one using `0` seconds as start time an the beginning of the intro as end time.

## Getting started

1. Clone this repo

2. Obtain the library_id for later use.
    Hint: Open this link in your Webbrowser by using a Jellyfin API key to see all libraries and their IDs.
    https://jellyfin.example.com/Items?API_Key=<api-key>

2. Copy `.env.example` to `.env` and configure the script.

3. Create a venv and install all required packages.
    ```bash
    python3 -m venv venv
    source venv/bin/acivate
    python3 -m pip install -r requirements.txt
    ```

4. Run `main.py`.
    ```bash
    python3 main.py
    ```