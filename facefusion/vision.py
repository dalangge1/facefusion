from typing import Optional, List
from functools import lru_cache
import cv2

from facefusion.filesystem import is_image, is_video
from facefusion.typing import Frame, Resolution


def get_video_frame(video_path : str, frame_number : int = 0) -> Optional[Frame]:
	if is_video(video_path):
		video_capture = cv2.VideoCapture(video_path)
		if video_capture.isOpened():
			frame_total = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
			video_capture.set(cv2.CAP_PROP_POS_FRAMES, min(frame_total, frame_number - 1))
			has_frame, frame = video_capture.read()
			video_capture.release()
			if has_frame:
				return frame
	return None


def count_video_frame_total(video_path : str) -> int:
	if is_video(video_path):
		video_capture = cv2.VideoCapture(video_path)
		if video_capture.isOpened():
			video_frame_total = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
			video_capture.release()
			return video_frame_total
	return 0


def detect_video_fps(video_path : str) -> Optional[float]:
	if is_video(video_path):
		video_capture = cv2.VideoCapture(video_path)
		if video_capture.isOpened():
			video_fps = video_capture.get(cv2.CAP_PROP_FPS)
			video_capture.release()
			return video_fps
	return None


def detect_video_resolution(video_path : str) -> Optional[Resolution]:
	if is_video(video_path):
		video_capture = cv2.VideoCapture(video_path)
		if video_capture.isOpened():
			width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
			height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
			video_capture.release()
			return width, height
	return None


def create_video_resolutions(video_path : str) -> Optional[List[str]]:
	temp_range = []
	video_resolution_range = []
	template_range = [ 240, 360, 480, 540, 720, 1080, 1440, 2160 ]
	video_resolution = detect_video_resolution(video_path)

	if video_resolution:
		width, height = video_resolution
		temp_range.append(normalize_resolution(video_resolution))
		if width > height:
			for template_height in template_range:
				template_width = width / height * template_height
				temp_range.append(normalize_resolution((template_width, template_height)))
		else:
			for template_width in template_range:
				template_height = height / width * template_width # type: ignore[assignment]
				temp_range.append(normalize_resolution((template_width, template_height)))
		temp_range = sorted(set(temp_range))
		for temp in temp_range:
			video_resolution_range.append(stringify_resolution(temp))
		return video_resolution_range
	return None


def normalize_resolution(resolution : Resolution) -> Resolution:
	width, height = resolution

	if width and height:
		normalize_width = round(width / 2) * 2
		normalize_height = round(height / 2) * 2

		return normalize_width, normalize_height
	return 0, 0


def stringify_resolution(resolution : Resolution) -> str:
	width, height = normalize_resolution(resolution)
	return str(width) + 'x' + str(height)


def resize_frame_resolution(frame : Frame, max_width : int, max_height : int) -> Frame:
	height, width = frame.shape[:2]

	if height > max_height or width > max_width:
		scale = min(max_height / height, max_width / width)
		new_width = int(width * scale)
		new_height = int(height * scale)
		return cv2.resize(frame, (new_width, new_height))
	return frame


def normalize_frame_color(frame : Frame) -> Frame:
	return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


@lru_cache(maxsize = 128)
def read_static_image(image_path : str) -> Optional[Frame]:
	return read_image(image_path)


def read_static_images(image_paths : List[str]) -> Optional[List[Frame]]:
	frames = []
	if image_paths:
		for image_path in image_paths:
			frames.append(read_static_image(image_path))
	return frames


def read_image(image_path : str) -> Optional[Frame]:
	if is_image(image_path):
		return cv2.imread(image_path)
	return None


def write_image(image_path : str, frame : Frame) -> bool:
	if image_path:
		return cv2.imwrite(image_path, frame)
	return False
