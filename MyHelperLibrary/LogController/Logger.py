import logging
import colorlog
import sys 
import time
import os
import io

# ========================================================================================

def setupLogger(obj, programName, logLevel=None):
    """
        Setup the root logger for any object
    """
    log_directory = "Logs"
    os.makedirs(log_directory, exist_ok=True)

    if not logLevel:
        logLevel = "DEBUG"
    else:
        logLevel = logLevel.upper()

    if not hasattr(logging, logLevel):
        logging.warning(f"Warning: Invalid log level '{logLevel}'. Defaulting to debug")

    numeric_level = getattr(logging, logLevel, logging.DEBUG)

    # Create colored formatter for console
    colored_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s: %(message)s',
        log_colors={
            'DEBUG'     : 'light_cyan',
            'INFO'      : 'green',
            'WARNING'   : 'yellow',
            'ERROR'     : 'red',
            'CRITICAL'  : 'red,bg_white',
        }
    )
    
    # Create plain formatter for file
    plain_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    
    # Console handler with colors
    utf8_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    console_handler = logging.StreamHandler(utf8_stdout)
    console_handler.setFormatter(colored_formatter)
    
    # File handler without colors
    file_handler = logging.FileHandler(f'{log_directory}/{programName}_{int(time.time())}.log',
                                            encoding='utf-8'
                                      )

    file_handler.setFormatter(plain_formatter)
    
    # Configure logging with both handlers
    logging.basicConfig(
        level=numeric_level,
        handlers=[console_handler, file_handler]
    )

    logger_name     = obj.__class__.__name__
    obj.logger      = logging.getLogger(logger_name)
    obj.debug       = "debug"
    obj.info        = "info"
    obj.warning     = "warning"
    obj.error       = "error"

    obj.log = _log_method.__get__(obj, obj.__class__)

# ========================================================================================

def _log_method(self, level: str, message: str):

    # No logs are generated for empty levels allowing the logs to be turned off
    if not level:
        return

    level = level.upper()

    if not hasattr(logging, level):
        self.logger.warning(f"Warning: Invalid log level '{level}'. Defaulting to debug")

    numeric_level = getattr(logging, level, logging.DEBUG)
        
    self.logger.log(numeric_level, message)

# ========================================================================================
