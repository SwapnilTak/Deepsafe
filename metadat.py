import os
import moviepy.editor as mpe

def get_video_metadata(video_path):
  """
  Extracts basic metadata from a video file.

  Args:
    video_path: Path to the video file.

  Returns:
    A dictionary containing the extracted metadata.
  """

  if not os.path.isfile(video_path):
    raise FileNotFoundError(f"File not found: {video_path}")

  video = mpe.VideoFileClip(video_path)
  metadata = {
    "filename": video.filename,
    "duration": video.duration,
    "fps": video.fps,
    "resolution": video.size,
    "creation_date": video.metadata.get("creation_date"),
    "codec": video.video_codec_info.title(),
  }

  return metadata

# Example usage
video_path = "path/to/your/video.mp4"
metadata = get_video_metadata(video_path)

print(f"Filename: {metadata['filename']}")
print(f"Duration: {metadata['duration']} seconds")
print(f"FPS: {metadata['fps']}")
print(f"Resolution: {metadata['resolution']}")
print(f"Creation Date: {metadata['creation_date']}")
print(f"Codec: {metadata['codec']}")