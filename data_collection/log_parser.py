from police_logs import PoliceLog


class LogParser(object):

    def __init__(self, log_class):
        self.log_class = log_class
        self.dispositions = log_class.dispositions

    @staticmethod
    def remove_headers(lines):
        line = None
        while len(lines) > 0 and (not line or line != 'Disposition'):
            line = lines.pop(0).strip()
        return lines

    def pop_chunk(self, data_list):
        """
        Pops a police log chunk off of data_list

        :return: decapitated data_list and the chunk
        """

        copy = data_list[:]

        def pop_list_and_append(list_to_append, the_list):
            next_line = the_list.pop(0)
            list_to_append.append(next_line)
            return next_line, the_list

        # Add all lines up until after the disposition line
        # after disposition, we have the detail, where multiple new lines can be present and so we cannot
        # rely on the \n\n split
        chunk = []
        line = None
        while not line or line not in self.dispositions:
            line, data_list = pop_list_and_append(chunk, data_list)

        # Add all the lines of the detail. Stop when we hit a datetime (that will signify a new chunk)
        detail = []
        while len(data_list) > 0 and not PoliceLog.datetime_reg.search(data_list[0]):
            line, data_list = pop_list_and_append(detail, data_list)
        chunk.append(' '.join(detail))
        return chunk, data_list

    def _chunk(self, data_list):
        """
        Breaks up a log report into chunks of logs

        :type data_list: list of double-newline separated txt versions of log pdfs
        :return: list of chunks
        """
        chunks = []
        while len(data_list) > 0:
            chunk, data_list= self.pop_chunk(data_list)
            chunks.append(chunk)
        return chunks

    # TODO: Cleanup this method
    def parse(self, filename=None, text=None):
        if filename:
            assert not text
            with open(filename, 'r') as f:
                text = f.read()

        assert text
        pages = [page for page in text.split('\x0c') if page]
        police_logs = []
        for page in pages:
            lines = [line for line in page.split('\n\n') if line]
            lines = LogParser.remove_headers(lines)
            if len(lines) == 0:  # It is possible that *only* headers exist on the page, in which case just break
                break
            chunks = self._chunk(lines)
            for chunk in chunks:
                try:
                    police_log_obj = self.log_class(chunk)
                    police_logs.append(police_log_obj)
                except Exception as e:
                    print e
        return police_logs
