import logging.config
import os
import sys
from flask import Flask, Blueprint, request, jsonify, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import settings
import requests
import json
from feedgen.feed import FeedGenerator
from flask import make_response
from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed
from urllib.request import urlopen



app = Flask(__name__)
Bootstrap(app)



def get_abs_url(url):
    """ Returns absolute url by joining post url with base url """
    return urljoin(request.url_root, url)


@app.route('/feeds/')
def feeds():
    feed = AtomFeed(title='All Advertisements feed',
                    feed_url=request.url, url=request.url_root)

    response = requests.get(settings.API_URL + '/getAdvertisements')
    posts = response.json()

    for key, value in posts.items():
        print("key,value: " + key + ", " + value)

    #     feed.add(post.title,
    #              content_type='html',
    #              author= post.author_name,
    #              url=get_abs_url(post.url),
    #              updated=post.mod_date,
    #              published=post.created_date)

    # return feed.get_response()




@app.route('/')
def home():
    response = requests.get(settings.API_URL + 'getAdvertisements')
    response2 = urlopen(settings.API_URL + 'getPosts')

    
    addurl = urlopen(settings.API_URL + 'getAdvertisements')

    ads = json.loads(addurl.read())

    
    posts = json.loads(response2.read())
    return render_template("index.html", ads=ads, posts=posts)


@app.route('/ad/add', methods=['GET'])
def add_ad_view():
    return render_template("new_ad.html")


@app.route('/ad/edit/<id>', methods=['GET'])
def edit_ad_view(id):
    addurl = urlopen(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = json.loads(addurl.read())
    return render_template("edit_ad.html", ad=ad)


@app.route('/ad/delete/<id>', methods=['GET'])
def delete_ad_view(id):
    response = urlopen(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = json.loads(response.read())
    return render_template("delete_ad.html", ad=ad)

@app.route('/ad/view/<id>', methods=['GET'])
def view_ad_view(id):
    response = urlopen(settings.API_URL + '/getAdvertisement?id=' + id)
    ad = json.loads(response.read())
    return render_template("view_ad.html", ad=ad)

@app.route('/ad/new', methods=['POST'])
def add_ad_request():
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }
    wurl = urlopen(settings.API_URL + '/getAdvertisement?id=' + id)
    response = requests.post(wurl, json.dumps(req_data))
    return redirect(url_for('home'))

@app.route('/ad/update/<id>', methods=['POST'])
def update_ad_request(id):
    # Get item from the POST body
    req_data = {
        'title': request.form['title'],
        'city': request.form['city'],
        'description': request.form['description'],
        'email': request.form['email'],
        'imgUrl': request.form['imgUrl'],
        'price': request.form['price']
    }


    wurl= settings.API_URL + '/updateAdvertisement?id=' + id
    response = requests.put(wurl, json.dumps(req_data))
    return redirect(url_for('home'))

@app.route('/ad/delete/<id>', methods=['POST'])
def delete_ad_request(id):
    wurl= settings.API_URL + '/deleteAdvertisement?id=' + id
    response = requests.delete(wurl)
    if response.status_code == 200:
        return redirect(url_for('home'))

# running app
def main():
    print(' ----->>>> Flask Python Application running in development server')
    app.run(host=settings.SERVER_HOST, port=settings.SERVER_PORT, debug=settings.FLASK_DEBUG)


if __name__ == '__main__':
    main()
