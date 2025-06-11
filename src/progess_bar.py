'''
Josh O'Connor
University of Kansas
McNair Scholar's Program 2025
'''

import time

class ProgessBar:
    def __init__(self, total_objects):
        self.start_time = time.time()
        self.total_objects = total_objects
        
    def print_progress(self, current_object):
        elapsed = time.time() - self.start_time
        avg_time = elapsed / current_object
        remaining = avg_time * (self.total_objects - current_object)

        # Format times
        def format_seconds(s):
            mins, secs = divmod(int(s), 60)
            return f"{mins:02d}:{secs:02d}"

        elapsed_str = format_seconds(elapsed)
        eta_str = format_seconds(remaining)

        # Progress bar
        percent = (current_object / self.total_objects) * 100
        bar_length = 40
        filled = int(bar_length * current_object // self.total_objects)
        bar = '█' * filled + '-' * (bar_length - filled)

        print(f'\rProgress: |{bar}| {percent:.1f}% ({current_object}/{self.total_objects}) | Elapsed: {elapsed_str} | Current ETA: {eta_str}', end='', flush=True)