# Get & Clean YouTube Comments from Multiple Videos and Detect English Content for Corpus Analysis

By Ting Xu, 31 March 2026

This is to extend the functionality of a wonderful, powerful, and free researcher-oriented [YouTube Data Tool](https://ytdt.digitalmethods.net/index.php) (Rieder 2015 @[bernorieder](https://github.com/bernorieder)) by allowing the retrieval of multiple videos' comments at once in Python. It also facilitates data cleaning (remove duplicates, remove empty values, remove HTML entities, remove usernames) and language detection for corpus linguistics studies through software like [AntConc](https://www.laurenceanthony.net/software/antconc/) (Anthony 2024) and [Sketch Engine](https://www.sketchengine.eu/) (Kilgarriff et al., 2014).


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

Step 2: Download Anaconda, create a virtual environment, choose Python and Jupyter Notebook, and install different packages. See [this tutorial video](https://www.youtube.com/watch?v=SwSbnmqk3zY&t=10s) by a YouTuber (techTFQ 2021). 

Step 3: Attain videos' IDs

Supposing you like to explore comments from multiple videos without repeated single clicks to download them, you choose the Video List module in the YouTube Data Tool to attain many video IDs.

Clean and keep English comments: each comment is saved into an independent txt file to allow a full view of the content without mixing up with other comments. Sketch Engine allows 100 files and 1 million tokens. AntConc has no such limits, so the comments are saved into various txt files in a folder. Auto-language detection is applied with manual detection because extremely short comments may be easily mistaken for non-English. Check the identified files in the non-English CSV and manually decide which ones you like to keep and delete. So the corpus would be mainly in English. 

This process improves transparency and accuracy. It advances this [corpus-assisted critical discourse analysis of YouTube comments](https://methods.sagepub.com/hnbk/edvol/the-sage-handbook-of-social-media-research-methods-2e-srm/chpt/17-corpusassisted-critical) (Hodson and Lefevre 2022). 

# In addition, to read the comment network file from the YouTube Data Tool in Gephi...

Gephi can open GDF, but the GDF file (graph format) from the module "Video Comments" on the YouTube Data Tool page cannot be directly parsed when I used it in winter and spring 2026. To properly open it, the script from the "read_commentnetwork" file will help prepare the graph in NetworkX and then export it to the right format GraphML for Gephi.
