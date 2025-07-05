from flask import Flask, render_template, request, jsonify
import re
import os

app = Flask(__name__)

# URL detection regex - matches common URL patterns
URL_PATTERN = re.compile(
    r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:[/\w\-._~:/?#[\]@!$&\'()*+,;=%]*)?')


def detect_urls(text):
    """Detect URLs in text and return list of matches"""
    return URL_PATTERN.findall(text)


def calculate_post_length(text, service):
    """Calculate the effective length of a post for a given service"""
    # Remove trailing whitespace for counting
    text = text.rstrip()

    # Count base characters
    base_length = len(text)

    # Find URLs and adjust length based on service
    urls = detect_urls(text)
    url_adjustment = 0

    for url in urls:
        if service == 'twitter':
            # X: URLs count as 23 characters
            url_adjustment += 23 - len(url)
        elif service == 'bluesky':
            # Bluesky: URLs count as 31 characters
            url_adjustment += 31 - len(url)
        # Threads: URLs count as their actual length (no adjustment)

    return base_length + url_adjustment


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/api/calculate-length', methods=['POST'])
def calculate_length():
    """API endpoint to calculate post length"""
    data = request.json
    text = data.get('text', '')
    service = data.get('service', 'twitter')

    length = calculate_post_length(text, service)
    urls = detect_urls(text)

    return jsonify({
        'length': length,
        'urls_found': len(urls),
        'urls': urls
    })


if __name__ == '__main__':
    app.run(debug=True)
