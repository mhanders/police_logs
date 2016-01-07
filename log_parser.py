class LogParser(object):

	def __init__(self, log_class):
		self.log_class = log_class

	def _remove_headers(self, lines):
		line = None
		while(not line or line != 'Disposition'): line = lines.pop(0).strip()
		return lines

	def _chunk(self, chunk_list, chunk_length):
		num_chunks = len(chunk_list) / chunk_length
		chunks = [chunk_list[(i-1)*chunk_length : i*chunk_length] for i in xrange(1, num_chunks)]
		trailing_chunk = chunk_list[(num_chunks-1)*chunk_length:]

		# Need to fix the final comments of the trailing chunk, which could be multiline
		trailing_chunk, comment = trailing_chunk[:chunk_length-1], trailing_chunk[chunk_length-1:]
		trailing_chunk.append(' '.join(comment))
		chunks.append(trailing_chunk)

		return chunks

	# TODO: Cleanup this method
	def get_logs_from_report(self, filename):
		with open(filename, 'r') as f:
			data = f.read()
			pages = [page for page in data.split('\x0c') if page]
			police_logs = []
			for page in pages:
				lines = [line for line in page.split('\n\n') if line]
				lines = self._remove_headers(lines)
				chunks = self._chunk(lines, 6)
				police_logs +=map(lambda x: self.log_class(x), chunks)
			return police_logs