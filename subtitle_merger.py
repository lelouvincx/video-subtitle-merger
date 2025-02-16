import webvtt
from moviepy import VideoFileClip, TextClip, CompositeVideoClip


def time_to_seconds(time_str):
    """Convert WebVTT timestamp to seconds"""
    h, m, s = time_str.split(":")
    seconds = float(s) + int(m) * 60 + int(h) * 3600
    return seconds


def merge_subtitles(video_path, subtitle_path, output_path):
    print(f"Loading video: {video_path}")
    video = VideoFileClip(video_path)

    print(f"Reading subtitles: {subtitle_path}")
    captions = webvtt.read(subtitle_path)

    print("Creating subtitle clips...")
    subtitle_clips = []

    for caption in captions:
        start_time = time_to_seconds(caption.start)
        end_time = time_to_seconds(caption.end)

        print(f"Processing subtitle: {caption.text[:30]}...")
        text_clip = (
            TextClip(
                font="Arial",
                text=caption.text,
                font_size=32,
                color="white",
                stroke_color="black",
                stroke_width=1,
                bg_color="black",
            )
            .with_position(("center", "bottom"))
            .with_duration(end_time - start_time)
            .with_start(start_time)
        )

        subtitle_clips.append(text_clip)

    print("Combining video with subtitles...")
    final_video = CompositeVideoClip([video] + subtitle_clips)

    print(f"Writing output video to: {output_path}")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print("Cleaning up resources...")
    video.close()
    final_video.close()
    print("Process completed successfully!")


if __name__ == "__main__":
    # Example usage
    video_file = "examples/video.mp4"
    subtitle_file = "examples/subtitle.vtt"
    output_file = "examples/output.mp4"

    merge_subtitles(video_file, subtitle_file, output_file)
