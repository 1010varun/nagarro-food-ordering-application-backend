from flask import Blueprint, jsonify, request

from admin_service import AdminService


admin_bp = Blueprint("admin", __name__)


admin_service = AdminService()


@admin_bp.route("/users", methods=["GET"])
def get_user_accounts():
    try:
        users = admin_service.get_user_accounts()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/restaurants", methods=["GET"])
def get_restaurants():
    try:
        restaurants = admin_service.get_restaurants()
        return jsonify(restaurants), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@admin_bp.route("/issues", methods=["GET"])
def get_issues():
    try:
        issues = admin_service.get_issues()
        return jsonify(issues), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/issues/<int:issue_id>", methods=["PUT"])
def resolve_issue(issue_id):
    resolution_data = request.json
    try:
        admin_service.resolve_issue(issue_id, resolution_data)
        return jsonify({"message": "Issue resolved successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
