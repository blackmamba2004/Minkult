import json

from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from park.models import Park


def clean_description(html_text: str) -> str:
    return BeautifulSoup(html_text, "html.parser").get_text(separator=" ", strip=True)


def parse_object(obj: dict) -> dict:
    data = obj.get("data", {})
    general = data.get("general", {})
    address = general.get("address", {})

    coordinates = address.get("mapPosition", {}).get("coordinates", [None, None])
    lon, lat = coordinates if len(coordinates) == 2 else (None, None)

    return {
        "id": general.get("id"),
        "name": general.get("name"),
        "description": clean_description(general.get("description", "")),
        "category": general.get("category", {}).get("name"),
        "status": general.get("status"),
        "full_address": address.get("fullAddress"),
        "street": address.get("street"),
        "lat": lat,
        "lon": lon,
    }


class Command(BaseCommand):
    help = "Load parks data from a JSON file into the database"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str, help="The path to the JSON file")

    def handle(self, **options):
        filename = options["filename"]

        self.stdout.write(self.style.SUCCESS(f"Loading data from {filename}..."))
        try:
            with open(filename, "r", encoding="utf-8") as f:
                objects = json.load(f)

            for raw_obj in objects:
                parsed = parse_object(raw_obj)
                Park.objects.update_or_create(id=parsed["id"], defaults=parsed)

            self.stdout.write(self.style.SUCCESS("Data loaded successfully"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {filename} not found"))

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Error decoding JSON from file {filename}"))
