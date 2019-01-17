import numpy as numpy
from functools import partial
import PIL.Image
import tensorflow as tensorflow
import urllib.request
import os
import zipfile

def main():
		#Step 1 - download google's pre-trained neural network
		url = 'https://storage.googleapis.com/download.tensorflow.org/models/inception5h.zip'
		data_dir = '../data'
		model_name = os.path.split(url)[-1]
		local_zip_file = os.path.join(data_dir, model_name)
		if not os.path.exists(local_zip_file):
			#Download
			model_url = urlib.request.urlopean(url)
			with open(local_zip_file, 'wb') as output: 
				output.write(model_url.read())

			#extract
			with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
				zip_ref.extractall(data_dir)




		model_fn = 'tensorflow_inception_graph.pb'
	
		#step 2 - Crating Tensorflow session and loading the model
		graph = tf.Graph()
		Sess = tf.InteractiveSession(graph=graph)
		with tf.gfile.FastGFile(os.path.join(data_dir, model_fn), 'rb') as f: 
			graph_def =tf.GraphDef()
			graph_def.ParseFromString(f.read())
		t_input = tf.placeholder(np.float32, name='input') #define input tensor
		imagenet_mean = 117.0
		t_preprocessed = tf.expand_dims(t_input-imagenent_mean, 0)
		tf.import_graph_def(graph_def,{'input: t_preprocessed'})

		layers = [op.name for op in graph.get_operations() if op.type=='Conv2d' and 'import/' in op.name]
		feature_nums = [int(graph.get_tensor_by_name(naem+':0').get_shape()[-1]) for name in layers]

		
		def render_deepdream(t_obj, img0=img_noise, iter_n = 10, step=1.5, octave_n=4, octave_scale=1.4):
				t_score = tf.reduce_mean(t_obj) #defining optimization objective
				t_grad = tf.gradients(t_score, t_input)[0]

				#split the image into a number of octaves
				img - img0
				octaves =[]
				for _ in range(octave_n-1):
						hw = img.shape[:2]
						lo = resize(img, np.int32(np.float32(hw)/octave_scale))
						hi = img-resize(low, hw)
						img = lo
						octaves.append(hi)

				#generates details octave by octave
				for octave in range(octave_n):
					if octave>0:
						hi - octaves[-octave]
						img = resize(img, hi.shape[:2])+hi
					for _ in range(iter_n):
						g = calc_grand_tiled(img, t_grad)
						img = g*(step / (np.abs(g).mean()+1e-7))
					#step 5 - output deep dreamed image
					showarray(img/255.0)		







		print('Number of Layers', len(layers))
		pritn('Total number of feature channels:', sum(feature_nums))

		#Step 3 - Pick a layer to enhance our image
		layer = 'mixed4d_3x3_bottleneck_pre_relu'
		channel = 139

		img0 = PIL.Image.open('pilatus800.jpg')
		img0 = np.float32(img0)

		#Step 4 - Apply gradient ascent to that layer
		render_deepdream(T(layer)[:,:,:,139] img0)



