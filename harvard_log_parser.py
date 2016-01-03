import ipdb

class HardvardPoliceLog(object):

	def __init__(self, data):
		self.datetime_reported = data[0]
		self.incident_type = data[1]
		self.datetime_occurred = data[2]
		self.location = data[3]
		self.disposition = data[4]
		self.detail = data[5]


def chunk(chunk_list, chunk_length):
	num_chunks = len(chunk_list) / chunk_length
	chunks = [chunk_list[(i-1)*chunk_length : i*chunk_length] for i in xrange(1, num_chunks)]
	trailing_chunk = chunk_list[(num_chunks-1)*chunk_length:]

	# Need to fix the final comments of the trailing chunk, which could be multiline
	trailing_chunk, comment = trailing_chunk[:chunk_length-1], trailing_chunk[chunk_length-1:]
	trailing_chunk.append(' '.join(comment))
	chunks.append(trailing_chunk)

	return chunks

def remove_headers(lines):
	line = None
	while(not line or line != 'Disposition'): line = lines.pop(0).strip()
	return lines

with open('sample_2page.txt', 'r') as f:
	data = f.read()
	pages = [page for page in data.split('\x0c') if page]
	for page in pages:
		lines = [line for line in page.split('\n\n') if line]
		lines = remove_headers(lines)
		chunks = chunk(lines, 6)
		police_logs = map(lambda x: HardvardPoliceLog(x), chunks)
		ipdb.set_trace()
