from app.services.functions.managers import LoggingManager


class NotificationManager:

    def __init__(self, logging_manager):
        """
        Initialize NotificationManager with a LoggingManager instance.

        Parameters:
            logging_manager (LoggingManager): A LoggingManager object for handling logs.
        """
        self.logging_manager = logging_manager

    def send_notification(self, message):
        """
        Send a notification and log the action.

        Parameters:
            message (str): The notification message to send.
        """
        try:
            # TBD Placeholder for notification sending logic
            print(message)
            self.logging_manager.log(f'Sent notification: {message}', 'INFO')
        except Exception as e:
            error_location = LoggingManager.get_error_location()
            self.handle_error(
                f'Error sending notification: {str(e)} at {error_location}')

    def handle_error(self, error_message):
        """
        Handle and log errors that occur during notification sending.

        Parameters:
            error_message (str): The error message to handle.
        """
        print(f'Error: {error_message}')
        critical = LoggingManager.is_critical(Exception(error_message))
        severity = 'CRITICAL' if critical else 'ERROR'
        self.logging_manager.log(f'Error: {error_message}', severity)
