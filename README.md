# YouTube-Comments-via-Data-API-User-Key

By Ting Xu, 31 March 2026

This is to extend the functionality of the YouTube Data Tool (Rieder 2015) by allowing the retrieval of multiple videos' comments at once. It also facilitates data cleaning (remove duplicates, remove empty values, remove HTML entities) and language detection for corpus linguistics studies through software like AntConc (Anthony 2024) and Sketch Engine (Kilgarriff et al., 2014).


Step 1: Set Up Google Cloud Project.
  Go to the [Google Cloud Console](https://console.cloud.google.com/).
  Create a new project or use an existing one.
  Enable the YouTube Data API v3 for your project.
  Navigate to API & Services > Library.
  Search for "YouTube Data API v3" and click Enable.
  Create credentials to access the API:
  Go to API & Services > Credentials.
  Click on Create Credentials and select API key.
  Copy the API key for use in the scripts.

Understanding [the default quota](https://developers.google.com/youtube/v3/determine_quota_cost) and how many comments you may get with it is a plus. 

Step 2: Download Anaconda, create a virtual environment, and install different packages. See [this tutorial video](https://www.youtube.com/watch?v=SwSbnmqk3zY&t=10s) by a YouTuber (techTFQ 2021). 
