import logging
import datetime
import json
import traceback
import sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),  # UTC timestamp
            "level": record.levelname,  # Log level (e.g., INFO, ERROR)
            "logger": record.name,  # Logger name
            "message": record.getMessage(),  # Log message
        }
        
        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            # Extract the last traceback frame where the exception occurred
            tb_frame = traceback.extract_tb(exc_traceback)[-1]
            log_record["exception"] = {
                "type": exc_type.__name__,  # Exception type
                "message": str(exc_value),  # Exception message
                "function": tb_frame.name,  # Function where the exception occurred
                "line_number": tb_frame.lineno,  # Line number where the exception occurred
                "file": tb_frame.filename,  # Line number where the exception occurred
                "traceback": self.formatException(record.exc_info),  # Full traceback
            }

        
        return json.dumps(log_record, indent=2)

logger = logging.getLogger("vz_cloud_logger")

logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

low_level_handler = logging.StreamHandler()

low_level_handler.setLevel(logging.INFO)

low_level_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

low_level_handler.setFormatter(logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s"))

handler.setLevel(logging.ERROR)

handler.setFormatter(JsonFormatter())

logger.addHandler(handler)
logger.addHandler(low_level_handler)