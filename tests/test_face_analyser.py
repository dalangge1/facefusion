import subprocess

import pytest

from facefusion import face_attributor, face_detector, face_landmarker, face_recognizer, state_manager
from facefusion.download import conditional_download
from facefusion.face_analyser import get_many_faces, get_one_face
from facefusion.typing import Face
from facefusion.vision import read_static_image
from .helper import get_test_example_file, get_test_examples_directory


@pytest.fixture(scope = 'module', autouse = True)
def before_all() -> None:
	conditional_download(get_test_examples_directory(),
	[
		'https://github.com/facefusion/facefusion-assets/releases/download/examples-3.0.0/source.jpg'
	])
	subprocess.run([ 'ffmpeg', '-i', get_test_example_file('source.jpg'), '-vf', 'crop=iw*0.8:ih*0.8', get_test_example_file('source-80crop.jpg') ])
	subprocess.run([ 'ffmpeg', '-i', get_test_example_file('source.jpg'), '-vf', 'crop=iw*0.7:ih*0.7', get_test_example_file('source-70crop.jpg') ])
	subprocess.run([ 'ffmpeg', '-i', get_test_example_file('source.jpg'), '-vf', 'crop=iw*0.6:ih*0.6', get_test_example_file('source-60crop.jpg') ])
	face_attributor.pre_check()
	face_detector.pre_check()
	face_landmarker.pre_check()
	face_recognizer.pre_check()
	state_manager.init_item('execution_providers', [ 'cpu' ])
	state_manager.init_item('face_detector_angles', [ 0 ])
	state_manager.init_item('face_detector_score', 0.5)
	state_manager.init_item('face_landmarker_score', 0.5)


@pytest.fixture(autouse = True)
def before_each() -> None:
	face_attributor.clear_inference_pool()
	face_detector.clear_inference_pool()
	face_landmarker.clear_inference_pool()
	face_recognizer.clear_inference_pool()


def test_get_one_face_with_retinaface() -> None:
	state_manager.init_item('face_detector_model', 'retinaface')
	state_manager.init_item('face_detector_size', '320x320')

	source_paths =\
	[
		get_test_example_file('source.jpg'),
		get_test_example_file('source-80crop.jpg'),
		get_test_example_file('source-70crop.jpg'),
		get_test_example_file('source-60crop.jpg')
	]
	for source_path in source_paths:
		source_frame = read_static_image(source_path)
		many_faces = get_many_faces([ source_frame ])
		face = get_one_face(many_faces)

		assert isinstance(face, Face)


def test_get_one_face_with_scrfd() -> None:
	state_manager.init_item('face_detector_model', 'scrfd')
	state_manager.init_item('face_detector_size', '640x640')

	source_paths =\
	[
		get_test_example_file('source.jpg'),
		get_test_example_file('source-80crop.jpg'),
		get_test_example_file('source-70crop.jpg'),
		get_test_example_file('source-60crop.jpg')
	]
	for source_path in source_paths:
		source_frame = read_static_image(source_path)
		many_faces = get_many_faces([ source_frame ])
		face = get_one_face(many_faces)

		assert isinstance(face, Face)


def test_get_one_face_with_yoloface() -> None:
	state_manager.init_item('face_detector_model', 'yoloface')
	state_manager.init_item('face_detector_size', '640x640')

	source_paths =\
	[
		get_test_example_file('source.jpg'),
		get_test_example_file('source-80crop.jpg'),
		get_test_example_file('source-70crop.jpg'),
		get_test_example_file('source-60crop.jpg')
	]
	for source_path in source_paths:
		source_frame = read_static_image(source_path)
		many_faces = get_many_faces([ source_frame ])
		face = get_one_face(many_faces)

		assert isinstance(face, Face)


def test_get_many_faces() -> None:
	source_path = get_test_example_file('source.jpg')
	source_frame = read_static_image(source_path)
	many_faces = get_many_faces([ source_frame, source_frame, source_frame ])

	assert isinstance(many_faces[0], Face)
	assert isinstance(many_faces[1], Face)
	assert isinstance(many_faces[2], Face)
