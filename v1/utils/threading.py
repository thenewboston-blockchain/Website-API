import threading


class EmailThread(threading.Thread):
    """To improve speed of sending emails

    thread class enables us to send
        emails on a separate process thread
    """

    def __init__(self, server, from_email, to_email, message):
        """Email object requires:

        the smtp server, from, to, and message
        """
        self.server = server
        self.from_email = from_email
        self.to_email = to_email
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        self.server.sendmail(self.from_email, [self.to_email], self.message)
