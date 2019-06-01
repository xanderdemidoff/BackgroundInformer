from app import app
from flask import render_template, redirect, url_for
from flask import request
from flask import abort
from app.forms import InterpolSearchForm
import requests


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DictFromMainPageRequest(metaclass=Singleton):
    response_from_main_global = dict()

    def set_global_dict(self, new_dict: dict):
        if self.response_from_main_global:
            self.response_from_main_global.clear()
        self.response_from_main_global.update(new_dict)

    def get_global_dict(self) -> dict:
        copy = self.response_from_main_global.copy()
        self.response_from_main_global.clear()
        return copy


@app.route('/', methods=['GET', 'POST'])
def main_page():
    d = DictFromMainPageRequest()
    form = InterpolSearchForm()
    r = requests

    if request.method == 'POST':
        if form.validate_on_submit():
            args = ['name', 'forename', 'nationality', 'sexId', 'ageMin', 'ageMax']
            params_dict = {}
            for arg in args:
                if request.form.get(arg):
                    params_dict[arg] = request.form.get(arg)
            response_json = r.get(url=r'https://ws-public.interpol.int/notices/v1/red',
                                  params=params_dict).json()
            d.set_global_dict(new_dict=response_json)
            return render_template('interpol_results.html', search_result=response_json, r=r, url_for=url_for)
    return render_template('interpol.html', form=form)


@app.route('/next')
def next_page():
    d = DictFromMainPageRequest()
    main_global = d.get_global_dict()
    r = requests
    try:
        next_page_link = main_global.get('_links').get('next').get('href')
        last_page_link = main_global.get('_links').get('last').get('href')
        if next_page_link == last_page_link:
            return redirect(location=url_for('main_page'))
    except AttributeError:
        return abort(404)
    if main_global and next_page_link:
        response_json = r.get(url=next_page_link).json()
        d.set_global_dict(new_dict=response_json)
        return render_template('interpol_results.html', search_result=response_json, r=r, url_for=url_for)
    else:
        return abort(404)


@app.route('/previous')
def previous_page():
    d = DictFromMainPageRequest()
    main_global = d.get_global_dict()
    r = requests
    try:
        next_page_link = main_global.get('_links').get('next').get('href')
        last_page_link = main_global.get('_links').get('last').get('href')
        previous_page_link = main_global.get('_links').get('previous').get('href')
        if next_page_link == last_page_link:
            return redirect(location=url_for('main_page'))
    except AttributeError:
        return abort(404)
    if main_global and previous_page_link:
        response_json = r.get(url=previous_page_link).json()
        d.set_global_dict(new_dict=response_json)
        return render_template('interpol_results.html', search_result=response_json, r=r, url_for=url_for)
    else:
        return abort(404)
