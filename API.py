from __future__ import annotations

from sqlalchemy.exc import IntegrityError

import schema
import flask
from flask import jsonify, Flask, request
from flask.views import MethodView
import requests
from error_handle import HttpError
import pydantic

from models import Session, Advertisements

app = flask.Flask("app")

#обработчик входных данных на соответствие схеме
def validate(validation_schema, validation_data):
    try:
        model = validation_schema(**validation_data)
        return model.dict(exclude_none=True)
    except pydantic.ValidationError as err:
        raise HttpError(400, err.errors())


#получение объявления
def get_adv(session, adv_id):
    adv = session.get(Advertisements, adv_id)
    if adv is None:
        raise HttpError(404, "usr not found")
    return adv


#собственный обработчик ошибок
@app.errorhandler(HttpError)
def error_handler(er: HttpError):
    response = jsonify({"status": "error", "description": er.message})
    response.status_code = er.status_code
    return response

#API-методы
class AdvsView(MethodView):
    def get(self, adv_id):
        with Session() as session:
            adv = get_adv(session, adv_id)
            return jsonify(
                {
                "id": adv_id,
                "header": adv.header,
                "description": adv.description,
                "owner": adv.owner,
                "creation_time": adv.creation_time.isoformat(),
                }
            )

    def post(self):
        validated_json = validate(schema.CreateAdv, request.json)
        with Session() as session:
            adv = Advertisements(**validated_json)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "Adv already exists")
            return jsonify({"id": adv.id})


    def patch(self, adv_id):
        validated_json = validate(schema.UpdateAdv, request.json)
        with Session() as session:
            adv = get_adv(session, adv_id)
            for field, value in validated_json.items():
                setattr(adv, field, value)
            session.add(adv)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, "User already exists")
            return jsonify({'id': adv.id})

    def delete(self, adv_id):
        with Session() as session:
            adv = get_adv(session, adv_id)
            session.delete(adv)
            session.commit()
            return jsonify({'status': 'success'})


#настройка ссылок
advs_view = AdvsView.as_view('advs')
app.add_url_rule("/adv/<int:adv_id>", view_func=advs_view, methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule("/adv/", view_func=advs_view, methods=['POST'])

#запуск приложения
if __name__ == '__main__':
    app.run()