import streamlit as st
from pytube import YouTube
from io import BytesIO

st.title("Free Media Downloader")

url = st.text_input("Paste YouTube Link Here:")

if url:
    try:
        yt = YouTube(url)
        st.image(yt.thumbnail_url, width=300)
        st.write(f"**Title:** {yt.title}")

        # Choose format
        option = st.selectbox("Select Format:", ["MP4 (Video)", "MP3 (Audio)"])

        if st.button("Prepare Download"):
            with st.spinner("Processing..."):
                buffer = BytesIO()
                if option == "MP4 (Video)":
                    # Get the highest resolution progressive mp4
                    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                    stream.stream_to_buffer(buffer)
                    file_name = f"{yt.title}.mp4"
                    mime = "video/mp4"
                else:
                    # Get audio only
                    stream = yt.streams.filter(only_audio=True).first()
                    stream.stream_to_buffer(buffer)
                    file_name = f"{yt.title}.mp3"
                    mime = "audio/mpeg"
                
                buffer.seek(0)
                st.download_button(
                    label=f"Download {option}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime
                )
                st.success("Ready! Click the button above to save.")

    except Exception as e:
        st.error(f"YouTube is blocking this request. Error: {e}")
