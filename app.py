#------------------------------------------------------------------#
#                          Imports                                 #
#------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from sqlalchemy import exc
from flask_cors import CORS, cross_origin
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    #------------------------------------------------------------------#
    #                        End Points                                #
    #------------------------------------------------------------------#

    # METHOD: 'GET' movies

    @app.route('/movies')
    def get_movies():
        try:
            movie_shelf = Movie.query.all()
            movies = [movie.format() for movie in movie_shelf]
            if len(movies) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'movies': movies
            })
        except BaseException:
            abort(404)

    # METHOD: 'GET' actors
    @app.route('/actors')
    def get_actors():
        try:
            actors = Actor.query.all()
            actor_list = [actor.format() for actor in actors]
            if len(actor_list) == 0:
                abort(404)
            return jsonify({
                'success': True,
                'actors': actor_list
            })
        except BaseException:
            abort(404)

    # METHOD: 'POST' movies
    '''
  Example of post data
    {
      "rate": 2.5 ,
      "release_date": "2020-05-15T23:00:00.000Z",
      "title": "new test new"
    }

  '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def new_movies(token):
        try:
            title = request.json['title']
            rate = request.json['rate']
            release_date = request.json['release_date']
            if title and release_date and rate:
                insert_new = Movie(
                    title=title, rate=rate, release_date=release_date)
                insert_new.insert()
            else:
                abort(400)
            movie_shelf = Movie.query.all()
            movies = [movie.format() for movie in movie_shelf]
            return jsonify({
                'success': True,
                'movies': movies
            })
        except BaseException:
            abort(400)

    '''
  Example of post data
    {
      "name": "Muhammed" ,
      "age": 20,
      "gender": "M"
    }

  '''
    # METHOD: 'POST' actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def new_actor(token):
        try:
            name = request.json['name']
            age = request.json['age']
            gender = request.json['gender']
            if name and gender and age:
                create_new = Actor(name=name, age=age, gender=gender)
                create_new.insert()
            else:
                abort(400)
            actors = Actor.query.all()
            actor_list = [actor.format() for actor in actors]
            return jsonify({
                'success': True,
                'actors': actor_list
            })
        except BaseException:
            abort(400)

    # METHOD: 'DELETE' movies

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(token, id):
        try:
            movie = Movie.query.get(id)
            if movie:
                movie.delete()
            else:
                abort(422)
            return jsonify({
                'success': True,
                'id': "The movie with id:{} has been deleted".format(id)
            })
        except BaseException:
            abort(422)

    # METHOD: 'DELETE' actors

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(token, id):
        try:
            actor = Actor.query.get(id)
            if actor:
                actor.delete()
            else:
                abort(422)
            return jsonify({
                'success': True,
                'id': "The actor with id:{} has been deleted".format(id)
            })
        except BaseException:
            abort(422)

    # METHOD: 'PATCH' movies
    # Helpful method in the website below for patch
    # https://rahmanfadhil.com/flask-rest-api/
    '''
  {
    "title":"Joker"
  }
  '''
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(token, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(400)
        if 'title' in request.json:
            movie.title = request.json['title']
        if 'rate' in request.json:
            movie.rate = request.json['rate']
        if 'release_date' in request.json:
            release_date = request.json['release_date']
        movie.update()
        return jsonify({
            'success': True,
            'id': "movie with the id:{} has been updated ".format(id)
        })

    # METHOD: 'PATCH' actors
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(token, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(400)
        if 'name' in request.json:
            actor.name = request.json['name']
        if 'age' in request.json:
            actor.age = request.json['age']
        if 'gender' in request.json:
            actor.gender = request.json['gender']
        actor.update()
        return jsonify({
            'success': True,
            'id': "actor with the id:{} has been updated ".format(id)
        })

    #------------------------------------------------------------------#
    #                        Erorr Handler                             #
    #------------------------------------------------------------------#
    @app.errorhandler(404)
    def resources_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "resources not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(422)
    def Unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unable to process"
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': "method not allowed"
        }), 405

    @app.errorhandler(500)
    def interal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "interal server error"
        }), 500

    @app.errorhandler(401)
    def not_authorizated(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "not authorizated"
        }), 401

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
