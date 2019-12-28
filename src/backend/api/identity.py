#
# Memento
# Backend
# Identity API
#

from flask import request, Blueprint, jsonify
from sqlalchemy.exc import IntegrityError

from .utils import parse_params
from ..config import API_VERSION
from ..mapping.identity import *
from ..ops.identity import *

identity = Blueprint("identity", __name__)

## Organisation API
# api - query organisations 
# returns organisation ids using
@identity.route(f"/api/v{API_VERSION}/{identity.name}/orgs", methods=["GET"])
def route_orgs():
    # parse query args
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    # query orgs
    org_ids = query_orgs(skip, limit)
    return jsonify(org_ids)

# api - read, create, update, delete organisations
@identity.route(f"/api/v{API_VERSION}/{identity.name}/org", methods=["POST"])
@identity.route(f"/api/v{API_VERSION}/{identity.name}/org/<org_id>", methods=["GET", "PATCH", "DELETE"])
def route_org(org_id=None):
    if request.method == "GET" and org_id:
        # get org for id
        org = get_org(org_id)
        return jsonify(org)
    elif request.method == "POST" and request.is_json:
        # create org with params in json
        params = parse_params(request, org_mapping)
        org_id = create_org(**params)
        return jsonify({ "id": org_id })
    elif request.method == "PATCH" and org_id and request.is_json:
        # parse params in json
        params = parse_params(request, org_mapping)
        # update org with params in json
        update_org(org_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and org_id:
        # delete org with params in json
        delete_org(org_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

## Team API
# api - query teams with url params
@identity.route(f"/api/v{API_VERSION}/{identity.name}/teams", methods=["GET"])
def route_teams():
    # parse query args
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    org_id = request.args.get("org", None)

    # query teams
    team_ids = query_teams(org_id, skip, limit)
    return jsonify(team_ids)

# api - read, create, update, delete teams
@identity.route(f"/api/v{API_VERSION}/{identity.name}/team", methods=["POST"])
@identity.route(f"/api/v{API_VERSION}/{identity.name}/team/<team_id>", methods=["GET", "PATCH", "DELETE"])
def route_team(team_id=None):
    if request.method == "GET" and team_id:
        # get team for id
        team = get_team(team_id)
        return jsonify(team)
    elif request.method == "POST" and request.is_json:
        # create team with params in json
        params = parse_params(request, team_mapping)
        team_id = create_team(**params)
        return jsonify({ "id": team_id })
    elif request.method == "PATCH" and team_id and request.is_json:
        # parse params in json
        params = parse_params(request, team_mapping)
        # update team with params in json
        update_team(team_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and team_id:
        # delete team with params in json
        delete_team(team_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

## User API
# api - query users with url params
@identity.route(f"/api/v{API_VERSION}/{identity.name}/users", methods=["GET"])
def route_users():
    # parse query url params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    org_id = request.args.get("org", None)
    if not org_id is None: org_id = int(org_id)
    team_id = request.args.get("team", None)
    if not team_id is None: team_id = int(team_id)

    # perform query with op
    user_ids = query_users(org_id, team_id, skip, limit)
    return jsonify(user_ids)

# api - read, create, update, delete users
@identity.route(f"/api/v{API_VERSION}/{identity.name}/user", methods=["POST"])
@identity.route(f"/api/v{API_VERSION}/{identity.name}/user/<user_id>", methods=["GET", "PATCH", "DELETE"])
def route_user(user_id=None):
    if request.method == "GET" and user_id:
        # get user for id
        user = get_user(user_id)
        return jsonify(user)
    elif request.method == "POST" and request.is_json:
        # create user with params in json
        params = parse_params(request, user_mapping)
        user_id = create_user(**params)
        return jsonify({ "id": user_id })
    elif request.method == "PATCH" and user_id and request.is_json:
        # parse params in json
        params = parse_params(request, user_mapping)
        # update user with params in json
        update_user(user_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and user_id:
        # delete user with params in json
        delete_user(user_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError

## manage api
# api - query manages with url params
@identity.route(f"/api/v{API_VERSION}/{identity.name}/manages", methods=["GET"])
def route_manages():
    # parse query url params
    skip = int(request.args.get("skip", 0))
    limit = request.args.get("limit", None)
    if not limit is None: limit = int(limit)
    org_id = request.args.get("org", None)
    if not org_id is None: org_id = int(org_id)
    managee_id = request.args.get("target", None)
    if not managee_id is None: managee_id = int(managee_id)
    manager_id = request.args.get("manager", None)
    if not manager_id is None: manager_id = int(manager_id)

    # perform query with op
    manage_ids = query_manage(org_id, managee_id, manager_id, skip, limit)
    return jsonify(manage_ids)

# api - read, create, update, delete managements
@identity.route(f"/api/v{API_VERSION}/{identity.name}/manage", methods=["POST"])
@identity.route(f"/api/v{API_VERSION}/{identity.name}/manage/<manage_id>", methods=["GET", "PATCH", "DELETE"])
def route_manage(manage_id=None):
    if request.method == "GET" and manage_id:
        # get manage for id
        manage = get_manage(manage_id)
        return jsonify(manage)
    elif request.method == "POST" and request.is_json:
        # create manage with params in json
        params = parse_params(request, manage_mapping)
        manage_id = create_manage(**params)
        return jsonify({ "id": manage_id })
    elif request.method == "PATCH" and manage_id and request.is_json:
        # parse params in json
        params = parse_params(request, manage_mapping)
        # update manage with params in json
        update_manage(manage_id, **params)
        return jsonify({"success": True })
    elif request.method == "DELETE" and manage_id:
        # delete manage with params in json
        delete_manage(manage_id)
        return jsonify({"success": True })
    else:
        raise NotImplementedError