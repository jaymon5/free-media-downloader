import streamlit as st
import yt_dlp
import os
import tempfile

st.set_page_config(page_title="Pro Media Downloader", page_icon="🚀")
st.title("🚀 Pro Media Downloader")
st.markdown("High-quality MP4 and MP3 downloads powered by FFmpeg.")

url = st.text_input("Enter Link:", placeholder="https://www.youtube.com/watch?v=...")

if url:
    try:
        # Create a temporary directory for the conversion
        with tempfile.TemporaryDirectory() as tmpdirname:
            ydl_opts_info = {'quiet': True, 'no_warnings': True}
            
            with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'video')
                st.image(info.get('thumbnail'), width=300)
                st.write(f"### {title}")

            choice = st.radio("Select Format:", ["Video (Best Quality MP4)", "Audio (High Quality MP3)"], horizontal=True)

            if st.button(f"Prepare {choice}"):
                with st.spinner("Merging streams with FFmpeg... this takes a few seconds."):
                    # Output path in the temp folder
                    output_path = os.path.join(tmpdirname, '%(title)s.%(ext)s')
                    
                    if "Video" in choice:
                        # Merges best video and best audio into one MP4
                        ydl_opts = {
                            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                            'outtmpl': output_path,
                            'merge_output_format': 'mp4',
                        }
                        ext = "mp4"
                        mime = "video/mp4"
                    else:
                        # Converts audio to high-quality MP3
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': output_path,
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                        }
                        ext = "mp3"
                        mime = "audio/mpeg"

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    # Find the newly created file in temp dir
                    downloaded_file = [f for f in os.listdir(tmpdirname)][0]
                    final_file_path = os.path.join(tmpdirname, downloaded_file)

                    with open(final_file_path, "rb") as f:
                        st.download_button(
                            label=f"💾 Download {ext.upper()}",
                            data=f,
                            file_name=f"{title}.{ext}",
                            mime=mime
                        )
                    st.success("Ready! Your file is processed.")

    except Exception as e:
        st.error(f"YouTube blocked the request or the link is invalid. Error: {e}")
