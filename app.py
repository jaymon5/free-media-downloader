import streamlit as st
import yt_dlp

st.set_page_config(page_title="Fast Downloader", page_icon="⚡")
st.title("⚡ Instant Media Downloader")

url = st.text_input("Paste Link:", placeholder="https://...")

if url:
    try:
        # We use 'noplaylist' and 'quiet' to speed up the metadata fetch
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We ONLY extract info (fast), we DON'T download (slow)
            info = ydl.extract_info(url, download=False)
            
            # Filter for the actual direct download URL
            formats = info.get('formats', [])
            
            st.image(info.get('thumbnail'), width=250)
            st.subheader(info.get('title'))

            # Create columns for the options
            col1, col2 = st.columns(2)
            
            with col1:
                # Get the best MP4 video link
                video_url = info.get('url')
                st.link_button("📺 Download MP4", video_url)
                st.caption("Best Available Resolution")

            with col2:
                # Find an audio-only format
                audio_formats = [f for f in formats if f.get('vcodec') == 'none']
                if audio_formats:
                    audio_url = audio_formats[0].get('url')
                    st.link_button("🎵 Download MP3", audio_url)
                    st.caption("High Quality Audio")

            st.info("Right-click the buttons and 'Save Link As' for the fastest experience.")

    except Exception as e:
        st.error(f"YouTube is throttling this server. Try again in a minute.")
