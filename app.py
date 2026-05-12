from dotenv import load_dotenv
from importers import JsonImporter, RemoteJsonImporter, UptimeRobotImporter
from uptime.ApiClient import ApiClient


if __name__ == '__main__':
    load_dotenv()

    api_client = ApiClient()
    try:
        # To import from local JSON file:
        # importer = RemoteJsonImporter(api_client)

        # To import from local JSON file:
        importer = JsonImporter(api_client)

        # To import from UptimeRobot:
        # importer = UptimeRobotImporter(api_client)

        importer.load_data_source()
        importer.migrate()
    finally:
        api_client.disconnect()
