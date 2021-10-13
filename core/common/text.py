

class Format:
    def clean(self, text: str):  # Shorthand for self.convert and self.remove
        for x in trace.tracers:
            text = text.replace(str(x), '')
        return ''.join(i for i in text if ord(i) < 128)
