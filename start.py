import loging
import traceback
import colors_log

log = loging.logging(Name='START', Color=colors_log.red)

try:
    import main  # noqa: F401
except Exception as CERROR:
    traceback_lines = traceback.format_exc().split('\n')
    try:
        for line in traceback_lines:
            if 'line' in line:
                error_line_number = int(line.split(',')[1].split('line')[1].strip())
        for file in traceback_lines:
            if 'File' in file:
                error_file = file.split(',')[0].replace('File ', '').strip()
        log.cerror(user_id=None, do=f'Critical error: {CERROR} | Line: {error_line_number} | File: {error_file}')
    except Exception:
        print(CERROR)
