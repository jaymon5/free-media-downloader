import streamlit as st
import yt_dlp

st.set_page_config(page_title="Free Media Downloader", page_icon="📥")
st.title("📥 Free Media Downloader")

url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Configuration for yt-dlp
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video')
            video_url = info.get('url') # This is the direct link to the file
            thumbnail = info.get('thumbnail')

            st.image(thumbnail, width=300)
            st.write(f"**Found:** {video_title}")

            # Direct link button
            st.link_button("🚀 Download Video Now", video_url)
            st.info("Right-click the button and 'Save Link As' if it just opens in a new tab.")

    except Exception as e:
        st.error(f"YouTube is being difficult! Error: {e}")
        st.warning("Tip: Make sure the URL is a standard video link, not a Short or a Playlist.")
