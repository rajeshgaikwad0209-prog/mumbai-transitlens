# Mumbai TransitLens

A beginner learning prototype: a Streamlit dashboard about public transport delays and passenger demand.

**All data is fictional sample data.** The app does not show live Mumbai bus information. The Hadoop/MapReduce section is an illustration that runs in plain Python, with no Hadoop installed.

## Files

- `app.py` - the whole Streamlit app
- `sample_bus_data.csv` - 120 simulated records (8 fictional routes x 15 hours)
- `requirements.txt` - libraries Streamlit Cloud installs
- `README.md` - this file

## Run on a computer (optional)

```
pip install -r requirements.txt
streamlit run app.py
```

## 1. Create a GitHub repository

1. Open github.com in your phone browser and sign in (or create a free account).
2. Tap your profile picture or the **+** icon, then **New repository**.
3. Name it `mumbai-transitlens`, choose **Public**, and tap **Create repository**.

## 2. Upload the files from a mobile browser

Streamlit needs `app.py`, `requirements.txt` and `sample_bus_data.csv` in the main folder of the repo. Pick whichever method works on your phone.

**Method A - paste each file (works well on phones):**
1. In your repo, tap **Add file**, then **Create new file**.
2. Type the exact file name (for example `app.py`) and paste the code.
3. Tap **Commit changes**, then **Commit changes** again.
4. Repeat for `requirements.txt`, `sample_bus_data.csv` and `README.md`.

**Method B - upload files:**
1. Save the four files to your phone first.
2. In your repo, tap **Add file**, then **Upload files**, and choose the files.
3. Tap **Commit changes**.

If you do not see these options, switch your browser to **Desktop site** mode.

## 3. Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io and sign in with GitHub. Allow access when asked.
2. Tap **Create app**, then choose the option for an app you already have on GitHub.
3. Select your repository, branch `main`, and main file path `app.py`.
4. Optional: type a custom subdomain, such as `mumbai-transitlens`.
5. Tap **Deploy** and wait a few minutes while libraries install.

Screen names can change over time. If a button looks different, follow the on-screen prompts or check Streamlit's deployment docs.

## 4. Get and share the live link

- When the app opens, copy the address from your browser. It ends in `.streamlit.app`.
- That address is your live link. Anyone can open it if the app is public.
- Free apps may go to sleep after a period of inactivity. Visitors can tap a button to wake them.

## Notes

- This is a learning prototype, not a production transport system.
- It has not been deployed or tested by the author of this file until you do so yourself.
