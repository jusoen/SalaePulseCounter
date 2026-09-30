# Pulse Counter: Saleae Logic 2 High Level Analyser.
#
# Input: the Simple Parallel analyser with its clock on the pulse channel
# (rising edge), so it emits one frame per rising edge.
# Output: one 'count' frame per gate window holding the running total of
# edges since the start of the capture.
#
# An HLA is only called when an input frame arrives. With no pulses there
# are no bubbles, and the last partial window is reported on the next edge.
# Logic creates a fresh instance per capture, so the total resets each time.

from saleae.analyzers import HighLevelAnalyzer, AnalyzerFrame, NumberSetting


class PulseCounter(HighLevelAnalyzer):
    gate_ms = NumberSetting(min_value=1, max_value=10000)

    result_types = {
        'count': {
            'format': 'Total: {{data.total}}'
        }
    }

    def __init__(self):
        # The setting box starts empty in Logic, so fall back to 100 ms.
        gate_ms = self.gate_ms if self.gate_ms else 100
        self.gate_s = float(gate_ms) / 1000.0
        self.total = 0
        self.window_start = None

    def decode(self, frame: AnalyzerFrame):
        self.total += 1

        if self.window_start is None:
            self.window_start = frame.start_time
            return None

        if float(frame.start_time - self.window_start) < self.gate_s:
            return None

        # Window closed. This edge opens the next window, and the total
        # reported includes it.
        result = AnalyzerFrame('count', self.window_start, frame.start_time,
                               {'total': self.total})
        # Carriage return without newline rewrites the same terminal line.
        print('\rPulse total: {}'.format(self.total), end='', flush=True)
        self.window_start = frame.start_time
        return result
