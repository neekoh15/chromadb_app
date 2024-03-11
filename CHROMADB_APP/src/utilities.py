import sys

def progress_bar(actual:int, total:int, lenght=50):
    percent = actual / total
    bar_length = int(50 * percent)
    bar = '█' * bar_length + '▯' * (50 - bar_length)
    sys.stdout.write(f'\r[{bar}] {percent:.2%} ')
    sys.stdout.flush()