from flask import jsonify, make_response

def succes(values, message):
    res = {
        'data' : values,
        'message' : message
    }

    return make_response(jsonify(res)), 200

def badRequest(values, message):
    res = {
        'data' : values,
        'message' : message
    }

    return make_response(jsonify(res)), 400

def succesSingle(message):
    res = {
        'message' : message
    }

    return make_response(jsonify(res)), 200

def badRequestSingle(message):
    res = {
        'message' : message
    }

    return make_response(jsonify(res)), 400