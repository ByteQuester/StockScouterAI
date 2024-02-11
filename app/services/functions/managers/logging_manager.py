import datetime
import logging
import traceback


class LoggingManager:
    """
    Manages logging for the application.
    """

    def __init__(self):
        self.log_file_path = None
        self.log_format = None
        self.log_level = logging.INFO
        self._configure_logging()

    def set_log_file_path(self, path):
        """
        Set the file path for logging output.

        Args:
            path (str): Path to the log file.
        """
        self.log_file_path = path
        self._configure_logging()

    def set_log_format(self, format):
        """
        Set the format for log messages.

        Args:
            format (str): Format string for log messages.
        """
        self.log_format = format
        self._configure_logging()

    def set_log_level(self, level):
        """
        Set the logging level.

        Args:
            level (str): Logging level (e.g., 'INFO', 'DEBUG').
        """
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if level in valid_levels:
            self.log_level = getattr(logging, level)
            self._configure_logging()
        else:
            logging.warning(
                f'Invalid log level "{level}". Using default log level "INFO".'
            )

    def _configure_logging(self):
        """
        Configure the logging settings based on current attributes.
        """
        if self.log_file_path:
            logging.basicConfig(filename=self.log_file_path,
                                level=self.log_level,
                                format=self.log_format)
        else:
            logging.basicConfig(level=self.log_level, format=self.log_format)

    def is_critical(self, error):
        """
        Check if an error is critical.

        Args:
            error (Exception): Error to evaluate.

        Returns:
            bool: True if error is critical, False otherwise.
        """
        error_severity = self.get_error_severity(error)
        return error_severity >= logging.ERROR

    @staticmethod
    def get_error_severity(error):
        """
        Get the severity level for a given error.

        Args:
            error (Exception): Error to evaluate.

        Returns:
            int: Severity level of the error.
        """
        severity_mapping = {
            ConnectionError: logging.CRITICAL,
            TimeoutError: logging.CRITICAL,
            ValueError: logging.WARNING,
            Exception: logging.ERROR
        }
        # Determine the error type and map it to the corresponding severity level
        for error_type, severity_level in severity_mapping.items():
            if isinstance(error, error_type):
                return severity_level
        # Default severity level if the error type is not in the mapping
        return logging.ERROR

    def log_error(self, error, severity='INFO'):
        """
        Log an error with detailed information.

        Args:
            error (Exception): Error to log.
            severity (str): Severity level of the error.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        location = self.get_error_location()
        message = f'{error.__class__.__name__}: {str(error)}'
        log_message = f'{timestamp} - {severity} - {location} - {message}'
        logger = logging.getLogger('__name__')
        if severity == 'INFO':
            logger.info(log_message)
        elif severity == 'WARNING':
            logger.warning(log_message)
        elif severity == 'ERROR':
            logger.error(log_message)
        elif severity == 'CRITICAL':
            logger.critical(log_message)
        elif severity == 'DEBUG':
            logger.debug(log_message)
        else:
            raise ValueError(f'Invalid severity level: {severity}')

    @staticmethod
    def get_error_location():
        """
        Retrieve the code location of an error.

        Returns:
            str: Location in the code where the error occurred.
        """
        traceback_info = traceback.extract_stack(
        )[:-2]  # Exclude the current method and caller from the traceback
        file_path, line_number, function_name, _ = traceback_info[-1]
        return f'{file_path} - {function_name}() - Line {line_number}'

    @staticmethod
    def format_log_message(message, message_type):
        """
        Format a log message with a timestamp and type.

        Args:
            message (str): Message to format.
            message_type (str): Type of the message (e.g., 'ERROR').

        Returns:
            str: Formatted log message.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_message = f"{timestamp} - {message_type} - {message}"
        return formatted_message

    @staticmethod
    def log(message, severity):
        """
        Log a message with a specified severity level.

        Args:
            message (str): Message to log.
            severity (str): Severity level (e.g., 'INFO').
        """
        valid_severity_levels = [
            'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        ]
        if severity in valid_severity_levels:
            severity = getattr(logging, severity)
        else:
            logging.warning(
                f'Invalid severity level "{severity}". Using default severity level "INFO".'
            )
            severity = logging.INFO
        logging.log(severity, message)
