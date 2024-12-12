from flask import (Blueprint, render_template, url_for)
import json

bp = Blueprint('gallery', __name__, url_prefix='/gallery')


@bp.route('/')
def show_gallery():
    """Busca por todas imagens presentes em static/GALLERY/images.json para mostrar as imagens de fato"""
    with bp.open_resource('static/GALLERY/images.json', 'r') as f:
        gallery_images = json.load(f)

    return render_template('gallery.html',
                           images=gallery_images['images'])
