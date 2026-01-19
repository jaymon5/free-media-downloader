import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Ultimate Media Downloader", page_icon="🎬")
st.title("🎬 Ultimate Media Downloader")
st.markdown("Download videos or audio in the best quality for free.")

url = st.text_input("Paste your link here:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        with st.spinner("Fetching available qualities..."):
            # Setup yt-dlp to just get info, not download yet
            ydl_opts = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                title = info.get('title', 'video')
                thumbnail = info.get('thumbnail')

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(thumbnail)
        with col2:
            st.write(f"### {title}")
            
            # Filter for specific formats
            media_type = st.radio("Select Type:", ["Video (MP4)", "Audio (MP3)"])
            
            if media_type == "Video (MP4)":
                # Get unique resolutions
                res_options = sorted(list(set([f.get('height') for f in formats if f.get('height')])))
                choice = st.selectbox("Select Resolution:", [f"{r}p" for r in res_options[::-1]])
                selected_res = choice.replace("p", "")
                format_str = f"bestvideo[height<={selected_res}]+bestaudio/best"
                ext = "mp4"
            else:
                format_str = "bestaudio/best"
                ext = "mp3"

            if st.button(f"Convert to {media_type}"):
                with st.spinner("Processing... this will take just a moment."):
                    # Final download options
                    final_opts = {
                        'format': format_str,
                        'outtmpl': 'download.%(ext)s',
                        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}] if media_type == "Audio (MP3)" else [],
                        'merge_output_format': 'mp4' if media_type == "Video (MP4)" else None,
                    }
                    
                    with yt_dlp.YoutubeDL(final_opts) as ydl:
                        ydl.download([url])
                    
                    # Determine the actual filename created
                    actual_file = f"download.{ext}"
                    
                    with open(actual_file, "rb") as f:
                        st.download_button(
                            label="💾 Save to Device",
                            data=f,
                            file_name=f"{title}.{ext}",
                            mime="audio/mpeg" if ext == "mp3" else "video/mp4"
                        )
                    os.remove(actual_file) # Clean up the server space

    except Exception as e:
        st.error(f"Something went wrong: {e}")
