import random
import sys
import requests
import matplotlib.pyplot as plt
import numpy as np

# If USE_RANDOM_DOT_ORG is false, we will simply generate random numbers with numpy.
USE_RANDOM_DOT_ORG = True

# Max number of pixels in either dimension.
MAX_SIZE = 128

# Checks the remaining quota from random.org, i.e the number of bits still available.
def get_quota():
	return int(requests.get("https://www.random.org/quota/?format=plain").text)

def generate_random_integers(num, min_val, max_val):
	# If we've exceeded the quota at the moment, tell the user to try again later.
	quota = get_quota()
	print("Current quota: " + str(quota))
	if quota <= 0:
		raise Exception("Sorry, your random.org API limit is exceeded at the moment. Please try again later.")

	ret = []

	# Because random.org can only serve at most 10e4 numbers at a time, we might need to 
	# batch the query into multiple requests.
	batch_size = 10000
	size = 0

	# A function to read the string output and parse it into an array of ints.
	parse = lambda string : [int(x.strip()) for x in string.strip().split("\n")]

	# Keep querying random.org until we have enough integers.
	while size < num:
		query = "https://www.random.org/integers/?num=%d&min=%d&max=%d&col=1&base=10&format=plain&rnd=new" % (min(num - size, batch_size), min_val, max_val)
		resp = requests.get(query)
		# If there is an error code, raise an exception.
		resp.raise_for_status()
		ret.extend(parse(resp.text))
		size += batch_size
	return np.array(ret)

def display_random_RGB_image(width, height):
	# If we're debugging, just generate random numbers with numpy so we don't overload
	# random.org's API unnecessarily.
	if USE_RANDOM_DOT_ORG:
		random_integers = generate_random_integers(width * height * 3, 0, 255)
		# Reshape the array to be width x height x 3.
		rgb_array = np.asarray(random_integers).reshape((width, height, 3))
	else:
		rgb_array = np.random.random((width, height, 3))	

	# Display the image using matplot.
	img = plt.imshow(rgb_array)
	img.set_cmap('hot')
	plt.axis('off')
	plt.show()

def help():
	# Print usage information if the user malforms their command.
	print ("Usage: python imagegen.py HEIGHT WIDTH\n" 
	 		"Dimensions must be integers in [1, " + str(MAX_SIZE) + "]. "
	 		"If you supply no width or height, uses 128x128 by default."
	 		)

def main(args):
	# By default, display a 128x128 image.
	if len(args) == 1:
		display_random_RGB_image(128, 128)
	# If the user supplied a width and height, use that instead.
	elif len(args) == 3:
		try:
			width = int(args[1])
			height = int(args[2])
		except:
			help()
			return

		if width <= 0 or width > MAX_SIZE or height <= 0 or height > MAX_SIZE:
			help()
			return

		display_random_RGB_image(width, height)
	else:
		help()

if __name__ == "__main__": 
	main(sys.argv)
