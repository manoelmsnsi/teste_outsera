from flask import Blueprint, jsonify
from app.services.movies import get_producers_with_longest_and_shortest_intervals
from app.schemas.movies import ProducerIntervalResponse, ResponseModel, AwardedProducerResponse

movies_bp = Blueprint("movies", __name__)

@movies_bp.route("/awarded-producer", methods=["GET"])
def get_awarded_producer()-> ResponseModel:
    try:
        longest_interval_producer, longest_interval, shortest_interval_producer, shortest_interval = get_producers_with_longest_and_shortest_intervals()
        
        if not (longest_interval_producer and shortest_interval_producer):
            return jsonify({
                "status_code": 404,
                "data": None,
                "detail": "Unable to calculate intervals."
            }), 404

        # Preparing response
        response_data = ProducerIntervalResponse(
            producer_with_longest_interval=AwardedProducerResponse(
                producer=longest_interval_producer,
                interval=longest_interval
            ),
            producer_with_shortest_interval=AwardedProducerResponse(
                producer=shortest_interval_producer,
                interval=shortest_interval
            )
        )
        
        return jsonify({
            "status_code": 200,
            "data": response_data.model_dump(),
            "detail": None
        }), 200

    except (ValueError, TypeError) as e:
        return jsonify({
            "status_code": 400,
            "data": None,
            "detail": f"Invalid input: {str(e)}"
        }), 400
    except Exception as e:
        return jsonify({
            "status_code": 500,
            "data": None,
            "detail": f"An unexpected error occurred: {str(e)}"
        }), 500
