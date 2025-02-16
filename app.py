import streamlit as st
import tempfile
import os
from subtitle_merger import merge_subtitles

st.title("Video Subtitle Merger")
st.write("Upload your video and subtitle files to merge them together.")

# File uploaders
video_file = st.file_uploader("Choose a video file", type=["mp4"])
subtitle_file = st.file_uploader("Choose a subtitle file", type=["vtt"])

if video_file and subtitle_file:
    # Create a button to process the files
    if st.button("Merge Subtitles"):
        with st.spinner("Processing..."):
            try:
                # Create temporary files
                temp_dir = tempfile.mkdtemp()
                temp_video = os.path.join(temp_dir, "input_video.mp4")
                temp_subtitle = os.path.join(temp_dir, "subtitle.vtt")
                temp_output = os.path.join(temp_dir, "output.mp4")

                # Save uploaded files to temporary location
                with open(temp_video, "wb") as f:
                    f.write(video_file.getbuffer())
                with open(temp_subtitle, "wb") as f:
                    f.write(subtitle_file.getbuffer())

                # Process the merge
                merge_subtitles(temp_video, temp_subtitle, temp_output)

                # Offer the processed file for download
                with open(temp_output, "rb") as f:
                    st.download_button(
                        label="Download Processed Video",
                        data=f,
                        file_name="video_with_subtitles.mp4",
                        mime="video/mp4",
                    )

                # Clean up
                os.remove(temp_video)
                os.remove(temp_subtitle)
                os.remove(temp_output)
                os.rmdir(temp_dir)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
else:
    st.info("Please upload both video and subtitle files to proceed.")

# Add some usage instructions
st.markdown(
    """
### Instructions:
1. Upload your MP4 video file
2. Upload your VTT subtitle file
3. Click 'Merge Subtitles' to process
4. Download the resulting video with embedded subtitles
"""
)
