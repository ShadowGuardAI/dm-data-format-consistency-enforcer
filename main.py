import argparse
import logging
import re
import sys
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFormatEnforcer:
    """
    Enforces data format consistency within a column or field,
    even if the underlying data is masked.
    """

    def __init__(self, format_type, locale='en_US'):
        """
        Initializes the DataFormatEnforcer.

        Args:
            format_type (str): The type of format to enforce (e.g., 'phone_number', 'zip_code').
            locale (str): The locale to use for Faker (e.g., 'en_US', 'de_DE').
        """
        self.format_type = format_type
        self.fake = Faker(locale)
        self.formatter = self._get_formatter()  # Determines which function to use for formatting

    def _get_formatter(self):
        """
        Returns the appropriate Faker method based on the format type.
        """
        if self.format_type == 'phone_number':
            return self.fake.phone_number
        elif self.format_type == 'zip_code':
            return self.fake.postcode
        elif self.format_type == 'email':
            return self.fake.email
        elif self.format_type == 'ssn':
            return self.fake.ssn
        elif self.format_type == 'credit_card_number':
            return self.fake.credit_card_number
        else:
            logging.error(f"Unsupported format type: {self.format_type}")
            raise ValueError(f"Unsupported format type: {self.format_type}")

    def enforce_format(self, data):
        """
        Enforces the defined format on the input data.

        Args:
            data (str): The input data to format.

        Returns:
            str: The formatted data.  Returns None if formatting fails.
        """
        try:
            # Replace existing data with a new, formatted value. No need to format the existing data.
            formatted_data = self.formatter()
            return formatted_data
        except Exception as e:
            logging.error(f"Error enforcing format: {e}")
            return None


def setup_argparse():
    """
    Sets up the argparse command-line interface.

    Returns:
        argparse.ArgumentParser: The argument parser.
    """
    parser = argparse.ArgumentParser(description="Enforces data format consistency.")
    parser.add_argument("format_type", help="The type of format to enforce (e.g., phone_number, zip_code, email, ssn, credit_card_number)")
    parser.add_argument("input_data", nargs='?', default=None, help="The input data to format (optional).  If not provided, a single formatted value is generated.") #Input is now optional
    parser.add_argument("--locale", default="en_US", help="The locale to use (e.g., en_US, de_DE). Default is en_US.")
    parser.add_argument("--count", type=int, default=1, help="The number of formatted values to generate when no input data is provided. Default is 1.")

    return parser


def main():
    """
    Main function to parse arguments, enforce data format, and output the result.
    """
    try:
        parser = setup_argparse()
        args = parser.parse_args()

        # Input validation
        supported_formats = ["phone_number", "zip_code", "email", "ssn", "credit_card_number"]
        if args.format_type not in supported_formats:
            logging.error(f"Invalid format type: {args.format_type}. Supported types are: {supported_formats}")
            print(f"Error: Invalid format type. Supported types are: {supported_formats}") #output error for user, outside of log
            sys.exit(1)
        
        if args.count < 1 and args.input_data is None:
            logging.error("Count must be a positive integer when no input data is provided.")
            print("Error: Count must be a positive integer when no input data is provided.") #User facing error
            sys.exit(1)


        enforcer = DataFormatEnforcer(args.format_type, args.locale)

        if args.input_data:
            # Enforce format on the provided input data
            formatted_data = enforcer.enforce_format(args.input_data)
            if formatted_data:
                print(formatted_data)
            else:
                logging.error("Failed to format data.")
                print("Error: Failed to format data.") #User facing error
                sys.exit(1)
        else:
            # Generate a specified number of formatted values
            for _ in range(args.count):
                formatted_data = enforcer.enforce_format(None)
                if formatted_data:
                    print(formatted_data)
                else:
                    logging.error("Failed to generate formatted data.")
                    print("Error: Failed to generate formatted data.") #User facing error
                    sys.exit(1)

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}") #User facing error
        sys.exit(1)


if __name__ == "__main__":
    main()