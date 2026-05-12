from dotenv import load_dotenv
from importers.json.JsonImporter import JsonImporter
from importers.uptime_robot.UptimeRobotImporter import UptimeRobotImporter
from uptime.ApiClient import ApiClient


if __name__ == '__main__':

    # Load environment variables from .env file
    load_dotenv()
    
    apiClient = ApiClient()

    # To Import Local Json Data
    # importer = JsonImporter(apiClient)

    # To Import UptimeRobot Data
    importer = UptimeRobotImporter(apiClient)

    # Load data from source
    # JSON or UptimeRobot
    importer.load_data_source()

    # Upload data to Uptime Kuma
    importer.migrate()