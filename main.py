from moviepy.editor import VideoFileClip, concatenate_videoclips
import math

video_path = '03.mp4'

threshold = 0.2
window_size = 0.5

video = VideoFileClip(video_path)

n_windows = math.floor(video.audio.end / window_size)

keep_clips = []

is_prev_silence = True
start_time = 0
end_time = 0

for i in range(n_windows):
    s = video.audio.subclip(i * window_size, (i + 1) * window_size)
    if s.max_volume() >= threshold:
        if is_prev_silence: # start speaking
            start_time = i * window_size

        is_prev_silence = False
    else:
        if not is_prev_silence: # end speaking
            end_time = i * window_size
            keep_clips.append(video.subclip(start_time, end_time))
            print(f'{start_time} - {end_time}')

        is_prev_silence = True

edited_video = concatenate_videoclips(keep_clips)

edited_video.write_videofile(
    'out.mp4',
    audio_codec='aac',
    threads=16
)

video.close()
edited_video.close()
