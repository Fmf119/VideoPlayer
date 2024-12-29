import streamlit as st
import re
import os
from urllib.parse import urlparse
from moviepy.editor import VideoFileClip

def is_youtube_url(url):
    """Check if the URL is a YouTube link"""
    return 'youtube.com' in urlparse(url).hostname or 'youtu.be' in urlparse(url).hostname

def is_vimeo_url(url):
    """Check if the URL is a Vimeo link"""
    return 'vimeo.com' in urlparse(url).hostname

def get_video_id_from_youtube(url):
    """Extract the YouTube video ID from the URL"""
    if 'youtube.com' in url:
        match = re.search(r'(?<=v=)[\w-]+', url)
        return match.group(0) if match else None
    elif 'youtu.be' in url:
        match = re.search(r'youtu.be/([\w-]+)', url)
        return match.group(1) if match else None
    return None

def get_video_id_from_vimeo(url):
    """Extract the Vimeo video ID from the URL"""
    match = re.search(r'vimeo.com/(\d+)', url)
    return match.group(1) if match else None

def convert_to_mp4(input_video_path, output_video_path="converted_video.mp4"):
    """Convert unsupported video formats to MP4 using moviepy"""
    try:
        # Load the video file with moviepy
        video = VideoFileClip(input_video_path)
        
        # Write it to an mp4 file
        video.write_videofile(output_video_path, codec='libx264')
        return output_video_path
    except Exception as e:
        st.error(f"Error converting video: {e}")
        return None

def main():
    st.title("Universal Video Player")

    st.write("Enter the URL of a video below:")

    # Take URL input from the user
    video_url = st.text_input("Video URL")

    if video_url:
        # Check if it's a YouTube URL
        if is_youtube_url(video_url):
            video_id = get_video_id_from_youtube(video_url)
            if video_id:
                st.write(f"Displaying YouTube video: https://www.youtube.com/watch?v={video_id}")
                # Embed YouTube video using iframe
                st.markdown(f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
            else:
                st.error("Could not extract YouTube video ID from the URL.")
        
        # Check if it's a Vimeo URL
        elif is_vimeo_url(video_url):
            video_id = get_video_id_from_vimeo(video_url)
            if video_id:
                st.write(f"Displaying Vimeo video: https://vimeo.com/{video_id}")
                # Embed Vimeo video using iframe
                st.markdown(f'<iframe src="https://player.vimeo.com/video/{video_id}" width="640" height="360" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>', unsafe_allow_html=True)
            else:
                st.error("Could not extract Vimeo video ID from the URL.")
        
        # Check if it's a direct video URL (mp4, webm, etc.)
        elif video_url.endswith(('.mp4', '.webm', '.ogg')):
            try:
                # Try to load and play the direct video file
                st.video(video_url)
            except Exception as e:
                st.error(f"Error loading the video: {e}")
        
        # If the video is MOV, AVI, or WMV, attempt conversion to MP4
        elif video_url.endswith(('.mov', '.avi', '.wmv')):
            try:
                # Here we assume a local video file path for this demo, you can modify it for remote downloads
                local_video_path = "path_to_video_file.mov"  # Replace with the actual path to the file

                # Convert the video to MP4
                converted_video = convert_to_mp4(local_video_path)
                
                if converted_video:
                    st.video(converted_video)
                else:
                    st.error("Failed to convert video.")
            except Exception as e:
                st.error(f"Error processing video: {e}")
        
        else:
            st.error("The video URL is not from a supported platform or is not a direct video file.")

    else:
        st.info("Please enter a valid video URL to play.")

if __name__ == "__main__":
    main()
