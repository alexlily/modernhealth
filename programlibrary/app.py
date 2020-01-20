#!/usr/bin/env python

from flask import Flask, abort, send_file, request
import json
from programlibrary.db import makeQuery
from programlibrary.models import Program, Section, Activity


def create_app():
  """
  Create app
  """
  
  # app initiliazation
  app = Flask(__name__)

  @app.route('/api/v1/programs/list', methods=['GET'])
  def getProgramsList():
    GET_PROGRAMS_QUERY = """select * from programs;"""
    res = makeQuery(GET_PROGRAMS_QUERY)
    if not res:
      abort(404, 'no programs found')
    programs = [Program(result) for result in res]

    return json.dumps([p.serialize() for p in programs])

  @app.route('/api/v1/program/<int:program_id>', methods=['GET'])
  def getProgramDetail(program_id):
    GET_PROGRAM_QUERY = """select * from public.programs where id = {};"""
    program_result = makeQuery(GET_PROGRAM_QUERY, program_id)
    if not program_result or len(program_result) != 1:
      abort(404, 'program {} not found '.format(program_id))
    program = Program(program_result[0])
    GET_SECTIONS_QUERY = """select * from sections where program_id = {}"""
    sections_result = makeQuery(GET_SECTIONS_QUERY, program_id)
    sections = [Section(result, request.host_url) for result in sections_result]

    for section in sections:
      GET_ACTIVITIES_QUERY = """select * from activities where section_id = {}"""
      activities_result = makeQuery(GET_ACTIVITIES_QUERY, section.id)
      activities = [Activity(result) for result in activities_result]
      section.activities = activities

    return json.dumps({"program": program.serialize(), "sections": [section.serialize() for section in sections]})

  @app.route('/api/v1/image/<id>')
  def get_image(id):
    filename = 'images/{}'.format(id)
    return send_file(filename, mimetype='image/jpg')

  return app