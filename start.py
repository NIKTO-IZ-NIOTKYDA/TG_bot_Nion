import loging
import traceback
import colors_log

log = loging.logging(Name='START', Color=colors_log.red)

try:
    import main  # noqa: F401
except Exception as CERROR:
    print(traceback.format_exc())

    traceback_lines = traceback.format_exc().split('\n')
    traceback_lines.remove(traceback_lines[0])

    traceback_lines_size = 0 
    for x in traceback_lines:
        traceback_lines_size += 1

    try:
        i = 0
        while i < traceback_lines_size - 2:

            error_command = traceback_lines[i+1].replace('    ', '').strip()

            error_line_number = traceback_lines[i].split('line ')[-1].replace(', in <module>', '').strip()
            
            error_file = traceback_lines[i].split(',')[0].replace('File ', '').strip()
            
            i += 2
            log.cerror(user_id=None, msg=f'Critical error: "{CERROR}"')
            log.cerror(user_id=None, msg=f'Command: "{error_command}"')
            log.cerror(user_id=None, msg=f'Line: {error_line_number}')
            log.cerror(user_id=None, msg=f'File: {error_file}\n')
        
        print(traceback.format_exc())

        exit(1)
    
    except Exception as E:
        print(traceback.format_exc())
        print(E)
        print(CERROR)
