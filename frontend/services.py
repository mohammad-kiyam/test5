import pika, time, json, requests, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
rabbitmq_host = '10.147.17.228'
api_key = os.getenv('API_KEY')

# RabbitMQ Functions
def send_message(queue_name, message): #All queue_names and messages are declards inside app.py
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # Makes the message persistent
    )
    connection.close()

def consume_message(queue_name, delay=5): #All queue_names and messages are declards inside app.py
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    time.sleep(delay)  # delay needed for message to reach all the way around
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=True)
    connection.close()

    if body:
        message = body.decode('utf-8')
        try:
            # Attempt to parse as JSON
            return json.loads(message)
        except json.JSONDecodeError:
            # If not JSON, return as plain string
            return message
    return None


# External API Functions
def fetch_job_results(job_title, location):
    url = "https://linkedin-data-api.p.rapidapi.com/search-jobs"
    headers = {
	"x-rapidapi-key": "5ad49cae09msh9ca2d0578e8a801p168e63jsnbc6c9895684c",
	"x-rapidapi-host": "linkedin-api8.p.rapidapi.com"
}
    querystring = {
        "keywords": job_title,
        "location" : location
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        print(f"Request URL: {response.url}")
        print(f"Response Code: {response.status_code}")
        print(f"Text: Response: {response.text}")
        print(f"JSON Response: {response.json()}")
        response.raise_for_status()
        jobs = response.json().get('data', [])
        return [
            {
                'title': job.get('title', 'N/A'),
                'company_name': job.get('company', {}).get('name', 'N/A'),
                'benefits': job.get('benefits', 'N/A'),
                'location': job.get('location', 'N/A'),
                'job_url': job.get('url', '#'),
                'description': job.get('description', 'Description not available'),
                'employment_type': job.get('type', 'N/A'),
                'post_date': job.get('postDate', 'N/A'),
                'company_logo': job.get('company', {}).get('logo', 'N/A'),
                'company_url': job.get('company', {}).get('url', 'N/A')
            }
            for job in jobs
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
