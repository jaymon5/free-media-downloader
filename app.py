import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Ultimate Free Downloader", page_icon="🚀")
st.title("🚀 Ultimate Free Downloader")

url = st.text_input("Enter Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Setting common paths for free Linux servers
            FFMPEG_PATH = '/usr/bin/ffmpeg' 
            
            # Step 1: Get Video Info (Preview)
            ydl_opts_info = {'quiet': True, 'no_warnings': True}
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                st.image(info.get('thumbnail'), width=300)
                st.write(f"### {info.get('title')}")

            choice = st.radio("Format:", ["Video (MP4)", "Audio (MP3)"], horizontal=True)

            if st.button(f"Prepare {choice}"):
                with st.spinner("Processing with FFmpeg..."):
                    output_template = os.path.join(tmpdirname, '%(title)s.%(ext)s')
                    
                    # Common settings for both formats
                    ydl_opts = {
                        'outtmpl': output_template,
                        'ffmpeg_location': FFMPEG_PATH, # <--- THE CRITICAL FIX
                        'quiet': True,
                    }

                    if "Video" in choice:
                        ydl_opts.update({
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'merge_output_format': 'mp4',
                        })
                        ext = "mp4"
                        mime = "video/mp4"
                    else:
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        })
                        ext = "mp3"
                        mime = "audio/mpeg"

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    # Get the file from temp directory
                    files = os.listdir(tmpdirname)
                    if files:
                        final_file = os.path.join(tmpdirname, files[0])
                        with open(final_file, "rb") as f:
                            st.download_button(
                                label=f"💾 Click to Save {ext.upper()}",
                                data=f,
                                file_name=f"{info.get('title')}.{ext}",
                                mime=mime
                            )
                        st.success("Download ready!")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check if you have 'ffmpeg' in your packages.txt file!")
