import re
import unicodedata
from flask import jsonify 

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).lower()

    return text.strip('-')


def check_missing_fields(request_data, required_fields):
    if not all(field in request_data for field in required_fields):
        return jsonify({"error": f"Missing one or more required fields: {', '.join(required_fields)}"}), 400
