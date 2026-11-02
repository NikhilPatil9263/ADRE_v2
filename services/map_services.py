
import os
import logging
import requests


logger = logging.getLogger(__name__)


class MapService:
    """
    TomTom truck-routing service.

    Coordinates must be supplied as:
        (latitude, longitude)

    Existing interface is preserved:
        get_route_distance_km(origin, destination)
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("TOMTOM_API_KEY")

        self.url = (
            "https://api.tomtom.com/routing/1/calculateRoute"
        )

        # Truck configuration is read from environment variables.
        # Zero means that the corresponding restriction is not applied.
        self.vehicle_config = {
            "vehicleWeight": self._get_int_env(
                "TRUCK_WEIGHT_KG", 0
            ),
            "vehicleAxleWeight": self._get_int_env(
                "TRUCK_AXLE_WEIGHT_KG", 0
            ),
            "vehicleNumberOfAxles": self._get_int_env(
                "TRUCK_NUMBER_OF_AXLES", 0
            ),
            "vehicleLength": self._get_float_env(
                "TRUCK_LENGTH_M", 0
            ),
            "vehicleWidth": self._get_float_env(
                "TRUCK_WIDTH_M", 0
            ),
            "vehicleHeight": self._get_float_env(
                "TRUCK_HEIGHT_M", 0
            ),
            "vehicleMaxSpeed": self._get_int_env(
                "TRUCK_MAX_SPEED_KMH", 0
            ),
        }

        self.last_route_details = None

    @staticmethod
    def _get_int_env(name, default):
        value = os.getenv(name)

        if not value:
            return default

        try:
            return int(value)
        except ValueError:
            raise ValueError(
                f"{name} must contain a valid integer."
            )

    @staticmethod
    def _get_float_env(name, default):
        value = os.getenv(name)

        if not value:
            return default

        try:
            return float(value)
        except ValueError:
            raise ValueError(
                f"{name} must contain a valid number."
            )

    @staticmethod
    def _validate_coordinates(coordinates, name):
        if (
            not isinstance(coordinates, (tuple, list))
            or len(coordinates) != 2
        ):
            raise ValueError(
                f"{name} must be (latitude, longitude)."
            )

        latitude, longitude = coordinates

        if not (-90 <= latitude <= 90):
            raise ValueError(
                f"Invalid latitude in {name}: {latitude}"
            )

        if not (-180 <= longitude <= 180):
            raise ValueError(
                f"Invalid longitude in {name}: {longitude}"
            )

    def get_route_details(self, origin, destination):
        """
        Get TomTom truck route details.

        Returns:
            {
                "distance_km": float,
                "travel_time_min": float,
                "travel_time_sec": int,
                "traffic_delay_sec": int
            }
        """

        if not self.api_key:
            raise RuntimeError(
                "TomTom API key is missing. "
                "Set the TOMTOM_API_KEY environment variable."
            )

        self._validate_coordinates(origin, "origin")
        self._validate_coordinates(destination, "destination")

        # TomTom expects latitude,longitude.
        locations = (
            f"{origin[0]},{origin[1]}:"
            f"{destination[0]},{destination[1]}"
        )

        endpoint = f"{self.url}/{locations}/json"

        params = {
            "key": self.api_key,
            "travelMode": "truck",
            "traffic": "true",
            "routeType": "fastest",
            "vehicleCommercial": "true",
            "vehicleMaxSpeed": self.vehicle_config[
                "vehicleMaxSpeed"
            ],
        }

        # Include only configured truck restrictions.
        for parameter, value in self.vehicle_config.items():
            if parameter == "vehicleMaxSpeed":
                continue

            if value > 0:
                params[parameter] = value

        try:
            response = requests.get(
                endpoint,
                params=params,
                timeout=20
            )

            if not response.ok:
                error_message = "No additional error information."

                try:
                    error_data = response.json()
                    error_message = (
                        error_data.get("detailedError", {}).get(
                            "message"
                        )
                        or error_data.get("errorText")
                        or error_message
                    )
                except (ValueError, AttributeError):
                    pass

                raise RuntimeError(
                    f"TomTom API returned HTTP "
                    f"{response.status_code}: {error_message}"
                )

            data = response.json()

            route_summary = data["routes"][0]["summary"]

            distance_m = route_summary["lengthInMeters"]
            travel_time_sec = route_summary[
                "travelTimeInSeconds"
            ]

            details = {
                "distance_km": round(distance_m / 1000, 2),
                "travel_time_min": round(
                    travel_time_sec / 60, 2
                ),
                "travel_time_sec": travel_time_sec,
                "traffic_delay_sec": route_summary.get(
                    "trafficDelayInSeconds", 0
                ),
            }

            self.last_route_details = details

            logger.info(
                "TomTom truck route: %.2f km, %.2f minutes",
                details["distance_km"],
                details["travel_time_min"]
            )

            return details

        except requests.exceptions.Timeout:
            raise RuntimeError(
                "TomTom request timed out after 20 seconds."
            ) from None

        except requests.exceptions.RequestException:
            raise RuntimeError(
                "Unable to connect to TomTom Routing API."
            ) from None

        except (KeyError, IndexError, TypeError, ValueError):
            raise RuntimeError(
                "TomTom returned an unexpected route response."
            ) from None

    def get_route_distance_km(self, origin, destination):
        """
        Backward-compatible method used by run_phase3.py.
        Returns truck road distance in kilometers.
        """

        route = self.get_route_details(
            origin,
            destination
        )

        return route["distance_km"]
